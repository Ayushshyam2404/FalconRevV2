# SendGrid Setup Guide

## ✅ Migration Complete: Gmail SMTP → SendGrid API

Your Falcon Rev portal now uses **SendGrid API** instead of Gmail SMTP for sending emails.

---

## 📋 Setup Steps

### 1. Get Your SendGrid API Key
- Go to [SendGrid Console](https://app.sendgrid.com)
- Log in or create a free account
- Navigate to **Settings → API Keys**
- Click **Create API Key**
- Choose **Restricted Access** (recommended)
- Give it a name like "Falcon Rev"
- Enable: `Mail Send`
- Create the key and **copy the API key** (you won't see it again!)

### 2. Update Your .env File

Replace the contents of `.env` with:

```env
# SendGrid Configuration
SENDGRID_API_KEY=SG.your_api_key_here
SENDER_EMAIL=your_email@yourdomain.com
```

**Example:**
```env
SENDGRID_API_KEY=SG.1234567890abcdefghijklmnop
SENDER_EMAIL=noreply@yourhotel.com
```

### 3. Verify Setup
```bash
python3 -c "from app import app; print('✅ Ready to go!')"
```

---

## 🎯 Benefits of SendGrid

✅ **More Reliable** - Enterprise-grade infrastructure  
✅ **Better Deliverability** - Automatic bounce/complaint handling  
✅ **Free Tier** - 100 emails/day free (perfect for testing)  
✅ **No Password Needed** - Just your API key  
✅ **Analytics** - Track opens, clicks, bounces in SendGrid dashboard  

---

## 📊 Free Plan Details

- **100 emails/day** - Enough for testing
- **Unlimited contacts** - Store recipient data
- **Basic email reporting** - See delivery status
- **24/7 support** - Help when you need it

**Paid Plans** start at $19.95/month for unlimited emails.

---

## 🧪 Test Email

Once your `.env` is configured:

```bash
cd /Users/caliber/private/FLrevV2
python3 app.py
```

Then use the web portal at `http://localhost:9000` to send a test email!

---

## ❓ Troubleshooting

### "SendGrid API key not configured"
- Check your `.env` file has `SENDGRID_API_KEY` set
- Make sure there are no spaces: `SENDGRID_API_KEY=SG.xxx` (not `= SG.xxx`)

### "Invalid recipient email"
- Double-check the recipient email address format
- Make sure it doesn't have extra spaces

### Email not arriving
- Check SendGrid dashboard for bounces or blocks
- Verify SENDER_EMAIL is verified in SendGrid

---

## 🔒 Security Note

- **Never commit .env to version control**
- Keep your API key secret
- Rotate keys regularly in production
- Use restricted access API keys (Mail Send only)

---

## 📝 What Changed

| Feature | Before (Gmail) | After (SendGrid) |
|---------|---|---|
| Method | SMTP | API |
| Credentials | Email + Password | API Key |
| Setup | 🔑 App Password needed | 🔑 API Key |
| Reliability | 📊 Moderate | ⭐⭐⭐⭐⭐ Enterprise |
| Features | Basic | Advanced analytics |
| Cost | Free | Free (100/day) |

---

Ready to send emails with SendGrid! 🚀
