from pydantic import BaseModel
from enum import Enum

class EmailStatus(str, Enum):
    unprocessed = "unprocessed"
    processed = "processed"

class TicketRequest(BaseModel):
    subject: str
    body: str

class TicketResponse(BaseModel):
    cause_code: str
    priority: str
    brief_description: str
    assignment: str
    summarized_issue: str
    raw_email: str
    reason: str

class EmailResponse(BaseModel):
    id: str
    subject: str
    from_: str
    body: str
    status: EmailStatus = EmailStatus.unprocessed


