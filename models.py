from enum import Enum
from pydantic import BaseModel

# Recruitment stages
class ApplicationStatus(str, Enum):
    APPLIED = "Applied"
    SCREENING = "Screening"
    SHORTLISTED = "Shortlisted"
    INTERVIEW = "Interview"
    SELECTED = "Selected"
    REJECTED = "Rejected"

# Payload schema for status transition requests
class StatusUpdateRequest(BaseModel):
    status: ApplicationStatus
