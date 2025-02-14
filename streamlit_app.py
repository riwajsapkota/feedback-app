import streamlit as st
from datetime import datetime

def main():
    st.set_page_config(page_title="360° Feedback Form", layout="wide")
    
    st.title("360° Feedback Form for Riwaj")
    st.write("This form follows the GIVE feedback model (Growth-oriented, Immediate, Verified, Explicit)")
    
    # Create a form using st.form to batch all inputs
    with st.form("feedback_form"):
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

        # Hidden input for FormSubmit configuration
        st.markdown("""
        <form action="https://formsubmit.co/riwaj.sapkota@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="hidden" name="_template" value="table">
        </form>
        """, unsafe_allow_html=True)
        
        # Submit button
        submitted = st.form_submit_button("Submit Feedback")
        
        if submitted:
            # Create form data HTML
            form_html = f"""
                <form id="feedback_submit" action="https://formsubmit.co/riwaj.sapkota@mailpit.net" method="POST" style="display:none;">
                    <input type="hidden" name="Name" value="{name}">
                    <input type="hidden" name="Email" value="{email}">
                    <input type="hidden" name="Relationship" value="{relationship}">
                    <input type="hidden" name="Timestamp" value="{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}">
                    
                    {"".join([f'<input type="hidden" name="Rating_{comp}" value="{rating}">' for comp, rating in ratings.items()])}
                    {"".join([f'<input type="hidden" name="Feedback_{comp}" value="{feed}">' for comp, feed in feedback.items()])}
                    
                    <input type="hidden" name="Growth_Opportunities" value="{growth}">
                    <input type="hidden" name="Key_Strengths" value="{strengths}">
                    <input type="hidden" name="_captcha" value="false">
                    <input type="hidden" name="_template" value="table">
                </form>
                <script>
                    document.getElementById("feedback_submit").submit();
                </script>
            """
            
            st.markdown(form_html, unsafe_allow_html=True)
            st.success("Thank you! Your feedback has been submitted successfully.")

if __name__ == "__main__":
    main()
