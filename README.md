# 🔍 SpecTrace - AI Safety Monitor

**The AI Behavior Auditor That Catches What Others Miss**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

---

## 🎯 What is SpecTrace?

SpecTrace is **not just another chatbot**. It's a comprehensive **AI Safety Monitor** that provides:

- ✅ **Real-time Risk Scoring** - Multi-engine detection (OpenAI, Google, Pattern Analysis)
- ✅ **Deception Detection** - Behavioral pattern analysis
- ✅ **Compliance Checking** - Regulatory violation alerts
- ✅ **Behavioral Drift Tracking** - Long-term AI behavior monitoring
- ✅ **15+ AI Models** - Free (Groq, Gemini, Cohere) & Paid (GPT-4, Claude)
- ✅ **ChatGPT-like UI** - Beautiful, modern interface with dark mode
- ✅ **Explainable AI** - Transparent risk calculations with confidence scores

---

## 🚀 Quick Start (5 Minutes)

### **1. Clone Repository**

```bash
git clone https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor.git
cd spectrace-ai-auditor
```

### **2. Get FREE API Keys**

- **Groq** (Fastest): https://console.groq.com
- **Google Gemini**: https://aistudio.google.com/app/apikey
- **Cohere**: https://dashboard.cohere.com/api-keys
- **Perspective API**: https://developers.perspectiveapi.com/s/docs-get-started

### **3. Configure Environment**

Create `backend/.env`:

```env
# FREE APIs (No credit card required!)
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxx
COHERE_API_KEY=xxxxxxxxxxxxx
PERSPECTIVE_API_KEY=AIzaSyxxxxxxxxxxxxx

# Optional: Paid APIs
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

DATABASE_URL=sqlite:///./spectrace.db
```

### **4. Install & Run Backend**

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac

pip install -r requirements.txt
pip install google-generativeai cohere anthropic httpx

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **5. Run Frontend**

```bash
cd frontend-v2
python -m http.server 3000
```

### **6. Open Browser**

```
http://localhost:3000
```

**Done! 🎉**

---

## 📊 What Makes SpecTrace Unique?

### **1. Multi-Engine Risk Scoring**

Unlike single-model systems, SpecTrace uses **3+ independent detection engines**:

```
Risk Assessment Consensus:
✓ OpenAI Moderation API: Safe (0.12)
✓ Perspective API (Google): Safe (0.15)
✓ Pattern Matching: Safe (0.14)

Consensus: SAFE (Average: 0.14)
Confidence: 94%
```

### **2. Explainable AI**

Every risk score comes with **detailed explanations**:

```
Risk Score Breakdown:
├─ Content Safety (40%): 0.15
│  ├─ Harmful content detection
│  ├─ Bias detection
│  └─ Toxicity analysis
├─ Behavioral Patterns (30%): 0.23
│  ├─ Deception indicators
│  ├─ Manipulation tactics
│  └─ Evasion patterns
├─ Factual Accuracy (20%): 0.10
│  └─ Fact-checking
└─ Compliance (10%): 0.05
   └─ Regulatory violations

Final Risk Score: 0.18 (Low)
```

### **3. Real-Time Monitoring**

- Risk scores update **as AI responds**
- Violations flagged **immediately**
- Behavioral patterns tracked **over time**

### **4. 15+ AI Models**

| Provider | Models | Cost | Speed |
|----------|--------|------|-------|
| **Groq** | Llama 3.1 70B, Mixtral | 🆓 FREE | ⚡⚡⚡ Fastest |
| **Google** | Gemini 1.5 Flash/Pro | 🆓 FREE / 💰 Paid | ⚡⚡ Fast |
| **Cohere** | Command R/R+ | 🆓 FREE / 💰 Paid | ⚡⚡ Fast |
| **Mistral** | Small/Medium | 🆓 FREE / 💰 Paid | ⚡⚡ Fast |
| **OpenAI** | GPT-3.5/4/4o | 💰 Paid | ⚡ Slow |
| **Anthropic** | Claude 3.5 Sonnet/Opus | 💰 Paid | ⚡⚡ Fast |

---

## 🎨 Features

### **ChatGPT-Like Interface**

- ✅ Sidebar with chat history
- ✅ Dark mode toggle
- ✅ Model selector
- ✅ Copy/regenerate buttons
- ✅ Mobile responsive
- ✅ Markdown rendering

### **Safety Features**

- ✅ Real-time risk indicator
- ✅ Collapsible safety panel
- ✅ Violation alerts
- ✅ Behavioral analysis
- ✅ Confidence scores
- ✅ Multi-engine consensus

### **Analytics**

- ✅ Behavioral drift tracking
- ✅ Risk trend analysis
- ✅ Execution history
- ✅ Model comparison
- ✅ Export reports

---

## 🎯 Use Cases

### **1. AI Safety Research**

Monitor AI behavior, detect deception, and track behavioral drift for research papers.

### **2. Enterprise AI Deployment**

Ensure production AI systems remain safe, compliant, and aligned with company values.

### **3. AI Development**

Test AI agents for safety issues before deployment. Compare models for risk profiles.

### **4. Regulatory Compliance**

Generate audit trails and compliance reports for regulatory requirements.

### **5. Customer Service**

Monitor customer-facing AI to prevent manipulation, bias, or harmful responses.

---

## 📖 Documentation

- **[Implementation Guide](IMPLEMENTATION_GUIDE.md)** - Complete setup instructions
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when running)
- **[Architecture](docs/ARCHITECTURE.md)** - System design and components
- **[Risk Scoring](docs/RISK_SCORING.md)** - How risk scores are calculated

---

## 🔬 How Risk Scoring Works

### **Layer 1: Content Safety (40% weight)**

- OpenAI Moderation API
- Google Perspective API
- Pattern-based detection

### **Layer 2: Behavioral Patterns (30% weight)**

- Evasion detection
- Manipulation tactics
- Ambiguity analysis

### **Layer 3: Deception Detection (20% weight)**

- Linguistic markers
- Hedging language
- Truth emphasis patterns

### **Layer 4: Compliance (10% weight)**

- Medical advice disclaimers
- Financial advice warnings
- Legal advice notices

**Final Score = Weighted Average + Confidence Adjustment**

---

## 🆚 SpecTrace vs Competitors

| Feature | SpecTrace | ChatGPT | Claude | Other Monitors |
|---------|-----------|---------|--------|----------------|
| **AI Responses** | ✅ | ✅ | ✅ | ❌ |
| **Risk Scoring** | ✅ Multi-engine | ❌ | ❌ | ✅ Single |
| **Deception Detection** | ✅ | ❌ | ❌ | ❌ |
| **Behavioral Drift** | ✅ | ❌ | ❌ | ❌ |
| **Explainable AI** | ✅ | ❌ | ❌ | ⚠️ Limited |
| **Multi-Model** | ✅ 15+ | ❌ | ❌ | ⚠️ Few |
| **Compliance Reports** | ✅ | ❌ | ❌ | ⚠️ Basic |
| **Free Tier** | ✅ | ⚠️ Limited | ⚠️ Limited | ❌ |

---

## 💰 Pricing (Planned)

### **Free Tier**
- 100 messages/month
- Free models only
- Basic risk analysis
- Community support

### **Pro ($29/mo)**
- Unlimited messages
- All models (GPT-4, Claude)
- Advanced analytics
- Export reports
- Email support

### **Enterprise ($299/mo)**
- Custom models
- API access
- White-label option
- SLA support
- Dedicated account manager

---

## 🛠️ Tech Stack

### **Backend**
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **OpenAI SDK** - AI model integration
- **Anthropic SDK** - Claude integration
- **Google AI SDK** - Gemini integration
- **Cohere SDK** - Command R integration

### **Frontend**
- **Pure HTML/CSS/JS** - No framework overhead
- **Modern CSS** - ChatGPT-like styling
- **Responsive Design** - Mobile-first approach
- **Dark Mode** - System preference support

### **AI Models**
- **Groq** - Llama 3.1, Mixtral (FREE)
- **Google** - Gemini 1.5 (FREE/Paid)
- **Cohere** - Command R (FREE/Paid)
- **Mistral** - Small/Medium (FREE/Paid)
- **OpenAI** - GPT-3.5/4/4o (Paid)
- **Anthropic** - Claude 3.5 (Paid)

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### **Areas We Need Help:**

- 🎨 UI/UX improvements
- 🔬 New risk detection algorithms
- 🌐 Internationalization
- 📚 Documentation
- 🧪 Testing
- 🐛 Bug fixes

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **OpenAI** - Moderation API
- **Google** - Perspective API, Gemini
- **Groq** - Fast inference
- **Anthropic** - Claude models
- **Cohere** - Command R models
- **Mistral AI** - Open models

---

## 📞 Support

- **GitHub Issues**: [Report bugs](https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor/issues)
- **Discussions**: [Ask questions](https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor/discussions)
- **Email**: nagarajuyadav291@gmail.com

---

## 🗺️ Roadmap

### **Q1 2024**
- ✅ Multi-provider support
- ✅ ChatGPT-like UI
- ✅ Risk scoring engine
- 🔄 Streaming responses
- 🔄 Export reports

### **Q2 2024**
- 📅 API access
- 📅 Custom safety rules
- 📅 Team collaboration
- 📅 Slack/Discord integration

### **Q3 2024**
- 📅 Enterprise features
- 📅 White-label option
- 📅 Advanced analytics
- 📅 Compliance certifications

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=nagarajuyadav291-ctrl/spectrace-ai-auditor&type=Date)](https://star-history.com/#nagarajuyadav291-ctrl/spectrace-ai-auditor&Date)

---

## 🎉 Get Started Now!

```bash
git clone https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor.git
cd spectrace-ai-auditor
# Follow IMPLEMENTATION_GUIDE.md
```

**Build the future of AI safety!** 🚀

---

Made with ❤️ by [Nagaraju Yadav](https://github.com/nagarajuyadav291-ctrl)
