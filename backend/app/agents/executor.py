"""
Agent Executor Module
Executes AI agent tasks and captures full execution traces
"""

import openai
import anthropic
import json
from typing import List, Dict, Any
from datetime import datetime
import os

class AgentExecutor:
    """Execute AI agent tasks with full tracing"""
    
    def __init__(self, agent_type: str = "gpt-4"):
        self.agent_type = agent_type
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
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
        
        system_prompt = """You are an AI agent executing tasks. 
        For each step, provide:
        1. Your thought process (reasoning)
        2. The action you'll take
        3. Any tool calls needed
        
        Format your response as JSON:
        {
            "thought": "your detailed reasoning here",
            "action": "specific action description",
            "tool_call": {"tool": "tool_name", "params": {"key": "value"}},
            "needs_more_steps": true/false
        }
        
        Be thorough and transparent in your reasoning.
        """
        
        conversation = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Task: {task}"}
        ]
        
        for step in range(max_steps):
            try:
                # Execute based on agent type
                if "gpt" in self.agent_type.lower():
                    response = self.openai_client.chat.completions.create(
                        model=self.agent_type,
                        messages=conversation,
                        temperature=0.7,
                        response_format={"type": "json_object"}
                    )
                    content = response.choices[0].message.content
                else:
                    # Anthropic Claude
                    response = self.anthropic_client.messages.create(
                        model="claude-3-sonnet-20240229",
                        max_tokens=1024,
                        messages=[{"role": m["role"], "content": m["content"]} 
                                 for m in conversation if m["role"] != "system"]
                    )
                    content = response.content[0].text
                
                # Parse response
                step_data = json.loads(content)
                
                # Create trace entry
                trace = {
                    "step": step + 1,
                    "thought": step_data.get("thought", ""),
                    "action": step_data.get("action", ""),
                    "tool_call": step_data.get("tool_call"),
                    "observation": f"Step {step + 1} completed successfully",
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                traces.append(trace)
                
                # Add to conversation history
                conversation.append({"role": "assistant", "content": content})
                
                # Check if more steps needed
                if not step_data.get("needs_more_steps", True):
                    break
                    
                # Simulate observation feedback
                conversation.append({
                    "role": "user", 
                    "content": f"Observation: {trace['observation']}. Continue if needed."
                })
                
            except json.JSONDecodeError as e:
                traces.append({
                    "step": step + 1,
                    "error": f"JSON parsing error: {str(e)}",
                    "timestamp": datetime.utcnow().isoformat()
                })
                break
            except Exception as e:
                traces.append({
                    "step": step + 1,
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                })
                break
        
        return traces
