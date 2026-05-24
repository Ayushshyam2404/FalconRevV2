from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import openpyxl
import os
from datetime import datetime
from utils.excel_processor import process_excel_file
from utils.email_generator import generate_email_html, convert_html_to_image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'), override=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['LOGO_FOLDER'] = 'uploads/logos'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# In-memory cache: stores the most recently processed Excel data
_latest_data = None

# Create folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['LOGO_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.svg')

@app.route('/uploads/logos/<filename>')
def serve_logo(filename):
    return send_from_directory(app.config['LOGO_FOLDER'], filename)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file format. Use Excel files'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the file
        data = process_excel_file(filepath)
        
        # Add our hotel's current day ADR for comparison
        if data['daily_data']:
            current_adr = data['daily_data'][0].get('adr', 0)
            data['our_adr'] = current_adr
        
        # Cache for /api/latest-data
        global _latest_data
        _latest_data = data
        
        return jsonify({
            'success': True,
            'data': data,
            'filename': filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-logo', methods=['POST'])
def upload_logo():
    if 'logo' not in request.files:
        return jsonify({'error': 'No logo file provided'}), 400
    
    file = request.files['logo']
    if file.filename == '':
        return jsonify({'error': 'No logo selected'}), 400
    
    if not allowed_image(file.filename):
        return jsonify({'error': 'Invalid image format. Use PNG, JPG, GIF, SVG, or WebP'}), 400
    
    try:
        import base64
        
        # Read file and convert to base64
        file.seek(0)
        file_data = file.read()
        logo_base64 = base64.b64encode(file_data).decode('utf-8')
        
        # Determine MIME type
        ext = file.filename.rsplit('.', 1)[1].lower()
        mime_types = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'svg': 'image/svg+xml',
            'webp': 'image/webp'
        }
        mime_type = mime_types.get(ext, 'image/png')
        
        # Create data URI
        data_uri = f"data:{mime_type};base64,{logo_base64}"
        
        return jsonify({
            'success': True,
            'logo_base64': data_uri,
            'filename': file.filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/latest-data', methods=['GET'])
def latest_data():
    """Return the most recently processed Excel data (for integration with external software)."""
    if _latest_data is None:
        return jsonify({'error': 'No data available. Upload an Excel file first.'}), 404
    return jsonify({'success': True, 'data': _latest_data})

@app.route('/api/send-email', methods=['POST'])
def send_email():
    try:
        payload = request.json
        recipient_email = payload.get('email')
        data = payload.get('data')
        subject = payload.get('subject', 'Falcon Rev - Revenue Report')
        logo_base64 = payload.get('logo_base64', '')
        
        if not recipient_email or not data:
            return jsonify({'error': 'Missing email or data'}), 400
        
        # Generate email HTML with base64 logo and chosen theme
        report_theme = payload.get('report_theme', 'dark')
        email_html = generate_email_html(data, logo_base64=logo_base64, theme=report_theme)
        
        # Send email
        send_smtp_email(
            recipient_email=recipient_email,
            subject=subject,
            html_content=email_html
        )
        
        return jsonify({'success': True, 'message': 'Email sent successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def send_smtp_email(recipient_email, subject, html_content):
    """Send email via IONOS SMTP with embedded report image"""
    smtp_host = os.getenv('SMTP_HOST', 'smtp.ionos.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    smtp_username = os.getenv('SMTP_USERNAME', '').strip()
    smtp_password = os.getenv('SMTP_PASSWORD', '').strip()
    sender_email = os.getenv('SENDER_EMAIL', smtp_username).strip()

    if not smtp_username or not smtp_password:
        raise Exception('SMTP credentials not configured in .env file (SMTP_USERNAME / SMTP_PASSWORD)')

    try:
        # Convert HTML to image
        email_image = convert_html_to_image(html_content)

        # Build the MIME message
        msg = MIMEMultipart('related')
        msg['Subject'] = subject
        msg['From'] = f'Falcon Rev <{sender_email}>'
        msg['To'] = recipient_email

        html_body = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: #f5f5f5; font-family: Arial, sans-serif;">
            <div style="max-width: 800px; margin: 0 auto;">
                <h2 style="color: #ff9500; margin-top: 0;">Falcon Rev - Revenue Report</h2>
                <p style="color: #666; margin-bottom: 20px; font-size: 14px;">
                    7 Day Forecast Analysis
                </p>
                <img src="cid:email_report" alt="Falcon Rev Report" style="width: 100%; max-width: 800px; border-radius: 8px; display: block;">
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, 'html'))

        # Attach the report image inline
        img_part = MIMEImage(email_image, _subtype='png')
        img_part.add_header('Content-ID', '<email_report>')
        img_part.add_header('Content-Disposition', 'inline', filename='falcon_rev_report.png')
        msg.attach(img_part)

        # Send via IONOS SMTP with STARTTLS
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        return True

    except smtplib.SMTPAuthenticationError:
        raise Exception('SMTP authentication failed — check SMTP_USERNAME and SMTP_PASSWORD in .env')
    except smtplib.SMTPException as e:
        raise Exception(f'SMTP error: {str(e)}')
    except Exception as e:
        raise Exception(f'Email sending failed: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True, port=3000)
