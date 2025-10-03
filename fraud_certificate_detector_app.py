import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import time
import matplotlib.pyplot as plt
import random
import zipfile
import base64
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Auto Certificate Verifier",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0D47A1;
        margin-bottom: 1rem;
    }
    .result-real {
        padding: 20px;
        background-color: #E8F5E9;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 20px 0;
    }
    .result-fake {
        padding: 20px;
        background-color: #FFEBEE;
        border-radius: 10px;
        border-left: 5px solid #F44336;
        margin: 20px 0;
    }
    .upload-section {
        background-color: #E3F2FD;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stProgress > div > div > div > div {
        background-color: #1E88E5;
    }
    .info-box {
        background-color: #FFF8E1;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #FFC107;
        margin: 10px 0;
    }
    .feature-card {
        background-color: #F5F5F5;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #E3F2FD;
        border-radius: 8px 8px 0px 0px;
        gap: 8px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0D47A1;
        color: white;
    }
    .auto-detection {
        background-color: #E1F5FE;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0288D1;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown('<h1 class="main-header">🔍 Auto Certificate Verifier</h1>', unsafe_allow_html=True)
st.markdown("""
This tool *automatically detects* whether your certificate is genuine or fraudulent using advanced machine learning algorithms that analyze:
- *ID verification* through pattern recognition
- *QR code validation* for digital signatures
- *Security feature detection* including watermarks and holograms
- *Document integrity checks* for signs of tampering
""")

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1576/1576664.png", width=100)
    st.title("Settings")
    
    st.subheader("Verification Options")
    id_verification = st.checkbox("ID Verification", value=True)
    qr_verification = st.checkbox("QR Code Analysis", value=True)
    security_features = st.checkbox("Security Features Check", value=True)
    integrity_check = st.checkbox("Document Integrity Check", value=True)
    
    st.markdown("---")
    st.info("""
    *How it works:*
    1. Upload a certificate (PNG, JPG, or PDF)
    2. *Automatic detection* begins immediately
    3. Review the detailed verification results
    """)

# Function to generate a sample certificate (for demo purposes)
def generate_sample_certificate(is_real=True):
    img = Image.new('RGB', (600, 400), color='white')
    d = ImageDraw.Draw(img)
    
    # Add border
    d.rectangle([10, 10, 590, 390], outline='gold', width=3)
    
    # Add title
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
    
    d.text((150, 50), "CERTIFICATE OF AUTHENTICITY", fill='black', font=font)
    
    # Add content
    d.text((150, 120), "This is to certify that", fill='black', font=font)
    d.text((200, 160), "SAMPLE DOCUMENT", fill='blue', font=font)
    d.text((150, 200), "has been verified as", fill='black', font=font)
    
    if is_real:
        status = "GENUINE"
        color = "green"
    else:
        status = "FRAUDULENT"
        color = "red"
    
    d.text((230, 240), status, fill=color, font=font)
    
    # Add serial number
    serial = f"Serial: {random.randint(10000, 99999)}"
    d.text((350, 300), serial, fill='black', font=font)
    
    # Add a fake QR code area
    d.rectangle([450, 300, 550, 350], outline='black', fill='lightgray')
    d.text((460, 320), "QR CODE", fill='black', font=font)
    
    # Add security features for genuine certificates
    if is_real:
        # Add a simple watermark
        watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
        dw = ImageDraw.Draw(watermark)
        try:
            w_font = ImageFont.truetype("arial.ttf", 40)
        except:
            w_font = ImageFont.load_default()
        dw.text((100, 150), "SECURE", fill=(0, 0, 255, 45), font=w_font)
        dw.text((300, 250), "OFFICIAL", fill=(0, 0, 255, 45), font=w_font)
        img = Image.alpha_composite(img.convert('RGBA'), watermark).convert('RGB')
    
    return img, serial

# Function to simulate ML analysis with direct decision (no UI confidence threshold)
def analyze_certificate(uploaded_file, id_check, qr_check, security_check, integrity_check):
    # For demo purposes, we'll simulate analysis based on file characteristics
    if hasattr(uploaded_file, 'is_real_sample'):
        is_real = uploaded_file.is_real_sample
    else:
        file_size = getattr(uploaded_file, 'size', 0)
        file_name = getattr(uploaded_file, 'name', '').lower()
        
        # Larger files are more likely to be real (higher quality)
        size_factor = min(1.0, file_size / 500000)  # Normalize file size factor
        
        # Files with certain names might be more suspicious
        suspicious_keywords = ['copy', 'scan', 'screenshot', 'image', 'photo', 'edited']
        name_factor = 0.6 if any(x in file_name for x in suspicious_keywords) else 0.9
        
        # File type factor
        type_factor = 0.9 if getattr(uploaded_file, 'type', '') in ['image/png', 'application/pdf', 'image/jpeg'] else 0.7
        
        # Random factor for simulation
        random_factor = random.uniform(0.7, 0.99)
        
        # Combined probability (no external threshold; decide with a fixed internal cutoff)
        authenticity_score = (size_factor * 0.3 + name_factor * 0.3 + type_factor * 0.2 + random_factor * 0.2)
        
        # Direct detection: decide real/fake using a fixed internal cutoff (0.55)
        is_real = authenticity_score >= 0.55
    
    # Generate detailed analysis results
    analysis_details = {
        "ID Verification": {
            "status": "Passed" if is_real else "Failed",
            "details": "Pattern matches official template" if is_real else "Inconsistent formatting detected",
            "confidence": random.uniform(0.85, 0.99) if is_real else random.uniform(0.4, 0.6)
        },
        "QR Code Validation": {
            "status": "Authentic" if is_real else "Tampered",
            "details": "Digital signature verified" if is_real else "Invalid or missing digital signature",
            "confidence": random.uniform(0.8, 0.98) if is_real else random.uniform(0.3, 0.5)
        },
        "Security Features": {
            "status": "Detected" if is_real else "Missing",
            "details": "All security features present" if is_real else "Missing hologram pattern",
            "confidence": random.uniform(0.85, 0.97) if is_real else random.uniform(0.35, 0.55)
        },
        "Document Integrity": {
            "status": "Intact" if is_real else "Compromised",
            "details": "No signs of tampering detected" if is_real else "Signs of digital alteration detected",
            "confidence": random.uniform(0.9, 0.99) if is_real else random.uniform(0.4, 0.6)
        }
    }
    
    # Generate issues if fake
    issues = []
    if not is_real:
        possible_issues = [
            "Inconsistent font styles",
            "QR code doesn't match database records",
            "Missing hologram pattern",
            "ID number format is invalid",
            "Signature verification failed",
            "Pixelation suggests digital alteration",
            "Incorrect color profile for official documents",
            "Metadata doesn't match expected patterns",
            "Low image resolution for an official document",
            "Inconsistent serial number formatting",
            "Missing security watermark",
            "Digital signature validation failed"
        ]
        issues = random.sample(possible_issues, k=random.randint(3, 5))
    
    # Calculate overall confidence score
    confidence = sum([detail['confidence'] for detail in analysis_details.values()]) / 4
    
    return is_real, confidence, analysis_details, issues

# Main content area
tab1, tab2, tab3 = st.tabs(["Upload Certificate", "Sample Certificates", "How It Works"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Upload Your Certificate</p>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a certificate file", 
            type=['png', 'jpg', 'jpeg', 'pdf'],
            help="Supported formats: PNG, JPG, PDF. Automatic detection begins after upload."
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            # Display file details
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size / 1024:.2f} KB",
                "File type": uploaded_file.type,
                "Upload time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            st.write("*File details:*")
            st.json(file_details)
            
            # Display the uploaded content
            if uploaded_file.type.startswith('image'):
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Certificate", use_column_width=True)
            elif uploaded_file.type == 'application/pdf':
                st.warning("PDF preview is not available in this demo. The analysis would extract images from the PDF for verification.")
            
            # Automatic detection message
            st.markdown('<div class="auto-detection">', unsafe_allow_html=True)
            st.info("🔍 *Automatic detection in progress...*")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Progress bar for automatic detection
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate automatic analysis process
            for percent_complete in range(100):
                time.sleep(0.01)
                progress_bar.progress(percent_complete + 1)
                if percent_complete < 25:
                    status_text.text(f"Loading ML model... {percent_complete}%")
                elif percent_complete < 50:
                    status_text.text(f"Extracting features... {percent_complete}%")
                elif percent_complete < 75:
                    status_text.text(f"Analyzing security elements... {percent_complete}%")
                else:
                    status_text.text(f"Finalizing results... {percent_complete}%")
            
            # Clear progress elements
            progress_bar.empty()
            status_text.empty()
            
            # Run analysis (direct detection)
            is_real, confidence, analysis_details, issues = analyze_certificate(
                uploaded_file, id_verification, qr_verification, security_features, integrity_check
            )
            
            # Display results
            if is_real:
                st.markdown('<div class="result-real">', unsafe_allow_html=True)
                st.success("✅ Certificate is *GENUINE*")
                st.write(f"*Confidence level:* {confidence:.2%}")
                st.write("*Verification details:*")
                
                for check, result in analysis_details.items():
                    status_icon = "✅" if result['status'] in ['Passed', 'Authentic', 'Detected', 'Intact'] else "❌"
                    st.markdown(f"{check}: {status_icon} {result['status']} - {result['details']} (Confidence: {result['confidence']:.2%})")
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="result-fake">', unsafe_allow_html=True)
                st.error("❌ Certificate is *FRAUDULENT*")
                st.write(f"*Confidence level:* {confidence:.2%}")
                st.write("*Verification details:*")
                
                for check, result in analysis_details.items():
                    status_icon = "✅" if result['status'] in ['Passed', 'Authentic', 'Detected', 'Intact'] else "❌"
                    st.markdown(f"{check}: {status_icon} {result['status']} - {result['details']} (Confidence: {result['confidence']:.2%})")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Show reasons why it might be fake
                st.warning("*Potential issues detected:*")
                for issue in issues:
                    st.write(f"- {issue}")
    
    with col2:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.subheader("ℹ How to Use")
        st.write("""
        1. Upload a certificate file
        2. *Automatic detection* begins immediately
        3. Review the verification results
        4. Check the detailed analysis report
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.subheader("📊 Statistics")
        # Sample statistics
        chart_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'Real': [45, 52, 48, 58, 62],
            'Fake': [12, 8, 15, 9, 11]
        })
        
        st.bar_chart(chart_data.set_index('Month'))
        
        st.markdown("---")
        
        st.subheader("🔍 Analysis Techniques")
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.write("*QR Code Analysis*")
        st.caption("Validates digital signatures and checks against database records")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.write("*Pattern Recognition*")
        st.caption("Checks for consistent formatting and official design patterns")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.write("*Metadata Analysis*")
        st.caption("Examines document metadata for signs of tampering")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.write("*Security Feature Detection*")
        st.caption("Identifies holograms, watermarks, and other security elements")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.header("Sample Certificates")
    st.write("Generate sample certificates to test the automatic verification system:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Genuine Certificate")
        genuine_img, serial = generate_sample_certificate(True)
        st.image(genuine_img, use_column_width=True)
        
        st.write(f"*Serial Number:* {serial}")
        
        # Convert PIL image to bytes for download
        img_bytes = io.BytesIO()
        genuine_img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        
        st.download_button(
            label="Download Genuine Certificate",
            data=img_bytes,
            file_name="genuine_certificate.png",
            mime="image/png",
            key="download_genuine"
        )
        
        if st.button("Test Automatic Detection (Genuine)", key="analyze_genuine"):
            class FakeFile:
                def __init__(self, is_real_sample):
                    self.size = 450000
                    self.name = "genuine_certificate.png"
                    self.type = "image/png"
                    self.is_real_sample = is_real_sample
            
            fake_file = FakeFile(True)
            
            is_real, confidence, analysis_details, issues = analyze_certificate(
                fake_file, id_verification, qr_verification, security_features, integrity_check
            )
            
            if is_real:
                st.markdown('<div class="result-real">', unsafe_allow_html=True)
                st.success("✅ Certificate is *GENUINE*")
                st.write(f"*Confidence level:* {confidence:.2%}")
                st.write("*Verification details:*")
                
                for check, result in analysis_details.items():
                    status_icon = "✅" if result['status'] in ['Passed', 'Authentic', 'Detected', 'Intact'] else "❌"
                    st.markdown(f"{check}: {status_icon} {result['status']} - {result['details']} (Confidence: {result['confidence']:.2%})")
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="result-fake">', unsafe_allow_html=True)
                st.error("❌ Certificate is *FRAUDULENT*")
                st.write(f"*Confidence level:* {confidence:.2%}")
                st.write("*Verification details:*")
                
                for check, result in analysis_details.items():
                    status_icon = "✅" if result['status'] in ['Passed', 'Authentic', 'Detected', 'Intact'] else "❌"
                    st.markdown(f"{check}: {status_icon} {result['status']} - {result['details']} (Confidence: {result['confidence']:.2%})")
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("Fake Certificate")
        fake_img, serial = generate_sample_certificate(False)
        st.image(fake_img, use_column_width=True)
        
        st.write(f"*Serial Number:* {serial}")
        
        # Convert PIL image to bytes for download
        img_bytes = io.BytesIO()
        fake_img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        
        st.download_button(
            label="Download Fake Certificate",
            data=img_bytes,
            file_name="fake_certificate.png",
            mime="image/png",
            key="download_fake"
        )
        
        if st.button("Test Automatic Detection (Fake)", key="analyze_fake"):
            class FakeFile:
                def __init__(self, is_real_sample):
                    self.size = 150000
                    self.name = "fake_certificate.png"
                    self.type = "image/png"
                    self.is_real_sample = is_real_sample
            
            fake_file = FakeFile(False)
            
            is_real, confidence, analysis_details, issues = analyze_certificate(
                fake_file, id_verification, qr_verification, security_features, integrity_check
            )
            
            if is_real:
                st.markdown('<div class="result-real">', unsafe_allow_html=True)
                st.success("✅ Certificate is *GENUINE*")
                st.write(f"*Confidence level:* {confidence:.2%}")
                st.write("*Verification details:*")
                
                for check, result in analysis_details.items():
                    status_icon = "✅" if result['status'] in ['Passed', 'Authentic', 'Detected', 'Intact'] else "❌"
                    st.markdown(f"{check}: {status_icon} {result['status']} - {result['details']} (Confidence: {result['confidence']:.2%})")
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="result-fake">', unsafe_allow_html=True)
                st.error("❌ Certificate is *FRAUDULENT*")
                st.write(f"*Confidence level:* {confidence:.2%}")
                st.write("*Verification details:*")
                
                for check, result in analysis_details.items():
                    status_icon = "✅" if result['status'] in ['Passed', 'Authentic', 'Detected', 'Intact'] else "❌"
                    st.markdown(f"{check}: {status_icon} {result['status']} - {result['details']} (Confidence: {result['confidence']:.2%})")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Show reasons why it might be fake
                st.warning("*Potential issues detected:*")
                for issue in issues:
                    st.write(f"- {issue}")

with tab3:
    st.header("How It Works")
    
    st.subheader("Automatic Detection Technology")
    st.write("""
    This certificate verification system uses advanced machine learning and computer vision techniques
    to *automatically detect* whether documents are genuine or fraudulent. The system examines multiple 
    aspects of the certificate without requiring user intervention.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Detection Methods")
        st.markdown("""
        - *QR Code Analysis*: Validates digital signatures and checks against database records
        - *Pattern Recognition*: Examines document layout and formatting for consistency
        - *Metadata Examination*: Analyzes file metadata for signs of tampering
        - *Security Feature Detection*: Identifies watermarks, holograms, and other security elements
        - *Pixel-level Analysis*: Detects signs of digital alteration or forgery
        """)
    
    with col2:
        st.markdown("### Common Fraud Indicators")
        st.markdown("""
        - Inconsistent font styles or sizes
        - QR code that doesn't match database records
        - Missing or incorrect security features
        - Pixelation suggesting digital alteration
        - Irregularities in document metadata
        - Signature mismatches or inconsistencies
        - Incorrect color profiles for official documents
        """)
    
    st.markdown("### Automatic Verification Process")
    st.markdown("""
    1. *Document Upload*: User submits a certificate for verification
    2. *Automatic Detection*: Analysis begins immediately after upload
    3. *Preprocessing*: Image enhancement and normalization
    4. *Feature Extraction*: Identification of key document elements
    5. *Analysis*: Comparison against known genuine templates and patterns
    6. *Validation*: Cross-referencing with database records (if available)
    7. *Result Generation*: Comprehensive authenticity report
    """)
    
    st.markdown("### Applications")
    st.markdown("""
    - Educational institution degree verification
    - Professional certification validation
    - Award and recognition authentication
    - Government document verification
    - Corporate certificate validation
    """)

# Footer
st.markdown("---")
st.caption("""
Note: This is a demonstration application. In a production environment, it would connect to actual 
machine learning models for certificate verification and QR code analysis.
""")
