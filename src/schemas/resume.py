from datetime import datetime

from pydantic import BaseModel, computed_field

__all__ = (
    "ResumeCreate",
    "ResumeRead",
    "ResumeUpdate",
    "ResumeBasicInformationRead"
)

from src.core import enums
from src.schemas.citezenship import MinimizedCitizenship


class ResumeCreate(BaseModel):
    position: str


class ResumeBasicInformationRead(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None
    gender: enums.Gender
    phone: str
    birthday: datetime

    citizenship: MinimizedCitizenship
    city: str


class ResumeEducation(BaseModel):
    level: str
    name: str
    faculty: str
    specialization: str
    year_of_graduation: int


class ResumeWorkExperience(BaseModel):
    name: str
    position: str
    description: str
    start_work_month: str
    start_work_year: int
    is_end: bool


class ResumeUpdate(BaseModel):
    is_public: bool
    is_ready_for_move: bool
    is_ready_for_trips: bool

    position: str
    salary_from: int | None
    salary_to: int | None

    busyness: enums.Busyness
    work_schedule: enums.WorkSchedule

    basic_information: ResumeBasicInformationRead | None
    education: ResumeEducation | None
    work_experience: ResumeWorkExperience


class ResumeRead(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime | None

    user_id: int
    is_public: bool
    is_ready_for_move: bool
    is_ready_for_trips: bool

    position: str
    salary_from: int | None
    salary_to: int | None

    busyness: enums.Busyness
    work_schedule: enums.WorkSchedule

    basic_information: ResumeBasicInformationRead | None = None
    education: ResumeEducation | None = None
    work_experience: ResumeWorkExperience | None = None

    @computed_field
    @property
    def stage(self) -> int:
        stages: list[int] = []
        if self.position:
            stages.append(1)
        if self.basic_information:
            stages.append(2)
        if self.education:
            stages.append(3)
        if self.work_experience:
            stages.append(4)

        return max(stages)
