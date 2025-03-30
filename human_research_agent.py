import asyncio
from typing import List, Union, Dict, Any
from pydantic import BaseModel, Field
from agents import Agent, Runner, RunContextWrapper, FunctionTool
from dotenv import load_dotenv
import os
import json

# Load environment variables
model = os.getenv('MODEL_NAME', 'gpt-4o-mini')

# --- Data Models ---
class DriverEvent(BaseModel):
    """Single driver event data"""
    timestamp: str = Field(description="ISO 8601 timestamp of the event")
    event: str = Field(description="Description of the driver's condition or behavior")

class DriverHealthReport(BaseModel):
    """Driver condition evaluation and improvement recommendations"""
    score: int = Field(description="Overall driver health and behavior score from 1 (poor) to 10 (excellent)")
    summary: str = Field(description="Brief overview of the driver's current condition")
    recommendations: List[str] = Field(description="List of actionable, personalized suggestions")

class ChatResponse(BaseModel):
    """Response for regular chat interactions"""
    message: str = Field(description="The assistant's response message")
    recommendations: List[str] = Field(description="List of recommendations if applicable")

# --- Specialized Agents ---
health_advisor_agent = Agent(
    name="Health Advisor",
    instructions="""
    You are a supportive health advisor for drivers. Your role is to:
    1. Provide helpful advice about driver health and safety
    2. Answer questions about driver monitoring and health management
    3. Offer practical recommendations for maintaining good health while driving
    4. Maintain a professional but friendly tone
    
    Focus on practical, actionable advice that drivers can implement immediately.
    """,
    model=model,
    output_type=ChatResponse
)

event_analyzer_agent = Agent(
    name="Event Analyzer",
    instructions="""
    You are a driver monitoring expert who analyzes events to assess driver health.
    
    For each set of events, you should:
    1. Analyze the sequence of events to assess the driver's overall condition
    2. Assign a health and behavior score from 1 to 10
    3. Provide a concise summary of the findings
    4. Recommend specific actions based on the events
    
    Be objective but professional. Consider the frequency and severity of negative events.
    """,
    model=model,
    output_type=DriverHealthReport
)

# --- Function Tools ---
async def process_events(ctx: RunContextWrapper[Any], args: str) -> str:
    """Process driver events and return health report"""
    data = json.loads(args)
    events = data["events"]
    query = "\n".join(f"{event['timestamp']}: {event['event']}" for event in events)
    result = await Runner.run(event_analyzer_agent, query)
    return result.final_output.model_dump_json()

async def handle_chat(ctx: RunContextWrapper[Any], args: str) -> str:
    """Handle regular chat messages"""
    data = json.loads(args)
    message = data["message"]
    result = await Runner.run(health_advisor_agent, message)
    return result.final_output.model_dump_json()

# --- Main Orchestrator Agent ---
orchestrator_agent = Agent(
    name="Driver Health Orchestrator",
    instructions="""
    You are the main driver health monitoring system. You can handle both event analysis and general health advice.
    
    When receiving input:
    1. If it's a JSON array of events, use the event_analyzer tool
    2. If it's a regular message, use the health_advisor tool
    
    Always provide clear, helpful responses and maintain a professional tone.
    """,
    model=model,
    tools=[
        FunctionTool(
            name="event_analyzer",
            description="Analyze driver events and generate health report",
            params_json_schema={
                "type": "object",
                "properties": {
                    "events": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "timestamp": {"type": "string"},
                                "event": {"type": "string"}
                            },
                            "required": ["timestamp", "event"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["events"],
                "additionalProperties": False
            },
            on_invoke_tool=process_events,
        ),
        FunctionTool(
            name="health_advisor",
            description="Provide health advice and recommendations",
            params_json_schema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "User's health-related question or concern"
                    }
                },
                "required": ["message"],
                "additionalProperties": False
            },
            on_invoke_tool=handle_chat,
        ),
    ]
)

user_input = '''
[
    {"timestamp": "2025-03-25T08:15:00", "event": "fell asleep at the wheel"},
    {"timestamp": "2025-03-26T10:00:00", "event": "high blood pressure"}
]
'''

async def main():
    print("\n" + "*"*50)
    print("DRIVER HEALTH MONITOR")
    print("="*50)
    print("Enter your message or JSON events (type 'exit' to quit):")
    result = await Runner.run(orchestrator_agent, user_input)
    print("\nRESPONSE:")
    print(result.final_output)
  

if __name__ == "__main__":
    asyncio.run(main())