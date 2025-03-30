import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

#
cred = credentials.Certificate("secret_keys/drivers-monitor-1w5kqr-firebase-adminsdk-fbsvc-55696da9c1.json")
firebase_admin.initialize_app(cred)


db = firestore.client()

def add_driver_report(driver_id: int, vehicle_id: int, score: int, summary: str, recommendations: list):
    doc_ref = db.collection("driver_reports").document()
    doc_ref.set({
        "driver_id": driver_id,
        "vehicle_id": vehicle_id,
        "score": score,
        "summary": summary,
        "recommendations": recommendations,
        "created_at": datetime.utcnow()
    })
    print(f"✅ Report added: driver_id={driver_id}, vehicle_id={vehicle_id}")
