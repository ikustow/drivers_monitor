import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from typing import List, Union

# Firebase initialization (safe)
if not firebase_admin._apps:
    cred = credentials.Certificate("secret_keys/drivers-monitor-1w5kqr-firebase-adminsdk-fbsvc-55696da9c1.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def save_vehicle_report_group_to_firestore(reports: List[Union[dict, object]]):
    if not reports:
        return

    # Convert each report to dictionary / Преобразуем каждый отчет в словарь
    reports_data = []
    for report in reports:
        if isinstance(report, dict):
            reports_data.append(report)
        else:
            reports_data.append(report.dict())

    # Get vehicle_id from first report / vehicle_id = vehicle_id or data.get("vehicle_id")  # берем первый попавшийся
    vehicle_id = reports_data[0].get("vehicle_id")
    if not vehicle_id:
        return

    # Create a new document with timestamp
    timestamp = datetime.now().isoformat()
    doc_ref = db.collection("vehicle_reports").document()
    doc_ref.set({
        "vehicle_id": vehicle_id,
        "timestamp": timestamp,
        "reports": reports_data
    })

    print(f"✅ Saved {len(reports_data)} report(s) in one Firestore document.")