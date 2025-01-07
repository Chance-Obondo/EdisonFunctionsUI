import streamlit as st
import requests

# http://127.0.0.1:8000 https://edison.bynarybots.co.ke
url = "http://127.0.0.1:8000"
print(st.session_state.agent)

response = requests.get(url=f"{url}/bots/{st.session_state.agent}/topics",
                        headers={
                            "Authorization": f"bearer {st.session_state.access_token}"
                        })
response_body = response.json()

# get all the user topics
st.title("Topics :book:")


def create_topic(topic_name: str):
    response = requests.post(url=f"{url}/bots/{st.session_state.agent}/topics?topic_name={topic_name}",
                            headers={
                                "Authorization": f"bearer {st.session_state.access_token}"})
    st.session_state.topic_created = response.json()["response"]


def delete_topic(topic_id: str):
    response = requests.delete(url=f"{url}/bots/{st.session_state.agent}/{topic_id}/topics",
                            headers={
                                "Authorization": f"bearer {st.session_state.access_token}"})
    st.session_state.topic_deleted = response.json()["response"]


def update_topic(topic_id: str, name: str):
    response = requests.put(url=f"{url}/bots/{st.session_state.agent}/{topic_id}?name={name}",
                               headers={
                                   "Authorization": f"bearer {st.session_state.access_token}"})
    st.session_state.topic_updated = response.json()["response"]


@st.dialog("Create Topic")
def add_topic():
    topic_name = st.text_input(label="Topic name")
    clicked = st.button(label="Save Name", on_click=create_topic, kwargs={"topic_name": topic_name})
    if clicked == True:
        if st.session_state.topic_created == 1:
            st.success("✅ Operation Successful")
        else:
            st.error("❌ Error occurred")
        st.rerun()


@st.dialog("Edit Topic")
def edit_topic(name: str, topic_id: str):
    # edit topic name
    new_topic_name = st.text_input(label="Topic name", value=name)
    edit_topic_clicked = st.button(label="Save Name", on_click=update_topic, kwargs={"topic_id": topic_id, "name": new_topic_name})
    if edit_topic_clicked == True:
        if st.session_state.topic_updated == 1:
            st.success("✅ Operation Successful")
        else:
            st.error("❌ Error occurred")
        st.rerun()

    # add content to topic
    uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False)
    save_content_button_clicked = st.button(label="Save Content")
    if save_content_button_clicked == True:
        content_upload_response = requests.post(url=f"{url}/bots/{st.session_state.agent}/{topic_id}/content",
                                                files={"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)},
                                                headers={
                                                    "Authorization": f"bearer {st.session_state.access_token}",
                                                    "accept": "application/json"
                                                })

        if content_upload_response.json()["success"] == True:
            response = requests.put(url=f"{url}/bots/{st.session_state.agent}/{topic_id}?documents={content_upload_response.json()['documents']}",
                                    headers={
                                        "Authorization": f"bearer {st.session_state.access_token}"})
            if response.json()["response"] == 1:
                st.success("✅ Operation Successful")
            else:
                st.error("❌ Error occurred")
        else:
            st.error("❌ Error occurred")
        st.rerun()

    # delete topic
    st.text("Delete topic")
    delete_button_clicked = st.button(label="Delete❌", on_click=delete_topic, kwargs={"topic_id": topic_id})
    if delete_button_clicked == True:
        if st.session_state.topic_deleted == 1:
            st.success("✅ Operation Successful")
        else:
            st.error("❌ Error occurred")
        st.rerun()


st.button(label="Add Topic :heavy_plus_sign:", on_click=add_topic)
with st.container(height=600):
    st.text("Topics")
    topics = response_body["response"]
    for topic in topics:
        expander = st.expander(label=topic["name"])
        expander.text(body=f"Documents: {topic['documents']}")
        expander.button(label="Edit :pencil:", key=topic["name"], on_click=edit_topic, args=(topic["name"],
                                                                                             topic["id"],))



