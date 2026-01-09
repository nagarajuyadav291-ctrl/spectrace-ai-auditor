// SpecTrace - ChatGPT Clone with AI Safety
const API_URL = 'http://localhost:8000/api';

let currentModel = 'llama-3.1-70b-versatile';
let isProcessing = false;
let chatHistory = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  newChat();
});

// New Chat
function newChat() {
  const container = document.getElementById('chatContainer');
  container.innerHTML = `
    <div class="welcome" id="welcome">
      <h1>SpecTrace</h1>
      <p style="font-size: 18px; color: var(--text-secondary);">AI Safety Monitor with Real-Time Risk Analysis</p>
      
      <div class="examples">
        <div class="example-card" onclick="setPrompt('What is artificial intelligence?')">
          <h3>💡 Examples</h3>
          <p>What is artificial intelligence?</p>
        </div>
        <div class="example-card" onclick="setPrompt('Explain quantum computing')">
          <h3>🔬 Science</h3>
          <p>Explain quantum computing</p>
        </div>
        <div class="example-card" onclick="setPrompt('What are the risks of AI?')">
          <h3>⚠️ Safety</h3>
          <p>What are the risks of AI?</p>
        </div>
      </div>
    </div>
  `;
  chatHistory = [];
}

// Set Prompt
function setPrompt(text) {
  document.getElementById('messageInput').value = text;
  document.getElementById('messageInput').focus();
}

// Send Message
async function sendMessage() {
  if (isProcessing) return;
  
  const input = document.getElementById('messageInput');
  const message = input.value.trim();
  
  if (!message) return;
  
  // Clear input
  input.value = '';
  input.style.height = 'auto';
  
  // Remove welcome
  const welcome = document.getElementById('welcome');
  if (welcome) welcome.remove();
  
  // Add user message
  addMessage('user', message);
  
  // Add loading
  const loadingId = addLoading();
  
  // Disable input
  isProcessing = true;
  document.getElementById('sendBtn').disabled = true;
  
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, model: currentModel })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'API Error');
    }
    
    const data = await response.json();
    
    // Remove loading
    removeMessage(loadingId);
    
    // Add response
    addMessage('assistant', data.response, data.risk_analysis);
    
    // Update safety panel
    updateSafety(data.risk_analysis);
    
  } catch (error) {
    console.error('Error:', error);
    removeMessage(loadingId);
    addMessage('assistant', `❌ Error: ${error.message}\n\nMake sure:\n1. Backend is running (port 8000)\n2. API keys are in .env file\n3. Database is SQLite (not PostgreSQL)`, null);
  } finally {
    isProcessing = false;
    document.getElementById('sendBtn').disabled = false;
    input.focus();
  }
}

// Add Message
function addMessage(role, content, risk = null) {
  const container = document.getElementById('chatContainer');
  
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${role}`;
  messageDiv.id = `msg-${Date.now()}`;
  
  messageDiv.innerHTML = `
    <div class="message-content">
      <div class="message-avatar">${role === 'user' ? '👤' : '🤖'}</div>
      <div style="flex: 1;">
        <div class="message-text">${content}</div>
        ${risk ? `
          <div class="risk-badge ${getRiskLevel(risk.risk_score)}">
            ${getRiskEmoji(risk.risk_score)} Risk: ${(risk.risk_score * 100).toFixed(0)}%
          </div>
          <div class="message-actions">
            <button class="action-btn" onclick="copyText('${messageDiv.id}')">📋 Copy</button>
            <button class="action-btn" onclick="regenerate()">🔄 Regenerate</button>
            <button class="action-btn" onclick="toggleSafety()">🛡️ Safety</button>
          </div>
        ` : ''}
      </div>
    </div>
  `;
  
  container.appendChild(messageDiv);
  container.scrollTop = container.scrollHeight;
  
  chatHistory.push({ role, content, risk });
  
  return messageDiv.id;
}

// Add Loading
function addLoading() {
  const container = document.getElementById('chatContainer');
  
  const loadingDiv = document.createElement('div');
  loadingDiv.className = 'message assistant';
  const loadingId = `loading-${Date.now()}`;
  loadingDiv.id = loadingId;
  
  loadingDiv.innerHTML = `
    <div class="message-content">
      <div class="message-avatar">🤖</div>
      <div class="loading">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  `;
  
  container.appendChild(loadingDiv);
  container.scrollTop = container.scrollHeight;
  
  return loadingId;
}

// Remove Message
function removeMessage(id) {
  const msg = document.getElementById(id);
  if (msg) msg.remove();
}

// Get Risk Level
function getRiskLevel(score) {
  if (score < 0.3) return 'low';
  if (score < 0.6) return 'medium';
  return 'high';
}

// Get Risk Emoji
function getRiskEmoji(score) {
  if (score < 0.3) return '✅';
  if (score < 0.6) return '⚡';
  return '⚠️';
}

// Update Safety Panel
function updateSafety(risk) {
  const content = document.getElementById('safetyContent');
  
  content.innerHTML = `
    <div class="safety-section">
      <h4>Risk Score</h4>
      <div class="metric">
        <div class="metric-label">Overall Risk</div>
        <div class="metric-value" style="color: ${getRiskColor(risk.risk_score)}">
          ${(risk.risk_score * 100).toFixed(1)}%
        </div>
      </div>
      <div class="metric">
        <div class="metric-label">Deception Probability</div>
        <div class="metric-value">${(risk.deception_probability * 100).toFixed(1)}%</div>
      </div>
      <div class="metric">
        <div class="metric-label">Confidence</div>
        <div class="metric-value">${(risk.confidence * 100).toFixed(0)}%</div>
      </div>
    </div>
    
    <div class="safety-section">
      <h4>Analysis Breakdown</h4>
      ${renderBreakdown(risk.breakdown)}
    </div>
    
    <div class="safety-section">
      <h4>Explanation</h4>
      ${risk.explanation.map(exp => `
        <div class="metric">
          <div style="font-size: 14px;">${exp}</div>
        </div>
      `).join('')}
    </div>
    
    ${risk.violations.length > 0 ? `
      <div class="safety-section">
        <h4>⚠️ Violations (${risk.violations.length})</h4>
        ${risk.violations.map(v => `
          <div class="metric" style="border-left: 3px solid ${v.severity === 'critical' ? '#ef4444' : v.severity === 'high' ? '#f59e0b' : '#3b82f6'}">
            <div class="metric-label">${v.severity.toUpperCase()}: ${v.rule_name}</div>
            <div style="font-size: 13px; margin-top: 4px; color: var(--text-secondary);">${v.description}</div>
          </div>
        `).join('')}
      </div>
    ` : ''}
  `;
  
  // Auto-open if high risk
  if (risk.risk_score >= 0.5) {
    document.getElementById('safetyPanel').classList.add('open');
  }
}

// Render Breakdown
function renderBreakdown(breakdown) {
  return `
    <div class="metric">
      <div class="metric-label">Content Safety (40%)</div>
      <div class="metric-value">${(breakdown.content_safety.score * 100).toFixed(0)}%</div>
      <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
        ${breakdown.content_safety.engine_count} engines
      </div>
    </div>
    <div class="metric">
      <div class="metric-label">Behavioral (30%)</div>
      <div class="metric-value">${(breakdown.behavioral_patterns.score * 100).toFixed(0)}%</div>
      <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
        ${breakdown.behavioral_patterns.patterns_detected} patterns
      </div>
    </div>
    <div class="metric">
      <div class="metric-label">Deception (20%)</div>
      <div class="metric-value">${(breakdown.deception_detection.score * 100).toFixed(0)}%</div>
      <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
        ${breakdown.deception_detection.confidence} confidence
      </div>
    </div>
    <div class="metric">
      <div class="metric-label">Compliance (10%)</div>
      <div class="metric-value">${(breakdown.compliance.score * 100).toFixed(0)}%</div>
      <div style="font-size: 12px; color: var(--text-secondary); margin-top: 4px;">
        ${breakdown.compliance.compliant ? 'Compliant' : 'Violations'}
      </div>
    </div>
  `;
}

// Get Risk Color
function getRiskColor(score) {
  if (score < 0.3) return '#10b981';
  if (score < 0.6) return '#f59e0b';
  return '#ef4444';
}

// Copy Text
function copyText(msgId) {
  const msg = document.getElementById(msgId);
  const text = msg.querySelector('.message-text').textContent;
  navigator.clipboard.writeText(text);
  
  // Show feedback
  const btn = event.target;
  const originalText = btn.textContent;
  btn.textContent = '✓ Copied';
  setTimeout(() => btn.textContent = originalText, 2000);
}

// Regenerate
function regenerate() {
  if (chatHistory.length >= 2) {
    const lastUser = chatHistory[chatHistory.length - 2];
    if (lastUser.role === 'user') {
      document.getElementById('messageInput').value = lastUser.content;
      sendMessage();
    }
  }
}

// Toggle Safety
function toggleSafety() {
  document.getElementById('safetyPanel').classList.toggle('open');
}

// Update Model
function updateModel() {
  currentModel = document.getElementById('modelSelect').value;
}

// Handle Key Press
function handleKeyPress(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
}

// Auto Resize
function autoResize(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
}
