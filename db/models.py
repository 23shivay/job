from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .database import Base

class JobPost(Base):
    __tablename__ = "job_posts"

    id = Column(Integer, primary_key=True, index=True)
    # Job details
    job_title = Column(String(255), nullable=True)                   # Can be NULL if not provided
    company_name = Column(String(255), nullable=False, index=True)   # Required
    location = Column(String(255), nullable=True)
    eligibility = Column(String(255), nullable=True)
    stipend_salary = Column(String(255), nullable=True)              # Salary / Stipend
    post_summary = Column(Text, nullable=True)
    click_count = Column(Integer, default=0)               
    apply_link = Column(Text, nullable=False)                        # Required
    # Metadata
    timestamp = Column(String(255), nullable=True)                   # e.g. "1 hour ago"
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Auto timestamp
