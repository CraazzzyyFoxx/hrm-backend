from datetime import datetime

from sqlalchemy import ForeignKey, String, Text, Enum, DateTime, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core import db, enums
from src.models.auth import User
from src.models.citizenship import Citizenship

__all__ = (
    "Resume",
    "ResumeBasicInfo",
    "ResumeEducation",
    "ResumeWorkExperience"
)


class Resume(db.TimeStampMixin):
    __tablename__ = "resume"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship()

    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    is_ready_for_move: Mapped[bool] = mapped_column(Boolean, default=False)
    is_ready_for_trips: Mapped[bool] = mapped_column(Boolean, default=False)

    position: Mapped[str] = mapped_column(String(255))
    salary_from: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_to: Mapped[int | None] = mapped_column(Integer, nullable=True)
    busyness: Mapped[enums.Busyness] = mapped_column(Enum(enums.Busyness), default=enums.Busyness.full)
    work_schedule: Mapped[enums.WorkSchedule] = mapped_column(Enum(enums.WorkSchedule), default=enums.WorkSchedule.full)

    basic_information: Mapped["ResumeBasicInfo"] = relationship("ResumeBasicInfo", back_populates="resume")
    education: Mapped["ResumeEducation"] = relationship("ResumeEducation", back_populates="resume")
    work_experience: Mapped["ResumeWorkExperience"] = relationship("ResumeWorkExperience", back_populates="resume")


class ResumeBasicInfo(db.TimeStampMixin):
    __tablename__ = "resume_basic_info"

    resume_id: Mapped[int] = mapped_column(ForeignKey("resume.id", ondelete="CASCADE"), unique=True)
    resume: Mapped[Resume] = relationship(back_populates="basic_information")

    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    middle_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(255))
    gender: Mapped[enums.Gender] = mapped_column(Enum(enums.Gender))
    birthday: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    city: Mapped[str] = mapped_column(String(255))

    citizenship_id: Mapped[int] = mapped_column(ForeignKey("citizenship.id"))
    citizenship: Mapped[Citizenship] = relationship("Citizenship")


class ResumeEducation(db.TimeStampMixin):
    __tablename__ = "resume_education"

    resume_id: Mapped[int] = mapped_column(ForeignKey("resume.id", ondelete="CASCADE"), unique=True)
    resume: Mapped[Resume] = relationship(back_populates="education")

    level: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    faculty: Mapped[str] = mapped_column(String(255))
    specialization: Mapped[str] = mapped_column(String(255))
    year_of_graduation: Mapped[int]


class ResumeWorkExperience(db.TimeStampMixin):
    __tablename__ = " Resume_work_experience"

    resume_id: Mapped[int] = mapped_column(ForeignKey("resume.id", ondelete="CASCADE"), unique=True)
    resume: Mapped[Resume] = relationship(back_populates="work_experience")

    name: Mapped[str] = mapped_column(String(255))
    position: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())
    start_work_month: Mapped[str] = mapped_column(String(255))
    start_work_year: Mapped[int]
    is_end: Mapped[bool]
