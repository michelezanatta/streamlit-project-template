import streamlit as st
import streamlit_authenticator as stauth
import sys
from pathlib import Path
import yaml
from yaml.loader import SafeLoader
import hmac

sys.path.append(str(Path(__file__).resolve().parent.parent))

from rsc.config import config_params

pages_dir = config_params.pages_dir

# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# # Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days']
# )




# def check_password():
#     """Returns `True` if the user had a correct password."""

#     def login_form():
#         """Form with widgets to collect user information"""
#         with st.form("Credentials"):
#             st.text_input("Username", key="username")
#             st.text_input("Password", type="password", key="password")
#             st.form_submit_button("Log in", on_click=password_entered)

#     def password_entered():
#         """Checks whether a password entered by the user is correct."""
#         if st.session_state["username"] in st.secrets[
#             "passwords"
#         ] and hmac.compare_digest(
#             st.session_state["password"],
#             st.secrets.passwords[st.session_state["username"]],
#         ):
#             st.session_state["password_correct"] = True
#             del st.session_state["password"]  # Don't store the username or password.
#             del st.session_state["username"]
#         else:
#             st.session_state["password_correct"] = False

#     # Return True if the username + password is validated.
#     if st.session_state.get("password_correct", False):
#         return True

#     # Show inputs for username + password.
#     login_form()
#     if "password_correct" in st.session_state:
#         st.error("😕 User not known or password incorrect")
#     return False


# if not check_password():
#     st.stop()

pages = {
    'Home' : [st.Page(f"{pages_dir}/home.py", title="Home", icon="🏠",)],
    'SimpleComponents' : [st.Page(f"{pages_dir}/text.py", title="Text", icon="📝"),
                        st.Page(f"{pages_dir}/input_widgets.py", title="Input Widgets", icon="🔢"),
                        st.Page(f"{pages_dir}/extras.py", title="Extras", icon="🎉")],
    'Media' : [st.Page(f"{pages_dir}/media.py", title="Media", icon="📺")],
    'Layouts' : [st.Page(f"{pages_dir}/layouts.py", title="Layouts", icon="📐")],
    'DataAnalysis' : [st.Page(f"{pages_dir}/plots.py", title="Plots", icon="📊"),
                    st.Page(f"{pages_dir}/dataframe.py", title="Data", icon="📈")],
    'Modeling' : [st.Page(f"{pages_dir}/model.py", title="Model", icon="🧠")],

}

pg = st.navigation(pages)
pg.run()


# try:
#     authenticator.login()
# except Exception as e:
#     st.error(e)

# authentication_status = st.session_state.get('authentication_status')
# name = st.session_state.get('name')


# if authentication_status:
#     authenticator.logout(location='sidebar')
#     pg.run()
# elif authentication_status is False:
#     st.error('Username/password is incorrect')
#     st.stop()
# elif authentication_status is None:
#     st.warning('Please enter your username and password')
#     st.stop()





