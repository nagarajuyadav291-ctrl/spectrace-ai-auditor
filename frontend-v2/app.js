// SpecTrace 2.0 - ChatGPT-like Interface
const API_URL = 'http://localhost:8000/api';

let currentChatId = null;
let chatHistory = [];
let currentModel = 'llama-3.1-70b-versatile';
let isProcessing = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  loadChatHistory();
  loadSettings();
  newChat();
});

// Chat Functions
function newChat() {
  currentChatId = Date.now();
  const chatContainer = document.getElementById('chatContainer');
  chatContainer.innerHTML = '';
  
  // Show welcome screen
  const welcomeScreen = createWelcomeScreen();
  chatContainer.appendChild(welcomeScreen);
  
  // Add to history
  chatHistory.unshift({
    id: currentChatId,
    title: 'New Chat',
    messages: [],
    timestamp: new Date()
  });
  
  updateChatHistorySidebar();
}

function createWelcomeScreen() {
  const welcome = document.createElement('div');
  welcome.className = 'welcome-screen';
  welcome.id = 'welcomeScreen';
  welcome.innerHTML = `
    <div class="welcome-content">
      <h1>🔍 SpecTrace</h1>
      <p class="tagline">AI Safety Monitor with Real-Time Risk Analysis</p>
      
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">🛡️</div>
          <h3>Multi-Engine Safety</h3>
          <p>3+ independent detection systems</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📊</div>
          <h3>Risk Scoring</h3>
          <p>Transparent, explainable metrics</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🔍</div>
          <h3>Deception Detection</h3>
          <p>Behavioral pattern analysis</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">✅</div>
          <h3>Compliance Check</h3>
          <p>Regulatory violation alerts</p>
        </div>
      </div>
      
      <div class="example-prompts">
        <p class="example-label">Try asking:</p>
        <button class="example-btn" onclick="setPrompt('What is artificial intelligence?')">
          What is artificial intelligence?
        </button>
        <button class="example-btn" onclick="setPrompt('Explain quantum computing in simple terms')">
          Explain quantum computing
        </button>
        <button class="example-btn" onclick="setPrompt('What are the risks of AI?')">
          What are the risks of AI?
        </button>
      </div>
    </div>
  `;
  return welcome;
}

function setPrompt(text) {
  document.getElementById('messageInput').value = text;
  document.getElementById('messageInput').focus();
}

async function sendMessage() {
  if (isProcessing) return;
  
  const input = document.getElementById('messageInput');
  const message = input.value.trim();
  
  if (!message) return;
  
  // Clear input
  input.value = '';
  input.style.height = 'auto';
  
  // Remove welcome screen
  const welcomeScreen = document.getElementById('welcomeScreen');
  if (welcomeScreen) {
    welcomeScreen.remove();
  }
  
  // Add user message
  addMessage('user', message);
  
  // Add loading message
  const loadingId = addLoadingMessage();
  
  // Disable input
  isProcessing = true;
  document.getElementById('sendBtn').disabled = true;
  
  try {
    // Call API
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: message,
        model: currentModel
      })
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    // Remove loading
    removeMessage(loadingId);
    
    // Add assistant response
    addMessage('assistant', data.response, data.risk_analysis);
    
    // Update safety panel
    updateSafetyPanel(data.risk_analysis);
    
    // Update chat title if first message
    const currentChat = chatHistory.find(c => c.id === currentChatId);
    if (currentChat && currentChat.messages.length === 2) {
      currentChat.title = message.substring(0, 50) + (message.length > 50 ? '...' : '');
      updateChatHistorySidebar();
    }
    
  } catch (error) {
    console.error('Error:', error);
    removeMessage(loadingId);
    addMessage('assistant', `❌ Error: ${error.message}`, null);
  } finally {
    isProcessing = false;
    document.getElementById('sendBtn').disabled = false;
    input.focus();
  }
}

function addMessage(role, content, riskAnalysis = null) {
  const chatContainer = document.getElementById('chatContainer');
  
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${role}`;
  messageDiv.id = `msg-${Date.now()}`;
  
  const avatar = document.createElement('div');
  avatar.className = 'message-avatar';
  avatar.textContent = role === 'user' ? '👤' : '🤖';
  
  const contentDiv = document.createElement('div');
  contentDiv.className = 'message-content';
  
  const textDiv = document.createElement('div');
  textDiv.className = 'message-text';
  textDiv.textContent = content;
  
  contentDiv.appendChild(textDiv);
  
  // Add risk badge for assistant messages
  if (role === 'assistant' && riskAnalysis) {
    const riskBadge = createRiskBadge(riskAnalysis.risk_score);
    contentDiv.appendChild(riskBadge);
    
    // Add actions
    const actions = document.createElement('div');
    actions.className = 'message-actions';
    actions.innerHTML = `
      <button class="action-btn" onclick="copyMessage('${messageDiv.id}')">📋 Copy</button>
      <button class="action-btn" onclick="regenerateResponse()">🔄 Regenerate</button>
      <button class="action-btn" onclick="viewDetails(${riskAnalysis.execution_id || 0})">🔍 Details</button>
    `;
    contentDiv.appendChild(actions);
  }
  
  messageDiv.appendChild(avatar);
  messageDiv.appendChild(contentDiv);
  
  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  
  // Save to chat history
  const currentChat = chatHistory.find(c => c.id === currentChatId);
  if (currentChat) {
    currentChat.messages.push({ role, content, riskAnalysis, timestamp: new Date() });
  }
  
  return messageDiv.id;
}

function addLoadingMessage() {
  const chatContainer = document.getElementById('chatContainer');
  
  const messageDiv = document.createElement('div');
  messageDiv.className = 'message assistant';
  const loadingId = `loading-${Date.now()}`;
  messageDiv.id = loadingId;
  
  const avatar = document.createElement('div');
  avatar.className = 'message-avatar';
  avatar.textContent = '🤖';
  
  const contentDiv = document.createElement('div');
  contentDiv.className = 'message-content';
  
  const loadingDiv = document.createElement('div');
  loadingDiv.className = 'loading-dots';
  loadingDiv.innerHTML = '<span></span><span></span><span></span>';
  
  contentDiv.appendChild(loadingDiv);
  messageDiv.appendChild(avatar);
  messageDiv.appendChild(contentDiv);
  
  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  
  return loadingId;
}

function removeMessage(id) {
  const message = document.getElementById(id);
  if (message) {
    message.remove();
  }
}

function createRiskBadge(score) {
  const badge = document.createElement('div');
  
  let level = 'low';
  let emoji = '✅';
  if (score >= 0.6) {
    level = 'high';
    emoji = '⚠️';
  } else if (score >= 0.3) {
    level = 'medium';
    emoji = '⚡';
  }
  
  badge.className = `risk-badge ${level}`;
  badge.innerHTML = `${emoji} Risk: ${(score * 100).toFixed(0)}%`;
  
  return badge;
}

// Safety Panel
function updateSafetyPanel(riskAnalysis) {
  const safetyContent = document.getElementById('safetyContent');
  
  safetyContent.innerHTML = `
    <div class="safety-section">
      <h4>Risk Score</h4>
      <div class="safety-metric">
        <div class="metric-label">Overall Risk</div>
        <div class="metric-value" style="color: ${getRiskColor(riskAnalysis.risk_score)}">
          ${(riskAnalysis.risk_score * 100).toFixed(1)}%
        </div>
      </div>
      <div class="safety-metric">
        <div class="metric-label">Deception Probability</div>
        <div class="metric-value">${(riskAnalysis.deception_probability * 100).toFixed(1)}%</div>
      </div>
      <div class="safety-metric">
        <div class="metric-label">Confidence</div>
        <div class="metric-value">${(riskAnalysis.confidence * 100).toFixed(0)}%</div>
      </div>
    </div>
    
    <div class="safety-section">
      <h4>Analysis Breakdown</h4>
      ${renderBreakdown(riskAnalysis.breakdown)}
    </div>
    
    <div class="safety-section">
      <h4>Explanation</h4>
      <ul class="explanation-list">
        ${riskAnalysis.explanation.map(exp => `<li>${exp}</li>`).join('')}
      </ul>
    </div>
    
    ${riskAnalysis.violations.length > 0 ? `
      <div class="safety-section">
        <h4>⚠️ Violations (${riskAnalysis.violations.length})</h4>
        ${renderViolations(riskAnalysis.violations)}
      </div>
    ` : ''}
  `;
  
  // Auto-open if high risk
  if (riskAnalysis.risk_score >= 0.5) {
    document.getElementById('safetyPanel').classList.add('open');
  }
}

function renderBreakdown(breakdown) {
  return `
    <div class="safety-metric">
      <div class="metric-label">Content Safety (40%)</div>
      <div class="metric-value">${(breakdown.content_safety.score * 100).toFixed(0)}%</div>
      <small>${breakdown.content_safety.engine_count} engines</small>
    </div>
    <div class="safety-metric">
      <div class="metric-label">Behavioral (30%)</div>
      <div class="metric-value">${(breakdown.behavioral_patterns.score * 100).toFixed(0)}%</div>
      <small>${breakdown.behavioral_patterns.patterns_detected} patterns</small>
    </div>
    <div class="safety-metric">
      <div class="metric-label">Deception (20%)</div>
      <div class="metric-value">${(breakdown.deception_detection.score * 100).toFixed(0)}%</div>
      <small>${breakdown.deception_detection.confidence} confidence</small>
    </div>
    <div class="safety-metric">
      <div class="metric-label">Compliance (10%)</div>
      <div class="metric-value">${(breakdown.compliance.score * 100).toFixed(0)}%</div>
      <small>${breakdown.compliance.compliant ? 'Compliant' : 'Violations'}</small>
    </div>
  `;
}

function renderViolations(violations) {
  return violations.map(v => `
    <div class="safety-metric" style="border-left: 3px solid ${v.severity === 'critical' ? '#ef4444' : v.severity === 'high' ? '#f59e0b' : '#3b82f6'}">
      <div class="metric-label">${v.severity.toUpperCase()}: ${v.rule_name}</div>
      <div style="font-size: 0.875rem; margin-top: 0.25rem;">${v.description}</div>
    </div>
  `).join('');
}

function getRiskColor(score) {
  if (score < 0.3) return '#10b981';
  if (score < 0.6) return '#f59e0b';
  return '#ef4444';
}

// UI Functions
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('hidden');
}

function toggleSafetyPanel() {
  document.getElementById('safetyPanel').classList.toggle('open');
}

function toggleDarkMode() {
  const html = document.documentElement;
  const currentTheme = html.getAttribute('data-theme');
  html.setAttribute('data-theme', currentTheme === 'dark' ? 'light' : 'dark');
  localStorage.setItem('theme', currentTheme === 'dark' ? 'light' : 'dark');
}

function toggleSettings() {
  document.getElementById('settingsModal').classList.toggle('open');
}

function updateModel() {
  currentModel = document.getElementById('modelSelect').value;
}

function handleKeyPress(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
}

function autoResize(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
}

function copyMessage(messageId) {
  const message = document.getElementById(messageId);
  const text = message.querySelector('.message-text').textContent;
  navigator.clipboard.writeText(text);
  alert('Copied to clipboard!');
}

function regenerateResponse() {
  // Get last user message
  const currentChat = chatHistory.find(c => c.id === currentChatId);
  if (currentChat && currentChat.messages.length >= 2) {
    const lastUserMessage = currentChat.messages[currentChat.messages.length - 2];
    if (lastUserMessage.role === 'user') {
      document.getElementById('messageInput').value = lastUserMessage.content;
      sendMessage();
    }
  }
}

function viewDetails(executionId) {
  alert(`Viewing details for execution #${executionId}\n\nFull execution trace and analysis would be shown here.`);
}

// Chat History
function updateChatHistorySidebar() {
  const historyDiv = document.getElementById('chatHistory');
  historyDiv.innerHTML = chatHistory.map(chat => `
    <div class="chat-history-item ${chat.id === currentChatId ? 'active' : ''}" 
         onclick="loadChat(${chat.id})">
      ${chat.title}
    </div>
  `).join('');
}

function loadChat(chatId) {
  const chat = chatHistory.find(c => c.id === chatId);
  if (!chat) return;
  
  currentChatId = chatId;
  
  const chatContainer = document.getElementById('chatContainer');
  chatContainer.innerHTML = '';
  
  // Reload messages
  chat.messages.forEach(msg => {
    addMessage(msg.role, msg.content, msg.riskAnalysis);
  });
  
  updateChatHistorySidebar();
}

function loadChatHistory() {
  const saved = localStorage.getItem('chatHistory');
  if (saved) {
    chatHistory = JSON.parse(saved);
    updateChatHistorySidebar();
  }
}

function saveChatHistory() {
  localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
}

// Settings
function loadSettings() {
  const theme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', theme);
}

function changeTheme() {
  const theme = document.getElementById('themeSelect').value;
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
}

// Auto-save chat history
setInterval(saveChatHistory, 5000);
