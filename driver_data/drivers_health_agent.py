from typing import List
from pydantic import BaseModel, Field
from agents import Agent, Runner, RunContextWrapper, FunctionTool
from dotenv import load_dotenv
import os

# Load environment variables
model = os.getenv('MODEL_NAME', 'gpt-4o-mini')

# --- Data Models ---
class DriverEvent(BaseModel):
    """Single driver event data"""
    timestamp: str = Field(description="ISO 8601 timestamp of the event")
    event: str = Field(description="Description of the driver's condition or behavior")

class DriverHealthReport(BaseModel):
    """Driver condition evaluation and improvement recommendations"""
    driver_id: int = Field(description="Unique identifier for the driver")
    vehicle_id: int = Field(description="Unique identifier for the vehicle")
    score: int = Field(description="Overall driver health and behavior score from 1 (poor) to 10 (excellent)")
    summary: str = Field(description="Brief overview of the driver's current condition")
    recommendations: List[str] = Field(description="List of actionable, personalized suggestions")

# --- Specialized Agents ---
health_advisor_agent = Agent(
    name="Health Advisor",
    instructions="""
    You are a driver monitoring expert. You receive a list of events (timestamp + description).
    Analyze them, give a health score (1–10), a summary, and recommendations.
    Be objective and consider the frequency and severity of negative events.
    """,
    model=model,
    output_type=DriverHealthReport
)



