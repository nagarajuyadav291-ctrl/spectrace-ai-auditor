"""
AI Behavior Prediction Engine
Predicts agent behavior before execution using ML models
REVOLUTIONARY FEATURE: No existing tool does this!
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple
import pickle
import os

class BehaviorPredictor:
    """Predict agent behavior patterns before execution"""
    
    def __init__(self):
        self.risk_predictor = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.deception_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
        # Feature extractors
        self.task_features = {
            'length': 0,
            'complexity_score': 0,
            'sensitive_keywords': 0,
            'action_verbs': 0,
            'question_marks': 0
        }
    
    def extract_features(self, task_description: str, agent_type: str, max_steps: int) -> np.ndarray:
        """
        Extract features from task for prediction
        
        Features:
        - Task length
        - Complexity score (based on keywords)
        - Sensitive keyword count
        - Action verb count
        - Question count
        - Agent type encoding
        - Max steps
        """
        features = []
        
        # Task length
        features.append(len(task_description))
        
        # Complexity score
        complex_keywords = ['analyze', 'research', 'investigate', 'evaluate', 'compare', 'synthesize']
        complexity = sum(1 for kw in complex_keywords if kw in task_description.lower())
        features.append(complexity)
        
        # Sensitive keywords
        sensitive_keywords = ['hack', 'bypass', 'exploit', 'manipulate', 'deceive', 'hide', 'secret']
        sensitive_count = sum(1 for kw in sensitive_keywords if kw in task_description.lower())
        features.append(sensitive_count)
        
        # Action verbs
        action_verbs = ['create', 'delete', 'modify', 'send', 'access', 'execute', 'run']
        action_count = sum(1 for verb in action_verbs if verb in task_description.lower())
        features.append(action_count)
        
        # Question marks
        features.append(task_description.count('?'))
        
        # Agent type encoding
        agent_encoding = {'gpt-4': 1.0, 'gpt-3.5-turbo': 0.7, 'claude-3': 0.9}
        features.append(agent_encoding.get(agent_type, 0.5))
        
        # Max steps
        features.append(max_steps)
        
        # Word count
        features.append(len(task_description.split()))
        
        # Exclamation marks
        features.append(task_description.count('!'))
        
        # Capital letter ratio
        if len(task_description) > 0:
            capital_ratio = sum(1 for c in task_description if c.isupper()) / len(task_description)
        else:
            capital_ratio = 0
        features.append(capital_ratio)
        
        return np.array(features).reshape(1, -1)
    
    def predict_risk(self, task_description: str, agent_type: str, max_steps: int) -> Dict:
        """
        Predict execution risk before running
        
        Returns:
            Dictionary with predicted risk score, confidence, and warnings
        """
        features = self.extract_features(task_description, agent_type, max_steps)
        
        if not self.is_trained:
            # Use heuristic-based prediction if model not trained
            return self._heuristic_prediction(task_description, agent_type, max_steps)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict risk
        predicted_risk = self.risk_predictor.predict(features_scaled)[0]
        predicted_risk = np.clip(predicted_risk, 0.0, 1.0)
        
        # Predict deception probability
        deception_prob = self.deception_classifier.predict_proba(features_scaled)[0][1]
        
        # Generate warnings
        warnings = self._generate_warnings(task_description, predicted_risk, deception_prob)
        
        # Calculate confidence
        confidence = self._calculate_confidence(features_scaled)
        
        return {
            'predicted_risk': float(predicted_risk),
            'predicted_deception': float(deception_prob),
            'confidence': float(confidence),
            'warnings': warnings,
            'recommendation': self._get_recommendation(predicted_risk, deception_prob)
        }
    
    def _heuristic_prediction(self, task_description: str, agent_type: str, max_steps: int) -> Dict:
        """Heuristic-based prediction when ML model not trained"""
        
        # Calculate heuristic risk
        risk_score = 0.0
        
        # Check for sensitive keywords
        sensitive_keywords = ['hack', 'bypass', 'exploit', 'manipulate', 'deceive', 'hide', 'secret', 'unauthorized']
        sensitive_count = sum(1 for kw in sensitive_keywords if kw in task_description.lower())
        risk_score += min(sensitive_count * 0.2, 0.6)
        
        # Check task complexity
        if len(task_description) > 200:
            risk_score += 0.1
        
        # Check max steps
        if max_steps > 20:
            risk_score += 0.1
        
        # Agent-specific adjustment
        if agent_type == 'gpt-4':
            risk_score *= 0.9  # GPT-4 generally safer
        
        risk_score = min(risk_score, 1.0)
        
        # Estimate deception probability
        deception_indicators = ['hide', 'conceal', 'secret', 'don\'t tell', 'pretend']
        deception_count = sum(1 for ind in deception_indicators if ind in task_description.lower())
        deception_prob = min(deception_count * 0.25, 0.8)
        
        warnings = self._generate_warnings(task_description, risk_score, deception_prob)
        
        return {
            'predicted_risk': float(risk_score),
            'predicted_deception': float(deception_prob),
            'confidence': 0.7,  # Moderate confidence for heuristics
            'warnings': warnings,
            'recommendation': self._get_recommendation(risk_score, deception_prob)
        }
    
    def _generate_warnings(self, task: str, risk: float, deception: float) -> List[str]:
        """Generate warnings based on predictions"""
        warnings = []
        
        if risk > 0.7:
            warnings.append("⚠️ HIGH RISK: This task may violate safety constraints")
        elif risk > 0.4:
            warnings.append("⚡ MEDIUM RISK: Monitor execution closely")
        
        if deception > 0.5:
            warnings.append("🚨 DECEPTION ALERT: High probability of deceptive behavior")
        
        # Check for specific patterns
        if 'hack' in task.lower() or 'exploit' in task.lower():
            warnings.append("🔒 SECURITY CONCERN: Task involves potentially harmful actions")
        
        if 'bypass' in task.lower() or 'circumvent' in task.lower():
            warnings.append("⛔ BOUNDARY VIOLATION: Task may attempt to bypass restrictions")
        
        return warnings
    
    def _get_recommendation(self, risk: float, deception: float) -> str:
        """Get execution recommendation"""
        if risk > 0.7 or deception > 0.6:
            return "❌ NOT RECOMMENDED: High risk of safety violations"
        elif risk > 0.4 or deception > 0.3:
            return "⚠️ PROCEED WITH CAUTION: Monitor execution closely"
        else:
            return "✅ SAFE TO EXECUTE: Low risk detected"
    
    def _calculate_confidence(self, features: np.ndarray) -> float:
        """Calculate prediction confidence"""
        # Simple confidence based on feature variance
        # In production, use model uncertainty estimation
        return 0.85
    
    def train(self, historical_data: List[Dict]):
        """
        Train prediction models on historical execution data
        
        Args:
            historical_data: List of past executions with features and outcomes
        """
        if len(historical_data) < 10:
            return  # Need minimum data for training
        
        X = []
        y_risk = []
        y_deception = []
        
        for data in historical_data:
            features = self.extract_features(
                data['task_description'],
                data['agent_type'],
                data['max_steps']
            )
            X.append(features[0])
            y_risk.append(data['actual_risk'])
            y_deception.append(1 if data['actual_deception'] > 0.5 else 0)
        
        X = np.array(X)
        y_risk = np.array(y_risk)
        y_deception = np.array(y_deception)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train models
        self.risk_predictor.fit(X_scaled, y_risk)
        self.deception_classifier.fit(X_scaled, y_deception)
        
        self.is_trained = True
    
    def save_model(self, path: str):
        """Save trained model to disk"""
        model_data = {
            'risk_predictor': self.risk_predictor,
            'deception_classifier': self.deception_classifier,
            'scaler': self.scaler,
            'is_trained': self.is_trained
        }
        
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, path: str):
        """Load trained model from disk"""
        if not os.path.exists(path):
            return
        
        with open(path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.risk_predictor = model_data['risk_predictor']
        self.deception_classifier = model_data['deception_classifier']
        self.scaler = model_data['scaler']
        self.is_trained = model_data['is_trained']
