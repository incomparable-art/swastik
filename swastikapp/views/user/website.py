import random
import time
from flask import render_template, request, flash, redirect, url_for, jsonify
from email.utils import formataddr
from flask_mail import Message
from swastikapp import mail
import os


# Format: { "email@example.com": {"otp": "123456", "expires_at": timestamp, "verified": False} }
otp_store = {}

# ----------------------------------------------------
# Endpoint 1: Send OTP
# ----------------------------------------------------
def send_otp():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    # Expiry: 5 minutes from now
    expires_at = time.time() + 300

    otp_store[email] = {
        'otp': otp,
        'expires_at': expires_at,
        'verified': False
    }

    # Send Email
    try:
        msg = Message(
            subject="Your Service Verification OTP",
            recipients=[email],
            body=f"Your OTP for verification is: {otp}\n\nThis OTP is valid for 5 minutes."
        )
        mail.send(msg)
        return jsonify({'message': 'OTP sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to send email: {str(e)}'}), 500

# ----------------------------------------------------
# Endpoint 2: Verify OTP
# ----------------------------------------------------
def verify_otp():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    user_otp = data.get('otp', '').strip()

    if not email or not user_otp:
        return jsonify({'error': 'Email and OTP are required'}), 400

    record = otp_store.get(email)

    if not record:
        return jsonify({'error': 'No OTP requested for this email'}), 400

    if time.time() > record['expires_at']:
        del otp_store[email]
        return jsonify({'error': 'OTP has expired. Please request a new one.'}), 400

    if record['otp'] == user_otp:
        record['verified'] = True
        return jsonify({'success': True, 'message': 'Email verified successfully'}), 200
    else:
        return jsonify({'error': 'Invalid OTP'}), 400

# ----------------------------------------------------
# Endpoint 3: Final Form Submission
# ----------------------------------------------------
def submit_service_request():
    # Read form data
    name = request.form.get('name')
    company = request.form.get('company')
    phone = request.form.get('phone')
    email = request.form.get('email', '').strip().lower()
    model = request.form.get('model')
    service = request.form.get('service')
    detail = request.form.get('detail')

    # Security check: verify if email was validated
    record = otp_store.get(email)
    if not record or not record.get('verified'):
        return jsonify({'error': 'Unauthorized: Email is not verified'}), 403

    # Clean up OTP record after successful submission
    del otp_store[email]

    html = render_template(
        "emails/service_request.html",
        name=name,
        company=company,
        phone=phone,
        email=email,
        model=model,
        service=service,
        detail=detail
    )
    service_team = os.getenv("SERVICE_TEAM")
    sales_team = os.getenv("SALES_TEAM")

    msg = Message(
        subject="🔧 New Service Request | Swastik Technology & Services",
        sender=formataddr(("Swastik Technology & Services", "247668.swastik@gmail.com")),
        recipients=[
            formataddr(("Service Team", service_team))
        ],
        cc=[
            formataddr(("Customer", email)),
            formataddr(("Sales Team", sales_team))
        ]
    )

    msg.html = html
    mail.send(msg)

    return jsonify({
        'status': 'success',
        'message': f'Service request submitted for {name} ({company})'
    }), 200


def index():
    return render_template('index.html')
