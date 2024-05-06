import streamlit as st
from google.cloud import firestore
from datetime import datetime

# Function to initialize Firestore client
def get_db():
    db = firestore.Client.from_service_account_json('key.json')
    return db

# Function to check uniqueness of email
def unique_email(email):
    db = get_db()
    duser = db.collection('admin')
    check = duser.where('email', '==', email).limit(1).get()
    return len(check) == 1

# Function to check uniqueness of username
def unique_username(username):
    db = get_db()
    duser = db.collection('admin')
    check = duser.where('username', '==', username).limit(1).get()
    return len(check) == 1
    
def number_length(num):
    if num == 0:
        return 1
    count = 0
    while num != 0:
        count += 1
        num //= 10
    return count

# Main Streamlit application
def admin_signin_page():
    st.title("Hello, ")
    st.header("Create Account:")

    # Create a form for user signup
    with st.form("signup_form"):
        name = st.text_input("Enter your name")
        username = st.text_input("Enter username")
        email = st.text_input("Enter your email")
        mobile = st.number_input("Enter your mobile number", step=1, format="%d")
        password = st.text_input("Enter the password", type='password')
        age = st.number_input("Enter your Age", step=1, format="%d")
        dob = st.date_input("Enter your Date of Birth", min_value=datetime(1900, 1, 1), max_value=datetime.now())
        occupation = st.text_input("Enter your Occupation")
        address = st.text_area("Enter your Address")
        
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if (len(username)==0) or (len(name)==0) or (len(email)==0) or (len(occupation)==0) or (len(address)==0) or (number_length(age) == 0):
                st.warning('Username must have a minimum of 6 characters', icon="⚠")
            elif len(password) < 6:
                st.warning('Password must have a minimum of 6 characters', icon="⚠")
            elif unique_username(username):
                st.warning('Username already exists', icon="⚠")
            elif unique_email(email):
                st.warning('Email already exists', icon="⚠")
            else:
                # Initialize Firestore client
                db = get_db()

                # Convert dob to Firestore datetime object
                dob_firestore = datetime.combine(dob, datetime.min.time())

                # Create a dictionary of user data
                admin_data = {
                    "name": name,
                    "username": username,
                    "email": email,
                    "mobile" : mobile,
                    "password": password,
                    "age": age,
                    "dob": dob_firestore,
                    "occupation": occupation,
                    "address": address
                }

                # Add user data to Firestore collection
                admin_ref = db.collection('admin')
                admin_ref.document(username).set(admin_data)

                st.success("Account created successfully!")

# Run the main Streamlit application
if __name__ == "__main__":
    admin_signin_page()
