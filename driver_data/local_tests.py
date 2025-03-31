import asyncio
from agents import Runner
from .drivers_health_agent import health_advisor_agent
from .driver_agent_tools import add_driver_report
from .example_data import example_events





async def main():
    # Form input string / Формируем строку для ввода
    query = f"Driver ID: {example_events['driver_id']}\nVehicle ID: {example_events['vehicle_id']}\n\n"
    query += "\n".join(f"{event['timestamp']}: {event['event']}" for event in example_events["events"])

    print("\n" + "*"*50)
    print("DRIVER HEALTH CHECK")
    print("="*50)

    # Run agent with text input / Запуск агента с текстовым вводом
    result = await Runner.run(health_advisor_agent, query)

    print("\nSTRUCTURED RESPONSE:")
    print(result.final_output)

    print("\nSUMMARY:")
    print(result.final_output.summary)

    print("\nSCORE:")
    print(result.final_output.score)

    print("\nDriver ID:")
    print(result.final_output.driver_id)

    print("\nVehicle ID:")
    print(result.final_output.vehicle_id)

    print("\nRECOMMENDATIONS:")
    for rec in result.final_output.recommendations:
        print(f"- {rec}")

    add_driver_report(result.final_output.driver_id, result.final_output.vehicle_id, result.final_output.score, result.final_output.summary, result.final_output.recommendations)

if __name__ == "__main__":
    asyncio.run(main())
