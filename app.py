import streamlit as st
import smtplib
from email.mime.text import MIMEText
import random
import string
import time
from extract import query_data, DEFAULT_PROMPT_TEMPLATE

# Function to generate a random 6-digit code
def generate_code():
    return ''.join(random.choices(string.digits, k=6))

# Function to send email
def send_email(email, code):
    sender_email = "youngmetronome3x@gmail.com"  # Replace with your Gmail address
    sender_password = "dfegipozdoxfehod"  # Your app password

    msg = MIMEText(f"""
    This is a verification email for the Flex A.I. Wise at flex.com.

    Your verification code is: {code}

    If you did not request this code, please ignore this email.

    To ensure you receive future emails from us, please add {sender_email} to your contacts.
    """)
    msg['Subject'] = "Verification Code for Audit Answering App"
    msg['From'] = sender_email
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False


# Streamlit app
def main():
    st.title("Flex A.I. Wise")

    # Use session state to keep track of the user's progress
    if 'email_verified' not in st.session_state:
        st.session_state.email_verified = False
    if 'code_verified' not in st.session_state:
        st.session_state.code_verified = False

    # Email verification
    if not st.session_state.email_verified:
        st.header("Email Verification")
        email = st.text_input("Enter your email:")
        if st.button("Submit Email"):
            if email.endswith("@flex.com"):
                code = generate_code()
                if send_email(email, code):
                    st.session_state.verification_code = code
                    st.session_state.email_verified = True
                    st.success("Please check your email for the verification code.")
                else:
                    st.error("Error sending email. Please contact support.")
            else:
                st.error("I'm sorry, you are not part of this domain. Please enter a valid @flex.com email.")

    # Code verification
    elif not st.session_state.code_verified:
        st.header("Code Verification")
        input_code = st.text_input("Enter the verification code:")
        if st.button("Verify Code"):
            if input_code == st.session_state.verification_code:
                st.session_state.code_verified = True
                st.success("Code verified successfully!")
            else:
                st.error("Incorrect code. Please try again.")

    # Main app
    else:
        st.header("Ask Your Question")
        question = st.text_input("Enter your Question:")
        prompt_template = st.text_area("Edit Prompt Template:", value=DEFAULT_PROMPT_TEMPLATE, height=200)
        if st.button("Submit"):
            with st.spinner("Processing your query..."):
                start_time = time.time()
                output1, output2 = query_data(question, prompt_template)
                end_time = time.time()
                elapsed_time = end_time - start_time

            st.success(f"Query processed in {elapsed_time:.2f} seconds")
            st.text_area("Output using Open A.I.", value=output2, height=200)
            st.text_area("Raw Results from Database", value=output1, height=150)

if __name__ == "__main__":
    main()