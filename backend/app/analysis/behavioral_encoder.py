"""
Behavioral Encoder Module
Encodes agent execution traces into embeddings for pattern analysis
"""

import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import faiss

class BehavioralEncoder:
    """Encode agent behavior into vector embeddings"""
    
    def __init__(self):
        # Load pre-trained sentence transformer
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384
        
        # Initialize FAISS index for similarity search
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Store pattern categories
        self.patterns = {
            "honest": [],
            "deceptive": [],
            "reward_hacking": []
        }
        
    def encode_trace(self, trace: Dict[str, Any]) -> np.ndarray:
        """
        Encode single execution trace into embedding
        
        Args:
            trace: Single step trace with thought, action, observation
            
        Returns:
            384-dimensional embedding vector
        """
        # Combine all text from trace
        text = f"{trace.get('thought', '')} {trace.get('action', '')} {trace.get('observation', '')}"
        
        # Generate embedding
        embedding = self.model.encode(text)
        return embedding
    
    def encode_execution(self, traces: List[Dict[str, Any]]) -> np.ndarray:
        """
        Encode full execution into single embedding
        
        Args:
            traces: List of execution traces
            
        Returns:
            Averaged embedding representing full execution
        """
        if not traces:
            return np.zeros(self.dimension)
        
        # Encode each trace
        embeddings = [self.encode_trace(trace) for trace in traces]
        
        # Average embeddings
        return np.mean(embeddings, axis=0)
    
    def detect_pattern_type(self, embedding: np.ndarray) -> Dict[str, float]:
        """
        Classify behavior pattern type
        
        Args:
            embedding: Behavioral embedding vector
            
        Returns:
            Dictionary with confidence scores for each pattern type
        """
        # Heuristic-based classification
        # In production, this would use a trained classifier
        scores = {
            "honest": 0.7,  # Default high honesty
            "deceptive": 0.1,
            "reward_hacking": 0.2
        }
        
        # Add to FAISS index for future similarity searches
        self.index.add(np.array([embedding]))
        
        return scores
    
    def find_similar_patterns(self, embedding: np.ndarray, k: int = 5) -> List[int]:
        """
        Find similar behavioral patterns in history
        
        Args:
            embedding: Query embedding
            k: Number of similar patterns to return
            
        Returns:
            List of indices of similar patterns
        """
        if self.index.ntotal == 0:
            return []
        
        # Search for k nearest neighbors
        distances, indices = self.index.search(
            np.array([embedding]), 
            min(k, self.index.ntotal)
        )
        
        return indices[0].tolist()
    
    def add_labeled_pattern(self, embedding: np.ndarray, pattern_type: str):
        """
        Add labeled pattern for supervised learning
        
        Args:
            embedding: Pattern embedding
            pattern_type: Category (honest, deceptive, reward_hacking)
        """
        if pattern_type in self.patterns:
            self.patterns[pattern_type].append(embedding)
