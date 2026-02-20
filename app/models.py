from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    title: str
    description: str
    completed: bool = False
    created_at: Optional[datetime] = datetime.utcnow()
