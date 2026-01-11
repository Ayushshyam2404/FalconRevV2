# Developer Quick Reference

Fast lookup guide for developers working on Falcon Rev.

## 📁 File Locations

| Purpose | File |
|---------|------|
| Main App | `/app.py` |
| Portal UI | `/templates/index.html` |
| Data Processing | `/utils/excel_processor.py` |
| Email Generator | `/utils/email_generator.py` |
| Config | `/.env` |
| Dependencies | `/requirements.txt` |

## 🔗 API Routes

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/` | Serve portal UI |
| POST | `/api/upload` | Process Excel file |
| POST | `/api/upload-logo` | Convert logo to base64 |
| POST | `/api/send-email` | Send formatted email |

## 📊 Data Processing Pipeline

```
Excel File → Parser → Extract Daily Data
                   → Extract Competitors (8 hotels)
                   → Calculate Metrics
                   → Return JSON
```

## 🎨 Color Constants

```python
PRIMARY_ORANGE = "#ff9500"
ORANGE_DARK = "#ff6b35"
BACKGROUND = "#0a0a0a"
CARD_BG = "#1a1a1a"
TEXT_LIGHT = "#ffffff"
SUCCESS = "#34c759"
WARNING = "#ff3b30"
```

## 📧 SMTP Configuration

```python
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD').strip()
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
```

## 🧪 Testing Commands

```bash
# Test SMTP connection
python3 test_email.py

# Run app in debug
python3 app.py

# Check Python version
python3 --version

# List installed packages
pip list
```

## 💾 Key Data Structures

### Metrics JSON
```json
{
  "average_adr": 90.83,
  "average_revenue": 2177.36,
  "average_pickups": 20.9,
  "average_occupancy": 24.0
}
```

### Daily Data Array
```json
[
  {
    "date": "2024-01-15",
    "pickups": 18,
    "adr": 89.50,
    "revenue": 1611.00,
    "occupancy": 22.5,
    "pickup_change": -2
  }
]
```

### Competitor Data
```json
{
  "competitor_1": 134.50,
  "competitor_2": 156.75,
  ...
  "competitor_8": 186.25,
  "average": 158.44
}
```

## 🎯 Common Tasks

### Add New Email Field
1. Edit `/utils/email_generator.py`
2. Update `generate_email_html()` function
3. Add HTML section with your content
4. Test with `/api/send-email` endpoint

### Change Colors
1. Update constants in `/utils/email_generator.py`
2. Update CSS in `/templates/index.html`
3. Rebuild email template

### Add New API Route
1. Edit `/app.py`
2. Add `@app.route('/api/new-route')` decorator
3. Define function with logic
4. Return JSON response
5. Test with curl or browser

### Debug Email
```bash
python3 test_email.py  # Check SMTP first
```

## 🔑 Environment Variables

```env
SENDER_EMAIL=          # Gmail address
SENDER_PASSWORD=       # App password (16 chars)
SMTP_SERVER=           # Default: smtp.gmail.com
SMTP_PORT=             # Default: 587
```

## 📐 Excel Column Mapping

| Purpose | Column Name | Notes |
|---------|-------------|-------|
| Date | Usually Column A or "Unnamed: 1" |  |
| Pickups | "Transient" | Daily count |
| ADR | "ADR" | Average Daily Rate |
| Occupancy | "On the Books" | Percentage |
| Competitors | Columns 68-75 | 8 hotels |

## 🎭 Email Template Structure

```html
<header>          <!-- Logo and title -->
<metrics>         <!-- 3 cards: ADR, Revenue, Occupancy -->
<forecast>        <!-- 7-day table -->
<competitors>     <!-- 8 hotel grid -->
<footer>          <!-- Branding -->
```

## 🚀 Performance Tips

- Excel processing: cached in memory
- Logo encoding: done once, reused
- Email: sent asynchronously in background
- UI: responds immediately with loading state

## 📱 Responsive Breakpoints

```css
Desktop:  > 1024px
Tablet:   768px - 1024px
Mobile:   < 768px
```

## 🔐 Security Checklist

- [ ] `.env` not committed to git
- [ ] App password used (not main Gmail password)
- [ ] 2FA enabled on Gmail
- [ ] Email credentials never logged
- [ ] File uploads validated (size, type)
- [ ] Recipients validated (basic email format)

## 🐛 Debugging Tips

1. **Check logs:** Flask prints to terminal
2. **Test email:** Run `python3 test_email.py`
3. **Verify .env:** Check for spaces/typos
4. **Browser console:** Check JavaScript errors (F12)
5. **Network tab:** Check API responses
6. **Email preview:** Check with Litmus or EmailOnAcid

## 📦 Dependencies

```
Flask==3.0.0              # Web framework
python-dotenv==1.0.0      # Environment variables
openpyxl==3.11.2          # Excel reading
pandas==2.1.4             # Data processing
Werkzeug==3.0.1           # WSGI utilities
```

## 🎬 Startup Sequence

1. Load `.env` file
2. Initialize Flask app
3. Import utilities
4. Define routes
5. Start server on port 9000
6. Display: "Running on http://localhost:9000"

## 💬 Key Functions

### app.py
- `@app.route('/')` - Serve UI
- `upload_file()` - Process Excel
- `send_email()` - Send report
- `send_smtp_email()` - SMTP connection

### excel_processor.py
- `process_excel_file()` - Main parser
- `extract_daily_data()` - Get 7-day data
- `extract_competitor_pricing()` - Get hotel rates
- `calculate_metrics()` - Compute averages

### email_generator.py
- `generate_email_html()` - Main template
- `create_metrics_cards()` - Metric display
- `create_daily_section()` - Forecast table
- `create_competitor_section()` - Competitor grid

## 🎪 Testing Workflow

1. Upload Excel file
2. Check extracted data in browser console
3. Upload logo (optional)
4. Fill email details
5. Click "Send Email"
6. Check inbox (check spam folder!)
7. Review email formatting

## 🆘 Quick Fixes

| Problem | Solution |
|---------|----------|
| Port 9000 in use | `lsof -i :9000` then kill process |
| Excel not parsing | Check column names and format |
| Logo not showing | Verify file size < 2MB and format |
| Email won't send | Run `python3 test_email.py` |
| Gmail auth fails | Check app password, enable 2FA |

## 📞 Contact & Support

- **Issue?** Check TROUBLESHOOTING.md
- **Setup?** Check QUICK_START.md  
- **Config?** Check EMAIL_SETUP.md
- **Status?** Check PROJECT_STATUS.md

---

**Pro Tip:** Keep this file open while developing! 🚀
