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


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# declare all pages and navigation
log_in = st.Page("log_in.py")
create_agent_page = st.Page("CreateAgent.py")

actions_page = st.Page("Actions.py", default=True, title="Actions", icon="🔧")
topics_page = st.Page("Topics.py", title="Topics", icon="📖")
integrations_page = st.Page("Integrations.py", icon="🔌")
history_page = st.Page("History.py", icon="🧾")
settings_page = st.Page("Settings.py", icon="⚙️")


# create an agent dialog box
@st.dialog("Create Agent")
def create_agent():
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


@st.dialog("Add system prompt")
def update_system_prompt():
    system_prompt = st.text_area(label="Please give your agent a system prompt. Also PRESS ENTER for the system prommpt to be picked")
    save_system_prompt = st.button(label="Save")
    if save_system_prompt == True:
        response = requests.put(url=f"http://127.0.0.1:8000/bots/{st.session_state.agent}?system_prompt={system_prompt}",
                                 headers={
                                       "Authorization": f"bearer {st.session_state.access_token}"
                                       })
        if response.json()["response"] == "1":
            st.success("✅ System prompt saved")
            st.rerun()
        else:
            st.error("❌ Error occurred")


# control site navigation for users
if st.session_state.logged_in == False:
    pg = st.navigation([log_in])

else:
    # get user chatbots
    response = requests.get(
        url=f"{url}/bots",
        headers={
            "Authorization": f"bearer {st.session_state.access_token}"
        }
    )
    response_data = response.json()
    bots = []

    if response_data["bot"] == []:
        print("changing navigation to create agent page")
        pg = st.navigation([create_agent_page])
    else:
        for bot in response_data["bot"]:
            bots.append(bot["name"])
        st.sidebar.title("Edison Functions")
        selected_bot = st.sidebar.selectbox(label=":robot_face: Agents", options=bots)

        # set the selected session bot
        for bot in response_data["bot"]:
            if bot["name"] == selected_bot:
                st.session_state.agent = bot["id"]
                if "system_prompt" not in bot:
                    update_system_prompt()

        st.sidebar.button(label="Create Agent", on_click=create_agent)
        pg = st.navigation([actions_page, topics_page, integrations_page, history_page, settings_page])

pg.run()
