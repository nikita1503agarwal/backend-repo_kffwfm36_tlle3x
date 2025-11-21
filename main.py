import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from database import db, create_document
from schemas import Inquiry

app = FastAPI(title="Construction Solutions Consulting API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend running", "version": "1.0.0"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Inquiry endpoint
class InquiryResponse(BaseModel):
    status: str
    id: str

@app.post("/api/inquiries", response_model=InquiryResponse)
def create_inquiry(inquiry: Inquiry):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    try:
        inserted_id = create_document("inquiry", inquiry)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Simple insights endpoint to power frontend content if needed
@app.get("/api/insights", response_model=List[str])
def get_insights():
    return [
        "Optimized dispatch algorithms can reduce average truck cycle time by 12-18% in Nairobi traffic conditions.",
        "Implementing boom pump utilization planning typically saves 8-15% on total pour costs by reducing idle time.",
        "Onsite batching for high-rise pours above 30 floors can lower crane dependency and improve schedule adherence.",
        "IoT telemetry on transit mixers helps forecast maintenance and prevent breakdowns during peak delivery windows.",
    ]

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
