from typing import List
from pydantic import BaseModel, Field
from agents import Agent, Runner
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()
model = os.getenv('MODEL_NAME', 'gpt-4o-mini')

# Event Submodels / Подмодели событий
class DriverEvent(BaseModel):
    timestamp: str
    driver_id: int
    vehicle_id: int
    event: str

class VehicleEvent(BaseModel):
    timestamp: str
    vehicle_id: int
    vehicle_part: str
    description: str

# Main Output Object / Главный выходной объект
class LogClassifierOutput(BaseModel):
    driver_events: List[DriverEvent]
    vehicle_events: List[VehicleEvent]

# Orchestrator Agent / Агент-оркестратор
log_classifier_agent = Agent(
    name="Log Classifier Agent",
    model=model,
    output_type=LogClassifierOutput,
    instructions="""
    You receive a list of raw log entries. Each entry includes:
    - timestamp
    - driver_id
    - vehicle_id
    - message (natural language)

    Your task:
    1. Classify each log as either driver-related or vehicle-related.
    2. For driver-related logs, output: {"timestamp": ..., "driver_id": ..., "vehicle_id": ..., "event": "..."}
    3. For vehicle-related logs, output: {"timestamp": ..., "vehicle_id": ..., "vehicle_part": ..., "description": "..."}
    4. Group results into two arrays: "driver_events" and "vehicle_events".
    Only include clearly classifiable logs.
    """
)

# Async Test Function / Асинхронная функция для теста
async def test_log_classifier():
    print("\n🧠 RUNNING LOG CLASSIFIER AGENT")
    print("=" * 50)

    query = "\n".join(f"[{log['timestamp']}] Vehicle {log['vehicle_id']}, Driver {log['driver_id']}: {log['message']}" for log in raw_logs)

    result = await Runner.run(log_classifier_agent, query)

    # Print Driver Events / Выводим события водителя
    print("\n👤 DRIVER EVENTS:")
    for e in result.final_output.driver_events:
        print(f"- [{e.timestamp}] Driver {e.driver_id} in Vehicle {e.vehicle_id}: {e.event}")

    # Print Vehicle Events / Выводим события по машине
    print("\n🚗 VEHICLE EVENTS:")
    for e in result.final_output.vehicle_events:
        print(f"- [{e.timestamp}] Vehicle {e.vehicle_id} — {e.vehicle_part}: {e.description}")

# Run / Запуск
if __name__ == "__main__":
    asyncio.run(test_log_classifier())
