import streamlit as st
import smtplib
from email.mime.text import MIMEText
import os
from datetime import datetime

# Page config
st.set_page_config(page_title="360° Feedback Form", layout="wide")

def send_email(feedback_data):
    # Note: You'll need to set these environment variables
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.environ.get('GMAIL_ADDRESS')
    sender_password = os.environ.get('GMAIL_APP_PASSWORD')
    receiver_email = "riwaj16@gmail.com"

    # Create message
    msg_body = "\n".join([f"{k}: {v}" for k, v in feedback_data.items()])
    msg = MIMEText(msg_body)
    msg['Subject'] = f"New 360° Feedback Received - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")
        return False

# Main app
st.title("360° Feedback Form")
st.write("Thank you for taking the time to provide feedback. Your input is valuable for personal and professional development.")

# Anonymous option
is_anonymous = st.checkbox("Submit anonymously")

if not is_anonymous:
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
else:
    name = "Anonymous"
    email = "Anonymous"

# Relationship context
relationship = st.selectbox(
    "What is your working relationship?",
    ["Manager", "Peer", "Direct Report", "Cross-functional Colleague", "Other"]
)

# Leadership competencies (based on research-backed frameworks)
st.subheader("Leadership Competencies")
st.write("Please rate the following competencies on a scale of 1-5:")

competencies = {
    "Strategic Thinking": "Ability to see the big picture and make sound decisions",
    "Communication": "Clarity, effectiveness, and frequency of communication",
    "Collaboration": "Working effectively with others and promoting teamwork",
    "Emotional Intelligence": "Self-awareness and ability to manage relationships",
    "Execution": "Getting things done and delivering results",
    "Innovation": "Promoting and implementing new ideas and solutions",
    "People Development": "Supporting growth and development of others"
}

ratings = {}
for comp, desc in competencies.items():
    st.write(f"**{comp}**: {desc}")
    ratings[comp] = st.slider(
        f"Rate {comp}",
        min_value=1,
        max_value=5,
        value=3,
        help="1 = Needs significant improvement, 5 = Exceptional"
    )

# Open-ended feedback
st.subheader("Detailed Feedback")
strengths = st.text_area("What are the person's greatest strengths?")
improvements = st.text_area("What are the areas for improvement?")
suggestions = st.text_area("What specific suggestions do you have for their development?")

# Submit button
if st.button("Submit Feedback"):
    feedback_data = {
        "Submitted By": f"Name: {name}, Email: {email}",
        "Relationship": relationship,
        "Ratings": ratings,
        "Strengths": strengths,
        "Areas for Improvement": improvements,
        "Suggestions": suggestions,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if send_email(feedback_data):
        st.success("Thank you! Your feedback has been submitted successfully.")
    else:
        st.error("There was an error submitting your feedback. Please try again later.")

# Footer with privacy notice
st.markdown("---")
st.markdown("*Your feedback will be handled with confidentiality and used for developmental purposes only.*")
