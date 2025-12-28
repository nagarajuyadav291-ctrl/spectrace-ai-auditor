from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class TaskRequest(BaseModel):
    """Request model for executing agent tasks"""
    task_description: str = Field(..., min_length=10, description="Task for the agent to execute")
    agent_type: str = Field(default="gpt-4", description="AI model to use (gpt-4, gpt-3.5-turbo, claude-3)")
    max_steps: int = Field(default=10, ge=1, le=50, description="Maximum execution steps")

class ExecutionTrace(BaseModel):
    """Single step in agent execution"""
    step: int
    action: str
    tool_call: Optional[Dict[str, Any]] = None
    thought: Optional[str] = None
    observation: Optional[str] = None
    timestamp: datetime

class RiskAssessment(BaseModel):
    """Risk analysis results"""
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Overall risk score")
    deception_probability: float = Field(..., ge=0.0, le=1.0, description="Probability of deceptive behavior")
    spec_violations: List[Dict[str, Any]] = Field(default=[], description="List of specification violations")
    behavioral_flags: List[str] = Field(default=[], description="Behavioral warning flags")

class ExecutionResult(BaseModel):
    """Complete execution result with analysis"""
    execution_id: int
    status: str
    traces: List[ExecutionTrace]
    risk_assessment: RiskAssessment
    summary: str

class DriftAnalysis(BaseModel):
    """Behavioral drift analysis over time"""
    time_period: str
    drift_score: float
    trend: str  # increasing, decreasing, stable
    anomalies: List[Dict[str, Any]]
    average_risk: float
    recent_risk: float
    historical_risk: float
