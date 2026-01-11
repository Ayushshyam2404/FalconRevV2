# Falcon Rev - Email Troubleshooting Guide

## The Error You Received

```
Mail Delivery Subsystem - Delivery Status Notification (Failure)
Message not delivered. There was a problem delivering your message to
takshil@guestlove1.com. Contact the remote administrator.
```

This error means one of the following:

### Possibility 1: Recipient Email Doesn't Accept External Emails
- The email address `takshil@guestlove1.com` might be a corporate/restricted email
- Some corporate email systems block external senders
- **Solution**: Try sending to a different Gmail address first to test

### Possibility 2: SMTP Authentication Issues
- Your Gmail app password might be incorrect
- 2FA might not be enabled
- You might be using your regular password instead of app password
- **Solution**: Follow the setup in EMAIL_SETUP.md

### Possibility 3: Email Content Issues
- The base64 encoded logo or HTML might be too large
- Some email servers reject emails over 25MB
- **Solution**: Use a smaller logo image

## Quick Diagnostic Steps

### Step 1: Test Your SMTP Configuration
```bash
cd /Users/caliber/private/FLrevV2
python3 test_email.py
```

This will tell you:
- ✓ If your SMTP credentials are correct
- ✓ If you can connect to Gmail
- ✓ What exactly is failing

### Step 2: Send to Your Own Email First
1. Open http://localhost:9000
2. Upload your Excel file
3. Enter YOUR email address (not someone else's)
4. Click "Send Email"
5. Check your inbox (and spam folder)

If this works, the issue is with the recipient email, not your setup.

### Step 3: Check Gmail Security Settings
1. Go to https://myaccount.google.com/apppasswords
2. Verify you have a 16-character app password
3. Make sure 2FA is enabled: https://myaccount.google.com/security

### Step 4: Try a Different Recipient
Try sending to:
- Another Gmail address (test@gmail.com)
- Your personal email
- Your work email

This helps identify if the issue is with:
- Your SMTP setup (affects all emails)
- The recipient email server (only affects that specific email)

## Common Solutions

### "Authentication Failed"
```bash
# Update your .env file:
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=xxxx xxxx xxxx xxxx  # Remove the spaces!
```

**Important**: The app password from Gmail has spaces. Remove them all!

### "Recipient Email Rejected"
Try these:
1. Make sure the email address is spelled correctly
2. Try a public email like Gmail or Outlook
3. Check if your sending domain is on any blacklists

### "Connection Timeout"
```bash
# The SMTP server is slow or unreachable
# Solutions:
# 1. Check your internet connection
# 2. Try again in a few moments
# 3. Use a VPN if your network blocks SMTP port 587
```

### "Message Too Large"
The email is over the size limit:
1. Use a smaller logo image (compress it)
2. Try with fewer competitors in the Excel data
3. Check if the HTML is being bloated somehow

## Getting Help

### What to Check:
1. Run `python3 test_email.py` - saves diagnostic info
2. Check the app logs when you try to send
3. Look at the error message in the web UI

### Test Credentials Independently:
```python
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your-email@gmail.com', 'your-app-password')
# If this works without error, your credentials are correct!
```

### Email Forwarding Workaround:
If the recipient's email server is blocking your Gmail:
1. Forward the email from your account manually
2. OR change the SENDER_EMAIL to a corporate email if available

## Still Not Working?

1. **Take a screenshot** of the error message
2. **Note the recipient email** address
3. **Run test_email.py** and save output
4. Check if the problem is:
   - **All emails fail** → SMTP configuration issue
   - **Only specific email fails** → Recipient email server issue

## For Corporate/Exchange Emails

If `takshil@guestlove1.com` is a corporate email:
- It might be part of an Exchange server
- Try changing SMTP to Office 365 settings instead
- Use SMTP: smtp.office365.com, Port: 587

See EMAIL_SETUP.md for Office 365 configuration.
