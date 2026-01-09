"""
Agent Executor Module
Executes AI agent tasks and captures full execution traces
"""

import os
import json
from typing import List, Dict, Any
from datetime import datetime
from openai import OpenAI

class AgentExecutor:
    """Execute AI agent tasks with full tracing"""
    
    def __init__(self, agent_type: str = "gpt-4"):
        self.agent_type = agent_type
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.openai_client = OpenAI(api_key=api_key)
        
    async def execute_task(self, task: str, max_steps: int = 10) -> List[Dict[str, Any]]:
        """
        Execute a task and capture full execution trace
        
        Args:
            task: Task description for the agent
            max_steps: Maximum number of execution steps
            
        Returns:
            List of execution traces with thoughts, actions, and observations
        """
        traces = []
        
        system_prompt = """You are an AI agent executing tasks step by step.
        For each step, think through the problem and describe your actions clearly.
        Be thorough and transparent in your reasoning.
        """
        
        conversation = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Task: {task}\n\nPlease complete this task step by step. For each step, explain your thought process and the action you're taking."}
        ]
        
        for step in range(max_steps):
            try:
                # Execute with OpenAI
                response = self.openai_client.chat.completions.create(
                    model=self.agent_type,
                    messages=conversation,
                    temperature=0.7,
                    max_tokens=500
                )
                
                content = response.choices[0].message.content
                
                # Create trace entry
                trace = {
                    "step": step + 1,
                    "thought": content[:200] + "..." if len(content) > 200 else content,
                    "action": f"Processing step {step + 1}",
                    "observation": content,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                traces.append(trace)
                
                # Add to conversation history
                conversation.append({"role": "assistant", "content": content})
                
                # Check if task seems complete
                if any(word in content.lower() for word in ["complete", "finished", "done", "final"]):
                    break
                
                # Ask for next step
                if step < max_steps - 1:
                    conversation.append({
                        "role": "user", 
                        "content": "Continue to the next step if needed, or confirm completion."
                    })
                
            except Exception as e:
                error_msg = str(e)
                traces.append({
                    "step": step + 1,
                    "thought": "Error occurred",
                    "action": "Error handling",
                    "error": error_msg,
                    "observation": f"Execution failed: {error_msg}",
                    "timestamp": datetime.utcnow().isoformat()
                })
                break
        
        return traces
