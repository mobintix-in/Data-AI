from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any

class SearchHistoryBase(BaseModel):
    search_params: Dict[str, Any]
    results_count: int = 0

class SearchHistoryCreate(SearchHistoryBase):
    pass

class SearchHistoryResponse(SearchHistoryBase):
    id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SavedSearchBase(BaseModel):
    name: str
    filters: Dict[str, Any]

class SavedSearchCreate(SavedSearchBase):
    pass

class SavedSearchResponse(SavedSearchBase):
    id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class LeadTimelineBase(BaseModel):
    status: str
    notes: Optional[str] = None

class LeadTimelineCreate(LeadTimelineBase):
    search_result_id: int

class LeadTimelineResponse(LeadTimelineBase):
    id: int
    search_result_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class NoteBase(BaseModel):
    content: str

class NoteCreate(NoteBase):
    search_result_id: int

class NoteResponse(NoteBase):
    id: int
    search_result_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ReminderBase(BaseModel):
    reminder_date: datetime
    priority: str = "Medium"
    is_completed: bool = False

class ReminderCreate(ReminderBase):
    search_result_id: int

class ReminderResponse(ReminderBase):
    id: int
    search_result_id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ExportHistoryBase(BaseModel):
    file_type: str
    row_count: int = 0
    filters_used: Optional[Dict[str, Any]] = None
    file_path: Optional[str] = None

class ExportHistoryCreate(ExportHistoryBase):
    pass

class ExportHistoryResponse(ExportHistoryBase):
    id: int
    user_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
