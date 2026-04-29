from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_session import Session
import secrets
import json
import datetime
from functools import wraps
import hashlib
import uuid
import re
from mesh_network import mesh_network
from otp_service import otp_service

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Mock database
users_db = {}
kyc_data_db = {}
wallets_db = {}
sharing_logs_db = {}

# Mock user data
MOCK_USERS = {
    'demo@trustid.com': {
        'password': hashlib.sha256('demo123'.encode()).hexdigest(),
        'name': 'Demo User',
        'phone': '+91-9876543210',
        'has_completed_kyc': True,
        'wallet_passkey': '1234',
        'created_at': '2024-01-15'
    }
}

# Mock DigiLocker data
MOCK_DIGILOCKER_DATA = {
    'fullName': 'Arshad Khan',
    'dateOfBirth': '12/05/1992',
    'pan': 'ABCDE1234F',
    'aadhaar': 'XXXX XXXX 5678',
    'address': '123, Fintech Heights, Security Lane, New Delhi, 110001',
    'email': 'arshad.khan@example.com',
    'phone': '+91-9876543210'
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def kyc_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login'))
        user = users_db.get(session['user_email'], MOCK_USERS.get(session['user_email']))
        if not user or not user.get('has_completed_kyc', False):
            return redirect(url_for('digilocker_connect'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/create-account', methods=['POST'])
def create_account():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        terms_accepted = request.form.get('terms') == 'on'
        
        if not all([name, email, password]):
            flash('All fields are required', 'error')
            return redirect(url_for('signup'))
        
        if not terms_accepted:
            flash('You must accept the terms and conditions', 'error')
            return redirect(url_for('signup'))
        
        if email in users_db or email in MOCK_USERS:
            flash('Account already exists', 'error')
            return redirect(url_for('signup'))
        
        # Create user account
        users_db[email] = {
            'name': name,
            'email': email,
            'password': hashlib.sha256(password.encode()).hexdigest(),
            'has_completed_kyc': False,
            'created_at': datetime.datetime.now().isoformat()
        }
        
        session['user_email'] = email
        flash('Account created successfully! Starting KYC process...', 'success')
        return redirect(url_for('digilocker_connect'))
        
    except Exception as e:
        flash('Account creation failed', 'error')
        return redirect(url_for('signup'))

@app.route('/authenticate', methods=['POST'])
def authenticate():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required', 'error')
            return redirect(url_for('login'))
        
        # Check in mock users first, then in created users
        user = MOCK_USERS.get(email) or users_db.get(email)
        
        if not user:
            flash('No account found with this email address', 'error')
            return redirect(url_for('login'))
        
        if user['password'] != hashlib.sha256(password.encode()).hexdigest():
            flash('Invalid password', 'error')
            return redirect(url_for('login'))
        
        session['user_email'] = email
        
        if user.get('has_completed_kyc', False):
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('digilocker_connect'))
            
    except Exception as e:
        flash('Login failed', 'error')
        return redirect(url_for('login'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')
    
    try:
        identifier = request.form.get('identifier')
        
        if not identifier:
            flash('Email or phone number is required', 'error')
            return redirect(url_for('forgot_password'))
        
        # Determine identifier type
        identifier_type = 'email' if '@' in identifier else 'phone'
        
        # Check if user exists
        user_exists = identifier in users_db or identifier in MOCK_USERS
        
        if not user_exists:
            # Don't reveal if user exists or not
            flash('If the account exists, an OTP has been sent', 'info')
            return redirect(url_for('verify_forgot_password'))
        
        # Send OTP
        result = otp_service.send_otp(identifier, identifier_type)
        
        if result['success']:
            session['reset_identifier'] = identifier
            session['reset_identifier_type'] = identifier_type
            flash(f'Password reset code sent to {identifier}', 'success')
            return redirect(url_for('verify_forgot_password'))
        else:
            flash('Failed to send reset code. Please try again.', 'error')
            return redirect(url_for('forgot_password'))
            
    except Exception as e:
        flash('Failed to send OTP', 'error')
        return redirect(url_for('forgot_password'))

@app.route('/verify-forgot-password', methods=['GET', 'POST'])
def verify_forgot_password():
    if request.method == 'GET':
        return render_template('verify_forgot_password.html')
    
    try:
        identifier = session.get('reset_identifier')
        otp_code = request.form.get('otp')
        
        if not identifier or not otp_code:
            flash('OTP is required', 'error')
            return redirect(url_for('verify_forgot_password'))
        
        # Verify OTP
        result = otp_service.verify_otp(identifier, otp_code)
        
        if result['success']:
            session['otp_verified'] = True
            flash('OTP verified successfully', 'success')
            return redirect(url_for('reset_password'))
        else:
            flash(result['message'], 'error')
            return redirect(url_for('verify_forgot_password'))
            
    except Exception as e:
        flash('OTP verification failed', 'error')
        return redirect(url_for('verify_forgot_password'))

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if not session.get('otp_verified'):
        return redirect(url_for('forgot_password'))
    
    if request.method == 'GET':
        return render_template('reset_password.html')
    
    try:
        identifier = session.get('reset_identifier')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not new_password or not confirm_password:
            flash('All fields are required', 'error')
            return redirect(url_for('reset_password'))
        
        if new_password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('reset_password'))
        
        if len(new_password) < 8:
            flash('Password must be at least 8 characters', 'error')
            return redirect(url_for('reset_password'))
        
        # Update password
        if identifier in users_db:
            users_db[identifier]['password'] = hashlib.sha256(new_password.encode()).hexdigest()
        elif identifier in MOCK_USERS:
            MOCK_USERS[identifier]['password'] = hashlib.sha256(new_password.encode()).hexdigest()
        
        # Clear session
        session.pop('reset_identifier', None)
        session.pop('reset_identifier_type', None)
        session.pop('otp_verified', None)
        
        flash('Password reset successfully! Please log in.', 'success')
        return redirect(url_for('login'))
        
    except Exception as e:
        flash('Password reset failed', 'error')
        return redirect(url_for('reset_password'))

@app.route('/send-signup-otp', methods=['POST'])
def send_signup_otp():
    try:
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        if not email and not phone:
            return jsonify({'success': False, 'message': 'Email or phone is required'})
        
        # Send OTP to email
        if email:
            result = otp_service.send_otp(email, 'email')
            if not result['success']:
                return jsonify({'success': False, 'message': result['message']})
        
        # Send OTP to phone
        if phone:
            result = otp_service.send_otp(phone, 'phone')
            if not result['success']:
                return jsonify({'success': False, 'message': result['message']})
        
        return jsonify({
            'success': True, 
            'message': 'OTP sent successfully',
            'demo_otp': result.get('demo_otp')
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to send OTP'})

@app.route('/verify-signup-otp', methods=['POST'])
def verify_signup_otp():
    try:
        email = request.form.get('email')
        phone = request.form.get('phone')
        email_otp = request.form.get('email_otp')
        phone_otp = request.form.get('phone_otp')
        
        # Verify email OTP if provided
        if email and email_otp:
            result = otp_service.verify_otp(email, email_otp)
            if not result['success']:
                return jsonify({'success': False, 'message': f'Email OTP: {result["message"]}'})
        
        # Verify phone OTP if provided
        if phone and phone_otp:
            result = otp_service.verify_otp(phone, phone_otp)
            if not result['success']:
                return jsonify({'success': False, 'message': f'Phone OTP: {result["message"]}'})
        
        return jsonify({'success': True, 'message': 'OTP verified successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'OTP verification failed'})

@app.route('/digilocker-connect')
@login_required
def digilocker_connect():
    return render_template('digilocker_connect.html')

@app.route('/digilocker-verify', methods=['POST'])
@login_required
def digilocker_verify():
    try:
        phone = request.form.get('phone')
        otp = request.form.get('otp')
        
        if not phone or not otp:
            return jsonify({'success': False, 'message': 'Phone and OTP required'})
        
        # Mock OTP verification
        if otp == '123456':
            # Store DigiLocker data
            email = session['user_email']
            kyc_data_db[email] = {
                **MOCK_DIGILOCKER_DATA,
                'fetched_at': datetime.datetime.now().isoformat(),
                'phone': phone
            }
            
            return jsonify({'success': True, 'redirect': url_for('kyc_preview')})
        else:
            return jsonify({'success': False, 'message': 'Invalid OTP'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Verification failed'})

@app.route('/kyc-preview')
@login_required
def kyc_preview():
    email = session['user_email']
    kyc_data = kyc_data_db.get(email, MOCK_DIGILOCKER_DATA)
    return render_template('kyc_preview.html', kyc_data=kyc_data)

@app.route('/kyc-edit')
@login_required
def kyc_edit():
    email = session['user_email']
    kyc_data = kyc_data_db.get(email, MOCK_DIGILOCKER_DATA)
    return render_template('kyc_edit.html', kyc_data=kyc_data, original_data=MOCK_DIGILOCKER_DATA)

@app.route('/save-kyc-edits', methods=['POST'])
@login_required
def save_kyc_edits():
    try:
        email = session['user_email']
        
        edited_data = {
            'fullName': request.form.get('fullName'),
            'dateOfBirth': request.form.get('dateOfBirth'),
            'pan': request.form.get('pan'),
            'address': request.form.get('address')
        }
        
        # Calculate mismatches
        mismatches = []
        for field, value in edited_data.items():
            if value != MOCK_DIGILOCKER_DATA[field]:
                mismatches.append(field)
        
        # Update KYC data
        kyc_data_db[email] = {
            **kyc_data_db.get(email, MOCK_DIGILOCKER_DATA),
            **edited_data,
            'edited_at': datetime.datetime.now().isoformat(),
            'mismatches': mismatches
        }
        
        return jsonify({'success': True, 'redirect': url_for('kyc_preview')})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Save failed'})

@app.route('/video-kyc')
@login_required
def video_kyc():
    return render_template('video_kyc_enhanced.html')

@app.route('/process-video-kyc', methods=['POST'])
@login_required
def process_video_kyc():
    try:
        # Get verification data
        verification_data = json.loads(request.form.get('verification_data'))
        video_file = request.files.get('video')
        
        # Extract device fingerprint
        device_fingerprint = verification_data['deviceFingerprint']
        device_hash = hashlib.sha256(json.dumps(device_fingerprint, sort_keys=True).encode()).hexdigest()
        
        # Generate face hash (simplified - in production, use actual face embedding)
        face_hash = hashlib.sha256(f"face_{secrets.token_hex(16)}".encode()).hexdigest()
        
        # Get user data for hashing
        email = session.get('user_email')
        user_data = users_db.get(email, MOCK_USERS.get(email))
        kyc_data = kyc_data_db.get(email, MOCK_DIGILOCKER_DATA)
        
        # Generate hashes for cross-bank comparison
        pan_hash = hashlib.sha256(kyc_data.get('pan', '').encode()).hexdigest()
        aadhaar_hash = hashlib.sha256(kyc_data.get('aadhaar', '').encode()).hexdigest()
        email_hash = hashlib.sha256(email.encode()).hexdigest()
        phone_hash = hashlib.sha256(kyc_data.get('phone', '').encode()).hexdigest()
        
        # Perform mesh network precheck
        should_block, risk_analysis = mesh_network.precheck_session(
            bank_id='bank_a',  # Default bank for demo
            device_hash=device_hash,
            face_hash=face_hash,
            pan_hash=pan_hash,
            email_hash=email_hash,
            phone_hash=phone_hash
        )
        
        if should_block:
            # Block due to fraud detection
            session_id = mesh_network.create_session(
                bank_id='bank_a',
                user_id=email,
                device_hash=device_hash,
                face_hash=face_hash,
                pan_hash=pan_hash,
                aadhaar_hash=aadhaar_hash,
                email_hash=email_hash,
                phone_hash=phone_hash,
                risk_score=risk_analysis['risk_score'],
                decision='REJECTED'
            )
            
            return jsonify({
                'success': False,
                'message': f'Verification blocked: {risk_analysis["recommendation"]}',
                'risk_factors': risk_analysis['risk_factors'],
                'redirect': url_for('kyc_result')
            })
        
        # Calculate overall risk score
        liveness_score = verification_data.get('livenessScore', 0)
        deepfake_risk = verification_data.get('deepfakeRisk', 0.5)
        
        # Combined risk score (weighted)
        combined_risk = (deepfake_risk * 0.6) + ((1 - liveness_score) * 0.4) + (risk_analysis['risk_score'] * 0.2)
        
        # Make decision
        decision = 'APPROVED' if combined_risk < 0.7 else ('REJECTED' if combined_risk > 0.9 else 'MANUAL_REVIEW')
        
        # Create session in mesh network
        session_id = mesh_network.create_session(
            bank_id='bank_a',
            user_id=email,
            device_hash=device_hash,
            face_hash=face_hash,
            pan_hash=pan_hash,
            aadhaar_hash=aadhaar_hash,
            email_hash=email_hash,
            phone_hash=phone_hash,
            risk_score=combined_risk,
            decision=decision
        )
        
        # Store video KYC results
        if email not in kyc_data_db:
            kyc_data_db[email] = {}
        
        kyc_data_db[email]['video_kyc'] = {
            'session_id': session_id,
            'liveness_passed': liveness_score > 0.7,
            'deepfake_risk': verification_data.get('deepfakeLevel', 'Medium'),
            'deepfake_score': deepfake_risk,
            'device_hash': device_hash,
            'face_hash': face_hash,
            'risk_factors': risk_analysis.get('risk_factors', []),
            'processed_at': datetime.datetime.now().isoformat(),
            'decision': decision
        }
        
        # Issue verifiable credential if approved
        vc_id = None
        if decision == 'APPROVED':
            commitments = {
                'name_hash': hashlib.sha256(kyc_data.get('fullName', '').encode()).hexdigest(),
                'age_commitment': 'over_18',  # Simplified commitment
                'kyc_verified': 'true',
                'risk_score': str(combined_risk)
            }
            
            # Mock signature (in production, use actual Ed25519 signing)
            signature = f"sig_{secrets.token_hex(32)}"
            
            vc_id = mesh_network.issue_credential(
                issuer_id='bank_a',
                subject_id=email,
                commitments=commitments,
                signature=signature
            )
        
        return jsonify({
            'success': True,
            'liveness_passed': liveness_score > 0.7,
            'deepfake_risk': verification_data.get('deepfakeLevel', 'Medium'),
            'session_id': session_id,
            'vc_id': vc_id,
            'redirect': url_for('kyc_result')
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Video processing failed: {str(e)}'})

@app.route('/mesh-clusters')
@login_required
def mesh_clusters():
    """API endpoint to get fraud clusters for visualization"""
    try:
        clusters = mesh_network.get_fraud_clusters(limit=20)
        return jsonify({'success': True, 'clusters': clusters})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/audit-verify')
@login_required
def audit_verify():
    """API endpoint to verify audit trail integrity"""
    try:
        audit_result = mesh_network.verify_audit_trail()
        return jsonify({'success': True, 'audit': audit_result})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/kyc-result')
@login_required
def kyc_result():
    email = session['user_email']
    kyc_data = kyc_data_db.get(email, {})
    
    video_kyc = kyc_data.get('video_kyc', {})
    liveness_passed = video_kyc.get('liveness_passed', False)
    deepfake_risk = video_kyc.get('deepfake_risk', 'High')
    
    # Determine verification result
    verification_passed = liveness_passed and deepfake_risk in ['Low', 'Medium']
    
    return render_template('kyc_result.html', 
                         verification_passed=verification_passed,
                         liveness_passed=liveness_passed,
                         deepfake_risk=deepfake_risk)

@app.route('/set-wallet-passkey')
@login_required
def set_wallet_passkey():
    return render_template('set_passkey.html')

@app.route('/create-wallet', methods=['POST'])
@login_required
def create_wallet():
    try:
        passkey = request.form.get('passkey')
        
        if not passkey or len(passkey) != 4:
            flash('Please enter a 4-digit passkey', 'error')
            return redirect(url_for('set_passkey'))
        
        email = session['user_email']
        kyc_data = kyc_data_db.get(email, {})
        
        # Check if both processes are verified
        digilocker_verified = 'digiData' in kyc_data
        video_kyc_verified = kyc_data.get('video_kyc', {}).get('decision') == 'APPROVED'
        
        if not digilocker_verified or not video_kyc_verified:
            flash('Trust ID can only be created after both DigiLocker and Video KYC verification', 'error')
            return redirect(url_for('set_passkey'))
        
        # Generate unique Trust ID only after both verifications
        trust_id = f"TID-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        
        # Create wallet
        wallet_id = f"wallet_{uuid.uuid4().hex[:12]}"
        wallets_db[email] = {
            'wallet_id': wallet_id,
            'trust_id': trust_id,
            'passkey': hashlib.sha256(passkey.encode()).hexdigest(),
            'created_at': datetime.datetime.now().isoformat(),
            'status': 'locked',
            'credential_id': kyc_data.get('video_kyc', {}).get('vc_id'),
            'digilocker_verified': digilocker_verified,
            'video_kyc_verified': video_kyc_verified,
            'verification_date': datetime.datetime.now().isoformat()
        }
        
        # Update user KYC status
        if email in users_db:
            users_db[email]['has_completed_kyc'] = True
            users_db[email]['trust_id'] = trust_id
        else:
            MOCK_USERS[email]['has_completed_kyc'] = True
            MOCK_USERS[email]['trust_id'] = trust_id
        
        flash(f'Trust ID {trust_id} created successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        flash('Wallet creation failed', 'error')
        return redirect(url_for('set_passkey'))

@app.route('/dashboard')
@login_required
@kyc_required
def dashboard():
    email = session['user_email']
    user = users_db.get(email, MOCK_USERS.get(email))
    wallet = wallets_db.get(email, {})
    
    # Get recent activity
    recent_activity = sharing_logs_db.get(email, [])
    
    return render_template('dashboard.html', 
                         user=user, 
                         wallet=wallet,
                         recent_activity=recent_activity[:5])

@app.route('/unlock-wallet', methods=['POST'])
@login_required
@kyc_required
def unlock_wallet():
    try:
        passkey = request.form.get('passkey')
        email = session['user_email']
        
        user = users_db.get(email, MOCK_USERS.get(email))
        stored_passkey = user.get('wallet_passkey')
        
        if not stored_passkey or stored_passkey != hashlib.sha256(passkey.encode()).hexdigest():
            return jsonify({'success': False, 'message': 'Invalid passkey'})
        
        session['wallet_unlocked'] = True
        return jsonify({'success': True, 'redirect': url_for('wallet')})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Unlock failed'})

@app.route('/wallet')
@login_required
@kyc_required
def wallet():
    if not session.get('wallet_unlocked', False):
        return redirect(url_for('dashboard'))
    
    email = session['user_email']
    wallet_data = wallets_db.get(email, {})
    sharing_history = sharing_logs_db.get(email, [])
    
    return render_template('wallet.html', 
                         wallet=wallet_data,
                         sharing_history=sharing_history)

@app.route('/share-credential')
@login_required
@kyc_required
def share_credential():
    if not session.get('wallet_unlocked', False):
        return redirect(url_for('dashboard'))
    
    return render_template('share_select.html')

@app.route('/process-share', methods=['POST'])
@login_required
@kyc_required
def process_share():
    try:
        party = request.form.get('party')
        consent = request.form.get('consent') == 'on'
        
        if not consent:
            return jsonify({'success': False, 'message': 'Consent required'})
        
        email = session['user_email']
        
        # Log sharing
        if email not in sharing_logs_db:
            sharing_logs_db[email] = []
        
        sharing_logs_db[email].append({
            'party': party,
            'proof_id': f'ZK-{secrets.token_hex(12).upper()}',
            'timestamp': datetime.datetime.now().isoformat(),
            'status': 'shared'
        })
        
        return jsonify({
            'success': True,
            'proof_id': f'ZK-{secrets.token_hex(12).upper()}',
            'redirect': url_for('share_result', party=party)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Sharing failed'})

@app.route('/share-result')
@login_required
@kyc_required
def share_result():
    party = request.args.get('party', 'Unknown')
    return render_template('share_result.html', party=party)

@app.route('/revoke-credential', methods=['POST'])
@login_required
@kyc_required
def revoke_credential():
    try:
        email = session['user_email']
        
        # Update wallet status
        if email in wallets_db:
            wallets_db[email]['status'] = 'revoked'
            wallets_db[email]['revoked_at'] = datetime.datetime.now().isoformat()
        
        # Log revocation
        if email not in sharing_logs_db:
            sharing_logs_db[email] = []
        
        sharing_logs_db[email].append({
            'action': 'revoked',
            'timestamp': datetime.datetime.now().isoformat(),
            'status': 'revoked'
        })
        
        return jsonify({'success': True, 'message': 'Credential revoked'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Revocation failed'})

@app.route('/settings')
@login_required
@kyc_required
def settings():
    email = session['user_email']
    user = users_db.get(email, MOCK_USERS.get(email))
    return render_template('settings.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('landing'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
