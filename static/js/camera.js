// Camera and Video KYC functionality
class CameraKYC {
    constructor() {
        this.stream = null;
        this.mediaRecorder = null;
        this.recordedChunks = [];
        this.isRecording = false;
        this.constraints = {
            video: {
                width: { ideal: 1280 },
                height: { ideal: 720 },
                facingMode: 'user'
            },
            audio: false
        };
    }

    async startCamera(videoElement) {
        try {
            // Check for virtual cameras
            const devices = await navigator.mediaDevices.enumerateDevices();
            const videoDevices = devices.filter(device => device.kind === 'videoinput');
            
            // Detect virtual cameras (common patterns)
            const virtualCameras = videoDevices.filter(device => 
                device.label.toLowerCase().includes('virtual') ||
                device.label.toLowerCase().includes('obs') ||
                device.label.toLowerCase().includes('manyCam') ||
                device.label.toLowerCase().includes('splitCam') ||
                device.label.toLowerCase().includes('youCam')
            );

            if (virtualCameras.length > 0) {
                throw new Error('Virtual camera detected. Please use a real camera for verification.');
            }

            // Check for headless/emulator environment
            if (!navigator.userAgent || navigator.userAgent.includes('Headless')) {
                throw new Error('Invalid browser environment detected.');
            }

            // Get camera stream
            this.stream = await navigator.mediaDevices.getUserMedia(this.constraints);
            videoElement.srcObject = this.stream;
            
            return true;
        } catch (error) {
            console.error('Camera access error:', error);
            throw error;
        }
    }

    async startRecording(videoElement, maxDuration = 30000) {
        if (!this.stream) {
            throw new Error('Camera not started');
        }

        try {
            this.recordedChunks = [];
            this.isRecording = true;

            // Create MediaRecorder
            this.mediaRecorder = new MediaRecorder(this.stream, {
                mimeType: 'video/webm;codecs=vp8,opus'
            });

            // Handle data available
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.recordedChunks.push(event.data);
                }
            };

            // Handle recording stop
            this.mediaRecorder.onstop = () => {
                this.isRecording = false;
            };

            // Start recording
            this.mediaRecorder.start(1000); // Collect data every second

            // Auto-stop after max duration
            setTimeout(() => {
                if (this.isRecording) {
                    this.stopRecording();
                }
            }, maxDuration);

            return true;
        } catch (error) {
            console.error('Recording error:', error);
            throw error;
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
        }
    }

    getRecordedBlob() {
        return new Blob(this.recordedChunks, { type: 'video/webm' });
    }

    async getVideoFrame(videoElement) {
        const canvas = document.createElement('canvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoElement, 0, 0);
        
        return canvas.toDataURL('image/jpeg', 0.8);
    }

    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
    }

    // Face detection (simplified)
    async detectFace(videoElement) {
        // This is a simplified face detection
        // In production, you'd use a proper face detection library
        const frame = await this.getVideoFrame(videoElement);
        
        // Simulate face detection with random confidence
        const confidence = Math.random() * 0.3 + 0.7; // 0.7-1.0
        
        return {
            detected: confidence > 0.8,
            confidence: confidence,
            bbox: null // Would contain face bounding box in real implementation
        };
    }

    // Liveness detection
    async detectLiveness(videoElement, instructions) {
        const results = {
            blink: false,
            headMovement: false,
            overallScore: 0
        };

        // Simulate liveness detection based on instructions
        for (const instruction of instructions) {
            await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2 seconds per step
            
            switch(instruction) {
                case 'blink':
                    results.blink = Math.random() > 0.2; // 80% success rate
                    break;
                case 'head_turn':
                    results.headMovement = Math.random() > 0.15; // 85% success rate
                    break;
            }
        }

        // Calculate overall score
        const passedTests = [results.blink, results.headMovement].filter(Boolean).length;
        results.overallScore = passedTests / 2;

        return results;
    }

    // Deepfake detection (simplified)
    async detectDeepfake(videoElement) {
        // This is a simplified deepfake detection
        // In production, you'd use ONNX models or TensorFlow.js
        
        const frame = await this.getVideoFrame(videoElement);
        
        // Simulate deepfake analysis
        const riskFactors = {
            eyeBlinkRate: Math.random() * 0.3 + 0.7, // Normal range
            headMovementConsistency: Math.random() * 0.2 + 0.8,
            facialSymmetry: Math.random() * 0.15 + 0.85,
            skinTextureAnalysis: Math.random() * 0.25 + 0.75
        };

        // Calculate overall risk score (lower is better)
        const riskScore = 1 - (Object.values(riskFactors).reduce((a, b) => a + b, 0) / Object.keys(riskFactors).length);
        
        let riskLevel = 'Low';
        if (riskScore > 0.7) riskLevel = 'High';
        else if (riskScore > 0.4) riskLevel = 'Medium';

        return {
            riskScore: riskScore,
            riskLevel: riskLevel,
            riskFactors: riskFactors,
            isDeepfake: riskScore > 0.7
        };
    }
}

// Device fingerprinting
class DeviceFingerprint {
    static async generate() {
        const fingerprint = {
            userAgent: navigator.userAgent,
            language: navigator.language,
            platform: navigator.platform,
            screenResolution: `${screen.width}x${screen.height}`,
            colorDepth: screen.colorDepth,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            sessionStorage: typeof sessionStorage !== 'undefined',
            localStorage: typeof localStorage !== 'undefined',
            indexedDb: typeof indexedDB !== 'undefined',
            webgl: this.getWebGLInfo(),
            canvas: this.getCanvasFingerprint(),
            audio: await this.getAudioFingerprint(),
            fonts: this.getFonts(),
            hardware: {
                    cores: navigator.hardwareConcurrency || 4,
                    memory: navigator.deviceMemory || 4,
                    connection: navigator.connection ? {
                        effectiveType: navigator.connection.effectiveType,
                        downlink: navigator.connection.downlink,
                        rtt: navigator.connection.rtt
                    } : null
            }
        };

        return fingerprint;
    }

    static getWebGLInfo() {
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            
            if (!gl) return null;

            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
            
            return {
                vendor: gl.getParameter(gl.VENDOR),
                renderer: gl.getParameter(gl.RENDERER),
                version: gl.getParameter(gl.VERSION),
                unmaskedVendor: debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : null,
                unmaskedRenderer: debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : null
            };
        } catch (e) {
            return null;
        }
    }

    static getCanvasFingerprint() {
        try {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // Draw specific pattern
            ctx.textBaseline = 'top';
            ctx.font = '14px Arial';
            ctx.fillStyle = '#f60';
            ctx.fillRect(125, 1, 62, 20);
            ctx.fillStyle = '#069';
            ctx.fillText('TrustID Canvas Fingerprint', 2, 15);
            ctx.fillStyle = 'rgba(102, 204, 0, 0.7)';
            ctx.fillText('TrustID Canvas Fingerprint', 4, 17);
            
            return canvas.toDataURL();
        } catch (e) {
            return null;
        }
    }

    static async getAudioFingerprint() {
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const analyser = audioContext.createAnalyser();
            const gainNode = audioContext.createGain();
            const scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1);

            gainNode.gain.value = 0;
            oscillator.connect(analyser);
            analyser.connect(scriptProcessor);
            scriptProcessor.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.start(0);
            
            return new Promise((resolve) => {
                scriptProcessor.onaudioprocess = function(event) {
                    const samples = event.outputBuffer.getChannelData(0);
                    let sum = 0;
                    for (let i = 0; i < samples.length; i++) {
                        sum += Math.abs(samples[i]);
                    }
                    
                    oscillator.stop();
                    audioContext.close();
                    resolve(sum.toString());
                };
            });
        } catch (e) {
            return null;
        }
    }

    static getFonts() {
        const baseFonts = ['monospace', 'sans-serif', 'serif'];
        const testFonts = [
            'Arial', 'Arial Black', 'Arial Narrow', 'Arial Rounded MT Bold',
            'Avant Garde', 'Calibri', 'Cambria', 'Candara', 'Comic Sans MS',
            'Consolas', 'Courier', 'Courier New', 'Georgia', 'Helvetica',
            'Impact', 'Lucida Console', 'Lucida Sans Unicode', 'Microsoft Sans Serif',
            'Palatino', 'Tahoma', 'Times', 'Times New Roman', 'Trebuchet MS',
            'Verdana'
        ];

        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const detectedFonts = [];

        testFonts.forEach(font => {
            baseFonts.forEach(baseFont => {
                ctx.font = `12px '${font}', ${baseFont}`;
                const width = ctx.measureText('mmmmmmmmmmlli').width;
                
                ctx.font = `12px '${baseFont}'`;
                const baseWidth = ctx.measureText('mmmmmmmmmmlli').width;
                
                if (width !== baseWidth) {
                    detectedFonts.push(font);
                }
            });
        });

        return detectedFonts;
    }
}

// Export for use in templates
window.CameraKYC = CameraKYC;
window.DeviceFingerprint = DeviceFingerprint;
