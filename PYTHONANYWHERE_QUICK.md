# ⚡ PythonAnywhere Quick Reference

**5-Minute Quick Start for Manual Upload**

---

## 🎬 TL;DR - Fast Version

### 1. Create & Login to PythonAnywhere
- Go to https://www.pythonanywhere.com
- Create account → Verify email → Login

### 2. Upload Your Files
```
Dashboard → Files → Create folder "falconrev"
Upload:
  - app.py
  - templates/index.html
  - static/favicon.svg
  - utils/*.py
  - .env (with your SendGrid API key!)
  - Create "uploads" folder
```

### 3. Create Virtual Environment
```bash
# In Bash console:
cd ~/falconrev
python3 -m venv venv
source venv/bin/activate
pip install flask pandas openpyxl sendgrid python-dotenv
```

### 4. Configure .env
```
SENDGRID_API_KEY=SG.xxxxx
SENDER_EMAIL=your_email@domain.com
```

### 5. Create Web App
- Click **Web** → **Add a new web app**
- Choose domain → Python 3.x → Flask

### 6. Edit WSGI File
Replace full content with:
```python
import sys, os
project_home = '/home/USERNAME/falconrev'
if project_home not in sys.path:
    sys.path.insert(0, project_home)
activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')
exec(open(activate_this).read(), {'__file__': activate_this})
import dotenv
dotenv.load_dotenv(os.path.join(project_home, '.env'))
from app import app as application
```
*(Replace USERNAME with your PythonAnywhere username)*

### 7. Reload Web App
- Click **Web** → Green **Reload** button
- Wait for "Web app reloaded"

### 8. Test
- Open `https://USERNAME.pythonanywhere.com`
- ✅ Done!

---

## 🔧 File Paths Reference

```
Home Folder:        /home/yourusername/
Project Folder:     /home/yourusername/falconrev/
WSGI File:          /var/www/yourusername_pythonanywhere_com_wsgi.py
Error Log:          Click Web → Log files → Error log
Bash Console:       Click Consoles → Bash
Web Configuration:  Click Web (in sidebar)
```

---

## 📱 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Module not found | `pip install flask pandas openpyxl sendgrid python-dotenv` |
| .env not found | Verify file is in `/home/username/falconrev/.env` |
| Email not sending | Check `.env` has correct `SENDGRID_API_KEY` |
| App won't reload | Check error log in Web tab |
| 502 Bad Gateway | Click Reload button again, wait 30 seconds |

---

## 🎯 Your App URL

Once deployed:
```
https://yourusername.pythonanywhere.com
```

Replace `yourusername` with your PythonAnywhere username.

---

## 📖 See Full Guide

Open: `PYTHONANYWHERE_UPLOAD.md` for complete step-by-step instructions with screenshots tips.
