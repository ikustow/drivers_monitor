from typing import List
from pydantic import BaseModel, Field
from agents import Agent, Runner
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()
model = os.getenv('MODEL_NAME', 'gpt-4o-mini')

class VehicleCheckReport(BaseModel):
    vehicle_id: int = Field(description="Unique identifier for the vehicle")
    vehicle_part: str = Field(description="Vehicle part that is being checked")
    health_score: int = Field(description="Health score of the vehicle part from 1 (poor) to 10 (excellent)")  # без ge/le
    summary: str = Field(description="Brief overview of the vehicle part's current condition")
    recommendations: List[str] = Field(description="List of actionable, personalized suggestions")


# --- Vehicle diagnostic agent ---
vehicle_check_agent = Agent(
    name="Vehicle Health Inspector",
    instructions="""
    You are an automotive diagnostics expert.

    You will receive a vehicle_id and a list of time-stamped observations describing issues or statuses
    for different vehicle parts. Your task is to:

    1. Group observations by vehicle_part (only use if it's one of: tires, engine, fuel system, brakes, battery).
    2. For each valid vehicle_part, analyze the related entries and:
        - Assign a health_score from 1 (worst) to 10 (best).
        - Write a brief summary of the condition.
        - Suggest actionable recommendations.
    3. Return a separate report for each valid vehicle_part.

    Ignore components outside the supported list.
    """,
    model=model,
    output_type=List[VehicleCheckReport]
)




