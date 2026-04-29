import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import ssl
from typing import Dict, Optional

class EmailService:
    """Email service for sending OTP and notifications"""
    
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "proconnect795@gmail.com"
        self.sender_password = "your-app-password"  # Use app password for Gmail
        
    def send_otp_email(self, recipient_email: str, otp_code: str, purpose: str = "verification") -> Dict:
        """Send OTP email to user"""
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"TrustID - Your {purpose.title()} Code"
            message["From"] = f"TrustID <{self.sender_email}>"
            message["To"] = recipient_email
            
            # HTML email template
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>TrustID Verification Code</title>
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #f8f9fa;
                    }}
                    .container {{
                        background: white;
                        border-radius: 12px;
                        padding: 40px;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 30px;
                    }}
                    .logo {{
                        width: 60px;
                        height: 60px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0 auto 20px;
                    }}
                    .otp-code {{
                        font-size: 32px;
                        font-weight: bold;
                        color: #667eea;
                        letter-spacing: 8px;
                        text-align: center;
                        margin: 30px 0;
                        padding: 20px;
                        background: #f8f9ff;
                        border-radius: 8px;
                        border: 2px dashed #667eea;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #eee;
                        font-size: 12px;
                        color: #666;
                    }}
                    .security-note {{
                        background: #fff3cd;
                        border: 1px solid #ffeaa7;
                        border-radius: 6px;
                        padding: 15px;
                        margin: 20px 0;
                        font-size: 14px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="logo">
                            <span style="color: white; font-size: 24px;">T</span>
                        </div>
                        <h1>TrustID Verification</h1>
                        <p>Your secure digital identity platform</p>
                    </div>
                    
                    <p>Hello,</p>
                    <p>You requested a {purpose} code for your TrustID account. Use the code below to complete your verification:</p>
                    
                    <div class="otp-code">{otp_code}</div>
                    
                    <div class="security-note">
                        <strong>Security Notice:</strong><br>
                        • This code expires in 10 minutes<br>
                        • Never share this code with anyone<br>
                        • TrustID will never ask for your password via email
                    </div>
                    
                    <p>If you didn't request this code, please ignore this email or contact our support team.</p>
                    
                    <div class="footer">
                        <p>© 2024 TrustID. All rights reserved.</p>
                        <p>This is an automated message, please do not reply.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Attach HTML content
            message.attach(MIMEText(html_content, "html"))
            
            # Create secure SMTP connection
            context = ssl.create_default_context()
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            return {
                'success': True,
                'message': f'OTP sent to {recipient_email}',
                'otp': otp_code  # For demo purposes
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to send email: {str(e)}'
            }
    
    def send_password_reset_email(self, recipient_email: str, reset_link: str) -> Dict:
        """Send password reset email"""
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = "TrustID - Password Reset Request"
            message["From"] = f"TrustID <{self.sender_email}>"
            message["To"] = recipient_email
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>TrustID Password Reset</title>
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #f8f9fa;
                    }}
                    .container {{
                        background: white;
                        border-radius: 12px;
                        padding: 40px;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                    }}
                    .reset-button {{
                        display: inline-block;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 15px 30px;
                        text-decoration: none;
                        border-radius: 8px;
                        font-weight: bold;
                        margin: 20px 0;
                    }}
                    .security-note {{
                        background: #f8d7da;
                        border: 1px solid #f5c6cb;
                        border-radius: 6px;
                        padding: 15px;
                        margin: 20px 0;
                        font-size: 14px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>TrustID Password Reset</h1>
                    <p>You requested to reset your TrustID password. Click the button below to reset your password:</p>
                    
                    <div style="text-align: center;">
                        <a href="{reset_link}" class="reset-button">Reset Password</a>
                    </div>
                    
                    <div class="security-note">
                        <strong>Security Notice:</strong><br>
                        • This link expires in 1 hour<br>
                        • Never share this link with anyone<br>
                        • If you didn't request this reset, please contact support
                    </div>
                    
                    <p>If the button doesn't work, copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #667eea;">{reset_link}</p>
                </div>
            </body>
            </html>
            """
            
            message.attach(MIMEText(html_content, "html"))
            
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            return {'success': True, 'message': 'Password reset email sent'}
            
        except Exception as e:
            return {'success': False, 'message': f'Failed to send email: {str(e)}'}

# Global email service instance
email_service = EmailService()
