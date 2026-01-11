# Email Setup Guide for Falcon Rev

## Using Gmail SMTP

### Step 1: Enable 2-Factor Authentication
1. Go to https://myaccount.google.com/security
2. Scroll to "2-Step Verification"
3. Enable 2FA if not already enabled

### Step 2: Create App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer" (or your device)
3. Google will generate a 16-character app password
4. **Copy this password (it has spaces, remove them)**

### Step 3: Update .env File
```
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=xxxxxxxxxxxxxxxx
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**Important**: Remove all spaces from the app password!

### Step 4: Verify Configuration
- The app will automatically test the connection
- If authentication fails, check the error message in the web UI
- Common issues:
  - Wrong app password (must be 16 chars without spaces)
  - 2FA not enabled
  - Recipient email doesn't accept emails

## Using Other Email Providers

### Gmail (same as above)
- SMTP Server: smtp.gmail.com
- Port: 587
- Requires 2FA and App Password

### Microsoft Outlook/Office 365
- SMTP Server: smtp.office365.com
- Port: 587
- Use your email and password

### SendGrid
- SMTP Server: smtp.sendgrid.net
- Port: 587
- Username: apikey
- Password: your-sendgrid-api-key

### AWS SES
- SMTP Server: email-smtp.{region}.amazonaws.com
- Port: 587
- Requires AWS credentials

## Troubleshooting

### "Authentication failed"
- Check the app password is correct
- Verify 2FA is enabled
- Make sure you're using an app password, not your regular password

### "Recipient email rejected"
- The recipient email might not exist
- Some email servers might block your domain
- Try sending to a different email address to test

### "Connection timeout"
- Check your firewall settings
- SMTP port 587 should be open
- Some networks block SMTP - use VPN if needed

### "Message bounced"
- The HTML email format might be too large
- Try with a smaller Excel file
- Check if the recipient's email server has file size limits

## Testing Email

After updating .env, test by:
1. Open the Falcon Rev web UI
2. Upload an Excel file
3. Enter a test email address (your own)
4. Click "Send Email"
5. Check your inbox (and spam folder)

If you get an error in the web UI, it will tell you exactly what went wrong!
