import streamlit as st
from streamlit_option_menu import option_menu

from admin_signin import admin_signin_page
from admin_login import adminpage
PAGES = {
    "Login": adminpage,
    "Sign Up": adminpage
}
st.set_page_config(layout="wide")

def main():
        # with st.sidebar:
            selected = option_menu(
                menu_title="Welcome !",  # required
                options=["Login", "Create Account",], 
                icons=["house", "envelope"],
                menu_icon="cast",  # optional
                default_index=0,  # optional
                orientation="horizontal",

            )
    
            if selected == "Login":
                adminpage()
                    
            if selected == "Create Account":
                admin_signin_page()
if __name__ == "__main__":
    main()
