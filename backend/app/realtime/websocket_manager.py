"""
Real-Time Monitoring Service
WebSocket-based live agent execution streaming
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Set
import json
import asyncio
from datetime import datetime

class ConnectionManager:
    """Manage WebSocket connections for real-time monitoring"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.execution_streams: Dict[int, List[Dict]] = {}
    
    async def connect(self, websocket: WebSocket, execution_id: str):
        """Connect client to execution stream"""
        await websocket.accept()
        
        if execution_id not in self.active_connections:
            self.active_connections[execution_id] = set()
        
        self.active_connections[execution_id].add(websocket)
        
        # Send connection confirmation
        await websocket.send_json({
            "type": "connected",
            "execution_id": execution_id,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def disconnect(self, websocket: WebSocket, execution_id: str):
        """Disconnect client from execution stream"""
        if execution_id in self.active_connections:
            self.active_connections[execution_id].discard(websocket)
            
            if not self.active_connections[execution_id]:
                del self.active_connections[execution_id]
    
    async def broadcast_step(self, execution_id: str, step_data: Dict):
        """Broadcast execution step to all connected clients"""
        if execution_id not in self.active_connections:
            return
        
        # Store step in stream history
        if execution_id not in self.execution_streams:
            self.execution_streams[execution_id] = []
        
        self.execution_streams[execution_id].append(step_data)
        
        # Broadcast to all connected clients
        disconnected = set()
        
        for connection in self.active_connections[execution_id]:
            try:
                await connection.send_json({
                    "type": "step_update",
                    "execution_id": execution_id,
                    "step": step_data,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception:
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection, execution_id)
    
    async def broadcast_risk_update(self, execution_id: str, risk_data: Dict):
        """Broadcast real-time risk assessment"""
        if execution_id not in self.active_connections:
            return
        
        for connection in self.active_connections[execution_id]:
            try:
                await connection.send_json({
                    "type": "risk_update",
                    "execution_id": execution_id,
                    "risk": risk_data,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception:
                pass
    
    async def broadcast_completion(self, execution_id: str, result: Dict):
        """Broadcast execution completion"""
        if execution_id not in self.active_connections:
            return
        
        for connection in self.active_connections[execution_id]:
            try:
                await connection.send_json({
                    "type": "execution_complete",
                    "execution_id": execution_id,
                    "result": result,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception:
                pass
    
    def get_stream_history(self, execution_id: str) -> List[Dict]:
        """Get execution stream history"""
        return self.execution_streams.get(execution_id, [])

# Global connection manager instance
manager = ConnectionManager()
