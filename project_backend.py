from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
import sqlite3
import uuid
from pydantic import BaseModel, Field, ValidationError
import json


class StructuredResponse(BaseModel):
    reasoning: str = Field(description="Model reasoning inside <think> tags")
    answer: str = Field(description="Model final answer after </think>")
    title: str = Field(default=..., description="title of the chat") 

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    #api_key="_", # <---------------------------------ENTER YOUR GROK aPI------------------------------------
    temperature=0.5
)



structured_model = model.with_structured_output(schema= StructuredResponse)



class ChatState(TypedDict):
    answer: list[BaseMessage]
    history_messages: list[BaseMessage]
    human_input: str
    output : StructuredResponse

def chat(state: ChatState):
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""
        You are Dedicated.ai. You MUST respond with ONLY a valid JSON object. NO exceptions.

        REQUIRED JSON SCHEMA (exactly 3 fields):
        {
        "title": "string value here",
        "reasoning": "string value here", 
        "answer": "string value here"
        }

        STRICT RULES - VIOLATION WILL CAUSE SYSTEM ERROR:
        1. Output MUST start with { and end with }
        2. NO markdown formatting (no ```
        3. NO additional text before or after the JSON
        4. NO extra fields beyond title, reasoning, answer
        5. reasoning and answer should be in depth and long and clear , because you are an reasearcher 
        6. ALL field values MUST be strings in double quotes
        7. NO line breaks or formatting inside string values
        8. NO comments, explanations, or meta-commentary
        9. NO "Here's the response:" or similar prefixes

        FORBIDDEN OUTPUTS:
        ```json {...}```
        Here is my response: {...}
        {"title": "...", "extra_field": "..."}
        Any text before {
        Any text after }

        REQUIRED OUTPUT EXAMPLE:
        {"title": "Short Title", "reasoning": "My thinking process", "answer": "Direct response"}

        CRITICAL: If you output anything other than pure JSON matching the exact schema above, the system will crash. Your response must be parseable by JSON.parse() immediately.
        """)
,
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{human_input}")
    ])

    prompt_output = prompt.invoke({
        "history": state["history_messages"],
        "human_input": state["human_input"]
    })

    structured_output = structured_model.invoke(prompt_output)
    # print(structured_output)
    return {"output":structured_output}

conn = sqlite3.connect("chating5.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)
chatbot = graph.compile(checkpointer=checkpointer)

def retrive_history(thread_id):
    latest_state = None
    history = []
    for state in chatbot.get_state_history(config={"configurable": {"thread_id": thread_id}}):
        latest_state = state
        break

    if latest_state:
        for msg in latest_state.values["history_messages"]:
            if isinstance(msg, HumanMessage):
                history.append(HumanMessage(content=msg.content))
            elif isinstance(msg, AIMessage):
                history.append(AIMessage(content=msg.content))

        human_input = latest_state.values.get("human_input")
        if human_input is not None:
            history.append(HumanMessage(content=human_input))

        ai_output = latest_state.values.get("output")
        if ai_output is not None:
            history.append(
                AIMessage(content=json.dumps({
                    "reasoning": ai_output.reasoning,
                    "answer": ai_output.answer,
                    "title": ai_output.title
                }))
            )
    return history



# def retrive_all_threads():
#     ids = set()
#     for id in checkpointer.list(None):
#         ids.add(id.config['configurable']['thread_id'])
#     return list(ids)


def retrive_all_threads():

    thread_records = []
    for record in checkpointer.list(None):
        thread_id = record.config["configurable"]["thread_id"]
        created_at = getattr(record, "created_at", None)
        thread_records.append((thread_id, created_at))
    
    thread_records.sort(key=lambda x: x[1] or "")
    
    return [thread_id for thread_id, _ in reversed(thread_records)]


# history_messages = [
#     HumanMessage(content="Hi, my name is pritiyax shukla!"),
#     AIMessage(content="Hello, your name is pritiyax shukla")
# ]

# config = {"configurable": {"thread_id": "S12"}}

# prompt_output = chatbot.invoke({
#     "history_messages": history_messages,
#     "human_input": "hello ",
#     "title": ""
# }, config=config)

# print(prompt_output)
# print(prompt_output["output"].reasoning)
# print(prompt_output["output"].answer)
# print(prompt_output["output"].title)