import streamlit as st
import json
from datetime import datetime

# Page config
st.set_page_config(page_title="360° Feedback Form", layout="wide")

# Main app
st.title("360° Feedback Form")
st.write("Thank you for taking the time to provide feedback. Your input is valuable for personal and professional development.")

# Note about form submission
st.info("Note: Please use the 'Submit Feedback' button at the bottom to submit the form. Pressing Enter will only move to the next field.")

# Initialize session state for storing form data
if 'name' not in st.session_state:
    st.session_state.name = "Anonymous"
if 'email' not in st.session_state:
    st.session_state.email = "Anonymous"

# Create form using st.form to ensure single submission
with st.form("feedback_form", clear_on_submit=True):  # Added clear_on_submit=True to reset form after submission
    # Anonymous option
    is_anonymous = st.checkbox("Submit anonymously")

    # Conditionally render name and email fields
    if not is_anonymous:
        name = st.text_input("Your Name", key="name_input")
        email = st.text_input("Your Email", key="email_input")
        st.session_state.name = name
        st.session_state.email = email
    else:
        st.session_state.name = "Anonymous"
        st.session_state.email = "Anonymous"

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

    # Create hidden field for email
    st.markdown("""
    <form action="https://formsubmit.co/riwaj16@gmail.com" method="POST" id="feedback-form" style="display: none;">
        <input type="text" name="_honey" style="display:none">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="feedback_data" id="feedback-data">
    </form>
    """, unsafe_allow_html=True)

    # Submit button with clear label
    submitted = st.form_submit_button("Submit Feedback (Click here to submit)")
    
    if submitted:
        # Validate required fields when not anonymous
        if not is_anonymous and (not name.strip() or not email.strip()):
            st.error("Please fill in both name and email fields before submitting.")
        else:
            # Create feedback data dictionary
            feedback_data = {
                "Relationship": relationship,
                "Ratings": json.dumps(ratings),
                "Strengths": strengths,
                "Areas for Improvement": improvements,
                "Suggestions": suggestions,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Only add submitter info if not anonymous
            if not is_anonymous:
                feedback_data["Submitted By"] = f"Name: {st.session_state.name}, Email: {st.session_state.email}"
            else:
                feedback_data["Submitted By"] = "Anonymous"
            
            # Create JavaScript to submit the form
            js = f"""
            <script>
                var form = document.getElementById('feedback-form');
                document.getElementById('feedback-data').value = '{json.dumps(feedback_data)}';
                form.submit();
            </script>
            """
            st.markdown(js, unsafe_allow_html=True)
            st.success("Thank you! Your feedback has been submitted successfully.")

# Footer with privacy notice
st.markdown("---")
st.markdown("*Your feedback will be handled with confidentiality and used for developmental purposes only.*")
