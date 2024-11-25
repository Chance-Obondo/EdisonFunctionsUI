import streamlit as st
import requests
import json

url = "https://edison.bynarybots.co.ke"

st.title("Edison Functions")

sign_in, sign_up = st.tabs(["Log In", "Sign Up"])


def log_in(email, password):
    from urllib.parse import urlencode

    print(email, password)
    form_data = urlencode({
        "username": email,
        "password": password
    })

    response = requests.post(
        url=f"{url}/token",
        data=form_data,
        headers={
            "accept": "application/json",
             "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    response_data = response.json()
    print(response_data)

    if "access_token" in response_data:
        st.session_state.logged_in = True
        st.session_state.access_token = response_data["access_token"]
        print(st.session_state.access_token)
    else:
        st.header("Invalid Credentials")
    return "authentication data"


with sign_in:
    container = st.container(border=True)
    st.session_state.email = container.text_input(label="Email", key="login_email")
    st.session_state.password = container.text_input(label="Password", key="login_password")
    print(st.session_state.email, st.session_state.password)

    container.button(label="Log In", on_click=log_in, args=(st.session_state.email, st.session_state.password, ))


def register_user(email: str, password: str):
    body = {"email": email, "password": password}
    response = requests.post(url=f"{url}/users",
                             data=json.dumps(body))
    response_body = response.json()

    if response_body["response"] == "1":
        log_in(email=email, password=password)
    else:
        st.info("❌ Error occurred")


with sign_up:

    container = st.container(border=True)
    st.session_state.email = container.text_input(label="Email", key="signup_email")
    st.session_state.password = container.text_input(label="Password", key="signup_password")
    print(st.session_state.email, st.session_state.password)

    container.button(label="Sign Up", on_click=register_user, args=(st.session_state.email, st.session_state.password,))
