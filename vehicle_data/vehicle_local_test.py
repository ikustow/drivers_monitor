import asyncio
from agents import Runner
from vehicle_data.vehicle_check_agent import vehicle_check_agent
from vehicle_data.vehicle_agent_tools import save_vehicle_report_group_to_firestore

# Пример входных данных
example_events = {
    "vehicle_id": 42,
    "events": [
        {"timestamp": "2025-03-29T10:00:00", "vehicle_part": "engine", "description": "unusual knocking noise"},
        {"timestamp": "2025-03-29T10:05:00", "vehicle_part": "tires", "description": "tread depth below safe level"},
        {"timestamp": "2025-03-29T10:10:00", "vehicle_part": "battery", "description": "slow crank on startup"},
        {"timestamp": "2025-03-29T10:15:00", "vehicle_part": "radio", "description": "audio system cuts out randomly"},
        {"timestamp": "2025-03-29T10:20:00", "vehicle_part": "brakes", "description": "squeaking sound during braking"},
        {"timestamp": "2025-03-29T10:25:00", "vehicle_part": "fuel system", "description": "fuel efficiency dropped significantly"},
    ]
}
# Тестовая функция
async def test_vehicle_check():
    print("\n🚗 VEHICLE CHECK STARTING")
    print("=" * 50)
    
    query = f"Vehicle ID: {example_events['vehicle_id']}\n\n"
    query += "\n".join(
        f"{e['timestamp']} — {e['vehicle_part']}: {e['description']}" for e in example_events["events"]
    )

    print("\n📄 QUERY VIEW:")
    print(query)
    print("=" * 50)

    result = await Runner.run(vehicle_check_agent, query)

    print("\n🔧 REPORTS:")
    for report in result.final_output:
        print(f"\n📍 Vehicle Part: {report.vehicle_part}")
        print(f"Health Score: {report.health_score}/10")
        print(f"Summary: {report.summary}")
        print("Recommendations:")
        for r in report.recommendations:
            print(f"  - {r}")
        print("-" * 40)
     # ✅ Сохраняем в Firestore
    save_vehicle_report_group_to_firestore(result.final_output)
# Запуск
if __name__ == "__main__":
    asyncio.run(test_vehicle_check())