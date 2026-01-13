let API_BASE = 'http://localhost:8000';
let currentChatId = null;
let messageHistory = [];
let chatSessions = [];

// DOM Elements
const messagesContainer = document.getElementById('messagesContainer');
const welcomeScreen = document.getElementById('welcomeScreen');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const modelSelect = document.getElementById('modelSelect');
const mainContent = document.getElementById('mainContent');
const chatHistory = document.getElementById('chatHistory');
const safetyPanel = document.getElementById('safetyPanel');

// Auto-resize textarea
userInput.addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
});

// Handle Enter key
function handleKeyPress(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
}

// Send example
function sendExample(text) {
  userInput.value = text;
  sendMessage();
}

// New chat
function newChat() {
  currentChatId = null;
  messageHistory = [];
  messagesContainer.innerHTML = `
    <div class="welcome" id="welcomeScreen">
      <h1>How can I help you today?</h1>
      <div class="examples">
        <div class="example-card" onclick="sendExample('Explain quantum computing in simple terms')">
          <p>Explain quantum computing in simple terms</p>
        </div>
        <div class="example-card" onclick="sendExample('What is artificial intelligence?')">
          <p>What is artificial intelligence?</p>
        </div>
        <div class="example-card" onclick="sendExample('How does machine learning work?')">
          <p>How does machine learning work?</p>
        </div>
      </div>
    </div>
  `;
}

// Toggle safety panel
function toggleSafety() {
  safetyPanel.classList.toggle('active');
}

// Plans modal
function openPlans() {
  document.getElementById('plansModal').classList.add('active');
}

function closePlans() {
  document.getElementById('plansModal').classList.remove('active');
}

// Settings
function openSettings() {
  document.getElementById('settingsModal').classList.add('active');
}

function closeSettings() {
  document.getElementById('settingsModal').classList.remove('active');
}

function saveSettings() {
  API_BASE = document.getElementById('backendUrl').value;
  closeSettings();
  alert('Settings saved!');
}

// Add to history
function addToHistory(message) {
  const historyItem = document.createElement('div');
  historyItem.className = 'history-item';
  historyItem.textContent = message.substring(0, 30) + (message.length > 30 ? '...' : '');
  historyItem.onclick = () => {
    // Load this chat (future feature)
  };
  chatHistory.insertBefore(historyItem, chatHistory.firstChild);
}

// Update safety metrics
function updateSafetyMetrics(safety) {
  if (!safety) return;

  const risk = Math.round(safety.overall_risk_score * 100);
  const deception = Math.round((safety.deception_probability || 0) * 100);
  const toxicity = Math.round((safety.toxicity_score || 0) * 100);
  const drift = Math.round((safety.behavioral_drift || 0) * 100);
  const compliance = 100 - risk;

  document.getElementById('riskScore').textContent = risk + '%';
  document.getElementById('deceptionScore').textContent = deception + '%';
  document.getElementById('toxicityScore').textContent = toxicity + '%';
  document.getElementById('driftScore').textContent = drift + '%';
  document.getElementById('complianceScore').textContent = compliance + '%';

  updateBar('riskBar', risk);
  updateBar('deceptionBar', deception);
  updateBar('toxicityBar', toxicity);
  updateBar('driftBar', drift);
  updateBar('complianceBar', compliance);
}

function updateBar(barId, value) {
  const bar = document.getElementById(barId);
  bar.style.width = value + '%';
  
  bar.className = 'metric-fill';
  if (value > 70) {
    bar.classList.add('danger');
  } else if (value > 40) {
    bar.classList.add('warning');
  }
}

// Send message
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  // Hide welcome screen
  if (welcomeScreen) {
    welcomeScreen.remove();
  }

  // Add to history
  addToHistory(message);

  // Add user message
  addMessage('user', message);
  messageHistory.push({ role: 'user', content: message });
  
  // Clear input
  userInput.value = '';
  userInput.style.height = 'auto';

  // Disable send button
  sendBtn.disabled = true;
  sendBtn.textContent = 'Sending...';

  // Add loading message
  const loadingId = addMessage('assistant', 'Thinking...', true);

  try {
    console.log('Sending request to:', `${API_BASE}/chat`);
    
    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        model: modelSelect.value,
        chat_id: currentChatId
      })
    });

    console.log('Response status:', response.status);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    console.log('Response data:', data);

    if (data.error) {
      updateMessage(loadingId, `Error: ${data.error}`, false, true);
    } else {
      currentChatId = data.chat_id;
      updateMessage(loadingId, data.response, false, false);
      messageHistory.push({ role: 'assistant', content: data.response });
      
      // Update safety metrics
      if (data.safety) {
        updateSafetyMetrics(data.safety);
      }
    }

  } catch (error) {
    console.error('Fetch error:', error);
    updateMessage(loadingId, 
      `❌ Connection Error\n\n` +
      `Cannot reach backend at ${API_BASE}\n\n` +
      `Troubleshooting:\n` +
      `1. Check backend is running: http://localhost:8000/docs\n` +
      `2. Check .env file has GROQ_API_KEY\n` +
      `3. Restart backend server\n\n` +
      `Error: ${error.message}`, 
      false, true
    );
  } finally {
    sendBtn.disabled = false;
    sendBtn.textContent = 'Send';
  }
}

// Add message to UI
function addMessage(role, content, isLoading = false) {
  const messageId = 'msg-' + Date.now();
  const messageDiv = document.createElement('div');
  messageDiv.id = messageId;
  messageDiv.className = `message ${role}`;

  const avatar = role === 'user' ? '👤' : '🤖';
  
  messageDiv.innerHTML = `
    <div class="avatar">${avatar}</div>
    <div class="message-content ${isLoading ? 'loading' : ''}">${content}</div>
  `;

  messagesContainer.appendChild(messageDiv);
  mainContent.scrollTop = mainContent.scrollHeight;

  return messageId;
}

// Update message
function updateMessage(messageId, content, isLoading = false, isError = false) {
  const messageDiv = document.getElementById(messageId);
  if (!messageDiv) return;

  const contentDiv = messageDiv.querySelector('.message-content');
  contentDiv.classList.remove('loading');
  
  if (isError) {
    contentDiv.className = 'message-content error';
  }
  
  contentDiv.textContent = content;
  mainContent.scrollTop = mainContent.scrollHeight;
}

// Check backend on load
window.addEventListener('load', async () => {
  try {
    const response = await fetch(`${API_BASE}/docs`);
    if (response.ok) {
      console.log('✅ Backend is running!');
    }
  } catch (error) {
    console.error('❌ Backend not running:', error);
    alert('⚠️ Backend is not running!\n\nPlease start backend:\ncd backend\n.\\venv\\Scripts\\Activate.ps1\nuvicorn app.main:app --reload --port 8000');
  }
});