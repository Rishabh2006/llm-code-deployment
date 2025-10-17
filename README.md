# LLM Code Deployment Project (Google Gemini Version)

Automated system that receives requests, generates web applications using Google Gemini (FREE), and deploys them to GitHub Pages.

## ✨ Why Gemini Version?

- ✅ **100% FREE Forever** - No trial, no limits for this use case
- ✅ **No Installation Issues** - Works instantly, no Rust compiler needed
- ✅ **Excellent Code Quality** - Generates professional, working applications
- ✅ **No Credit Card Required** - Get API key instantly

---

## 🚀 Complete Setup Guide

### Step 1: Get Your API Keys

#### A. Get Google Gemini API Key (30 seconds, FREE)

1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Choose "Create API key in new project" or select existing project
4. **COPY THE KEY** (starts with `AIza...`)
5. Save it somewhere safe

**Your key looks like:** `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`

#### B. Get GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: `LLM Code Deployment`
4. Expiration: Choose "90 days" or "No expiration"
5. **Select permissions:**
   - ✅ Check **ALL boxes under `repo`**
   - ✅ Check **`workflow`**
6. Click "Generate token"
7. **COPY THE TOKEN** (starts with `ghp_`)

**Your token looks like:** `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

#### C. Your GitHub Username

- Find it at: https://github.com (top right corner)
- Example: `john-doe`

#### D. Choose Your Secret

- Create a strong password: `MySuper$ecretPass2025!`
- You'll need this for the Google Form later

---

### Step 2: Setup Project Files

#### Create `.env` file:

1. Copy `.env.example` to `.env`
2. Fill in YOUR actual values:

```bash
MY_EMAIL=your-actual-email@gmail.com
MY_SECRET=MySuper$ecretPass2025!
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_USERNAME=your-github-username
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Save the file!**

---

### Step 3: Install Dependencies

Open terminal in VSCode (Ctrl + `):

#### Delete old venv (if exists):
```bash
rm -rf venv
```

#### Create new venv:
```bash
python -m venv venv
```

#### Activate venv:

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate
```

**Mac/Linux/Git Bash:**
```bash
source venv/bin/activate
```

**✅ Check:** You should see `(venv)` at the start of your terminal line

#### Install packages:
```bash
pip install -r requirements.txt
```

Wait 1-2 minutes for installation to complete.

---

### Step 4: Test Locally

```bash
python -m api.main
```

You should see:
```
* Running on http://127.0.0.1:5000
```

**Open browser:** http://localhost:5000

You should see:
```json
{
  "status": "online",
  "message": "LLM Code Deployment API is running"
}
```

**✅ Perfect! Press Ctrl+C to stop the server.**

---

### Step 5: Deploy to Vercel

#### Install Node.js (if not installed):
- Download from: https://nodejs.org/ (LTS version)
- Install and restart VSCode

#### Install Vercel CLI:
```bash
npm install -g vercel
```

#### Login to Vercel:
```bash
vercel login
```

Browser will open - login with your account.

#### Deploy:
```bash
vercel
```

Answer prompts:
- Set up and deploy? **Y**
- Which scope? Choose your account
- Link to existing project? **N**
- Project name? **llm-code-deployment**
- Directory? Press Enter

#### Add Environment Variables:
```bash
vercel env add MY_EMAIL
vercel env add MY_SECRET
vercel env add GITHUB_TOKEN
vercel env add GITHUB_USERNAME
vercel env add GEMINI_API_KEY
```

For each one:
- Paste the value
- Select: **Production** (press Space, then Enter)

#### Deploy to Production:
```bash
vercel --prod
```

**COPY YOUR URL!** It looks like:
```
✅ Production: https://llm-code-deployment-abc123.vercel.app
```

---

### Step 6: Test Deployed API

Open browser and go to your Vercel URL:
```
https://your-vercel-url.vercel.app
```

You should see:
```json
{
  "status": "online",
  "message": "LLM Code Deployment API is running"
}
```

**🎉 YOU'RE DONE! Your API is live!**

---

### Step 7: Submit Google Form (When Available)

Fill the instructor's Google Form with:

```
Name: Your Full Name
Email: your-actual-email@gmail.com  (EXACT as in .env)
API Endpoint: https://your-vercel-url.vercel.app/build-app
Secret: MySuper$ecretPass2025!  (EXACT as in .env)
GitHub Username: your-github-username
```

**CRITICAL:**
- Email must EXACTLY match `.env`
- Secret must EXACTLY match `.env`
- API Endpoint must end with `/build-app`

---

## 🎯 What Happens Automatically

After you submit the form:

1. **Instructors send request** → Your API receives it
2. **API verifies secret** → Checks if it matches
3. **Gemini generates code** → Creates HTML/CSS/JS
4. **GitHub repo created** → Pushes code automatically
5. **GitHub Pages enabled** → App goes live
6. **Evaluator notified** → Results sent back

**You don't do anything!** Just wait for requests. ⏳

---

## 📊 Monitoring

### View Logs:
```bash
vercel logs --follow
```

### Check GitHub Repos:
Go to: https://github.com/your-username

New repos will appear when tasks are received!

### Check Gemini Usage:
Go to: https://aistudio.google.com/app/apikey

Click on your API key to see usage stats.

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "ModuleNotFoundError" | Activate venv first: `source venv/bin/activate` |
| "Invalid secret" | Check `.env` matches Google Form exactly |
| "GitHub API error" | Check token has `repo` + `workflow` permissions |
| "Gemini API error" | Verify API key is correct |
| "vercel: command not found" | Install Node.js first |

---

## ✅ Quick Reference


## 💰 Cost Breakdown

| Service | Cost |
|---------|------|
| Google Gemini | **$0.00** (FREE forever) |
| GitHub | **$0.00** (FREE) |
| Vercel | **$0.00** (FREE tier) |
| **TOTAL** | **$0.00** ✅ |

---

## 🎓 Summary

**Setup Time:** ~30 minutes
**Cost:** $0.00 (completely free)
**Complexity:** Easy
**Code Quality:** Excellent
**Maintenance:** Zero (automated)

---

## 📞 Support

If you encounter issues:
1. Check `vercel logs`
2. Verify all environment variables: `vercel env ls`
3. Test locally first: `python -m api.main`
4. Check GitHub token permissions
5. Verify Gemini API key works

---

## 📄 License

MIT License - Free to use and modify