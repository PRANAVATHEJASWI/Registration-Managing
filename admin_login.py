import streamlit as st
from google.cloud import firestore
import pandas as pd

# Function to initialize Firestore client
def get_db():
    db = firestore.Client.from_service_account_json('key.json')
    return db

def authenticate(username, password):
    db = get_db()
    auser = db.collection('admin')
    query = auser.where('username', '==', username).limit(1).get()
    if len(query) == 0:
        return False
    user_doc = query[0]
    user_data = user_doc.to_dict()
    return user_data.get('password') == password

# Function to fetch specific fields for all users from the Firestore collection
def get_all_users():
    db = get_db()
    users_ref = db.collection('users')
    all_users = users_ref.stream()
    users_data = []
    for user in all_users:
        user_data = user.to_dict()
        # Extracting only the required fields
        user_info = {
            "Username": user_data.get("username", ""),
            "Name": user_data.get("name", ""),
            "DOB": user_data.get("dob", "").date() if user_data.get("dob", "") else "",
            "Mobile": user_data.get("mobile", ""),
            "Occupation": user_data.get("occupation", ""),
            "Address": user_data.get("address", ""),
            "Age": user_data.get("age", ""),
            "qualification" : user_data.get("qualification", "")
        }
        users_data.append(user_info)
    return users_data

# Function to delete a user from the Firestore collection
def delete_user(username):
    db = get_db()
    users_ref = db.collection('users')
    users_query = users_ref.where('username', '==', username).stream()
    users_quer = users_ref.where('username', '==', username).limit(1).get()
    if len(users_quer) == 1:
        for user in users_query:
            user.reference.delete()
        st.success("User deleted successfully!")

    else:
        st.warning("User not found!")
    
# Function to update user data in the Firestore collection
def update_user(username, updated_data):
    db = get_db()
    users_ref = db.collection('users')
    users_query = users_ref.where('username', '==', username).limit(1).get()
    if len(users_query) == 1:
        user_doc = users_query[0]
        # Get the document ID (sub-collection name)
        doc_id = user_doc.id
        user_ref = user_doc.reference
        # Update only the specified fields
        for field, value in updated_data.items():
            user_ref.update({field: value})
        st.success("User updated successfully!")

    else:
        st.warning("User not found!")


# Main function for displaying all users and admin functionalities
def adminpage():
    if 'logged_in' not in st.session_state:
        st.title("Admin Login")
        st.header("Login")

        with st.form("login_form"):
            username = st.text_input("Enter your username")
            password = st.text_input("Enter the password", type='password')

            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if authenticate(username, password):
                    # Store logged-in user's information in session state
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.experimental_rerun()
                else:
                    st.warning("Incorrect username or password")
    else:
        st.title("Admin Panel")
        st.write("Welcome, ", st.session_state.username)

        # Functionality for displaying all users
        st.header("All Users")
        all_users = get_all_users()
        df = pd.DataFrame(all_users)
        st.write(df)

        # Functionality for deleting a user
        st.header("Delete User")
        delete_username = st.text_input("Enter the username to delete")
        if st.button("Delete"):
            delete_user(delete_username)
            st.experimental_rerun()

        # Functionality for editing a user
        st.header("Edit User")
        edit_username = st.text_input("Enter the username to edit")
        updated_data = {
                    "username": st.text_input("Enter new username"),
                    "mobile": st.text_input("Enter new mobile number"),
                    "occupation": st.text_input("Enter new occupation"),
                    "address": st.text_input("Enter new address"),
                    "age": st.number_input("Enter new age", step=1, format="%d"),
                    "qualification": st.text_input("Enter new qualification")
                }
        if st.button("Update"):
                    update_user(edit_username, updated_data)
                    st.experimental_rerun()

if __name__ == "__main__":
    adminpage()
