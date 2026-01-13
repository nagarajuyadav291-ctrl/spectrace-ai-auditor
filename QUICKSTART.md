# 🚀 SpecTrace - Quick Start Guide

## Fresh Clone & Run (5 Minutes)

### **Step 1: Clone**

```powershell
git clone https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor.git
cd spectrace-ai-auditor
code .
```

### **Step 2: Create .env File**

Create: `backend/.env`

```env
DATABASE_URL=sqlite:///./spectrace.db
GROQ_API_KEY=YOUR_GROQ_KEY_HERE
```

**Your Groq key:** `gsk_xTdUmMMJ...` (check your notes)

### **Step 3: Setup**

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### **Step 4: Run Backend (Terminal 1)**

```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

### **Step 5: Run Frontend (Terminal 2)**

```powershell
cd frontend-v2
python -m http.server 3000
```

### **Step 6: Open Browser**

```
http://localhost:3000
```

**Done!** Purple gradient UI should appear! 🎉

---

## 📋 Project Structure

```
spectrace-ai-auditor/
├── backend/          # FastAPI backend
│   ├── app/         # Main application
│   ├── .env         # API keys (create this)
│   └── venv/        # Virtual environment
├── frontend-v2/     # Modern UI
│   ├── index.html   # Main page
│   └── app.js       # JavaScript
└── README.md        # Documentation
```

---

## ⚡ Quick Commands

**Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```powershell
cd frontend-v2
python -m http.server 3000
```

---

## 🐛 Common Issues

**Port in use?**
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

**Module not found?**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Old UI?**
- Use `http://localhost:3000` (NOT 8000)
- Hard refresh: `Ctrl + Shift + R`

---

**That's it!** 🚀
