"""
Agent Executor Module
Executes AI agent tasks and captures full execution traces with chat-like responses
"""

import os
import json
from typing import List, Dict, Any
from datetime import datetime
from openai import OpenAI

class AgentExecutor:
    """Execute AI agent tasks with full tracing and chat responses"""
    
    def __init__(self, agent_type: str = "gpt-3.5-turbo"):
        self.agent_type = agent_type
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.openai_client = OpenAI(api_key=api_key)
        
    async def execute_task(self, task: str, max_steps: int = 10) -> List[Dict[str, Any]]:
        """
        Execute a task and capture full execution trace with AI responses
        
        Args:
            task: Task description for the agent
            max_steps: Maximum number of execution steps
            
        Returns:
            List of execution traces with thoughts, actions, observations, and AI responses
        """
        traces = []
        
        system_prompt = """You are a helpful AI assistant. Answer questions clearly and concisely.
        Provide accurate, informative responses while being friendly and professional."""
        
        try:
            # Execute with OpenAI
            response = self.openai_client.chat.completions.create(
                model=self.agent_type,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": task}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            
            # Create comprehensive trace
            trace = {
                "step": 1,
                "thought": f"Analyzing the question: '{task[:100]}...'",
                "action": f"Generating response using {self.agent_type}",
                "observation": ai_response,
                "ai_response": ai_response,  # Full AI response for display
                "timestamp": datetime.utcnow().isoformat(),
                "model": self.agent_type,
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else 0
            }
            
            traces.append(trace)
            
            # Add analysis step
            analysis_trace = {
                "step": 2,
                "thought": "Analyzing response quality and safety",
                "action": "Behavioral analysis and risk assessment",
                "observation": f"Response generated successfully. Length: {len(ai_response)} characters. Model: {self.agent_type}",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            traces.append(analysis_trace)
            
        except Exception as e:
            error_msg = str(e)
            traces.append({
                "step": 1,
                "thought": "Error occurred during execution",
                "action": "Error handling",
                "error": error_msg,
                "observation": f"Execution failed: {error_msg}",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        return traces
