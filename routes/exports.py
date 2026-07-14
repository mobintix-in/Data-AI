import os
import pandas as pd
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from database.session import SessionLocal
from models.user import User
from models.search_result import SearchResult
from models.export_history import ExportHistory
from dependencies.auth import get_current_active_user as get_current_user
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/generate")
def generate_export(
    export_type: str, # "excel" or "csv"
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if export_type not in ["excel", "csv"]:
        raise HTTPException(status_code=400, detail="Invalid export type. Must be 'excel' or 'csv'.")

    leads = db.query(SearchResult).filter(SearchResult.user_id == current_user.id).all()
    
    if not leads:
        raise HTTPException(status_code=404, detail="No data available to export.")

    data = []
    for lead in leads:
        data.append({
            "Business Name": lead.name,
            "Category": lead.category,
            "Lead Score": lead.lead_score,
            "Status": lead.lead_status,
            "Email": lead.email,
            "Phone": lead.phone,
            "Website": lead.website,
            "Address": lead.address,
            "Rating": lead.rating,
            "Reviews": lead.reviews,
            "Date Added": lead.created_at.strftime("%Y-%m-%d %H:%M:%S") if lead.created_at else ""
        })

    df = pd.DataFrame(data)
    
    os.makedirs("static/exports", exist_ok=True)
    filename = f"export_{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    if export_type == "excel":
        file_path = f"static/exports/{filename}.xlsx"
        df.to_excel(file_path, index=False)
    else:
        file_path = f"static/exports/{filename}.csv"
        df.to_csv(file_path, index=False)

    # Log the export
    export_log = ExportHistory(
        user_id=current_user.id,
        file_type=export_type.upper(),
        row_count=len(leads),
        file_path=file_path
    )
    db.add(export_log)
    db.commit()

    return {"status": "success", "file_url": f"/{file_path}", "row_count": len(leads)}

@router.get("/history")
def get_export_history(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history = db.query(ExportHistory).filter(ExportHistory.user_id == current_user.id).order_by(ExportHistory.created_at.desc()).limit(limit).all()
    return history

@router.delete("/bulk")
def delete_bulk_exports(
    export_type: str = None, # "excel" or "csv" or None for all
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(ExportHistory).filter(ExportHistory.user_id == current_user.id)
    if export_type:
        query = query.filter(ExportHistory.file_type == export_type.upper())
        
    export_records = query.all()
    
    deleted_count = 0
    for record in export_records:
        if record.file_path and os.path.exists(record.file_path):
            try:
                os.remove(record.file_path)
            except OSError:
                pass
        db.delete(record)
        deleted_count += 1
        
    db.commit()
    
    return {"status": "success", "message": f"{deleted_count} exports deleted successfully"}

@router.delete("/{export_id}")
def delete_export(
    export_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    export_record = db.query(ExportHistory).filter(
        ExportHistory.id == export_id, 
        ExportHistory.user_id == current_user.id
    ).first()
    
    if not export_record:
        raise HTTPException(status_code=404, detail="Export not found")
        
    if export_record.file_path and os.path.exists(export_record.file_path):
        try:
            os.remove(export_record.file_path)
        except OSError:
            pass

    db.delete(export_record)
    db.commit()
    
    return {"status": "success", "message": "Export deleted successfully"}
