import random
import string
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
import hashlib
import json
import sqlite3

class OTPService:
    """OTP generation and verification service"""
    
    def __init__(self, db_path: str = 'otp_service.db'):
        self.db_path = db_path
        self.init_database()
        
        # OTP configuration
        self.otp_length = 6
        self.otp_expiry_minutes = 10
        self.max_attempts = 3
        self.cooldown_minutes = 15
    
    def init_database(self):
        """Initialize OTP database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS otp_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                identifier TEXT,
                identifier_type TEXT,
                otp_code TEXT,
                attempts INTEGER DEFAULT 0,
                created_at TEXT,
                expires_at TEXT,
                verified_at TEXT,
                status TEXT
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_otp_identifier ON otp_requests(identifier)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_otp_status ON otp_requests(status)')
        
        conn.commit()
        conn.close()
    
    def generate_otp(self) -> str:
        """Generate 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=self.otp_length))
    
    def send_otp(self, identifier: str, identifier_type: str = 'email') -> Dict:
        """Send OTP to email or phone"""
        
        # Check cooldown period
        if self._is_in_cooldown(identifier):
            return {
                'success': False,
                'message': f'Please wait {self.cooldown_minutes} minutes before requesting another OTP'
            }
        
        # Generate OTP
        otp_code = self.generate_otp()
        created_at = datetime.now()
        expires_at = created_at + timedelta(minutes=self.otp_expiry_minutes)
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Mark previous OTPs as expired
        cursor.execute('''
            UPDATE otp_requests SET status = 'EXPIRED'
            WHERE identifier = ? AND status = 'PENDING'
        ''', (identifier,))
        
        # Insert new OTP
        cursor.execute('''
            INSERT INTO otp_requests 
            (identifier, identifier_type, otp_code, attempts, created_at, expires_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (identifier, identifier_type, otp_code, 0, 
               created_at.isoformat(), expires_at.isoformat(), 'PENDING'))
        
        conn.commit()
        conn.close()
        
        # Send OTP (mock implementation)
        sent_successfully = self._mock_send_otp(identifier, identifier_type, otp_code)
        
        if sent_successfully:
            return {
                'success': True,
                'message': f'OTP sent to {identifier_type}',
                'expires_in': self.otp_expiry_minutes * 60,
                'demo_otp': otp_code  # For demo purposes
            }
        else:
            return {
                'success': False,
                'message': 'Failed to send OTP. Please try again.'
            }
    
    def verify_otp(self, identifier: str, otp_code: str) -> Dict:
        """Verify OTP code"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get latest pending OTP
        cursor.execute('''
            SELECT id, otp_code, attempts, expires_at, created_at
            FROM otp_requests
            WHERE identifier = ? AND status = 'PENDING'
            ORDER BY created_at DESC
            LIMIT 1
        ''', (identifier,))
        
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return {
                'success': False,
                'message': 'No pending OTP found. Please request a new OTP.'
            }
        
        otp_id, stored_otp, attempts, expires_at_str, created_at_str = row
        expires_at = datetime.fromisoformat(expires_at_str)
        
        # Check expiry
        if datetime.now() > expires_at:
            cursor.execute('UPDATE otp_requests SET status = "EXPIRED" WHERE id = ?', (otp_id,))
            conn.commit()
            conn.close()
            return {
                'success': False,
                'message': 'OTP has expired. Please request a new OTP.'
            }
        
        # Check attempts
        if attempts >= self.max_attempts:
            cursor.execute('UPDATE otp_requests SET status = "BLOCKED" WHERE id = ?', (otp_id,))
            conn.commit()
            conn.close()
            return {
                'success': False,
                'message': f'Maximum attempts reached. Please wait {self.cooldown_minutes} minutes.'
            }
        
        # Verify OTP
        if otp_code == stored_otp:
            # Mark as verified
            cursor.execute('''
                UPDATE otp_requests 
                SET status = 'VERIFIED', verified_at = ?
                WHERE id = ?
            ''', (datetime.now().isoformat(), otp_id))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'message': 'OTP verified successfully'
            }
        else:
            # Increment attempts
            cursor.execute('''
                UPDATE otp_requests 
                SET attempts = attempts + 1
                WHERE id = ?
            ''', (otp_id,))
            
            conn.commit()
            conn.close()
            
            remaining_attempts = self.max_attempts - (attempts + 1)
            return {
                'success': False,
                'message': f'Invalid OTP. {remaining_attempts} attempts remaining.'
            }
    
    def _is_in_cooldown(self, identifier: str) -> bool:
        """Check if identifier is in cooldown period"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check last failed attempt or blocked request
        cursor.execute('''
            SELECT created_at, status
            FROM otp_requests
            WHERE identifier = ? AND status IN ('BLOCKED', 'EXPIRED')
            ORDER BY created_at DESC
            LIMIT 1
        ''', (identifier,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return False
        
        last_attempt_str, status = row
        last_attempt = datetime.fromisoformat(last_attempt_str)
        cooldown_end = last_attempt + timedelta(minutes=self.cooldown_minutes)
        
        return datetime.now() < cooldown_end
    
    def _mock_send_otp(self, identifier: str, identifier_type: str, otp_code: str) -> bool:
        """Send OTP using real email service or mock SMS"""
        
        try:
            if identifier_type == 'email':
                # Use real email service
                from email_service import email_service
                result = email_service.send_otp_email(identifier, otp_code, "verification")
                print(f"📧 Email OTP sent to {identifier}: {otp_code}")
                return result['success']
            elif identifier_type == 'phone':
                # Mock SMS sending for now
                print(f"📱 SMS sent to {identifier}: Your TrustID OTP is {otp_code}")
                return True
            else:
                return False
        except Exception as e:
            print(f"❌ Failed to send OTP: {str(e)}")
            return False
    
    def get_otp_status(self, identifier: str) -> Dict:
        """Get OTP status for debugging"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT otp_code, attempts, created_at, expires_at, status, verified_at
            FROM otp_requests
            WHERE identifier = ?
            ORDER BY created_at DESC
            LIMIT 1
        ''', (identifier,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return {'status': 'No OTP requested'}
        
        otp_code, attempts, created_at_str, expires_at_str, status, verified_at_str = row
        
        return {
            'status': status,
            'attempts': attempts,
            'created_at': created_at_str,
            'expires_at': expires_at_str,
            'verified_at': verified_at_str,
            'demo_otp': otp_code if status == 'PENDING' else None
        }

# Global OTP service instance
otp_service = OTPService()
