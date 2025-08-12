import streamlit as st
from project_backend import chatbot, retrive_history, retrive_all_threads
import uuid 
from langchain_core.messages import HumanMessage, AIMessage
import time
import json
import streamlit as st
from footer import footer

def generate_thread():
    return str(uuid.uuid4())

def resume_chat(thread_id):
    st.session_state["thread_id"] = thread_id
    st.session_state["message_history"] = retrive_history(st.session_state["thread_id"])
    st.rerun()

def new_chat():
    st.session_state["thread_id"] = generate_thread()
    st.session_state["message_history"] = []
    st.rerun()

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread()
if "title" not in st.session_state:
    st.session_state["title"] = []






all_threads = retrive_all_threads()
generate_title = st.session_state["thread_id"] not in all_threads

st.session_state['message_history'] = retrive_history(st.session_state["thread_id"])

if st.session_state["message_history"]:
    for msg in st.session_state["message_history"]:
        if isinstance(msg, HumanMessage):
            with st.chat_message("human"):
                st.text(msg.content)
        else:
            try:
                data = json.loads(msg.content)
                with st.chat_message("ai"):
                    with st.expander("Reasoning"):
                        st.write(data["reasoning"])
                    with st.expander("Answer"):
                        st.write(data["answer"])
            except json.JSONDecodeError:
                with st.chat_message("ai"):
                    st.text(msg.content)




st.sidebar.markdown(
    """
    <h1 style='font-size:32px; margin-bottom:0.2px;'>
        <span style='color:black;'>Dedicated.</span><span style='color:red;'>a</span><span style='color:black;'>i</span>
    </h1>
    <hr style='border:0.5px solid grey; margin-top:0.2px;'>
    """,
    unsafe_allow_html=True
)


# st.sidebar.header("Dedicated.:red[a]i" , divider="grey")



if st.sidebar.button("New Chat", key="new_chat_btn"):
    new_chat()

unique_thread = []

print("\n\n reversed threads :- \n\n", all_threads)
for i, thread in enumerate(reversed(all_threads)):

    if not thread in unique_thread:
        unique_thread.append(thread)

        history = retrive_history(thread)
        if history:
            try:
                last_ai_msg = [msg for msg in history if isinstance(msg, AIMessage)][0]
                title = json.loads(last_ai_msg.content)["title"]
                print(title)
            except (IndexError, json.JSONDecodeError, KeyError):
                title = thread[:8]
        else:
            title = thread[:8]
        
        if st.sidebar.button(str(title), key=f"btn_{i}_{thread}"):
            resume_chat(thread)



# st.markdown("<p style='text-align:center;'>© 2025 This project is made by <strong>Pritiyax Shukla</strong></p>", unsafe_allow_html=True)



# *****************************************footer code  only************************************************



footer()

# ****************************************************************main code starts ************************************************


user_input = st.chat_input("Type here")

if user_input:
    with st.chat_message("human"):
       st.text(user_input)

    initial_state = {
        "human_input": user_input,
        "history_messages": retrive_history(st.session_state["thread_id"])
    }

    config = {"configurable": {"thread_id": st.session_state["thread_id"]}}
    chatbot_output = chatbot.invoke(initial_state, config=config)

    reasoning_output = chatbot_output["output"].reasoning
    answer_output = chatbot_output["output"].answer
    title = chatbot_output["output"].title

    with st.chat_message("ai"):
        with st.expander("Reasoning"):
            placeholder = st.empty()
            text = ""
            for char in reasoning_output:
                text += char
                placeholder.write(text)
                time.sleep(0.00001) 

        with st.expander("Answer"):
            placeholder = st.empty()
            text = ""
            for char in answer_output:
                text += char
                placeholder.write(text)
                time.sleep(0.00001)

    if generate_title:
        st.session_state["title"].append(title)
