from app.database import Base, TimestampMixin
from sqlalchemy import Column, String, DateTime, Boolean, Text, Float, Integer, ForeignKey, JSON, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship
import enum


class PolicyType(str, enum.Enum):
    HEALTH = "health"
    LIFE = "life"
    MOTOR = "motor"
    HOME = "home"
    TRAVEL = "travel"
    TERM = "term"
    ULIP = "ulip"
    CRITICAL_ILLNESS = "critical_illness"
    GENERAL = "general"


class PolicyStatus(str, enum.Enum):
    PROCESSING = "processing"
    ANALYZED = "analyzed"
    FAILED = "failed"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    clerk_id = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    avatar_url = Column(Text, nullable=True)
    preferences = Column(JSON, default=dict)

    policies = relationship("Policy", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
    claim_assessments = relationship("ClaimAssessment", back_populates="user", cascade="all, delete-orphan")
    mis_selling_reports = relationship("MisSellingReport", back_populates="user", cascade="all, delete-orphan")


class Policy(Base, TimestampMixin):
    __tablename__ = "policies"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    insurer = Column(String(255), nullable=True)
    policy_number = Column(String(255), nullable=True, index=True)
    policy_type = Column(SAEnum(PolicyType), default=PolicyType.GENERAL, nullable=False)
    status = Column(SAEnum(PolicyStatus), default=PolicyStatus.PROCESSING, nullable=False)
    file_path = Column(Text, nullable=True)
    file_type = Column(String(50), nullable=True)
    file_size_bytes = Column(Integer, nullable=True)
    extracted_text = Column(Text, nullable=True)
    structured_data = Column(JSON, default=dict)
    summary = Column(Text, nullable=True)
    language = Column(String(10), default="en")
    page_count = Column(Integer, nullable=True)

    user = relationship("User", back_populates="policies")
    chunks = relationship("PolicyChunk", back_populates="policy", cascade="all, delete-orphan")
    benefits = relationship("Benefit", back_populates="policy", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="policy")
    claim_assessments = relationship("ClaimAssessment", back_populates="policy")
    mis_selling_reports = relationship("MisSellingReport", back_populates="policy")


class PolicyChunk(Base, TimestampMixin):
    __tablename__ = "policy_chunks"

    policy_id = Column(UUID(as_uuid=True), ForeignKey("policies.id"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384), nullable=True)
    chunk_metadata = Column(JSON, default=dict)

    policy = relationship("Policy", back_populates="chunks")


class Benefit(Base, TimestampMixin):
    __tablename__ = "benefits"

    policy_id = Column(UUID(as_uuid=True), ForeignKey("policies.id"), nullable=False, index=True)
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    coverage_amount = Column(String(255), nullable=True)
    currency = Column(String(10), default="INR")
    waiting_period = Column(String(255), nullable=True)
    exclusions = Column(Text, nullable=True)
    conditions = Column(Text, nullable=True)
    claim_limit = Column(String(255), nullable=True)
    deductible = Column(String(255), nullable=True)
    copay = Column(String(255), nullable=True)
    is_sub_limit = Column(Boolean, default=False)
    parent_benefit = Column(String(255), nullable=True)
    source_chunk_ids = Column(JSON, default=list)
    confidence = Column(String(50), default="verified")

    policy = relationship("Policy", back_populates="benefits")


class Recommendation(Base, TimestampMixin):
    __tablename__ = "recommendations"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    policy_id = Column(UUID(as_uuid=True), ForeignKey("policies.id"), nullable=True)
    recommendation_type = Column(String(100), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(50), default="medium")
    category = Column(String(100), nullable=True)
    reasoning = Column(Text, nullable=True)
    evidence_refs = Column(JSON, default=list)
    confidence = Column(String(50), default="verified")
    is_applied = Column(Boolean, default=False)

    user = relationship("User", back_populates="recommendations")
    policy = relationship("Policy", back_populates="recommendations")


class ClaimAssessment(Base, TimestampMixin):
    __tablename__ = "claim_assessments"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    policy_id = Column(UUID(as_uuid=True), ForeignKey("policies.id"), nullable=False)
    claim_type = Column(String(255), nullable=False)
    claim_amount = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    assessment_result = Column(JSON, default=dict)
    eligibility_score = Column(Float, nullable=True)
    estimated_payout = Column(String(255), nullable=True)
    confidence = Column(String(50), default="verified")
    report_html = Column(Text, nullable=True)
    evidence_refs = Column(JSON, default=list)

    user = relationship("User", back_populates="claim_assessments")
    policy = relationship("Policy", back_populates="claim_assessments")


class MisSellingReport(Base, TimestampMixin):
    __tablename__ = "mis_selling_reports"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    policy_id = Column(UUID(as_uuid=True), ForeignKey("policies.id"), nullable=False)
    findings = Column(JSON, default=list)
    severity = Column(String(50), default="low")
    summary = Column(Text, nullable=True)
    report_html = Column(Text, nullable=True)
    confidence = Column(String(50), default="verified")
    evidence_refs = Column(JSON, default=list)

    user = relationship("User", back_populates="mis_selling_reports")
    policy = relationship("Policy", back_populates="mis_selling_reports")


class Company(Base, TimestampMixin):
    __tablename__ = "companies"

    name = Column(String(500), nullable=False, index=True)
    irda_id = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    claim_settlement_ratio = Column(Float, nullable=True)
    complaints_data = Column(JSON, default=dict)
    financial_data = Column(JSON, default=dict)
    market_share = Column(Float, nullable=True)
    ratings = Column(JSON, default=dict)
    solvency_ratio = Column(Float, nullable=True)
    irda_compliance = Column(String(255), nullable=True)
    company_metadata = Column(JSON, default=dict)


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    action = Column(String(255), nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String(255), nullable=True)
    details = Column(JSON, default=dict)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    severity = Column(String(50), default="info")
