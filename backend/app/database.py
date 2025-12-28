from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://spectrace:spectrace123@localhost:5432/spectrace")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AgentExecution(Base):
    """Store agent execution traces and analysis results"""
    __tablename__ = "agent_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, index=True)
    task_description = Column(Text)
    execution_trace = Column(JSON)
    risk_score = Column(Float, default=0.0)
    deception_probability = Column(Float, default=0.0)
    spec_violations = Column(JSON, default=[])
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class BehavioralPattern(Base):
    """Store detected behavioral patterns"""
    __tablename__ = "behavioral_patterns"
    
    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(Integer, index=True)
    pattern_type = Column(String)  # honest, deceptive, reward_hacking
    embedding = Column(JSON)
    confidence = Column(Float)
    detected_at = Column(DateTime, default=datetime.utcnow)

class SpecRule(Base):
    """Store specification compliance rules"""
    __tablename__ = "spec_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    rule_name = Column(String, unique=True)
    rule_description = Column(Text)
    rule_pattern = Column(JSON)
    severity = Column(String)  # low, medium, high, critical
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
