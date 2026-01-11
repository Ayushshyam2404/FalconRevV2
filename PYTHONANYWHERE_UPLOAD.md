# 🚀 Manual Upload to PythonAnywhere Guide

Complete step-by-step instructions to deploy Falcon Rev to PythonAnywhere.

---

## 📋 Prerequisites

- PythonAnywhere account (create free at https://www.pythonanywhere.com)
- Your SendGrid API key
- Your sender email address
- All project files ready

---

## 🎯 STEP 1: Create PythonAnywhere Account & Login

1. Go to https://www.pythonanywhere.com
2. Click **Sign Up** and create a free account
3. Verify your email
4. Log in to your PythonAnywhere dashboard

---

## 📁 STEP 2: Upload Files via Web Interface

### Method A: Upload via Drag & Drop (Recommended)

1. In PythonAnywhere dashboard, click **Files**
2. Navigate to `/home/yourusername/`
3. Create a new folder for your app:
   - Click **New Folder**
   - Name it `falconrev` or similar
   - Click **Create**

4. Enter the new folder and upload your files:
   - **app.py**
   - **templates/** (folder with index.html)
   - **static/** (folder with favicon.svg and CSS)
   - **utils/** (folder with excel_processor.py and email_generator.py)
   - **.env** (with your SendGrid API key)
   - **uploads/** (create empty folder)

### Method B: Upload via Web Form

1. Go to **Files** section
2. Navigate to your project folder
3. Click **Upload a file** 
4. Select files from your computer and upload

### Method C: Upload via Bash Console (Advanced)

1. Click **Consoles** → **Bash**
2. Run these commands:

```bash
# Navigate to home folder
cd ~

# Create project folder
mkdir falconrev
cd falconrev

# Create subdirectories
mkdir templates static utils uploads

# Create empty .env (we'll edit it later)
touch .env
```

---

## 📦 STEP 3: Set Up Virtual Environment

### In PythonAnywhere Web Interface:

1. Click **Consoles** → **Bash**
2. Run these commands:

```bash
cd ~/falconrev

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install flask pandas openpyxl sendgrid

# Verify installation
pip list
```

**Expected output should show:**
- flask
- pandas
- openpyxl
- sendgrid

---

## 🔧 STEP 4: Configure .env File

### Option 1: Edit via Web Interface

1. Click **Files**
2. Navigate to `/home/yourusername/falconrev/`
3. Click on `.env` file
4. Click **Edit**
5. Paste this content:

```env
SENDGRID_API_KEY=SG.your_sendgrid_api_key_here
SENDER_EMAIL=your_email@yourdomain.com
```

**Replace with your actual values:**
- `SG.your_sendgrid_api_key_here` → Your SendGrid API key
- `your_email@yourdomain.com` → Your email address

6. Click **Save**

### Option 2: Edit via Bash Console

```bash
cd ~/falconrev

# Create/edit .env file
cat > .env << 'EOF'
SENDGRID_API_KEY=SG.your_sendgrid_api_key_here
SENDER_EMAIL=your_email@yourdomain.com
EOF
```

---

## 🌐 STEP 5: Create Web App

### In PythonAnywhere Dashboard:

1. Click **Web** (in left sidebar)
2. Click **Add a new web app**
3. Choose domain: `yourusername.pythonanywhere.com` or custom domain
4. Click **Next**
5. Select **Python 3.x** (latest version)
6. Click **Next**
7. Choose **Flask**
8. Click **Next**
9. Click **Next** (use default path)

✅ Your web app is created!

---

## ⚙️ STEP 6: Configure WSGI File

The WSGI file tells PythonAnywhere how to run your app.

### Edit WSGI Configuration:

1. Click **Web** in left sidebar
2. Under **Code**, click on the **WSGI configuration file** link
3. It will open `/var/www/yourusername_pythonanywhere_com_wsgi.py`

### Replace the entire content with:

```python
import sys
import os

# Add your project directory to path
project_home = '/home/yourusername/falconrev'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activate virtual environment
activate_this = os.path.join(project_home, 'venv/bin/activate_this.py')
exec(open(activate_this).read(), {'__file__': activate_this})

# Load environment variables from .env
import dotenv
dotenv.load_dotenv(os.path.join(project_home, '.env'))

# Import and run the Flask app
from app import app as application
```

4. Click **Save**

**Important:** Replace `yourusername` with your actual PythonAnywhere username!

---

## 📚 STEP 7: Install python-dotenv Package

Your app needs to read the .env file.

### In Bash Console:

```bash
cd ~/falconrev
source venv/bin/activate
pip install python-dotenv
```

---

## 🔄 STEP 8: Reload Web App

### Back in Web App Configuration:

1. Click **Web** in left sidebar
2. Scroll down and click the **Reload button** (green button)
3. Wait for it to say "Reloading web app..." → "Web app reloaded"

✅ Your app is now live!

---

## 🧪 STEP 9: Test Your App

1. Your app is now live at: `https://yourusername.pythonanywhere.com`
2. Click the link in PythonAnywhere dashboard
3. You should see your Falcon Rev portal!

### Test Features:

- ✅ Upload Excel file
- ✅ Upload logo (should display in header)
- ✅ See 7-day forecast
- ✅ See competitor rates
- ✅ Send email (will use SendGrid)

---

## 🐛 STEP 10: Troubleshooting

### App shows error page

1. Click **Web** → **Log files** → **Error log**
2. Scroll to bottom to see latest errors
3. Common issues:

**"No module named 'sendgrid'"**
```bash
cd ~/falconrev
source venv/bin/activate
pip install sendgrid
```

**"No such file or directory: .env"**
- Make sure `.env` file is in `/home/yourusername/falconrev/`
- Verify it has correct permissions

**"SendGrid API key not configured"**
- Check `.env` file has correct `SENDGRID_API_KEY`
- Restart web app (click Reload)

**Excel file upload fails**
- Make sure `uploads/` folder exists and has write permissions
- Check file is actual Excel file (.xlsx)

### Debug Mode

To see more detailed errors, edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:

Change:
```python
from app import app as application
```

To:
```python
from app import app
app.config['DEBUG'] = True
application = app
```

Then reload. (But remember to turn OFF debug in production!)

---

## 📊 File Structure Check

Your PythonAnywhere folder should look like:

```
/home/yourusername/falconrev/
├── app.py                          ← Main Flask app
├── .env                            ← Your API keys (private!)
├── venv/                           ← Virtual environment
│   ├── bin/
│   │   ├── python
│   │   └── activate
│   └── lib/
│       └── python3.x/
│           └── site-packages/
├── templates/
│   └── index.html                  ← Web interface
├── static/
│   └── favicon.svg                 ← Browser icon
├── utils/
│   ├── excel_processor.py          ← Excel reader
│   └── email_generator.py          ← Email creator
└── uploads/                        ← Where files are saved
    └── logos/                      ← Uploaded logos
```

---

## 🔐 Security Notes

✅ **DO THIS:**
- Keep `.env` file private (never share API key)
- Use restricted SendGrid API keys
- Set up custom domain with HTTPS
- Regularly rotate API keys

❌ **DON'T DO THIS:**
- Don't commit `.env` to GitHub
- Don't share your PythonAnywhere account
- Don't use production API key in development
- Don't make your .env file world-readable

---

## 📈 Next Steps

### After Deployment:

1. **Test email sending:**
   - Upload Excel file
   - Enter test email address
   - Click "Send Email"
   - Check if email arrives

2. **Monitor performance:**
   - Click **Web** → **CPU/Memory usage**
   - Check if app is using reasonable resources

3. **Set up logging:**
   - Click **Web** → **Log files**
   - Check error log periodically

4. **Upgrade if needed:**
   - Free tier: 100 CPU seconds/day
   - Paid tier: unlimited

---

## 💡 Useful PythonAnywhere Features

### View Live Logs
```bash
# In Bash console
cd ~/falconrev
tail -f /var/log/yourusername_pythonanywhere_com_server.log
```

### Restart Your App
```bash
# Click Web → Reload button
# Or in Bash:
touch /var/www/yourusername_pythonanywhere_com_wsgi.py
```

### Check Disk Usage
```bash
df -h ~
```

---

## ✅ Deployment Checklist

- [ ] PythonAnywhere account created
- [ ] All files uploaded to `/home/yourusername/falconrev/`
- [ ] Virtual environment created and packages installed
- [ ] `.env` file created with SendGrid API key
- [ ] WSGI file configured correctly
- [ ] Web app created and configured
- [ ] Web app reloaded
- [ ] App accessible at `yourusername.pythonanywhere.com`
- [ ] Excel upload works
- [ ] Email sending works
- [ ] Logo displays correctly
- [ ] Mobile UI works on phone

---

## 🆘 Support

- **PythonAnywhere Docs:** https://help.pythonanywhere.com/
- **SendGrid Docs:** https://docs.sendgrid.com/
- **Flask Docs:** https://flask.palletsprojects.com/

---

## 🎉 Congratulations!

Your Falcon Rev app is now live and accessible from anywhere! 🚀

**Your live URL:** `https://yourusername.pythonanywhere.com`
