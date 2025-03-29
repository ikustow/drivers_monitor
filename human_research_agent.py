import asyncio
from typing import List
from pydantic import BaseModel, Field
from agents import Agent, Runner
from dotenv import load_dotenv
import os

# Load environment variables
# Set model choice
model = os.getenv('MODEL_NAME', 'gpt-4o-mini')

# --- Structured Output ---
class DriverHealthReport(BaseModel):
    """Driver condition evaluation and improvement recommendations"""
    score: int = Field(description="Overall driver health and behavior score from 1 (poor) to 10 (excellent)")
    summary: str = Field(description="Brief overview of the driver's current condition")
    recommendations: List[str] = Field(description="List of actionable, personalized suggestions")


# --- Agent for Driver State Monitoring ---
driver_monitor_agent = Agent(
    name="Driver Health Monitor",
    instructions="""
    You are a driver monitoring expert.

    You receive input as a JSON array of events, where each event includes:
    - a timestamp in ISO 8601 format (e.g., '2025-03-28T14:30:00')
    - a short description of the driver's condition or behavior at that time.

    Example events: "fell asleep at the wheel", "high blood pressure", "took a rest break", 
    "ate a meal", "tested positive for alcohol", "reported stress", "feeling good", etc.

    Your task:
    1. Analyze all events to assess the driver's overall condition.
    2. Assign a health and behavior score from 1 to 10, where 10 = fully alert and healthy, 1 = critical or dangerous.
    3. Provide a concise summary of the findings.
    4. Recommend specific actions: rest, medical check, replace driver, adjust behavior, etc.

    Be objective but professional and supportive. Consider the frequency and severity of negative events.
    """,
    model=model,
    output_type=DriverHealthReport
)

example_events = [
    {"timestamp": "2025-03-25T08:15:00", "event": "fell asleep at the wheel"},
    {"timestamp": "2025-03-26T10:00:00", "event": "high blood pressure"},
    {"timestamp": "2025-03-27T12:30:00", "event": "took a rest break"},
    {"timestamp": "2025-03-28T09:45:00", "event": "feeling good"}
]

async def main():
    # Формируем строку для ввода
    query = "\n".join(f"{event['timestamp']}: {event['event']}" for event in example_events)

    print("\n" + "*"*50)
    print("DRIVER HEALTH CHECK")
    print("="*50)

    # Запуск агента с текстовым вводом
    result = await Runner.run(driver_monitor_agent, query)

    print("\nSTRUCTURED RESPONSE:")
    print(result.final_output)

    print("\nSUMMARY:")
    print(result.final_output.summary)

    print("\nSCORE:")
    print(result.final_output.score)

    print("\nRECOMMENDATIONS:")
    for rec in result.final_output.recommendations:
        print(f"- {rec}")


if __name__ == "__main__":
    asyncio.run(main())