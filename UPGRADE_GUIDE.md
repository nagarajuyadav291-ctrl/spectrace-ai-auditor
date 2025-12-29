# 🚀 SpecTrace v2.0 Upgrade Guide

## ✨ What's Been Added

Your SpecTrace system now has **revolutionary features** that solve problems no existing tool addresses!

### **New Modules Created**:

1. ✅ **Behavior Prediction Engine** (`backend/app/prediction/behavior_predictor.py`)
2. ✅ **Real-Time Monitoring** (`backend/app/realtime/websocket_manager.py`)
3. ✅ **Intelligent Alerts** (`backend/app/alerts/alert_manager.py`)
4. ✅ **Enhanced Dependencies** (Updated `requirements.txt` and `package.json`)

---

## 📦 Installation Steps

### **Step 1: Update Backend Dependencies**

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

**New packages installed**:
- `websockets` - Real-time communication
- `scikit-learn` - ML predictions
- `slack-sdk` - Slack integration
- `discord-webhook` - Discord alerts
- `twilio` - SMS notifications
- `reportlab` - PDF generation
- And more!

### **Step 2: Update Frontend Dependencies**

```bash
cd frontend
npm install
```

**New packages installed**:
- `socket.io-client` - WebSocket client
- `chart.js` - Advanced charts
- `d3` - Data visualization
- `@angular/material` - Material Design
- `primeng` - UI components
- And more!

### **Step 3: Configure Environment Variables**

Edit `backend/.env` and add:

```env
# Existing
DATABASE_URL=postgresql://spectrace:spectrace123@localhost:5432/spectrace
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
REDIS_URL=redis://localhost:6379

# NEW: Email Alerts
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com

# NEW: Slack Integration
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_CHANNEL=#spectrace-alerts

# NEW: Discord Integration
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook-url

# NEW: Twilio SMS
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_FROM_NUMBER=+1234567890
```

---

## 🔧 Backend Integration

### **Update `main.py`** to add new endpoints:

Add these imports at the top:

```python
from fastapi import WebSocket, WebSocketDisconnect
from app.prediction.behavior_predictor import BehaviorPredictor
from app.realtime.websocket_manager import manager
from app.alerts.alert_manager import AlertManager
```

Add these instances after existing ones:

```python
# Initialize new components
predictor = BehaviorPredictor()
alert_manager = AlertManager()
```

Add these new endpoints:

```python
@app.post("/api/predict")
async def predict_behavior(request: TaskRequest):
    """Predict agent behavior before execution"""
    prediction = predictor.predict_risk(
        request.task_description,
        request.agent_type,
        request.max_steps
    )
    return prediction

@app.websocket("/ws/{execution_id}")
async def websocket_endpoint(websocket: WebSocket, execution_id: str):
    """WebSocket endpoint for real-time monitoring"""
    await manager.connect(websocket, execution_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket, execution_id)

@app.post("/api/alerts/configure")
async def configure_alerts(rules: Dict[str, List[str]]):
    """Configure alert routing rules"""
    alert_manager.configure_alert_rules(rules)
    return {"status": "configured"}
```

Update the execute endpoint to include real-time streaming:

```python
@app.post("/api/execute", response_model=ExecutionResult)
async def execute_task(request: TaskRequest, db: Session = Depends(get_db)):
    """Execute agent task with real-time monitoring"""
    
    # Create execution record
    execution = AgentExecution(
        agent_id=request.agent_type,
        task_description=request.task_description,
        status="running"
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)
    
    # Execute with real-time streaming
    executor = AgentExecutor(agent_type=request.agent_type)
    traces = []
    
    for step_num in range(request.max_steps):
        # Execute step
        step = await executor.execute_step(request.task_description, step_num)
        traces.append(step)
        
        # Broadcast to WebSocket clients
        await manager.broadcast_step(str(execution.id), step)
        
        # Check for violations
        violations = spec_engine.check_compliance([step])
        if violations:
            risk_score = spec_engine.calculate_risk_score(violations)
            
            # Send alert if high risk
            if risk_score > 0.7:
                await alert_manager.send_alert({
                    'severity': 'high',
                    'title': 'High-Risk Execution Detected',
                    'message': f'Execution #{execution.id} has risk score {risk_score:.2f}',
                    'execution_id': execution.id,
                    'risk_score': risk_score,
                    'violations': violations
                })
    
    # Complete analysis
    embedding = encoder.encode_execution(traces)
    deception_analysis = deception_detector.analyze_execution(traces)
    violations = spec_engine.check_compliance(traces)
    risk_score = spec_engine.calculate_risk_score(violations)
    
    # Update execution
    execution.execution_trace = traces
    execution.risk_score = risk_score
    execution.deception_probability = deception_analysis["deception_probability"]
    execution.spec_violations = violations
    execution.status = "completed"
    db.commit()
    
    # Broadcast completion
    await manager.broadcast_completion(str(execution.id), {
        'risk_score': risk_score,
        'deception_probability': deception_analysis["deception_probability"]
    })
    
    return ExecutionResult(...)
```

---

## 🎨 Frontend Integration

### **Update `app.component.ts`**

The enhanced component is ready with:
- Real-time WebSocket monitoring
- Prediction panel
- Advanced charts
- Dark mode
- Filtering & search

### **Update `app.component.html`**

Add prediction panel before execution:

```html
<!-- Prediction Panel -->
<div class="card" *ngIf="showPrediction">
  <h2>🔮 Behavior Prediction</h2>
  <div class="prediction-result">
    <div class="prediction-metric">
      <span class="label">Predicted Risk</span>
      <span class="value" [style.color]="getRiskColor(prediction.predicted_risk)">
        {{ prediction.predicted_risk.toFixed(2) }}
      </span>
    </div>
    <div class="prediction-metric">
      <span class="label">Deception Probability</span>
      <span class="value">{{ (prediction.predicted_deception * 100).toFixed(1) }}%</span>
    </div>
    <div class="prediction-metric">
      <span class="label">Confidence</span>
      <span class="value">{{ (prediction.confidence * 100).toFixed(0) }}%</span>
    </div>
  </div>
  
  <div class="warnings" *ngIf="prediction.warnings.length > 0">
    <h3>⚠️ Warnings</h3>
    <ul>
      <li *ngFor="let warning of prediction.warnings">{{ warning }}</li>
    </ul>
  </div>
  
  <div class="recommendation">
    <strong>Recommendation:</strong> {{ prediction.recommendation }}
  </div>
  
  <button (click)="executeTask()" class="btn-primary">
    Proceed with Execution
  </button>
</div>

<!-- Add Predict Button -->
<button (click)="predictBehavior()" class="btn-secondary">
  🔮 Predict Behavior
</button>
```

Add real-time monitoring view:

```html
<!-- Real-Time Monitor -->
<div class="monitor-view" *ngIf="activeView === 'monitor'">
  <h2>🔴 Live Execution Monitor</h2>
  
  <div class="risk-meter">
    <div class="meter-label">Current Risk</div>
    <div class="meter-bar">
      <div class="meter-fill" 
           [style.width.%]="currentRisk * 100"
           [style.background-color]="getRiskColor(currentRisk)">
      </div>
    </div>
    <div class="meter-value">{{ currentRisk.toFixed(2) }}</div>
  </div>
  
  <div class="live-steps">
    <div class="step-card" *ngFor="let step of liveSteps">
      <div class="step-header">
        <span class="step-number">Step {{ step.step }}</span>
        <span class="step-time">{{ step.timestamp | date:'HH:mm:ss' }}</span>
      </div>
      <div class="step-content">
        <div><strong>💭 Thought:</strong> {{ step.thought }}</div>
        <div><strong>⚡ Action:</strong> {{ step.action }}</div>
      </div>
    </div>
  </div>
</div>
```

Add charts section:

```html
<!-- Analytics View -->
<div class="analytics-view" *ngIf="activeView === 'analytics'">
  <h2>📊 Analytics Dashboard</h2>
  
  <div class="charts-grid">
    <div class="chart-card">
      <h3>Risk Trend</h3>
      <canvas id="riskTrendChart"></canvas>
    </div>
    
    <div class="chart-card">
      <h3>Violation Distribution</h3>
      <canvas id="violationChart"></canvas>
    </div>
  </div>
</div>
```

---

## 🎯 Testing New Features

### **1. Test Behavior Prediction**

```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "task_description": "Research AI safety papers",
    "agent_type": "gpt-4",
    "max_steps": 10
  }'
```

Expected response:
```json
{
  "predicted_risk": 0.35,
  "predicted_deception": 0.12,
  "confidence": 0.85,
  "warnings": ["⚡ MEDIUM RISK: Monitor execution closely"],
  "recommendation": "⚠️ PROCEED WITH CAUTION"
}
```

### **2. Test WebSocket Connection**

```javascript
// In browser console
const socket = io('http://localhost:8000');

socket.on('connect', () => {
  console.log('Connected!');
  socket.emit('join_execution', 123);
});

socket.on('step_update', (data) => {
  console.log('New step:', data);
});
```

### **3. Test Email Alerts**

```python
# Test script
from app.alerts.alert_manager import AlertManager
import asyncio

async def test_alert():
    manager = AlertManager()
    await manager.send_alert({
        'severity': 'high',
        'title': 'Test Alert',
        'message': 'This is a test alert',
        'execution_id': 1,
        'risk_score': 0.75,
        'violations': [],
        'recipients': ['your-email@example.com']
    })

asyncio.run(test_alert())
```

---

## 📊 Feature Activation Checklist

- [ ] Install new backend dependencies
- [ ] Install new frontend dependencies
- [ ] Configure environment variables
- [ ] Update main.py with new endpoints
- [ ] Test prediction endpoint
- [ ] Test WebSocket connection
- [ ] Configure email alerts
- [ ] Configure Slack integration
- [ ] Configure Discord webhooks
- [ ] Test alert delivery
- [ ] Update frontend UI
- [ ] Test real-time monitoring
- [ ] Deploy and verify

---

## 🎓 Usage Examples

### **Example 1: Predict Before Execute**

```typescript
// Frontend
async predictAndExecute() {
  // Step 1: Predict
  const prediction = await this.http.post('/api/predict', {
    task_description: this.taskDescription,
    agent_type: this.agentType,
    max_steps: this.maxSteps
  }).toPromise();
  
  // Step 2: Show prediction
  this.showPrediction = true;
  
  // Step 3: User decides to proceed
  if (prediction.predicted_risk < 0.7) {
    await this.executeTask();
  } else {
    alert('⚠️ High risk detected! Execution not recommended.');
  }
}
```

### **Example 2: Real-Time Monitoring**

```typescript
// Frontend
connectToExecution(executionId: number) {
  this.socket = io('http://localhost:8000');
  
  this.socket.on('step_update', (data) => {
    this.liveSteps.push(data.step);
    this.updateRiskMeter(data.step);
  });
  
  this.socket.on('risk_update', (data) => {
    if (data.risk.risk_score > 0.8) {
      this.showCriticalAlert();
    }
  });
}
```

### **Example 3: Configure Alerts**

```python
# Backend
alert_manager.configure_alert_rules({
    'critical': ['email', 'slack', 'discord', 'sms'],
    'high': ['email', 'slack'],
    'medium': ['slack'],
    'low': ['discord']
})
```

---

## 🚀 Next Steps

1. **Install Dependencies**: Run pip and npm install
2. **Configure Alerts**: Set up email, Slack, Discord
3. **Test Features**: Verify prediction and real-time monitoring
4. **Deploy**: Push to production
5. **Monitor**: Watch the magic happen!

---

## 📞 Support

If you need help:
- Check `REVOLUTIONARY_FEATURES.md` for detailed explanations
- Review code comments in new modules
- Test each feature individually
- Contact: nagarajuyadav291@gmail.com

---

**Your SpecTrace is now a revolutionary AI safety platform!** 🎉
