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
health_advisor_agent_depr = Agent(
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





async def main():

    result = await Runner.run(health_advisor_agent_depr)
    print("\nRESPONSE:")
    print(result.final_output)
  

if __name__ == "__main__":
    asyncio.run(main())