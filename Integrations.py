import streamlit as st
import requests
from chainlit_jwt import token_generator

st.title("Integrations :electric_plug:")
fb, whatsapp, website, webapp = st.columns(4, vertical_alignment="top")
url = "https://edison.bynarybots.co.ke"

# get bot data to use for generating access token for website integration
bot_info_response = requests.get(url=f"{url}/bots/{st.session_state.agent}",
                   headers={
                        "Authorization": f"bearer {st.session_state.access_token}"
                   })
bot = bot_info_response.json()["bot"]
print(bot)


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
    container.button(label="Deploy", key="messenger", on_click=edit_messenger)


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
    container.button(label="Deploy", key="whatsapp", on_click=edit_whatsapp)


@st.dialog(title="Website")
def website_dialog():
    st.text(" Paste the following script right above the end of your body tag. "
            "Add the access token provided right before the end of the script tag!")
    code = """
    <script src="https://edison.bynarybots.co.ke/chainlit/agent/copilot/index.js"></script>
    <script>
        window.addEventListener("chainlit-call-fn", (e) => {
            const { name, args, callback } = e.detail;
            callback("You sent: " + args.msg);
        });
    </script>
  <script>
    window.mountChainlitWidget({
      chainlitServer: "https://edison.bynarybots.co.ke/chainlit/agent",
      accessToken: "",
    });
  </script>
    """
    st.code(body=code, language="javascript")
    st.text("Access token")
    st.code(body=token_generator.create_jwt(identifier=st.session_state.agent, metadata={"name": bot["name"], "toolsUse": bot["toolsUse"], "llm": bot["llm"]}), language=None)


with website:
    container = st.container(border=True)
    container.image(image="edison_website.png")
    container.text("Website")
    container.button(label="Deploy", key="website", on_click=website_dialog)


@st.dialog(title="Web Application")
def webapp_dialog():
    st.markdown("Below is the link to your AI agent. "
                "The :red[username] and :red[password] is the name of your AI agent!")
    st.code(body=f"{url}/chainlit/agent", language=None)


with webapp:
    container = st.container(border=True)
    container.image(image="edison_webapp.gif")
    container.text("Web app")
    container.button(label="Deploy", key="webapp", on_click=webapp_dialog)

