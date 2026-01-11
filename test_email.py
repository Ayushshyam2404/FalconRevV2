#!/usr/bin/env python3
"""
Test SMTP configuration for Falcon Rev
Run this to diagnose email issues
"""

import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_smtp():
    load_dotenv()
    
    sender_email = os.getenv('SENDER_EMAIL', '').strip()
    sender_password = os.getenv('SENDER_PASSWORD', '').strip()
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com').strip()
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    
    print("=" * 60)
    print("FALCON REV - SMTP CONFIGURATION TEST")
    print("=" * 60)
    
    # Check configuration
    print("\n1. Configuration Check:")
    print(f"   Sender Email: {sender_email if sender_email else '❌ NOT SET'}")
    print(f"   Password: {'✓ Set' if sender_password else '❌ NOT SET'}")
    print(f"   SMTP Server: {smtp_server}")
    print(f"   SMTP Port: {smtp_port}")
    
    if not sender_email or not sender_password:
        print("\n❌ ERROR: Email credentials not configured!")
        print("   Please set SENDER_EMAIL and SENDER_PASSWORD in .env")
        return False
    
    # Test connection
    print("\n2. Connecting to SMTP Server...")
    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
            print("   ✓ Connected to SMTP server")
            
            server.starttls()
            print("   ✓ TLS encryption enabled")
            
            server.login(sender_email, sender_password)
            print("   ✓ Authentication successful!")
            
        print("\n✅ SUCCESS! SMTP configuration is correct.")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ AUTHENTICATION FAILED: {e}")
        print("\n   Solutions:")
        print("   1. For Gmail: Use an App Password (not your regular password)")
        print("   2. Enable 2FA on Gmail: https://myaccount.google.com/security")
        print("   3. Get App Password: https://myaccount.google.com/apppasswords")
        print("   4. Make sure password has no spaces (remove them!)")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"\n❌ CONNECTION FAILED: {e}")
        print("\n   Solutions:")
        print("   1. Check your internet connection")
        print("   2. Verify SMTP server address is correct")
        print("   3. Check if port 587 is open on your network")
        print("   4. Try using a VPN if your network blocks SMTP")
        return False
        
    except smtplib.SMTPTimeoutError as e:
        print(f"\n❌ CONNECTION TIMEOUT: {e}")
        print("\n   The server took too long to respond.")
        print("   Try again in a moment or check your connection.")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n   Unexpected error. Check your configuration.")
        return False

if __name__ == '__main__':
    success = test_smtp()
    exit(0 if success else 1)
