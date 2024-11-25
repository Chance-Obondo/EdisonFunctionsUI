import streamlit as st
import requests

st.title("Integrations :electric_plug:")

fb, whatsapp, instagram = st.columns(3, vertical_alignment="top")

url = "https://edison.bynarybots.co.ke"

def save_messenger_settings(verify_token: str, page_access_token: str):
    change_response = requests.post(url=f"{url}/integrations/fb/{st.session_state.agent}?verify_token={verify_token}&access_token={page_access_token}",
                                   headers={
                                       "Authorization": f"bearer {st.session_state.access_token}"
                                   })


@st.dialog(title="Facebook Messenger")
def edit_messenger():
    st.text("Callback Url")
    text_to_copy = f"{url}/bots/{st.session_state.agent}/integrations/fb/webhook"
    st.code(text_to_copy, language=None)
    st.divider()

    verify_token = st.text_input("Verify Token")
    page_access_token = st.text_input("Page Access Token")
    messenger_save_button = st.button(label="Save", key="save_messenger_integration", on_click=save_messenger_settings,
                                      args=(verify_token, page_access_token, ))

    if messenger_save_button == True:
        response = requests.get(url=f"{url}/integrations/fb/{st.session_state.agent}",
                                 headers={
                                    "Authorization": f"bearer {st.session_state.access_token}"
                                 })
        if response.json()["response"] == "True":
            st.success("✅ Facebook Messenger Enabled")
        else:
            st.error("❌ Error occurred")


with fb:
    container = st.container(border=True)
    container.image(image="facebook-messenger.png")
    container.text("Facebook Messenger")
    container.button(label="Edit", key="messenger", on_click=edit_messenger)


def save_whatsapp_settings(verify_token: str, page_access_token: str):
    change_response = requests.post(url=f"{url}/integrations/wa/{st.session_state.agent}?verify_token={verify_token}&access_token={page_access_token}",
                                   headers={
                                       "Authorization": f"bearer {st.session_state.access_token}"
                                   })


@st.dialog(title="WhatsApp")
def edit_whatsapp():
    st.text("Callback Url")
    text_to_copy = f"{url}/bots/{st.session_state.agent}/integrations/wa/webhook"
    st.code(text_to_copy, language=None)
    st.divider()

    verify_token = st.text_input("Verify Token")
    page_access_token = st.text_input("Page Access Token")
    wa_save_button = st.button(label="Save", key="wa_messenger_integration", on_click=save_whatsapp_settings,
                               args=(verify_token, page_access_token,))

    if wa_save_button == True:
        response = requests.get(url=f"{url}/integrations/wa/{st.session_state.agent}",
                                headers={
                                    "Authorization": f"bearer {st.session_state.access_token}"
                                })
        if response.json()["response"] == "True":
            st.success("✅ Whatsapp Enabled")
        else:
            st.error("❌ Error occurred")


with whatsapp:
    container = st.container(border=True)
    container.image(image="whatsapp.png")
    container.text("WhatsApp Messenger")
    container.button(label="Edit", key="whatsapp", on_click=edit_whatsapp)

