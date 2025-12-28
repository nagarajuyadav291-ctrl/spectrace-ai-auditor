"""
SpecTrace FastAPI Application
Main API server for AI behavior auditing
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import uvicorn

from app.database import init_db, get_db, AgentExecution
from app.models import TaskRequest, ExecutionResult, RiskAssessment, ExecutionTrace
from app.agents.executor import AgentExecutor
from app.analysis.behavioral_encoder import BehavioralEncoder
from app.analysis.deception_detector import DeceptionDetector
from app.analysis.spec_compliance import SpecComplianceEngine

# Initialize FastAPI app
app = FastAPI(
    title="SpecTrace API",
    description="Autonomous AI-System Behavior Auditor for Agentic Models",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analysis components
encoder = BehavioralEncoder()
deception_detector = DeceptionDetector()
spec_engine = SpecComplianceEngine()

@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    init_db()
    print("🚀 SpecTrace API started successfully!")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SpecTrace API - AI Behavior Auditor",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.post("/api/execute", response_model=ExecutionResult)
async def execute_task(request: TaskRequest, db: Session = Depends(get_db)):
    """
    Execute agent task and analyze behavior
    
    Args:
        request: Task execution request
        db: Database session
        
    Returns:
        Complete execution result with risk assessment
    """
    try:
        # Execute task
        executor = AgentExecutor(agent_type=request.agent_type)
        traces = await executor.execute_task(request.task_description, request.max_steps)
        
        if not traces:
            raise HTTPException(status_code=500, detail="Execution failed - no traces generated")
        
        # Analyze behavior
        embedding = encoder.encode_execution(traces)
        pattern_scores = encoder.detect_pattern_type(embedding)
        
        # Detect deception
        deception_analysis = deception_detector.analyze_execution(traces)
        
        # Check spec compliance
        violations = spec_engine.check_compliance(traces)
        risk_score = spec_engine.calculate_risk_score(violations)
        
        # Save to database
        execution = AgentExecution(
            agent_id=request.agent_type,
            task_description=request.task_description,
            execution_trace=traces,
            risk_score=risk_score,
            deception_probability=deception_analysis["deception_probability"],
            spec_violations=violations,
            status="completed",
            completed_at=datetime.utcnow()
        )
        db.add(execution)
        db.commit()
        db.refresh(execution)
        
        # Return result
        return ExecutionResult(
            execution_id=execution.id,
            status="completed",
            traces=[ExecutionTrace(**t) for t in traces],
            risk_assessment=RiskAssessment(
                risk_score=risk_score,
                deception_probability=deception_analysis["deception_probability"],
                spec_violations=violations,
                behavioral_flags=deception_analysis["flags"]
            ),
            summary=f"Executed {len(traces)} steps with risk score {risk_score:.2f}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")

@app.get("/api/executions")
async def get_executions(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """
    Get execution history
    
    Args:
        skip: Number of records to skip
        limit: Maximum records to return
        db: Database session
        
    Returns:
        List of executions
    """
    executions = db.query(AgentExecution)\
        .order_by(AgentExecution.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return executions

@app.get("/api/executions/{execution_id}")
async def get_execution(execution_id: int, db: Session = Depends(get_db)):
    """
    Get specific execution details
    
    Args:
        execution_id: Execution ID
        db: Database session
        
    Returns:
        Execution details
    """
    execution = db.query(AgentExecution)\
        .filter(AgentExecution.id == execution_id)\
        .first()
    
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    return execution

@app.get("/api/analytics/drift")
async def get_drift_analysis(db: Session = Depends(get_db)):
    """
    Analyze behavioral drift over time
    
    Args:
        db: Database session
        
    Returns:
        Drift analysis results
    """
    # Get recent executions
    executions = db.query(AgentExecution)\
        .order_by(AgentExecution.created_at.desc())\
        .limit(50)\
        .all()
    
    if len(executions) < 2:
        return {
            "drift_score": 0.0,
            "trend": "insufficient_data",
            "average_risk": 0.0,
            "recent_risk": 0.0,
            "historical_risk": 0.0
        }
    
    # Calculate risk statistics
    risk_scores = [e.risk_score for e in executions]
    avg_risk = sum(risk_scores) / len(risk_scores)
    
    # Compare recent vs historical
    recent_count = min(10, len(risk_scores))
    recent_avg = sum(risk_scores[:recent_count]) / recent_count
    older_avg = sum(risk_scores[recent_count:]) / max(1, len(risk_scores) - recent_count)
    
    # Calculate drift
    drift = recent_avg - older_avg
    
    # Determine trend
    if drift > 0.1:
        trend = "increasing"
    elif drift < -0.1:
        trend = "decreasing"
    else:
        trend = "stable"
    
    return {
        "drift_score": abs(drift),
        "trend": trend,
        "average_risk": avg_risk,
        "recent_risk": recent_avg,
        "historical_risk": older_avg,
        "total_executions": len(executions)
    }

@app.get("/api/analytics/violations")
async def get_violation_stats(db: Session = Depends(get_db)):
    """
    Get violation statistics
    
    Args:
        db: Database session
        
    Returns:
        Violation statistics by severity
    """
    executions = db.query(AgentExecution).all()
    
    violation_counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }
    
    for execution in executions:
        for violation in execution.spec_violations:
            severity = violation.get("severity", "medium")
            violation_counts[severity] = violation_counts.get(severity, 0) + 1
    
    return violation_counts

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
