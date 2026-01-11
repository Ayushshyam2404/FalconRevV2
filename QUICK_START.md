# Falcon Rev - Quick Start Guide

Get up and running in 5 minutes!

## ⚡ 5-Minute Setup

### Step 1: Install (30 seconds)
```bash
cd /Users/caliber/private/FLrevV2
pip install -r requirements.txt
```

### Step 2: Configure Gmail (2 minutes)
1. Go to https://myaccount.google.com/apppasswords
2. If you don't see "App passwords":
   - Click "Security" in left menu
   - Enable "2-Step Verification" first
   - Then come back to "App passwords"
3. Select "Mail" and "macOS"
4. Copy the 16-character password shown

### Step 3: Create .env File (1 minute)
Create file `.env` in your project folder:
```env
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=xxxx xxxx xxxx xxxx
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**⚠️ Important:** 
- Remove spaces from password if present
- Keep this file secret (don't share!)

### Step 4: Start App (30 seconds)
```bash
python3 app.py
```

### Step 5: Open Portal
Go to: **http://localhost:9000**

You're ready to go! 🎉

---

## 📋 Using the Portal

### Basic Workflow (1 minute per email):
1. **Upload Logo** (optional) - PNG, JPG, GIF, SVG, or WebP
2. **Select Excel File** - Your revenue forecast
3. **Enter Email Subject** (optional) - Custom subject line
4. **Enter Recipient Email** - Where to send report
5. **Click "Send Email"** - Done!

### What You'll Get:
✓ Beautiful HTML email  
✓ Your company logo  
✓ 7-day revenue forecast  
✓ Key metrics (ADR, Revenue, Occupancy)  
✓ All competitor prices  
✓ Professional formatting  

---

## 🧪 Test Your Setup

### Verify Email Works:
```bash
python3 test_email.py
```

If it works, you're all set!  
If it fails, see "Troubleshooting" below.

---

## ❌ Troubleshooting

### "Authentication failed" error?
1. Check `.env` file for typos
2. Verify app password is 16 characters
3. Make sure 2FA is enabled on Gmail
4. Try copying password again (sometimes includes extra spaces)

### "Connection refused" error?
1. Make sure you're on the same WiFi/network
2. Check firewall settings
3. Try port 587 instead of 465

### Email won't send?
1. Run `python3 test_email.py` - tells you exact issue
2. Try sending to your own Gmail first
3. Check recipient email spelling
4. Verify recipient isn't blocking external emails

### Need detailed help?
See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 🎨 Portal Features

- **Dark/Orange Theme** - Professional Apple-style design
- **Drag & Drop Upload** - Easy file selection
- **Logo Preview** - See your logo before sending
- **Real-time Metrics** - View extracted data instantly
- **Custom Subjects** - Personalize each email
- **Responsive Design** - Works on any device

---

## 📊 Excel Requirements

Your Excel file should have:
- ✓ Date column
- ✓ "Transient" or "Pickups" column
- ✓ "ADR" column
- ✓ "On the Books" column (occupancy)
- ✓ Competitor pricing data

The app automatically finds these columns!

---

## 🚀 Next Steps

1. ✅ Install dependencies
2. ✅ Configure Gmail
3. ✅ Create .env file
4. ✅ Start app
5. ✅ Test with `test_email.py`
6. 🎯 Send your first revenue report!

---

## 📱 Pro Tips

💡 **Save your logo:** Upload once, use for all reports  
💡 **Draft emails:** Try sending to yourself first  
💡 **Custom subjects:** Use date in subject (e.g., "Revenue Report - Jan 15")  
💡 **Multiple recipients:** Copy/paste to send to different emails  
💡 **Offline use:** Portal works without internet after startup  

---

## ❓ Questions?

- Check [README.md](README.md) for full documentation
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Run `python3 test_email.py` to diagnose problems
- Review [EMAIL_SETUP.md](EMAIL_SETUP.md) for advanced config

---

**Ready?** Open http://localhost:9000 and start sending reports! 🚀
