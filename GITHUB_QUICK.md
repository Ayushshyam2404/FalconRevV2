# ⚡ GitHub Quick Reference

**Push Falcon Rev to GitHub in 5 Minutes**

---

## 🎬 TL;DR - Super Fast Version

```bash
# 1. Create repo on GitHub.com (click + → New repository)

# 2. Go to your project
cd ~/FLrevV2

# 3. Initialize git
git init
git remote add origin https://github.com/YOUR_USERNAME/falcon-rev.git

# 4. Add files (excludes .env automatically via .gitignore)
git add .

# 5. Commit
git commit -m "Initial commit: Falcon Rev Revenue Portal"

# 6. Push to GitHub
git branch -M main
git push -u origin main
```

✅ Done! Your code is on GitHub!

---

## 🔐 Security - CRITICAL

✅ **Your .gitignore file already protects:**
- `.env` (API keys) ✓
- `venv/` (virtual environment) ✓
- `__pycache__/` (Python cache) ✓
- `uploads/` (user files) ✓

❌ **NEVER commit:**
- SendGrid API key
- Email passwords
- Any secrets

---

## 📱 Common Git Commands

```bash
# Check status
git status

# See changes
git diff

# Add changes
git add .

# Commit
git commit -m "Your message"

# Push
git push

# Pull latest changes
git pull

# See history
git log

# Create branch
git checkout -b feature/new-feature

# Switch branch
git checkout main
```

---

## 🔗 Your Repository URL

Once created:
```
https://github.com/yourusername/falcon-rev
```

Share this URL with others!

---

## 🆚 GitHub vs Local

| Action | Local | GitHub |
|--------|-------|--------|
| Code changes | `git add .` | Already have latest |
| Save changes | `git commit` | Auto-saved in cloud |
| Share with others | Manual email | `git push` → share URL |
| Backup | On your computer | Cloud backup ✓ |
| History | Last few commits | All commits forever |

---

## 📋 Setup Checklist

- [ ] GitHub account created (github.com)
- [ ] Repository created on GitHub
- [ ] `.gitignore` file exists (protects .env)
- [ ] Git initialized locally (`git init`)
- [ ] Remote added (`git remote add origin...`)
- [ ] Files added (`git add .`)
- [ ] Committed (`git commit -m "..."`)
- [ ] Pushed to GitHub (`git push`)
- [ ] Repository visible on github.com

---

## 🆘 Quick Fixes

**"git: command not found"**
- Install Git: https://git-scm.com/

**"fatal: not a git repository"**
```bash
cd ~/FLrevV2
git init
```

**"fatal: Authentication failed"**
- Use Personal Access Token (not password)
- Settings → Developer settings → Personal access tokens

**".env still showing up"**
```bash
git rm --cached .env
git commit -m "Remove .env"
git push
```

---

## 📖 See Full Guide

Open: `GITHUB_HOSTING.md` for complete step-by-step instructions.

---

## 🎉 You're Ready!

Your code is safe on GitHub now! 🚀
