import streamlit as st
import requests
from typing import Union
st.title("Settings :gear:")

#https://edison.bynarybots.co.ke  http://127.0.0.1:8000
backend_url = "https://edison.bynarybots.co.ke"

agentSettings, toolsSettings = st.tabs(["Agent Settings", "Tools Settings"])
change_response = {}

response = requests.get(url=f"{backend_url}/tools/{st.session_state.agent}",
                        headers={
                            "Authorization": f"bearer {st.session_state.access_token}"
                        })
print(response.json())
response_body = response.json()

bot_info_response = requests.get(url=f"{backend_url}/bots/{st.session_state.agent}",
                        headers={
                            "Authorization": f"bearer {st.session_state.access_token}"
                        })
bot_info = bot_info_response.json()["bot"]

# get the bots tool status
bot_info_response = requests.get(
        url=f"{backend_url}/bots/{st.session_state.agent}",
        headers={
            "Authorization": f"bearer {st.session_state.access_token}"
        }
    )
tools_status = bot_info_response.json()["bot"]["toolsUse"]
if tools_status == "True":
    st.session_state.tools_status = True
else:
    st.session_state.tools_status = False


# function to edit bot
def edit_agent(bot_id: str, name: Union[str, None] = None, system_prompt: Union[str, None] = None, url: Union[str, None] = None, auth: Union[str, None] = None, toolsUse: Union[str, None] = None):

    if name != None:
        change_response = requests.put(url=f"{backend_url}/bots/{bot_id}?name={name}",
                                       headers={
                                           "Authorization": f"bearer {st.session_state.access_token}"
                                       })

    elif system_prompt != None:
        change_response = requests.put(
            url=f"{backend_url}/bots/{st.session_state.agent}?system_prompt={system_prompt}",
            headers={
                "Authorization": f"bearer {st.session_state.access_token}"
            })

    elif url != None:
        change_response = requests.put(url=f"{backend_url}/tools/{bot_id}?url={url}",
                                       headers={
                                           "Authorization": f"bearer {st.session_state.access_token}"
                                       })

    elif auth != None:
        change_response = requests.put(url=f"{backend_url}/tools/{bot_id}?auth_token={auth}",
                                       headers={
                                           "Authorization": f"bearer {st.session_state.access_token}"
                                       })

    elif toolsUse != None:
        change_response = requests.put(url=f"{backend_url}/bots/{bot_id}?toolsUse={toolsUse}",
                                       headers={
                                           "Authorization": f"bearer {st.session_state.access_token}"
                                       })

    print(f"the change request result: {change_response.json()}")
    st.session_state.agent_change = change_response.json()["response"]


@st.dialog(title="Delete Agent")
def delete_agent(bot_id: str):
    st.text(f"To delete the agent please the bot id: {bot_id}")

    agent_id = st.text_input(label="Agent Id")
    delete_agent_button = st.button(label="Delete")
    if delete_agent_button == True:
        delete_response = requests.delete(url=f"{backend_url}/bots/{bot_id}",
                                       headers={
                                           "Authorization": f"bearer {st.session_state.access_token}"
                                       })
        if delete_response.json()["response"] == True:
            st.success("✅ Agent deleted")
            st.rerun()
        else:
            st.error("❌ Error occurred deleting agent")


with agentSettings:

    container = st.container(border=True)
    st.session_state.agent_name = container.text_input(label="Change agent name", value=bot_info["name"])
    save_agent_name = container.button(label="Save name", on_click=edit_agent,
                                       kwargs={
                                           "bot_id": st.session_state.agent,
                                           "name": st.session_state.agent_name
                                       })
    if save_agent_name == True:
        if st.session_state.agent_change == "1":
            st.success("✅ Agent name changed")
        else:
            st.error("❌ Error occurred changing agent name")
        st.rerun()

    st.session_state.system_prompt = container.text_area(label="Change system prompt", value=bot_info["system_prompt"])
    save_agent_system_prompt = container.button(label="Save prompt", on_click=edit_agent,
                                       kwargs={
                                           "bot_id": st.session_state.agent,
                                           "system_prompt": st.session_state.system_prompt
                                       })
    if save_agent_system_prompt == True:
        if st.session_state.agent_change == "1":
            st.success("✅ Agent system prompt changed")
        else:
            st.error("❌ Error occurred changing system prompt")
        st.rerun()

    container.divider()
    container.button(label="Delete Agent", on_click=delete_agent, args=(st.session_state.agent, ))


with toolsSettings:
    container = st.container(border=True)

    # set the tools status
    new_tools_status = container.toggle(label="Tools status", value=st.session_state.tools_status)
    save_tools_status = container.button(label="Save Tool status", on_click=edit_agent,
                                      kwargs={
                                          "bot_id": st.session_state.agent,
                                          "toolsUse": new_tools_status
                                      })
    if save_agent_name == True:
        st.success("✅ Tool status changed")
        st.rerun()
    container.divider()

    new_tool_url = container.text_input(label="Add or change tool url", value=response_body["tool_url"])
    save_agent_url = container.button(label="Save Url", on_click=edit_agent,
                                      kwargs={
                                          "bot_id": st.session_state.agent,
                                          "url": new_tool_url
                                      })
    if save_agent_name == True:
        st.success("✅ Tool Url changed")
        st.rerun()
    container.divider()

    new_tool_auth = container.text_input(label="Add or change tool authentication", value=response_body["tool_auth"])
    save_agent_auth = container.button(label="Save Authentication", on_click=edit_agent,
                                       kwargs={
                                           "bot_id": st.session_state.agent,
                                           "auth": new_tool_auth
                                       })
    if save_agent_auth == True:
        st.success("✅ Tool authentication changed")
        st.rerun()

