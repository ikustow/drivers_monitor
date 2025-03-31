from firebase_admin import firestore, credentials, initialize_app
from datetime import datetime
from typing import List, Union
import firebase_admin

# Инициализация Firebase (однократно)
def init_firestore():
    if not firebase_admin._apps:
        cred =  credentials.Certificate("secret_keys/drivers-monitor-1w5kqr-firebase-adminsdk-fbsvc-55696da9c1.json")
        initialize_app(cred)

def save_vehicle_report_group_to_firestore(reports: List[Union[dict, object]]):
    init_firestore()
    db = firestore.client()

    if not reports:
        print("⚠️ No reports to save.")
        return

    # Преобразуем каждый отчет в словарь
    parsed_reports = []
    vehicle_id = None

    for report in reports:
        data = report.dict() if hasattr(report, "dict") else dict(report)

        vehicle_id = vehicle_id or data.get("vehicle_id")  # берем первый попавшийся
        parsed_reports.append({
            "vehicle_part": data["vehicle_part"],
            "health_score": data["health_score"],
            "summary": data["summary"],
            "recommendations": data["recommendations"]
        })

    doc_data = {
        "vehicle_id": vehicle_id,
        "created_at": datetime.utcnow(),
        "reports": parsed_reports
    }

    db.collection("vehicle_reports").add(doc_data)
    print(f"✅ Saved {len(parsed_reports)} report(s) in one Firestore document.")