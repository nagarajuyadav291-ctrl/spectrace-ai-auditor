// SpecTrace - Ultra-Modern AI Safety Monitor
const API_URL = 'http://localhost:8000/api';

let currentModel = 'llama-3.1-70b-versatile';
let isProcessing = false;
let chatHistory = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  newChat();
  loadChatHistory();
});

// New Chat
function newChat() {
  const container = document.getElementById('chatContainer');
  container.innerHTML = `
    <div id="welcome" class="h-full flex items-center justify-center p-8">
      <div class="max-w-4xl w-full text-center space-y-8">
        <div class="space-y-4">
          <div class="inline-block">
            <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center mb-4 mx-auto shadow-2xl shadow-purple-500/50">
              <i class="fas fa-shield-halved text-white text-4xl"></i>
            </div>
          </div>
          <h1 class="text-5xl font-bold gradient-text">Welcome to SpecTrace</h1>
          <p class="text-xl text-gray-400">AI Safety Monitor with Real-Time Risk Analysis</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-12">
          <div class="glass rounded-2xl p-6 hover:bg-white/10 transition-all cursor-pointer" onclick="setPrompt('What is artificial intelligence?')">
            <div class="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center mb-4">
              <i class="fas fa-lightbulb text-blue-400 text-2xl"></i>
            </div>
            <h3 class="font-semibold mb-2">Examples</h3>
            <p class="text-sm text-gray-400">What is artificial intelligence?</p>
          </div>
          
          <div class="glass rounded-2xl p-6 hover:bg-white/10 transition-all cursor-pointer" onclick="setPrompt('Explain quantum computing in simple terms')">
            <div class="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center mb-4">
              <i class="fas fa-atom text-purple-400 text-2xl"></i>
            </div>
            <h3 class="font-semibold mb-2">Science</h3>
            <p class="text-sm text-gray-400">Explain quantum computing</p>
          </div>
          
          <div class="glass rounded-2xl p-6 hover:bg-white/10 transition-all cursor-pointer" onclick="setPrompt('What are the risks of AI?')">
            <div class="w-12 h-12 rounded-xl bg-red-500/20 flex items-center justify-center mb-4">
              <i class="fas fa-exclamation-triangle text-red-400 text-2xl"></i>
            </div>
            <h3 class="font-semibold mb-2">Safety</h3>
            <p class="text-sm text-gray-400">What are the risks of AI?</p>
          </div>
        </div>
        
        <div class="grid grid-cols-3 gap-4 mt-8">
          <div class="glass rounded-xl p-4">
            <div class="text-3xl font-bold gradient-text">15+</div>
            <div class="text-sm text-gray-400">AI Models</div>
          </div>
          <div class="glass rounded-xl p-4">
            <div class="text-3xl font-bold gradient-text">100%</div>
            <div class="text-sm text-gray-400">Free Tier</div>
          </div>
          <div class="glass rounded-xl p-4">
            <div class="text-3xl font-bold gradient-text">Real-Time</div>
            <div class="text-sm text-gray-400">Safety Analysis</div>
          </div>
        </div>
      </div>
    </div>
  `;
  chatHistory = [];
  updateChatHistorySidebar();
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
  if (welcome) {
    document.getElementById('chatContainer').innerHTML = '<div class="p-6 space-y-6" id="messages"></div>';
  }
  
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
    
    // Save to history
    saveChatHistory(message, data.response);
    
  } catch (error) {
    console.error('Error:', error);
    removeMessage(loadingId);
    
    const errorMsg = `
      <div class="space-y-3">
        <div class="flex items-center gap-2 text-red-400">
          <i class="fas fa-exclamation-circle"></i>
          <span class="font-semibold">Error: ${error.message}</span>
        </div>
        <div class="text-sm text-gray-400 space-y-2">
          <p><strong>Troubleshooting:</strong></p>
          <ul class="list-disc list-inside space-y-1">
            <li>Backend running? Check <code class="bg-gray-800 px-2 py-1 rounded">http://localhost:8000/docs</code></li>
            <li>API keys in <code class="bg-gray-800 px-2 py-1 rounded">backend/.env</code>?</li>
            <li>Database set to SQLite? <code class="bg-gray-800 px-2 py-1 rounded">DATABASE_URL=sqlite:///./spectrace.db</code></li>
          </ul>
        </div>
      </div>
    `;
    addMessage('assistant', errorMsg, null);
  } finally {
    isProcessing = false;
    document.getElementById('sendBtn').disabled = false;
    input.focus();
  }
}

// Add Message
function addMessage(role, content, risk = null) {
  const messagesContainer = document.getElementById('messages');
  if (!messagesContainer) return;
  
  const messageDiv = document.createElement('div');
  messageDiv.className = 'flex gap-4';
  messageDiv.id = `msg-${Date.now()}`;
  
  const isUser = role === 'user';
  
  messageDiv.innerHTML = `
    <div class="flex-shrink-0">
      <div class="w-10 h-10 rounded-xl ${isUser ? 'bg-gradient-to-br from-blue-500 to-cyan-500' : 'bg-gradient-to-br from-purple-500 to-pink-500'} flex items-center justify-center shadow-lg">
        <i class="fas ${isUser ? 'fa-user' : 'fa-robot'} text-white"></i>
      </div>
    </div>
    
    <div class="flex-1 space-y-3">
      <div class="flex items-center gap-2">
        <span class="font-semibold">${isUser ? 'You' : 'SpecTrace AI'}</span>
        ${!isUser && risk ? `
          <span class="px-2 py-1 rounded-full text-xs font-medium ${getRiskBadgeClass(risk.risk_score)}">
            ${getRiskEmoji(risk.risk_score)} ${(risk.risk_score * 100).toFixed(0)}% Risk
          </span>
        ` : ''}
      </div>
      
      <div class="prose prose-invert max-w-none">
        ${content}
      </div>
      
      ${!isUser && risk ? `
        <div class="flex items-center gap-2">
          <button onclick="copyText('${messageDiv.id}')" class="px-3 py-1.5 rounded-lg glass hover:bg-white/10 transition-all text-sm flex items-center gap-2">
            <i class="fas fa-copy"></i>
            <span>Copy</span>
          </button>
          <button onclick="regenerate()" class="px-3 py-1.5 rounded-lg glass hover:bg-white/10 transition-all text-sm flex items-center gap-2">
            <i class="fas fa-redo"></i>
            <span>Regenerate</span>
          </button>
          <button onclick="toggleSafety()" class="px-3 py-1.5 rounded-lg glass hover:bg-white/10 transition-all text-sm flex items-center gap-2">
            <i class="fas fa-shield-halved text-purple-400"></i>
            <span>Safety</span>
          </button>
        </div>
      ` : ''}
    </div>
  `;
  
  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollIntoView({ behavior: 'smooth', block: 'end' });
  
  chatHistory.push({ role, content, risk });
}

// Add Loading
function addLoading() {
  const messagesContainer = document.getElementById('messages');
  if (!messagesContainer) return;
  
  const loadingDiv = document.createElement('div');
  loadingDiv.className = 'flex gap-4';
  const loadingId = `loading-${Date.now()}`;
  loadingDiv.id = loadingId;
  
  loadingDiv.innerHTML = `
    <div class="flex-shrink-0">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-lg">
        <i class="fas fa-robot text-white"></i>
      </div>
    </div>
    
    <div class="flex-1">
      <div class="font-semibold mb-2">SpecTrace AI</div>
      <div class="flex items-center gap-1">
        <div class="w-2 h-2 rounded-full bg-purple-400 typing-dot"></div>
        <div class="w-2 h-2 rounded-full bg-purple-400 typing-dot"></div>
        <div class="w-2 h-2 rounded-full bg-purple-400 typing-dot"></div>
      </div>
    </div>
  `;
  
  messagesContainer.appendChild(loadingDiv);
  messagesContainer.scrollIntoView({ behavior: 'smooth', block: 'end' });
  
  return loadingId;
}

// Remove Message
function removeMessage(id) {
  const msg = document.getElementById(id);
  if (msg) msg.remove();
}

// Get Risk Badge Class
function getRiskBadgeClass(score) {
  if (score < 0.3) return 'bg-green-500/20 text-green-400 border border-green-500/30';
  if (score < 0.6) return 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30';
  return 'bg-red-500/20 text-red-400 border border-red-500/30';
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
    <div class="space-y-6">
      
      <!-- Overall Score -->
      <div class="glass rounded-2xl p-6">
        <h4 class="text-sm font-semibold text-gray-400 mb-4">OVERALL RISK SCORE</h4>
        <div class="text-5xl font-bold gradient-text mb-2">${(risk.risk_score * 100).toFixed(1)}%</div>
        <div class="text-sm text-gray-400">Confidence: ${(risk.confidence * 100).toFixed(0)}%</div>
      </div>
      
      <!-- Metrics -->
      <div class="space-y-3">
        <h4 class="text-sm font-semibold text-gray-400">KEY METRICS</h4>
        
        <div class="glass rounded-xl p-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm">Deception Probability</span>
            <span class="font-semibold">${(risk.deception_probability * 100).toFixed(1)}%</span>
          </div>
          <div class="w-full bg-gray-800 rounded-full h-2">
            <div class="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full" style="width: ${risk.deception_probability * 100}%"></div>
          </div>
        </div>
        
        <div class="glass rounded-xl p-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm">Content Safety</span>
            <span class="font-semibold">${(risk.breakdown.content_safety.score * 100).toFixed(0)}%</span>
          </div>
          <div class="w-full bg-gray-800 rounded-full h-2">
            <div class="bg-gradient-to-r from-blue-500 to-cyan-500 h-2 rounded-full" style="width: ${risk.breakdown.content_safety.score * 100}%"></div>
          </div>
        </div>
        
        <div class="glass rounded-xl p-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm">Behavioral Patterns</span>
            <span class="font-semibold">${(risk.breakdown.behavioral_patterns.score * 100).toFixed(0)}%</span>
          </div>
          <div class="w-full bg-gray-800 rounded-full h-2">
            <div class="bg-gradient-to-r from-green-500 to-emerald-500 h-2 rounded-full" style="width: ${risk.breakdown.behavioral_patterns.score * 100}%"></div>
          </div>
        </div>
      </div>
      
      <!-- Explanation -->
      <div class="space-y-3">
        <h4 class="text-sm font-semibold text-gray-400">ANALYSIS</h4>
        ${risk.explanation.map(exp => `
          <div class="glass rounded-xl p-4 text-sm">
            <i class="fas fa-check-circle text-green-400 mr-2"></i>
            ${exp}
          </div>
        `).join('')}
      </div>
      
      ${risk.violations.length > 0 ? `
        <div class="space-y-3">
          <h4 class="text-sm font-semibold text-red-400">⚠️ VIOLATIONS (${risk.violations.length})</h4>
          ${risk.violations.map(v => `
            <div class="glass rounded-xl p-4 border-l-4 ${v.severity === 'critical' ? 'border-red-500' : v.severity === 'high' ? 'border-yellow-500' : 'border-blue-500'}">
              <div class="font-semibold text-sm mb-1">${v.severity.toUpperCase()}: ${v.rule_name}</div>
              <div class="text-xs text-gray-400">${v.description}</div>
            </div>
          `).join('')}
        </div>
      ` : ''}
      
    </div>
  `;
  
  // Auto-open if high risk
  if (risk.risk_score >= 0.5) {
    document.getElementById('safetyPanel').classList.remove('translate-x-full');
  }
}

// Copy Text
function copyText(msgId) {
  const msg = document.getElementById(msgId);
  const text = msg.querySelector('.prose').textContent;
  navigator.clipboard.writeText(text);
  
  // Show feedback
  const btn = event.target.closest('button');
  const originalHTML = btn.innerHTML;
  btn.innerHTML = '<i class="fas fa-check"></i><span>Copied!</span>';
  setTimeout(() => btn.innerHTML = originalHTML, 2000);
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
  document.getElementById('safetyPanel').classList.toggle('translate-x-full');
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

// Chat History
function saveChatHistory(userMsg, aiMsg) {
  const historyDiv = document.getElementById('chatHistory');
  const chatItem = document.createElement('div');
  chatItem.className = 'p-3 rounded-xl glass hover:bg-white/10 transition-all cursor-pointer text-sm';
  chatItem.textContent = userMsg.substring(0, 30) + (userMsg.length > 30 ? '...' : '');
  historyDiv.insertBefore(chatItem, historyDiv.firstChild);
}

function loadChatHistory() {
  // Load from localStorage if needed
}

function updateChatHistorySidebar() {
  // Update sidebar
}
