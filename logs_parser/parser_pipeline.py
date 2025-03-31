import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents import Runner
from logs_parser.parser_agent_tools import build_driver_events_input, build_vehicle_events_input
from logs_parser.parser_agent import log_classifier_agent
from driver_data.drivers_health_agent import health_advisor_agent
from vehicle_data.vehicle_check_agent import vehicle_check_agent
import asyncio
from driver_data.driver_agent_tools import add_driver_report
from vehicle_data.vehicle_agent_tools import save_vehicle_report_group_to_firestore
# Пример сырых логов
raw_logs = [
    {
        "timestamp": "2025-03-25T08:15:00",
        "driver_id": 101,
        "vehicle_id": 202,
        "message": "Driver reported feeling fatigued"
    },
    {
        "timestamp": "2025-03-25T08:30:00",
        "driver_id": 101,
        "vehicle_id": 202,
        "message": "Vehicle tire pressure dropped"
    },
    {
        "timestamp": "2025-03-25T09:00:00",
        "driver_id": 101,
        "vehicle_id": 202,
        "message": "Engine overheating warning triggered"
    },
    {
        "timestamp": "2025-03-25T09:15:00",
        "driver_id": 101,
        "vehicle_id": 202,
        "message": "Driver showed signs of distraction"
    },
    {
        "timestamp": "2025-03-25T09:30:00",
        "driver_id": 101,
        "vehicle_id": 202,
        "message": "Battery voltage below safe level"
    }
]

async def run_full_pipeline(raw_logs):
    print("\n🚀 STARTING FULL PIPELINE")
    print("=" * 60)

    # Шаг 1: Классификация логов
    print("\n📂 Classifying raw logs...")
    query = "\n".join(
        f"[{log['timestamp']}] Vehicle {log['vehicle_id']}, Driver {log['driver_id']}: {log['message']}"
        for log in raw_logs
    )
    classification_result = await Runner.run(log_classifier_agent, query)
    classified = classification_result.final_output
    print(f"Classified: {classified}")
    # Шаг 2: Форматирование данных
    driver_input = build_driver_events_input(classified.driver_events) if classified.driver_events else None
    vehicle_input = build_vehicle_events_input(classified.vehicle_events) if classified.vehicle_events else None

    # Шаг 3: Передаём в агентов
    if driver_input:
        print("\n👤 Running driver health agent...")
        driver_query = f"Driver ID: {driver_input['driver_id']}\nVehicle ID: {driver_input['vehicle_id']}\n\n"
        driver_query += "\n".join(f"{e['timestamp']}: {e['event']}" for e in driver_input["events"])

        driver_result = await Runner.run(health_advisor_agent, driver_query)
        print("\n✅ Driver Health Report:")
        print(driver_result.final_output)
        add_driver_report(driver_result.final_output.driver_id, driver_result.final_output.vehicle_id, driver_result.final_output.score, driver_result.final_output.summary, driver_result.final_output.recommendations)

    if vehicle_input:
        print("\n🚗 Running vehicle check agent...")
        vehicle_query = f"Vehicle ID: {vehicle_input['vehicle_id']}\n\n"
        vehicle_query += "\n".join(
            f"{e['timestamp']} — {e['vehicle_part']}: {e['description']}" for e in vehicle_input["events"]
        )
        vehicle_result = await Runner.run(vehicle_check_agent, vehicle_query)
        print("\n✅ Vehicle Health Reports:")
        for report in vehicle_result.final_output:
            print(f"- {report.vehicle_part}: Score {report.health_score}, Summary: {report.summary}")
        save_vehicle_report_group_to_firestore(vehicle_result.final_output)
    print("\n🎯 PIPELINE COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_full_pipeline(raw_logs))
