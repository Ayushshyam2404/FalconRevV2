# Falcon Rev - Revenue Report Portal

A professional, Apple-styled web portal for uploading revenue data via Excel, extracting key metrics, and sending beautifully formatted HTML emails with competitor analysis.

## ✨ Key Features

- **📊 7-Day Revenue Forecast** - Automatic data extraction and analysis
- **🎯 Key Metrics Cards** - Average ADR, Revenue, and Occupancy percentages
- **🏨 Competitor Pricing** - Display all competitor rates in professional grid format
- **🎨 Dark & Orange Theme** - Professional Falcon Rev branding with Apple-style minimalist design
- **📧 Email-Ready HTML** - Embedded logos (no external dependencies), works in all email clients
- **🏷️ Custom Subject Lines** - Personalize each email report
- **🎭 Universal Logo Upload** - Support for PNG, JPG, GIF, SVG, WebP formats
- **📱 Responsive Design** - Perfect on desktop, tablet, and mobile devices
- **⚡ Lightning Fast** - Real-time Excel processing and email generation

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /Users/caliber/private/FLrevV2
pip install -r requirements.txt
```

### 2. Configure Email (Gmail Recommended)
Create `.env` file with Gmail app password:
```env
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=xxxx xxxx xxxx xxxx
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**Gmail Setup:**
- Go to https://myaccount.google.com/apppasswords
- Enable 2-Factor Authentication first
- Generate App Password (16 characters)
- Copy password to .env (remove spaces if needed)

### 3. Start the App
```bash
python3 app.py
```

### 4. Open in Browser
```
http://localhost:9000
```

## 📝 How to Use

1. **Upload Logo** (optional) - Add your company branding image
2. **Upload Excel File** - Your revenue forecast spreadsheet
3. **Customize Subject** - Email subject line (optional)
4. **Enter Recipient Email** - Where to send the report
5. **Click "Send Email"** - Report sends immediately

## 📧 Email Content

The generated email includes:
- Header with your uploaded logo
- 3 Key Metrics cards (ADR, Revenue, Occupancy %)
- 7-Day forecast table with color-coded pickup changes
- All competitor hotel pricing
- Professional Falcon Rev footer

## 📁 File Structure

```
FLrevV2/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env                           # Email configuration (KEEP SECRET!)
├── README.md                      # This file
├── EMAIL_SETUP.md                 # Email setup instructions
├── TROUBLESHOOTING.md             # Common issues & solutions
├── test_email.py                  # SMTP configuration tester
├── utils/
│   ├── excel_processor.py         # Extract data from Excel files
│   └── email_generator.py         # Generate HTML email template
├── templates/
│   └── index.html                 # Web portal UI (dark/orange theme)
└── uploads/
    └── logos/                     # Uploaded logo storage
```

## ⚙️ Configuration

### Email Providers

**Gmail (Recommended)**
```env
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=xxxx xxxx xxxx xxxx  # App password (16 chars)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**Office 365 / Outlook**
```env
SENDER_EMAIL=your-email@company.com
SENDER_PASSWORD=your-password
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587
```

**SendGrid**
```env
SENDER_EMAIL=your-email@company.com
SENDER_PASSWORD=SG.xxxxxxxxxxxxx  # SendGrid API Key
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
```

### Excel File Format

Expected columns in your Excel file:
- **Date Column** - Daily date values
- **Transient** - Daily pickups
- **ADR** - Average Daily Rate
- **On the Books** - Occupancy percentage
- **Competitor Pricing** (Columns 68-75) - All competing hotel rates

The app automatically detects and extracts these columns.

## 🐛 Troubleshooting

### Email Not Sending?

**Step 1: Test SMTP Configuration**
```bash
python3 test_email.py
```

This script will tell you exactly what's wrong.

**Step 2: Verify Gmail Setup**
- ✓ 2FA enabled on Gmail account
- ✓ App password created (16 characters)
- ✓ App password copied correctly (remove spaces)
- ✓ Gmail "Less secure app access" is NOT needed

**Step 3: Send Test Email to Your Own Address**
Test with your own Gmail first to verify configuration.

**Step 4: Check Recipient Email**
- ✓ Email address is typed correctly
- ✓ Recipient email isn't blocking external emails
- ✓ Try different recipients if one fails

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

## 🔧 API Endpoints

### POST /api/upload
Upload and process Excel file
- **Parameters:** FormData with "file" (Excel file)
- **Returns:** Extracted metrics and 7-day data

### POST /api/upload-logo
Upload company logo
- **Parameters:** FormData with "logo" (image file)
- **Returns:** Base64 data URI

### POST /api/send-email
Send formatted revenue report
- **Parameters:** JSON with email, data, subject, logo_base64
- **Returns:** Success message or error details

## 🧪 Development & Testing

### Run Email Test
```bash
python3 test_email.py
```

### Check SMTP Credentials
Edit `.env` and verify:
- Email address is correct
- App password has no spaces
- SMTP server and port are correct

### Debug Mode
Flask app runs with debug mode enabled by default:
```bash
python3 app.py
```

### Change Port
Default port is 9000. To change, edit app.py:
```python
app.run(debug=True, port=YOUR_PORT)
```

## 🔒 Security Notes

⚠️ **Important Security Practices:**
- Never commit `.env` file with real credentials
- Keep app passwords secure (treat like real passwords)
- Only send reports to verified recipients
- The app runs on localhost by default (not exposed to internet)
- Use strong, unique email passwords
- Don't share your SMTP credentials

## ⚡ Performance

- **Excel Processing:** < 1 second
- **Email Generation:** Instant (in-memory)
- **Logo Embedding:** Base64 (no external requests)
- **UI Response:** Real-time feedback with loading states

## 📚 Documentation

- **[EMAIL_SETUP.md](EMAIL_SETUP.md)** - Complete email configuration guide with screenshots
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and step-by-step solutions
- **[test_email.py](test_email.py)** - Diagnostic tool for SMTP troubleshooting

## 🎯 Excel File Format

Your Excel file should have columns like:
- ADR (Average Daily Rate)
- Revenue / Sales
- Pickups / Orders / Bookings
- Any other metrics you want to include

The portal automatically detects these columns and calculates averages.

## Email Features

- Orange and dark theme matching the portal
- Three metric dials (ADR, Revenue, Pickups)
- Data cards with all row information
- Apple-style card design
- Responsive layout for all devices

## Configuration

Edit `app.py` to customize:
- Email sender settings
- Maximum upload file size
- Data preview limit
- Email subject and styling

## Troubleshooting

**Email not sending?**
- Check your `.env` file credentials
- Ensure you're using an App Password (if using Gmail)
- Check SMTP settings match your email provider

**File upload issues?**
- Ensure file is in Excel format (.xlsx, .xls, .csv)
- Check file size is under 16MB
- Verify column names match the processor expectations
