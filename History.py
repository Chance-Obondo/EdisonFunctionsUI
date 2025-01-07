import streamlit as st
import requests

#https://edison.bynarybots.co.ke  http://127.0.0.1:8000
backend_url = "https://edison.bynarybots.co.ke"
response = requests.get(url=f"{backend_url}/bots/{st.session_state.agent}/history",
                        headers={
                            "Authorization": f"bearer {st.session_state.access_token}"
                        })
fb_users = []
wa_users = []
web_users = []

for user in response.json()["response"]:
    if user["channel"] == "web":
        web_users.append(user)
    elif user["channel"] == "fb":
        fb_users.append(user)
    elif user["channel"] == "wa":
        wa_users.append(user)

print(f"number of fb users: {len(fb_users)}")
print(f"number of wa users: {len(wa_users)}")
print(f"number of web users: {len(web_users)}")


st.title("History :receipt:")
facebookMessenger, whatsappMessenger, webApplication = st.tabs(["Facebook Messenger", "Whatsapp Messenger", "Web application"])


@st.dialog("User chat history")
def view_user_history(user: dict):
    container = st.container(border=True)

    if "messages" in user:
        for message in user["messages"]:
            if "user" in message:
                st.markdown(f"""***User***: {message['user']}""")
            if "agent" in message:
                st.markdown(f"""***Agent***: {message['agent']}""")
            if "function_response" in message:
                st.markdown(f"""***Function response***: :red[{message['function_response']}]""")
            if "agent_response" in message:
                st.markdown(f"""***Agent***: {message['agent_response']}""")
            st.divider()
    else:
        st.text("No chats")


with facebookMessenger:
    container = st.container(border=True)
    for user in fb_users[::-1]:
        expander = container.expander(label=user["userChannelId"])
        expander.button(label="View history", key=user["userChannelId"], on_click=view_user_history,
                        kwargs={"user": user})

with whatsappMessenger:
    container = st.container(border=True)
    for user in wa_users[::-1]:
        expander = container.expander(label=user["userChannelId"])
        expander.button(label="View history", key=user["userChannelId"], on_click=view_user_history,
                        kwargs={"user": user})

with webApplication:
    container = webApplication.container(border=True)
    for user in web_users[::-1]:
        expander = container.expander(label=user["userChannelId"])
        expander.button(label="View history", key=user["userChannelId"], on_click=view_user_history,
                        kwargs={"user": user})



