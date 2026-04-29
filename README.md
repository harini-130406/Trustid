# 🏦 TrustID KYC System - Advanced Digital Identity Platform

## 🌟 Overview

TrustID is a comprehensive KYC (Know Your Customer) system that provides secure, reusable digital identity verification with advanced fraud detection capabilities. Built with Flask backend and modern frontend, it offers enterprise-grade security with cross-bank intelligence sharing.

## ✨ Key Features

### 🔐 Advanced Authentication
- **Secure signup/login** with email OTP verification
- **Forgot password** recovery system
- **Professional UI** with Material Design
- **Session management** and security

### 🎥 AI-Powered Video KYC
- **Real camera recording** with MediaRecorder API
- **Virtual camera detection** (blocks OBS, ManyCam, etc.)
- **Device fingerprinting** (WebGL, Canvas, Audio, Fonts)
- **Face detection** with real-time overlay
- **Liveness detection** (blink, head movement)
- **Deepfake analysis** with risk scoring
- **3 trial limit** with movement detection
- **Phone emulator detection**

### 🌐 Mesh Network Fraud Detection
- **Cross-bank fraud linkage** detection
- **Device and face hash tracking** across institutions
- **Risk scoring engine** with multiple factors
- **Fraud cluster visualization**
- **Real-time precheck** before KYC starts

### 🏦 Verifiable Credentials
- **VC issuance** upon successful KYC
- **Hash-based commitments** for privacy
- **Digital signatures** (Ed25519 compatible)
- **Revocation system** with mesh propagation

### 🔍 Audit Trail System
- **Immutable audit chain** with hash linking
- **Tamper detection** and verification
- **Complete operation logging**

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (for frontend development)
- Gmail account for email service

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/harini-130406/fintech.git
cd fintech/trustid-kyc
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure email service**
   - Update `email_service.py` with your Gmail credentials
   - Enable 2FA and generate app password

4. **Run the application**
```bash
python app.py
```

5. **Access the application**
   - Open `http://localhost:5000` in your browser
   - Use demo account: `demo@trustid.com` / `demo123`

## 📱 Demo Flow

### 1. Create Account
- Professional signup with enhanced UI
- Email OTP verification
- Phone number (10-digit) support

### 2. Complete KYC
- **DigiLocker Integration**: OTP `123456`
- **Document Review**: Editable with mismatch detection
- **Video KYC**: Real camera with fraud detection
- **Trust ID Creation**: Unique ID after verification

### 3. Dashboard Access
- Trust ID display
- Activity tracking
- Wallet management
- Cross-bank status

## 🛡️ Security Features

### Multi-Layer Fraud Detection
1. **Device Level**: Virtual camera, emulator detection
2. **Network Level**: Cross-bank fraud pattern matching
3. **Biometric Level**: Liveness, deepfake detection
4. **Document Level**: DigiLocker data verification

### Cross-Bank Intelligence
- **Same device + different identity** → BLOCK
- **Same face + different PAN** → HIGH RISK
- **Previous fraud history** → INSTANT REJECTION
- **Risk score propagation** across network

### Privacy-Preserving Verification
- **Selective disclosure** commitments
- **Zero-knowledge proofs** (simulated)
- **Hash-based comparisons** only
- **No raw data sharing**

## 🏗️ Architecture

### Backend Components
- **Flask** web framework with session management
- **SQLite** databases for mesh network, OTP, audit
- **Mesh Network** class for fraud detection
- **OTP Service** for secure verification
- **Email Service** for real email delivery
- **Device Fingerprinting** for unique identification

### Frontend Components
- **Camera API** integration with MediaRecorder
- **Real-time face detection** overlay
- **Device fingerprint** collection
- **Enhanced UI** with Tailwind CSS
- **Responsive design** patterns

### Database Schema
- **Users**: Authentication and profile data
- **KYC Data**: Verification results and documents
- **Wallets**: Trust ID and credential storage
- **Mesh Network**: Cross-bank fraud signals
- **Audit Trail**: Immutable operation logs

## 📊 API Endpoints

### Authentication
- `POST /create-account` - User registration
- `POST /authenticate` - User login
- `POST /forgot-password` - Password reset

### KYC Process
- `POST /digilocker-verify` - DigiLocker integration
- `POST /save-kyc-data` - Save KYC information
- `POST /process-video-kyc` - Video verification

### Advanced Features
- `GET /mesh-clusters` - Fraud cluster visualization
- `GET /audit-verify` - Audit trail verification
- `POST /unlock-wallet` - Wallet access

## 🔧 Configuration

### Email Service Setup
```python
# email_service.py
self.sender_email = "your-email@gmail.com"
self.sender_password = "your-app-password"
```

### Flask Configuration
```python
# app.py
app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
```

## 🎯 Use Cases

### Banking & Finance
- Customer onboarding
- Account opening
- Loan applications
- Compliance verification

### Fintech Applications
- Digital wallet creation
- Payment processing
- Investment platforms
- Insurance underwriting

### Enterprise Solutions
- Employee verification
- Partner onboarding
- Access control
- Identity management

## 🔒 Security Considerations

### Production Deployment
- Use environment variables for secrets
- Enable HTTPS with SSL certificates
- Implement rate limiting
- Set up monitoring and logging
- Regular security audits

### Compliance
- GDPR compliant data handling
- Privacy-preserving verification
- Audit trail maintenance
- Data retention policies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Email: proconnect795@gmail.com
- Documentation: See inline code comments

## 🌟 Acknowledgments

- Flask web framework
- Tailwind CSS for styling
- Material Design icons
- OpenCV for face detection
- WebRTC for camera access

---

**🏦 TrustID - The Future of Digital Identity Verification**

Built with ❤️ for secure, reusable, and privacy-preserving identity verification.
