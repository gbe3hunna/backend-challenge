import datetime
import uuid

from pydantic import BaseModel, UUID4, Field


class ECGSubmissionLead(BaseModel):
    name: str
    number_of_samples: int | None = None
    signal: list[int]


class ECGSubmission(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    date: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    leads: list[ECGSubmissionLead] = Field(default_factory=list)


class ECGUser(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    username: str
    password: str


class ECGUserCreate(ECGUser):
    hashed_password: str


class BaseResponse(BaseModel):
    message: str = ""


class ECGAPIAsyncResponse(BaseResponse):
    id: UUID4


class ECGAPIResponse(BaseResponse):
    id: UUID4
    zero_crosses_count: int | None = None
