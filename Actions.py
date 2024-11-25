import json
from typing import Union
import streamlit as st
import requests
import pandas as pd
from pandas import DataFrame

url = "https://edison.bynarybots.co.ke"

print(st.session_state.agent)
response = requests.get(url=f"{url}/tools/{st.session_state.agent}",
                        headers={
                            "Authorization": f"bearer {st.session_state.access_token}"
                        })
print(response)
response_body = response.json()
st.title("Actions :wrench:")
st.session_state.parameters_list = []


def create_action(name: str, description: str, parameters: list):
    print(parameters)

    set_parameters = []
    req_parameters = []

    # set the parameters and required parameters
    for item in parameters:
        new_item = {
            "name": item["name"],
            "type": item["type"],
            "description": item["description"]
        }
        set_parameters.append(new_item)
        if item["required"] == True:
            req_parameters.append(item["name"])

    print(f"new parameters list{set_parameters}")
    print(f"new required parameters list{req_parameters}")

    if parameters != []:
        body = {"name": name, "description": description, "parameters": set_parameters,
                "required_parameters": req_parameters}
        response = requests.post(url=f"{url}/tools/{st.session_state.agent}/tool",
                                 data=json.dumps(body),
                                 headers={
                                     "Authorization": f"bearer {st.session_state.access_token}"})
    else:
        body = {"name": name, "description": description}
        response = requests.post(url=f"{url}/tools/{st.session_state.agent}/tool",
                                 data=json.dumps(body),
                                 headers={
                                     "Authorization": f"bearer {st.session_state.access_token}" })

    st.session_state.result = response.json()


# use this function callback to post changes in an action
def update_action(tool_name: str, name: Union[str, None] = None, description: Union[str, None] = None, parameters: Union[list, None] = None, required_parameters: Union[str, None] = None):
    # st.session_state.action_name = name
    if name != None:
        body = {"payload": {"name": name}}
        response = requests.put(url=f"{url}/tools/{st.session_state.agent}/tool?tool_name={tool_name}",
                                data=json.dumps(body),
                                headers={
                                    "Authorization": f"bearer {st.session_state.access_token}"
                                })
    elif description != None:
        body = {"payload": {"description": description}}
        response = requests.put(url=f"{url}/tools/{st.session_state.agent}/tool?tool_name={tool_name}",
                                data=json.dumps(body),
                                headers={
                                    "Authorization": f"bearer {st.session_state.access_token}"
                                })
    elif parameters != None:
        # body = {"payload": {"parameters": parameters}}

        set_parameters = []
        req_parameters = []

        # set the parameters and required parameters
        for item in parameters:
            new_item = {
                "name": item["name"],
                "type": item["type"],
                "description": item["description"]
            }
            set_parameters.append(new_item)
            if item["required"] == True:
                req_parameters.append(item["name"])

        print(f"new parameters list{set_parameters}")
        print(f"new required parameters list{req_parameters}")

        body = {"payload": {"parameters": set_parameters}}
        response = requests.put(url=f"{url}/tools/{st.session_state.agent}/tool?tool_name={tool_name}",
                                data=json.dumps(body),
                                headers={
                                    "Authorization": f"bearer {st.session_state.access_token}"
                                })
        body = {"payload": {"required_parameters": req_parameters}}
        next_response = requests.put(url=f"{url}/tools/{st.session_state.agent}/tool?tool_name={tool_name}",
                                data=json.dumps(body),
                                headers={
                                    "Authorization": f"bearer {st.session_state.access_token}"
                                })
        st.session_state.required_params_result = next_response.json()

    elif required_parameters != None:

        body = {"payload": {"required_parameters": required_parameters}}
        response = requests.put(url=f"{url}/tools/{st.session_state.agent}/tool?tool_name={tool_name}",
                                data=json.dumps(body),
                                headers={
                                    "Authorization": f"bearer {st.session_state.access_token}"
                                })
    st.session_state.result = response.json()


def delete_action(name: str):
    response = requests.delete(url=f"{url}/tools/{st.session_state.agent}/tool?tool_name={name}",
                                headers={
                                    "Authorization": f"bearer {st.session_state.access_token}"
                                })
    st.session_state.result = response.json()

# use this dialog to edit an action
@st.dialog("Edit action")
def edit_action(name: str, description: str, parameters: list, required_params: list):
    action_name = st.text_input(label="Action name", value=name)
    clicked = st.button(label="Save Name", on_click=update_action, kwargs={"tool_name": name, "name": action_name})
    if clicked == True:
        if "response" in st.session_state.result:
            if st.session_state.result["response"] == "1":
                st.success("✅ Operation Successful")
            else:
                st.error("❌ Error occurred")
        st.rerun()

    description = st.text_area(label="Description", value=description)
    clicked = st.button(label="Save Description", on_click=update_action, kwargs={"tool_name": name, "description": description})
    if clicked == True:
        if "response" in st.session_state.result:
            if st.session_state.result["response"] == "1":
                st.success("✅ Operation Successful")
            else:
                st.error("❌ Error occurred")
        st.rerun()

    if parameters != []:
        # create the dataframe for the table
        new_parameters_list = []
        for parameter in parameters:
            if parameter["name"] in required_params:
                parameter_body = {"name": parameter["name"], "type": parameter["type"],
                                  "description": parameter["description"], "required": True}
                new_parameters_list.append(parameter_body)
            else:
                parameter_body = {"name": parameter["name"], "type": parameter["type"],
                                  "description": parameter["description"], "required": False}
                new_parameters_list.append(parameter_body)
        data_frame = pd.DataFrame(new_parameters_list)
        edited_df = st.data_editor(data=data_frame, num_rows="dynamic")
        clicked = st.button(label="Save Parameters", on_click=update_action,
                            kwargs={"tool_name": name, "parameters": edited_df.to_dict(orient="records")})

        if clicked == True:
            if "response" in st.session_state.result or st.session_state.required_params_result:
                if st.session_state.result["response"] == "1" or st.session_state.required_params_result[
                    "response"] == "1":
                    st.success("✅ Operation Successful")
                elif st.session_state.result["response"] == "0" or st.session_state.required_params_result[
                    "response"] == "0":
                    print(
                        f"required parameters change update ... {st.session_state.required_params_result['response']}")
                    st.error("❌ Error occurred")
            st.rerun()
    else:
        data_frame = pd.DataFrame([{"name": "", "type": "", "description": "", "required": False}])
        edited_df = st.data_editor(data=data_frame, num_rows="dynamic")
        clicked = st.button(label="Save Parameters", on_click=update_action,
                            kwargs={"tool_name": name, "parameters": edited_df.to_dict(orient="records")})
        if clicked == True:
            if "response" in st.session_state.result or st.session_state.required_params_result:
                if st.session_state.result["response"] == "1" or st.session_state.required_params_result["response"] == "1":
                    st.success("✅ Operation Successful")
                elif st.session_state.result["response"] == "0" or st.session_state.required_params_result["response"] == "0":
                    print(f"required parameters change update ... {st.session_state.required_params_result['response']}")
                    st.error("❌ Error occurred")
            st.rerun()

    st.multiselect(label="Required parameters", options=required_params, default=required_params)

    st.text("Delete action")
    clicked = st.button(label="Delete ❌", on_click=delete_action, args=(name,))
    if clicked == True:
        if "response" in st.session_state.result:
            if st.session_state.result["response"] == "Tool updated successfully":
                st.success("✅ Deleting function")
                st.rerun()
            else:
                st.error("❌ Error occurred")



@st.dialog("Create Action")
def add_action():
    action_name = st.text_input(label="Action name")
    action_description = st.text_area(label="Description")

    st.text("Parameters")
    data_frame = pd.DataFrame([{"name": "", "type": "", "description": "", "required": False}])
    edited_df = st.data_editor(data=data_frame, num_rows="dynamic")
    st.info("An action does not require parameters. If it has, save your parameters to select the required ones")

    save_parameters = True
    print(f"new parameters: {edited_df.to_dict(orient='records')}")
    clicked = st.button(label="Save action", on_click=create_action, args=(action_name,
                                                                           action_description,
                                                                           edited_df.to_dict(orient="records")
                                                                           ))
    if clicked == True:
        if "response" in st.session_state.result:
            if st.session_state.result["response"] == "1":
                st.success("✅ Operation Successful")
            else:
                st.error("❌ Error occurred")
        st.rerun()


print(response_body["tools"])

st.button(label="Create action :heavy_plus_sign:", on_click=add_action)
with st.container(height=600):
    actions = response_body["tools"]

    for action in actions:
        expander = st.expander(label=action["name"])
        expander.write(action["description"])
        expander.button(label="Edit :pencil:", key=action["name"], on_click=edit_action, args=(
                                                                                               action["name"],
                                                                                               action["description"],
                                                                                               action["parameters"],
                                                                                               action["required_parameters"],))

# get user actions and display them