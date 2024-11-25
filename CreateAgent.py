import streamlit as st
import requests
import json
import random
import string

url = "https://edison.bynarybots.co.ke"

# use this function to create random bot id
def generate_random_string(length):
    # Choose from all letters (upper & lowercase) and digits
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


agent_name = st.text_input(label="Agent Name")
bot_id = generate_random_string(10)
request_body = {
        "name": agent_name,
        "id": bot_id,
        "whatsappIntegration": False,
        "facebookIntegration": False,
        "toolsUse": True,
        "llm": "llama"
    }
create_agent_button = st.button(label="Create")
print(create_agent_button)

if create_agent_button == True:
    agent_creation_response = requests.post(url=f"{url}/bots",
                                                data=json.dumps(request_body),
                                                headers={
                                                    "Authorization": f"bearer {st.session_state.access_token}"
                                                })
    if agent_creation_response.json()["response"] == "1":
        tool_enable_body = {"bot_id": bot_id, "url": "http://127.0.0.1:8002", "auth_token": "", "tools": []}
        tool_enable_response = requests.post(url=f"{url}/tools/{bot_id}",
                                                    data=json.dumps(tool_enable_body),
                                                    headers={
                                                        "Authorization": f"bearer {st.session_state.access_token}"
                                                    })
        if tool_enable_response.json()["response"] == "1":
            st.success("✅ Operation Successful")
            st.rerun()
        else:
            st.error("❌ Error occurred enabling tools")
            st.rerun()

    elif agent_creation_response.json()["response"] == "0":
        st.error("❌ Error occurred")
    elif agent_creation_response.json()["response"] == "2":
        st.info("🤨 Agent already exists! ")
