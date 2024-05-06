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
    duser = db.collection('users')
    check = duser.where('email', '==', email).limit(1).get()
    return len(check) == 1

# Function to check uniqueness of username
def unique_username(username):
    db = get_db()
    duser = db.collection('users')
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
def register():
    st.title("Hello, ")
    st.header("Register :")

    # Create a form for user signup
    with st.form("signup_form"):
        name = st.text_input("Enter your name")
        username = st.text_input("Enter username")
        email = st.text_input("Enter your email")
        qualification = st.text_input("Enter your qualification")
        mobile = st.number_input("Enter the Mobile number", step=1, format="%d")
        age = st.number_input("Enter your Age", step=1, format="%d")
        dob = st.date_input("Enter your Date of Birth", min_value=datetime(1900, 1, 1), max_value=datetime.now())
        occupation = st.text_input("Enter your Occupation")
        address = st.text_area("Enter your Address")
        
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if (len(username)==0) or (len(name)==0) or (len(email)==0) or (len(qualification)==0) or (len(occupation)==0) or (len(address)==0) or (number_length(age) == 0):
                st.warning('Fill all the fields', icon="⚠")
            elif number_length(mobile) != 10:
                st.warning('Invalid Mobile number', icon="⚠")
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
                users_data = {
                    "name": name,
                    "username": username,
                    "email": email,
                    "age": age,
                    "mobile" : mobile,
                    "dob": dob_firestore,
                    "occupation": occupation,
                    "qualification" : qualification,
                    "address": address
                }

                # Add user data to Firestore collection
                users_ref = db.collection('users')
                users_ref.document(username).set(users_data)

                st.success("Registration successfully!")

# Run the main Streamlit application
if __name__ == "__main__":
    register()
