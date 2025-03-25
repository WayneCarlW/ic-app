from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Message
from extensions import mongo, mail

contact_bp = Blueprint('contact_bp', __name__, url_prefix='/contact')

@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not name or not email or not subject or not message:
            flash("All fields are required!", "danger")
            return redirect(url_for('contact_bp.contact'))

        
        contact_message = {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message
        }
        mongo.db.contact_messages.insert_one(contact_message)

        try:
            msg = Message(subject="Contact Form Submission",
                          sender=email,
                          recipients=["cwasonga@kabarak.ac.ke"])
            msg.body = f"New message from {name} ({email}):\n\n{message}"
            mail.send(msg)
        except Exception as e:
            print(f"Email error: {e}")

        flash("Message sent successfully! We'll get back to you soon.", "success")
        return redirect(url_for('contact_bp.contact'))

    return redirect(url_for('home') + '#contact-section')
