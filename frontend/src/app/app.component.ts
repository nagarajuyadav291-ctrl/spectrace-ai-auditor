import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface Execution {
  id: number;
  task_description: string;
  risk_score: number;
  deception_probability: number;
  status: string;
  created_at: string;
  spec_violations: any[];
  execution_trace: any[];
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'SpecTrace - AI Behavior Auditor';
  
  // Form fields
  taskDescription = '';
  agentType = 'gpt-3.5-turbo';  // Default to gpt-3.5-turbo
  maxSteps = 10;
  isExecuting = false;
  
  // Data
  executions: Execution[] = [];
  selectedExecution: any = null;
  driftAnalysis: any = null;
  
  apiUrl = 'http://localhost:8000/api';
  
  constructor(private http: HttpClient) {}
  
  ngOnInit() {
    this.loadExecutions();
    this.loadDriftAnalysis();
  }
  
  async executeTask() {
    if (!this.taskDescription.trim()) {
      alert('Please enter a task description');
      return;
    }
    
    this.isExecuting = true;
    
    try {
      const result: any = await this.http.post(`${this.apiUrl}/execute`, {
        task_description: this.taskDescription,
        agent_type: this.agentType,
        max_steps: this.maxSteps
      }).toPromise();
      
      // Get AI response from traces
      const aiResponse = this.extractAIResponse(result.traces);
      const preview = aiResponse ? aiResponse.substring(0, 100) + '...' : 'Response generated';
      
      alert(`✅ Task executed successfully!\n\n${preview}\n\nRisk Score: ${result.risk_assessment.risk_score.toFixed(2)}\nDeception: ${(result.risk_assessment.deception_probability * 100).toFixed(1)}%`);
      
      this.loadExecutions();
      this.loadDriftAnalysis();
      this.taskDescription = '';
    } catch (error: any) {
      console.error('Execution failed:', error);
      const errorMsg = error.error?.detail || error.message || 'Unknown error';
      alert(`❌ Execution failed: ${errorMsg}\n\nTip: Make sure you're using GPT-3.5 Turbo if you don't have GPT-4 access.`);
    } finally {
      this.isExecuting = false;
    }
  }
  
  extractAIResponse(traces: any[]): string {
    if (!traces || traces.length === 0) return '';
    
    // Look for ai_response field first
    for (const trace of traces) {
      if (trace.ai_response) {
        return trace.ai_response;
      }
    }
    
    // Fallback to observation
    for (const trace of traces) {
      if (trace.observation && trace.observation.length > 50) {
        return trace.observation;
      }
    }
    
    return '';
  }
  
  getAIResponse(execution: any): string {
    if (!execution || !execution.execution_trace) return '';
    return this.extractAIResponse(execution.execution_trace);
  }
  
  async loadExecutions() {
    try {
      this.executions = await this.http.get<Execution[]>(`${this.apiUrl}/executions`).toPromise() || [];
    } catch (error) {
      console.error('Failed to load executions:', error);
    }
  }
  
  async loadDriftAnalysis() {
    try {
      this.driftAnalysis = await this.http.get(`${this.apiUrl}/analytics/drift`).toPromise();
    } catch (error) {
      console.error('Failed to load drift analysis:', error);
    }
  }
  
  async viewExecution(id: number) {
    try {
      this.selectedExecution = await this.http.get(`${this.apiUrl}/executions/${id}`).toPromise();
    } catch (error) {
      console.error('Failed to load execution details:', error);
    }
  }
  
  closeModal() {
    this.selectedExecution = null;
  }
  
  getRiskColor(score: number): string {
    if (score < 0.3) return '#10b981';
    if (score < 0.6) return '#f59e0b';
    return '#ef4444';
  }
  
  getRiskLabel(score: number): string {
    if (score < 0.3) return 'Low';
    if (score < 0.6) return 'Medium';
    return 'High';
  }
}
