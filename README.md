# 🛡️ SpecTrace - AI Safety Monitor

**Ultra-modern AI chat interface with real-time safety monitoring**

![SpecTrace](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

---

## ✨ Features

- 🎨 **Ultra-Modern UI** - Tailwind CSS with purple gradients
- 🤖 **15+ AI Models** - Groq, Google Gemini, Cohere, OpenAI, Claude
- 🛡️ **Real-Time Safety** - Multi-engine risk analysis
- 🆓 **100% Free Tier** - No credit card required
- ⚡ **Lightning Fast** - Groq models respond instantly

---

## 🚀 Quick Start (5 Minutes)

### **Step 1: Clone & Setup**

```powershell
# Clone repository
git clone https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor.git
cd spectrace-ai-auditor

# Run clean setup (removes old files, installs everything)
.\clean-setup.ps1
```

### **Step 2: Get FREE API Key**

Get at least **Groq** (fastest, completely free):

1. Go to: https://console.groq.com
2. Sign up (Google/GitHub)
3. Click "API Keys" → "Create API Key"
4. Copy key: `gsk_xxxxxxxxxxxxx`

**More free APIs**: See [FREE_API_KEYS.md](FREE_API_KEYS.md)

### **Step 3: Add API Key**

Edit `backend/.env`:

```env
DATABASE_URL=sqlite:///./spectrace.db
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
```

### **Step 4: Run**

```powershell
# Backend (Terminal 1)
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000

# Frontend (Terminal 2)
cd frontend-v2
python -m http.server 3000
```

### **Step 5: Open Browser**

```
http://localhost:3000
```

**You should see purple gradients and a modern sidebar!** 🎉

---

## 📁 Project Structure

```
spectrace-ai-auditor/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py      # API endpoints
│   │   ├── models.py    # Database models
│   │   └── services/    # AI & safety services
│   ├── .env             # API keys (create this)
│   └── venv/            # Python virtual environment
│
├── frontend-v2/         # Modern UI (Tailwind CSS)
│   ├── index.html       # Main UI
│   └── app.js           # JavaScript logic
│
├── FREE_API_KEYS.md     # Guide to get free API keys
├── clean-setup.ps1      # Automated setup script
└── README.md            # This file
```

---

## 🎨 UI Preview

### **Welcome Screen**
- Purple gradient logo with shield icon
- Sidebar with chat history
- 3 example cards (Examples, Science, Safety)
- Modern input with gradient border

### **Chat Interface**
- User messages (blue gradient avatar)
- AI messages (purple gradient avatar)
- Real-time risk badges (green/yellow/red)
- Copy/Regenerate/Safety buttons

### **Safety Panel**
- Overall risk score
- Deception probability
- Content safety metrics
- Violation alerts

---

## 🔑 Supported AI Models

### **Free Models (No Credit Card)**
- 🦙 Llama 3.1 70B (Groq) - Fastest
- 🦙 Llama 3.1 8B (Groq) - Ultra-fast
- 🌀 Mixtral 8x7B (Groq)
- 💎 Gemini 1.5 Flash (Google)
- 💎 Gemini 1.5 Pro (Google)
- 🔮 Command R (Cohere)
- 🔮 Command R+ (Cohere)

### **Premium Models (Paid)**
- 🤖 GPT-4o (OpenAI)
- 🤖 GPT-4 Turbo (OpenAI)
- 🧠 Claude 3.5 Sonnet (Anthropic)

---

## 🛡️ Safety Features

- **Multi-Engine Analysis** - Combines multiple AI safety models
- **Risk Scoring** - 0-100% risk score for every response
- **Deception Detection** - Identifies misleading information
- **Content Safety** - Toxicity, hate speech, violence detection
- **Compliance Checking** - Regulatory compliance validation
- **Real-Time Monitoring** - Instant safety analysis

---

## 🐛 Troubleshooting

### **"Module not found" error**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn sqlalchemy python-dotenv google-generativeai cohere anthropic
```

### **"Database connection failed"**
Make sure `.env` has:
```env
DATABASE_URL=sqlite:///./spectrace.db
```

### **"API key invalid"**
- Check you copied the full key
- Check no extra spaces
- Get new key from provider

### **Old UI showing**
- Make sure you're on `http://localhost:3000` (NOT 8000)
- Hard refresh: `Ctrl + Shift + R`
- Clear cache: `Ctrl + Shift + Delete`

---

## 📖 Documentation

- [FREE_API_KEYS.md](FREE_API_KEYS.md) - Complete guide to get 10+ free API keys
- [LICENSE](LICENSE) - MIT License

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🌟 Star This Repo!

If you find SpecTrace useful, please star this repository! ⭐

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor/discussions)

---

**Built with ❤️ for AI Safety**
