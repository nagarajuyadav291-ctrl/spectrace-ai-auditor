# 🔑 FREE API KEYS - Complete Guide

## 🎯 ALL FREE AI APIs (No Credit Card Required!)

### ✅ **1. GROQ (FASTEST & FREE)**

**What**: Llama 3.1 70B, 8B, Mixtral - Lightning fast inference

**Steps**:
1. Go to: https://console.groq.com
2. Click "Sign Up" (use Google/GitHub)
3. Click "API Keys" in sidebar
4. Click "Create API Key"
5. Copy key: `gsk_xxxxxxxxxxxxx`

**Limits**: 30 requests/minute, 14,400/day (FREE forever!)

---

### ✅ **2. GOOGLE GEMINI (FREE)**

**What**: Gemini 1.5 Flash, Pro - Google's latest AI

**Steps**:
1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Select "Create API key in new project"
5. Copy key: `AIzaSyxxxxxxxxxxxxx`

**Limits**: 15 requests/minute, 1,500/day (FREE tier)

---

### ✅ **3. COHERE (FREE)**

**What**: Command R, Command R+ - Great for chat

**Steps**:
1. Go to: https://dashboard.cohere.com/api-keys
2. Sign up (email or Google)
3. Verify email
4. Go to "API Keys" tab
5. Copy "Trial Key": `xxxxxxxxxxxxx`

**Limits**: 100 requests/minute (FREE trial, then paid)

---

### ✅ **4. PERSPECTIVE API (FREE - For Risk Scoring)**

**What**: Google's toxicity/safety detection

**Steps**:
1. Go to: https://developers.perspectiveapi.com/s/docs-get-started
2. Click "Get Started"
3. Sign in with Google
4. Go to: https://console.cloud.google.com/apis/credentials
5. Create new project
6. Enable "Perspective Comment Analyzer API"
7. Create credentials → API Key
8. Copy key: `AIzaSyxxxxxxxxxxxxx`

**Limits**: 1 request/second, 1,000/day (FREE)

---

### ✅ **5. HUGGING FACE (FREE)**

**What**: 1000s of open-source models

**Steps**:
1. Go to: https://huggingface.co/join
2. Sign up (email or Google)
3. Go to: https://huggingface.co/settings/tokens
4. Click "New token"
5. Name it, select "Read" access
6. Copy token: `hf_xxxxxxxxxxxxx`

**Limits**: Unlimited (FREE tier available)

---

### ✅ **6. REPLICATE (FREE TIER)**

**What**: Run AI models via API (Llama, Stable Diffusion, etc.)

**Steps**:
1. Go to: https://replicate.com
2. Sign up with GitHub
3. Go to: https://replicate.com/account/api-tokens
4. Copy token: `r8_xxxxxxxxxxxxx`

**Limits**: $0.01 free credit (then pay-as-you-go)

---

### ✅ **7. TOGETHER AI (FREE TRIAL)**

**What**: Llama 3, Mixtral, and more

**Steps**:
1. Go to: https://api.together.xyz
2. Sign up
3. Go to Settings → API Keys
4. Create new key
5. Copy: `xxxxxxxxxxxxx`

**Limits**: $25 free credit

---

### ✅ **8. ANYSCALE (FREE TRIAL)**

**What**: Llama 2, Mistral, CodeLlama

**Steps**:
1. Go to: https://www.anyscale.com
2. Sign up
3. Go to API Keys
4. Create key
5. Copy: `xxxxxxxxxxxxx`

**Limits**: $10 free credit

---

### ✅ **9. DEEPINFRA (FREE TIER)**

**What**: Llama 3, Mixtral, Qwen

**Steps**:
1. Go to: https://deepinfra.com
2. Sign up
3. Go to: https://deepinfra.com/dash/api_keys
4. Create key
5. Copy: `xxxxxxxxxxxxx`

**Limits**: Free tier available

---

### ✅ **10. FIREWORKS AI (FREE TRIAL)**

**What**: Llama 3, Mixtral, fast inference

**Steps**:
1. Go to: https://fireworks.ai
2. Sign up
3. Go to API Keys
4. Create key
5. Copy: `xxxxxxxxxxxxx`

**Limits**: $1 free credit

---

## 💰 **PAID APIs (Optional)**

### **OpenAI (GPT-4, GPT-3.5)**

**Steps**:
1. Go to: https://platform.openai.com/api-keys
2. Sign up
3. Add payment method
4. Create API key
5. Copy: `sk-xxxxxxxxxxxxx`

**Cost**: $0.03/1K tokens (GPT-3.5), $0.03-$0.12/1K tokens (GPT-4)

---

### **Anthropic (Claude)**

**Steps**:
1. Go to: https://console.anthropic.com
2. Sign up
3. Add payment method
4. Create API key
5. Copy: `sk-ant-xxxxxxxxxxxxx`

**Cost**: $0.25-$15/1M tokens (depending on model)

---

## 📝 **ADD KEYS TO .ENV FILE**

Edit `backend/.env`:

```env
# Database
DATABASE_URL=sqlite:///./spectrace.db

# FREE APIs (No credit card!)
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxx
COHERE_API_KEY=xxxxxxxxxxxxx
PERSPECTIVE_API_KEY=AIzaSyxxxxxxxxxxxxx
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxx

# Optional: More FREE APIs
REPLICATE_API_KEY=r8_xxxxxxxxxxxxx
TOGETHER_API_KEY=xxxxxxxxxxxxx
ANYSCALE_API_KEY=xxxxxxxxxxxxx
DEEPINFRA_API_KEY=xxxxxxxxxxxxx
FIREWORKS_API_KEY=xxxxxxxxxxxxx

# Optional: PAID APIs
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

---

## ✅ **RECOMMENDED: Start with These 4**

For best results, get these first:

1. **GROQ** - Fastest, completely free
2. **GOOGLE GEMINI** - Free, powerful
3. **COHERE** - Free trial, good quality
4. **PERSPECTIVE API** - For safety scoring

**Total time**: ~10 minutes to get all 4 keys!

---

## 🚀 **QUICK START**

```powershell
# 1. Get API keys (10 minutes)
# Follow steps above

# 2. Add to .env file
notepad backend\.env

# 3. Pull latest code
git pull origin main

# 4. Install packages
cd backend
.\venv\Scripts\Activate.ps1
pip install google-generativeai cohere anthropic httpx

# 5. Run backend
uvicorn app.main:app --reload --port 8000

# 6. Run frontend (new terminal)
cd frontend-v2
python -m http.server 3000

# 7. Open browser
# http://localhost:3000
```

---

## 🎯 **WHICH MODELS TO USE?**

### **For Speed**: 
- Groq Llama 3.1 8B (instant responses)

### **For Quality**: 
- Groq Llama 3.1 70B (best free model)
- Google Gemini 1.5 Pro (very good)

### **For Safety**: 
- Perspective API (toxicity detection)

### **For Premium**: 
- GPT-4o (best overall, paid)
- Claude 3.5 Sonnet (best reasoning, paid)

---

## 🐛 **TROUBLESHOOTING**

### **"API Key Invalid"**
- Check you copied the full key
- Check no extra spaces
- Check key is active (not revoked)

### **"Rate Limit Exceeded"**
- Wait 1 minute
- Use different model
- Upgrade to paid tier

### **"Model Not Found"**
- Check model name in code
- Check API supports that model
- Try different model

---

## 💡 **PRO TIPS**

1. **Start with Groq** - It's the fastest and completely free
2. **Use Gemini for complex tasks** - Better reasoning
3. **Combine multiple APIs** - Fallback if one fails
4. **Monitor usage** - Check dashboard for limits
5. **Upgrade when needed** - Paid tiers are cheap

---

## 🎉 **YOU'RE READY!**

With these FREE API keys, you have:
- ✅ 10+ AI models
- ✅ Thousands of free requests/day
- ✅ No credit card needed
- ✅ Production-ready setup

**Go build something amazing!** 🚀
