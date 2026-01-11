# 🐙 GitHub Hosting Guide

Complete step-by-step instructions to push Falcon Rev to GitHub and manage your repository.

---

## 📋 Prerequisites

- GitHub account (create free at https://github.com)
- Git installed on your computer (check: `git --version`)
- Your project files ready

---

## 🎯 STEP 1: Create GitHub Account

1. Go to https://github.com
2. Click **Sign up**
3. Enter email, password, username
4. Verify email
5. Choose **Free** plan

---

## 🔧 STEP 2: Set Up Git on Your Computer

### Check if Git is Installed

```bash
git --version
```

If not installed, install from https://git-scm.com/

### Configure Git (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Example:
```bash
git config --global user.name "Ayush Shyam"
git config --global user.email "ayushshyam2404@gmail.com"
```

---

## 📁 STEP 3: Create GitHub Repository

### Option A: Via GitHub Website (Easiest)

1. Log in to GitHub
2. Click **+** icon (top right) → **New repository**
3. Fill in details:
   - **Repository name:** `falcon-rev` (or similar)
   - **Description:** `Revenue Management Portal with Competitor Pricing`
   - **Visibility:** Choose **Public** (if OK sharing) or **Private** (secure)
   - **Initialize with README:** Check this box
   - **.gitignore:** Select **Python**
   - Click **Create repository**

4. You'll see your repository URL:
   - `https://github.com/yourusername/falcon-rev.git`

### Option B: Via Command Line (Advanced)

```bash
# Create repo on GitHub website first, then:
cd ~/FLrevV2
git init
git remote add origin https://github.com/yourusername/falcon-rev.git
git branch -M main
```

---

## 🔐 STEP 4: Create .gitignore (Critical!)

⚠️ **NEVER commit your .env file to GitHub!**

Create/verify `.gitignore` file in your project:

```bash
cd ~/FLrevV2
```

Create `.gitignore` with:

```
# Environment variables - KEEP SECRET!
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Uploaded files
uploads/
uploads/logos/

# Flask
instance/
.webassets-cache

# Testing
.pytest_cache/
.coverage
htmlcov/
```

Save this as `.gitignore` in your project root.

---

## 📤 STEP 5: Initialize Git Repository Locally

Navigate to your project folder and initialize:

```bash
cd ~/FLrevV2

# Initialize git
git init

# Add GitHub as remote
git remote add origin https://github.com/yourusername/falcon-rev.git

# Verify remote
git remote -v
```

You should see:
```
origin  https://github.com/yourusername/falcon-rev.git (fetch)
origin  https://github.com/yourusername/falcon-rev.git (push)
```

---

## 📝 STEP 6: Add Files to Git

```bash
# Check status
git status

# Add all files (except those in .gitignore)
git add .

# Verify what will be committed
git status

# Should NOT show:
# - .env
# - __pycache__/
# - venv/
# - uploads/ folder
```

---

## 💾 STEP 7: Create First Commit

```bash
git commit -m "Initial commit: Falcon Rev Revenue Portal

- Flask web application
- Excel data processing
- SendGrid email integration
- Responsive mobile UI
- Competitor pricing analysis
- Logo upload and display"
```

---

## 🚀 STEP 8: Push to GitHub

### First Time Push

```bash
git branch -M main
git push -u origin main
```

You'll be asked for authentication. Choose one:

**Option A: Personal Access Token (Recommended)**

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click **Generate new token**
3. Name it `FalconRev`
4. Select scopes: `repo` (full control)
5. Click **Generate token**
6. **Copy the token** (you won't see it again!)
7. When git asks for password, paste the token

**Option B: SSH Key (More Secure)**

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Press Enter for default location
# Enter passphrase (optional)

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub
```

Then:
1. Go to GitHub Settings → SSH and GPG keys
2. Click **New SSH key**
3. Paste your public key
4. Click **Add SSH key**

---

## 📊 STEP 9: Verify on GitHub

1. Go to `https://github.com/yourusername/falcon-rev`
2. You should see your files:
   - ✅ app.py
   - ✅ templates/index.html
   - ✅ static/favicon.svg
   - ✅ utils/
   - ✅ README.md
   - ❌ .env (hidden, not committed)
   - ❌ venv/ (ignored)

---

## 📝 STEP 10: Create Professional README.md

Your README.md should already exist, but enhance it:

```markdown
# 🚀 Falcon Rev - Revenue Management Portal

A modern Flask web application for hotel revenue management with competitor pricing analysis.

## ✨ Features

- 📊 **7-Day Revenue Forecast** - Daily ADR, pickups, and revenue projections
- 🏨 **Competitor Pricing Analysis** - Track 8 competitors' rates with rate comparisons
- 📧 **Email Reports** - Generate and send beautiful HTML email reports via SendGrid
- 🎨 **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- 📤 **Excel Import** - Upload strategic analysis Excel files for processing
- 🔐 **Security** - Environment-based configuration, no hardcoded secrets

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Data Processing:** pandas, openpyxl
- **Email:** SendGrid API
- **Frontend:** HTML5, CSS3, JavaScript
- **Deployment:** PythonAnywhere (recommended)

## 📋 Requirements

- Python 3.7+
- Flask
- pandas
- openpyxl
- sendgrid
- python-dotenv

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/falcon-rev.git
cd falcon-rev
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create `.env` file:
```
SENDGRID_API_KEY=SG.your_key_here
SENDER_EMAIL=your_email@domain.com
```

### 5. Run Application
```bash
python3 app.py
```

Visit: http://localhost:3000

## 📖 Usage

1. **Upload Excel File** - Select your Strategic Analysis Excel file
2. **Upload Logo** (optional) - Add your company logo
3. **View Dashboard** - See 7-day forecast and competitor analysis
4. **Send Email** - Enter recipient email and send report via SendGrid

## 📂 Project Structure

```
falcon-rev/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── templates/
│   └── index.html         # Web interface
├── static/
│   └── favicon.svg        # Browser icon
├── utils/
│   ├── excel_processor.py # Excel data extraction
│   └── email_generator.py # HTML email generation
└── uploads/               # User uploaded files
```

## 🌐 Deployment

### PythonAnywhere
See [PYTHONANYWHERE_UPLOAD.md](PYTHONANYWHERE_UPLOAD.md) for detailed instructions.

### Other Platforms
- Heroku (with Procfile)
- AWS (with EC2 or Elastic Beanstalk)
- Google Cloud (with App Engine)
- DigitalOcean (with App Platform)

## 📊 Sample Data

Includes example Excel file with:
- 7 days of historical data
- 8 competitor hotels
- Revenue metrics
- Pricing data

## 🔒 Security

⚠️ **Important:**
- Never commit `.env` file to GitHub
- Use restricted SendGrid API keys
- Rotate API keys regularly
- Use environment variables in production

## 🤝 Contributing

Feel free to fork and submit pull requests!

## 📝 License

MIT License - feel free to use this project

## 🆘 Support

- [SendGrid Documentation](https://docs.sendgrid.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PythonAnywhere Help](https://help.pythonanywhere.com/)

## 👨‍💻 Author

[Your Name] - [Your GitHub Profile]

---

Made with ❤️ for hotel revenue managers
```

Save as `README.md`

---

## 🔄 STEP 11: Regular Commits & Updates

### After Making Changes

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with message
git commit -m "Updated email template with new branding"

# Push to GitHub
git push
```

### Useful Git Commands

```bash
# See commit history
git log

# See differences
git diff

# Undo last commit (if not pushed)
git reset HEAD~1

# Discard changes
git checkout -- filename

# See all branches
git branch -a

# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main
```

---

## 📚 STEP 12: Collaborate with Others

### Share Your Repository

1. Go to your GitHub repository
2. Click **Settings** → **Collaborators**
3. Click **Add people**
4. Search for GitHub username
5. They'll get an invitation

### Clone Repository (For Collaborators)

```bash
git clone https://github.com/yourusername/falcon-rev.git
cd falcon-rev
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🎯 GitHub Best Practices

✅ **DO:**
- Commit frequently with clear messages
- Use meaningful branch names (`feature/`, `fix/`, `docs/`)
- Keep `.env` and secrets out of repo
- Update README when adding features
- Create issues for bugs and feature requests
- Write good commit messages

❌ **DON'T:**
- Commit API keys or passwords
- Commit large files (>100MB)
- Commit generated files (__pycache__, venv/)
- Write vague commit messages ("fixed stuff")
- Delete important branches
- Force push to main branch

---

## 📦 STEP 13: Create requirements.txt

For collaborators and deployment:

```bash
pip freeze > requirements.txt
```

This creates a file with all dependencies. Collaborators can install with:

```bash
pip install -r requirements.txt
```

---

## 🚀 STEP 14: Deploy from GitHub

### Option A: PythonAnywhere (Recommended)

1. Clone your repo on PythonAnywhere
2. See PYTHONANYWHERE_UPLOAD.md

### Option B: Heroku

1. Create Procfile in repo:
```
web: gunicorn app:app
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Option C: GitHub Pages (Static Site Only)

GitHub Pages works for static sites, but Flask needs a backend. Use PythonAnywhere instead.

---

## 📖 GitHub Features to Explore

### Issues
- Track bugs and feature requests
- Assign to team members
- Use labels for organization

### Pull Requests
- Review code before merging
- Discussion and feedback
- Continuous Integration (CI)

### Discussions
- Q&A with collaborators
- Announcements
- Community building

### Actions
- Automated testing
- Continuous deployment
- Scheduled tasks

### Wiki
- Project documentation
- Setup guides
- API reference

---

## 🆘 Troubleshooting

### "fatal: not a git repository"
```bash
cd ~/FLrevV2
git init
git remote add origin https://github.com/yourusername/falcon-rev.git
```

### "fatal: Authentication failed"
- Use Personal Access Token instead of password
- Or set up SSH key
- See STEP 8 above

### ".env file keeps showing in commits"
```bash
# Remove from tracking (after .gitignore is created)
git rm --cached .env
git commit -m "Remove .env from tracking"
git push
```

### "Cannot push - rejected"
```bash
# Pull latest changes first
git pull origin main

# Resolve conflicts if any, then push
git push origin main
```

---

## 📊 Your GitHub URL

```
https://github.com/yourusername/falcon-rev
```

Replace `yourusername` with your actual GitHub username.

---

## ✅ GitHub Checklist

- [ ] GitHub account created
- [ ] Repository created
- [ ] .gitignore file added
- [ ] .env file is ignored (not committed)
- [ ] All files committed and pushed
- [ ] README.md is complete
- [ ] requirements.txt created
- [ ] Repository is public or private (as desired)
- [ ] Collaborators added (if needed)
- [ ] Personal Access Token or SSH key configured

---

## 🎉 Next Steps

1. **Share your repo** with your team
2. **Add collaborators** if working with others
3. **Deploy to PythonAnywhere** from GitHub
4. **Monitor activity** on GitHub dashboard
5. **Keep repository updated** with regular commits

---

## 📚 Additional Resources

- [GitHub Hello World](https://guides.github.com/activities/hello-world/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Skills](https://skills.github.com/)
- [Markdown Guide](https://www.markdownguide.org/)

---

Your Falcon Rev repository is now on GitHub! 🚀
