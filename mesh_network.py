import hashlib
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import secrets
from dataclasses import dataclass, asdict
import sqlite3
import uuid

@dataclass
class Signal:
    """Fraud detection signal from a session"""
    session_id: str
    signal_type: str  # 'device', 'face', 'pan', 'aadhaar', 'email', 'phone'
    hash_value: str
    bank_id: str
    timestamp: datetime
    risk_score: float = 0.0

@dataclass
class Session:
    """KYC session with fraud analysis"""
    session_id: str
    bank_id: str
    user_id: str
    device_hash: str
    face_hash: str
    pan_hash: str
    aadhaar_hash: str
    email_hash: str
    phone_hash: str
    risk_score: float
    decision: str  # 'APPROVED', 'REJECTED', 'MANUAL_REVIEW'
    signals: List[Signal]
    created_at: datetime
    status: str = 'ACTIVE'  # 'ACTIVE', 'REVOKED'

@dataclass
class VerifiableCredential:
    """Verifiable Credential for reusable KYC"""
    vc_id: str
    issuer_id: str
    subject_id: str
    issuance_date: datetime
    expiry_date: datetime
    commitments: Dict[str, str]  # Hashed commitments
    signature: str
    status: str  # 'ACTIVE', 'REVOKED'
    revocation_reason: Optional[str] = None

class MeshNetwork:
    """Cross-bank fraud detection and credential management network"""
    
    def __init__(self, db_path: str = 'mesh_network.db'):
        self.db_path = db_path
        self.init_database()
        
        # Bank participants
        self.banks = {
            'bank_a': {'name': 'HDFC Bank', 'risk_threshold': 0.7},
            'bank_b': {'name': 'ICICI Bank', 'risk_threshold': 0.6},
            'bank_c': {'name': 'SBI Bank', 'risk_threshold': 0.8}
        }
        
        # Global fraud patterns
        self.fraud_patterns = {
            'same_device_multiple_identity': 0.9,
            'same_face_different_pan': 0.85,
            'cross_bank_fraud_history': 0.95,
            'virtual_camera_detected': 1.0,
            'emulator_detected': 1.0
        }
    
    def init_database(self):
        """Initialize SQLite database for mesh network"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                bank_id TEXT,
                user_id TEXT,
                device_hash TEXT,
                face_hash TEXT,
                pan_hash TEXT,
                aadhaar_hash TEXT,
                email_hash TEXT,
                phone_hash TEXT,
                risk_score REAL,
                decision TEXT,
                signals TEXT,
                created_at TEXT,
                status TEXT
            )
        ''')
        
        # Signals table for fast lookup
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                signal_type TEXT,
                hash_value TEXT,
                bank_id TEXT,
                timestamp TEXT,
                risk_score REAL
            )
        ''')
        
        # Verifiable credentials table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                vc_id TEXT PRIMARY KEY,
                issuer_id TEXT,
                subject_id TEXT,
                issuance_date TEXT,
                expiry_date TEXT,
                commitments TEXT,
                signature TEXT,
                status TEXT,
                revocation_reason TEXT
            )
        ''')
        
        # Audit trail
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_trail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_hash TEXT,
                record TEXT,
                prev_hash TEXT,
                timestamp TEXT,
                operation TEXT
            )
        ''')
        
        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_signals_hash ON signals(hash_value)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_signals_type ON signals(signal_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_device ON sessions(device_hash)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_face ON sessions(face_hash)')
        
        conn.commit()
        conn.close()
    
    def generate_device_hash(self, user_agent: str, screen_resolution: str, timezone: str) -> str:
        """Generate device fingerprint hash"""
        device_string = f"{user_agent}|{screen_resolution}|{timezone}"
        return hashlib.sha256(device_string.encode()).hexdigest()
    
    def generate_face_hash(self, face_embedding: List[float]) -> str:
        """Generate face hash from embedding"""
        face_string = json.dumps(face_embedding)
        return hashlib.sha256(face_string.encode()).hexdigest()
    
    def precheck_session(self, bank_id: str, device_hash: str, face_hash: str, 
                        pan_hash: str, email_hash: str, phone_hash: str) -> Tuple[bool, Dict]:
        """Precheck session against mesh network for fraud signals"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        risk_factors = []
        total_risk = 0.0
        
        # Check device hash across all banks
        cursor.execute('''
            SELECT session_id, bank_id, decision, created_at 
            FROM sessions 
            WHERE device_hash = ? AND status = 'ACTIVE'
        ''', (device_hash,))
        
        device_matches = cursor.fetchall()
        if device_matches:
            for session_id, other_bank, decision, created_at in device_matches:
                if other_bank != bank_id:
                    risk_factors.append({
                        'type': 'same_device_cross_bank',
                        'bank': other_bank,
                        'session_id': session_id,
                        'decision': decision,
                        'created_at': created_at,
                        'risk_score': self.fraud_patterns['same_device_multiple_identity']
                    })
                    total_risk += self.fraud_patterns['same_device_multiple_identity']
        
        # Check face hash across all banks
        cursor.execute('''
            SELECT session_id, bank_id, decision, created_at, pan_hash
            FROM sessions 
            WHERE face_hash = ? AND status = 'ACTIVE'
        ''', (face_hash,))
        
        face_matches = cursor.fetchall()
        if face_matches:
            for session_id, other_bank, decision, created_at, other_pan_hash in face_matches:
                if other_bank != bank_id and other_pan_hash != pan_hash:
                    risk_factors.append({
                        'type': 'same_face_different_pan',
                        'bank': other_bank,
                        'session_id': session_id,
                        'decision': decision,
                        'created_at': created_at,
                        'risk_score': self.fraud_patterns['same_face_different_pan']
                    })
                    total_risk += self.fraud_patterns['same_face_different_pan']
        
        # Check for fraud history
        cursor.execute('''
            SELECT session_id, bank_id, risk_score, decision
            FROM sessions 
            WHERE (device_hash = ? OR face_hash = ?) AND decision = 'REJECTED'
        ''', (device_hash, face_hash))
        
        fraud_history = cursor.fetchall()
        if fraud_history:
            for session_id, other_bank, risk_score, decision in fraud_history:
                risk_factors.append({
                    'type': 'cross_bank_fraud_history',
                    'bank': other_bank,
                    'session_id': session_id,
                    'previous_risk_score': risk_score,
                    'risk_score': self.fraud_patterns['cross_bank_fraud_history']
                })
                total_risk += self.fraud_patterns['cross_bank_fraud_history']
        
        conn.close()
        
        # Determine if session should be blocked
        bank_threshold = self.banks.get(bank_id, {}).get('risk_threshold', 0.7)
        should_block = total_risk >= bank_threshold
        
        return should_block, {
            'risk_score': min(total_risk, 1.0),
            'risk_factors': risk_factors,
            'threshold': bank_threshold,
            'recommendation': 'BLOCK' if should_block else 'PROCEED'
        }
    
    def create_session(self, bank_id: str, user_id: str, device_hash: str, 
                      face_hash: str, pan_hash: str, aadhaar_hash: str,
                      email_hash: str, phone_hash: str, risk_score: float,
                      decision: str) -> str:
        """Create new KYC session"""
        
        session_id = f"session_{uuid.uuid4().hex}"
        created_at = datetime.now()
        
        # Create signals
        signals = [
            Signal(session_id, 'device', device_hash, bank_id, created_at, risk_score),
            Signal(session_id, 'face', face_hash, bank_id, created_at, risk_score),
            Signal(session_id, 'pan', pan_hash, bank_id, created_at, risk_score),
            Signal(session_id, 'aadhaar', aadhaar_hash, bank_id, created_at, risk_score),
            Signal(session_id, 'email', email_hash, bank_id, created_at, risk_score),
            Signal(session_id, 'phone', phone_hash, bank_id, created_at, risk_score)
        ]
        
        session = Session(
            session_id=session_id,
            bank_id=bank_id,
            user_id=user_id,
            device_hash=device_hash,
            face_hash=face_hash,
            pan_hash=pan_hash,
            aadhaar_hash=aadhaar_hash,
            email_hash=email_hash,
            phone_hash=phone_hash,
            risk_score=risk_score,
            decision=decision,
            signals=signals,
            created_at=created_at
        )
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert session
        cursor.execute('''
            INSERT INTO sessions 
            (session_id, bank_id, user_id, device_hash, face_hash, pan_hash, 
             aadhaar_hash, email_hash, phone_hash, risk_score, decision, 
             signals, created_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session.session_id, session.bank_id, session.user_id,
            session.device_hash, session.face_hash, session.pan_hash,
            session.aadhaar_hash, session.email_hash, session.phone_hash,
            session.risk_score, session.decision, json.dumps([asdict(s) for s in signals]),
            session.created_at.isoformat(), session.status
        ))
        
        # Insert signals for fast lookup
        for signal in signals:
            cursor.execute('''
                INSERT INTO signals 
                (session_id, signal_type, hash_value, bank_id, timestamp, risk_score)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (signal.session_id, signal.signal_type, signal.hash_value,
                  signal.bank_id, signal.timestamp.isoformat(), signal.risk_score))
        
        # Add to audit trail
        self._add_audit_entry('CREATE_SESSION', asdict(session))
        
        conn.commit()
        conn.close()
        
        return session_id
    
    def issue_credential(self, issuer_id: str, subject_id: str, commitments: Dict[str, str],
                        signature: str) -> str:
        """Issue a verifiable credential"""
        
        vc_id = f"vc_{uuid.uuid4().hex}"
        issuance_date = datetime.now()
        expiry_date = issuance_date + timedelta(days=365)
        
        credential = VerifiableCredential(
            vc_id=vc_id,
            issuer_id=issuer_id,
            subject_id=subject_id,
            issuance_date=issuance_date,
            expiry_date=expiry_date,
            commitments=commitments,
            signature=signature,
            status='ACTIVE'
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO credentials 
            (vc_id, issuer_id, subject_id, issuance_date, expiry_date, 
             commitments, signature, status, revocation_reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            credential.vc_id, credential.issuer_id, credential.subject_id,
            credential.issuance_date.isoformat(), credential.expiry_date.isoformat(),
            json.dumps(commitments), signature, credential.status, None
        ))
        
        # Add to audit trail
        self._add_audit_entry('ISSUE_VC', asdict(credential))
        
        conn.commit()
        conn.close()
        
        return vc_id
    
    def revoke_credential(self, vc_id: str, reason: str) -> bool:
        """Revoke a verifiable credential"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE credentials SET status = 'REVOKED', revocation_reason = ?
            WHERE vc_id = ? AND status = 'ACTIVE'
        ''', (reason, vc_id))
        
        if cursor.rowcount > 0:
            self._add_audit_entry('REVOKE_VC', {'vc_id': vc_id, 'reason': reason})
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False
    
    def get_fraud_clusters(self, limit: int = 10) -> List[Dict]:
        """Get largest fraud clusters for visualization"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find sessions with matching signals
        cursor.execute('''
            SELECT s1.session_id, s1.bank_id, s1.device_hash, s1.face_hash, 
                   s1.risk_score, s1.decision, s1.created_at,
                   COUNT(s2.session_id) as matches
            FROM sessions s1
            JOIN sessions s2 ON (s1.device_hash = s2.device_hash OR 
                                s1.face_hash = s2.face_hash)
            WHERE s1.session_id != s2.session_id AND s1.status = 'ACTIVE'
            GROUP BY s1.session_id
            HAVING matches > 0
            ORDER BY matches DESC, s1.risk_score DESC
            LIMIT ?
        ''', (limit,))
        
        clusters = []
        for row in cursor.fetchall():
            clusters.append({
                'session_id': row[0],
                'bank_id': row[1],
                'device_hash': row[2],
                'face_hash': row[3],
                'risk_score': row[4],
                'decision': row[5],
                'created_at': row[6],
                'matches': row[7]
            })
        
        conn.close()
        return clusters
    
    def verify_audit_trail(self) -> Dict:
        """Verify audit trail integrity"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT entry_hash, record, prev_hash, timestamp, operation FROM audit_trail ORDER BY id')
        entries = cursor.fetchall()
        
        prev_hash = None
        tampered_at = None
        
        for i, (entry_hash, record, stored_prev_hash, timestamp, operation) in enumerate(entries):
            # Calculate expected hash
            expected_hash = hashlib.sha256(f"{record}{prev_hash or ''}".encode()).hexdigest()
            
            if entry_hash != expected_hash:
                tampered_at = i + 1
                break
            
            prev_hash = entry_hash
        
        conn.close()
        
        return {
            'verified': tampered_at is None,
            'total_entries': len(entries),
            'tampered_at': tampered_at,
            'last_hash': prev_hash
        }
    
    def _add_audit_entry(self, operation: str, record: Dict):
        """Add entry to audit trail"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get previous hash
        cursor.execute('SELECT entry_hash FROM audit_trail ORDER BY id DESC LIMIT 1')
        prev_row = cursor.fetchone()
        prev_hash = prev_row[0] if prev_row else None
        
        # Calculate new hash
        record_str = json.dumps(record, sort_keys=True, default=str)
        entry_hash = hashlib.sha256(f"{record_str}{prev_hash or ''}".encode()).hexdigest()
        
        cursor.execute('''
            INSERT INTO audit_trail (entry_hash, record, prev_hash, timestamp, operation)
            VALUES (?, ?, ?, ?, ?)
        ''', (entry_hash, record_str, prev_hash, datetime.now().isoformat(), operation))
        
        conn.commit()
        conn.close()

# Global mesh network instance
mesh_network = MeshNetwork()
