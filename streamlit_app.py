import streamlit as st
import json
import requests
from datetime import datetime

def main():
    st.set_page_config(page_title="360° Feedback Form", layout="wide")
    
    st.title("360° Feedback Form for Riwaj")
    st.write("This form follows the GIVE feedback model (Growth-oriented, Immediate, Verified, Explicit)")
    
    # Anonymous feedback toggle
    is_anonymous = st.checkbox("Submit feedback anonymously")
    
    # Conditional display of personal information fields
    if not is_anonymous:
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
    else:
        name = "Anonymous"
        email = "Anonymous"
    
    # Relationship context
    relationship = st.selectbox(
        "What is your relationship with Riwaj?",
        ["Peer", "Manager", "Direct Report", "Cross-functional Colleague", "Other"]
    )
    
    # Core competencies evaluation
    st.header("Core Competencies")
    
    competencies = {
        "Leadership": "Ability to guide and influence others",
        "Communication": "Clarity and effectiveness in verbal and written communication",
        "Technical Skills": "Professional expertise and technical knowledge",
        "Collaboration": "Ability to work effectively with others",
        "Problem Solving": "Approach to analyzing and resolving challenges"
    }
    
    ratings = {}
    feedback = {}
    
    for comp, desc in competencies.items():
        st.subheader(comp)
        st.write(desc)
        
        ratings[comp] = st.slider(
            f"Rate {comp} (1-5)",
            1, 5, 3,
            help="1=Needs significant improvement, 5=Exceptional"
        )
        
        feedback[comp] = st.text_area(
            f"Please provide specific examples for {comp}",
            help="Use the STAR method (Situation, Task, Action, Result) for examples"
        )
    
    # Growth opportunities
    st.header("Growth and Development")
    growth = st.text_area(
        "What are the key areas where Riwaj could grow or improve?",
        help="Be specific and constructive"
    )
    
    # Strengths
    strengths = st.text_area(
        "What are Riwaj's key strengths?",
        help="Provide specific examples"
    )
    
    # Submit button
    if st.button("Submit Feedback"):
        # Prepare feedback data
        feedback_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "email": email,
            "relationship": relationship,
            "competency_ratings": ratings,
            "competency_feedback": feedback,
            "growth_opportunities": growth,
            "strengths": strengths
        }
        
        # Format email body
        email_body = f"""
New 360° Feedback Submission

From: {feedback_data['name']}
Email: {feedback_data['email']}
Relationship: {feedback_data['relationship']}

Competency Ratings:
{json.dumps(feedback_data['competency_ratings'], indent=2)}

Detailed Feedback:
{json.dumps(feedback_data['competency_feedback'], indent=2)}

Growth Opportunities:
{feedback_data['growth_opportunities']}

Key Strengths:
{feedback_data['strengths']}
        """
        
        # Send email using FormSubmit
        try:
            response = requests.post(
                "https://formsubmit.co/riwaj.sapkota@mailpit.net",
                data={
                    "name": feedback_data['name'],
                    "email": feedback_data['email'],
                    "message": email_body
                }
            )
            
            if response.status_code == 200:
                st.success("Thank you! Your feedback has been submitted successfully.")
            else:
                st.error("There was an error submitting your feedback. Please try again.")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
