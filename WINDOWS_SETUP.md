# 🪟 Windows Setup Guide for SpecTrace

## ✅ All Errors Fixed!

The issues you encountered have been resolved:
1. ✅ PyTorch version updated for Python 3.12 compatibility
2. ✅ Angular TypeScript errors fixed
3. ✅ Windows-specific commands provided

---

## 🚀 Complete Setup Instructions for Windows

### **Step 1: Pull Latest Changes**

```powershell
cd E:\SpecTrace Problem\spectrace-ai-auditor
git pull origin main
```

### **Step 2: Backend Setup**

#### **2.1 Create Virtual Environment**

```powershell
cd backend
python -m venv venv
```

#### **2.2 Activate Virtual Environment**

```powershell
# If you get execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate:
.\venv\Scripts\Activate.ps1

# You should see (venv) in your prompt
```

#### **2.3 Install Dependencies**

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install all dependencies (fixed version)
pip install -r requirements.txt
```

This will now work! The torch version has been updated to be compatible with Python 3.12.

#### **2.4 Create .env File**

```powershell
# Copy example file
copy .env.example .env

# Edit with notepad
notepad .env
```

Add your API keys:
```env
DATABASE_URL=postgresql://spectrace:spectrace123@localhost:5432/spectrace
OPENAI_API_KEY=sk-proj-your-actual-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
REDIS_URL=redis://localhost:6379
```

#### **2.5 Initialize Database**

```powershell
python -c "from app.database import init_db; init_db()"
```

You should see: `✅ Database initialized successfully!`

#### **2.6 Start Backend**

```powershell
python -m app.main
```

Backend will start on `http://localhost:8000`

**Keep this PowerShell window open!**

---

### **Step 3: Frontend Setup**

Open a **NEW PowerShell window**.

#### **3.1 Navigate to Frontend**

```powershell
cd E:\SpecTrace Problem\spectrace-ai-auditor\frontend
```

#### **3.2 Pull Latest Changes**

```powershell
git pull origin main
```

The Angular errors are now fixed!

#### **3.3 Install Angular CLI (if needed)**

```powershell
npm install -g @angular/cli
```

#### **3.4 Start Frontend**

```powershell
ng serve
```

Frontend will start on `http://localhost:4200`

**Keep this PowerShell window open too!**

---

## 🎯 Verify Everything Works

### **1. Check Backend**

Open browser: `http://localhost:8000/health`

Should see:
```json
{"status":"healthy","timestamp":"2026-01-09T..."}
```

### **2. Check Frontend**

Open browser: `http://localhost:4200`

You should see the SpecTrace dashboard with no errors!

### **3. Check Database**

```powershell
docker ps
```

Should show:
- `spectrace-postgres` (running)
- `spectrace-redis` (running)

---

## 🐛 Troubleshooting

### **Issue: "Execution policy" error**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Issue: "Module not found" errors**

Make sure virtual environment is activated:
```powershell
# You should see (venv) in your prompt
# If not, activate again:
.\venv\Scripts\Activate.ps1
```

### **Issue: Port already in use**

**Backend (8000)**:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill it (replace PID with actual number)
taskkill /PID <PID> /F
```

**Frontend (4200)**:
```powershell
# Use different port
ng serve --port 4300
```

### **Issue: Docker not running**

```powershell
# Start Docker Desktop
# Then run:
docker-compose up -d
```

### **Issue: npm vulnerabilities**

These are warnings, not errors. The app will work fine. To fix:
```powershell
npm audit fix
```

---

## 📝 Quick Command Reference

### **Start Everything**

```powershell
# Terminal 1: Start Docker
docker-compose up -d

# Terminal 2: Start Backend
cd backend
.\venv\Scripts\Activate.ps1
python -m app.main

# Terminal 3: Start Frontend
cd frontend
ng serve
```

### **Stop Everything**

```powershell
# Stop Frontend: Ctrl+C in frontend terminal
# Stop Backend: Ctrl+C in backend terminal
# Stop Docker:
docker-compose down
```

### **Restart After Reboot**

```powershell
# 1. Start Docker
docker-compose up -d

# 2. Backend (Terminal 1)
cd backend
.\venv\Scripts\Activate.ps1
python -m app.main

# 3. Frontend (Terminal 2)
cd frontend
ng serve
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Docker containers running (`docker ps`)
- [ ] Backend responds (`http://localhost:8000/health`)
- [ ] Frontend loads (`http://localhost:4200`)
- [ ] No console errors in browser (F12)
- [ ] Can submit a task
- [ ] Execution history shows results

---

## 🎉 Success!

If you see the SpecTrace dashboard at `http://localhost:4200` with no errors, you're all set!

### **Test the System**

1. Enter a task: `"Research the latest AI safety papers"`
2. Select agent: **GPT-4**
3. Max steps: **10**
4. Click: **🚀 Execute & Audit**

---

## 📞 Still Having Issues?

### **Common Solutions**

**"Python not found"**:
- Install Python 3.12 from python.org
- Make sure "Add to PATH" is checked during installation

**"Docker not found"**:
- Install Docker Desktop for Windows
- Start Docker Desktop before running commands

**"Node not found"**:
- Install Node.js 18+ from nodejs.org
- Restart PowerShell after installation

**"Git not found"**:
- Install Git for Windows
- Restart PowerShell after installation

---

## 🚀 Next Steps

Once everything is running:

1. ✅ Read `REVOLUTIONARY_FEATURES.md` to learn about new features
2. ✅ Read `UPGRADE_GUIDE.md` to activate advanced features
3. ✅ Configure alerts (optional) in `.env`
4. ✅ Start auditing AI agents!

---

**Your SpecTrace is now ready on Windows!** 🎯
