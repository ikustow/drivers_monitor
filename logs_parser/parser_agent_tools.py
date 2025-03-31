from typing import List, Dict

def build_driver_events_input(driver_events: List[object]) -> Dict:
    if not driver_events:
        raise ValueError("No driver events provided.")

    driver_id = driver_events[0].driver_id
    vehicle_id = driver_events[0].vehicle_id

    formatted_events = [
        {"timestamp": e.timestamp, "event": e.event}
        for e in driver_events
    ]

    return {
        "driver_id": driver_id,
        "vehicle_id": vehicle_id,
        "events": formatted_events
    }

def build_vehicle_events_input(vehicle_events: List[object]) -> Dict:
    if not vehicle_events:
        raise ValueError("No vehicle events provided.")

    vehicle_id = vehicle_events[0].vehicle_id

    formatted_events = [
        {
            "timestamp": e.timestamp,
            "vehicle_part": e.vehicle_part,
            "description": e.description
        }
        for e in vehicle_events
    ]

    return {
        "vehicle_id": vehicle_id,
        "events": formatted_events
    }

    
