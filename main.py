import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI

if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []

# define function to get user input
def get_text():
    """
    Get the user input text.
    returns:
        (str): the text entered by the user
     """

    input_text = st.text_input("You:", st.session_state["input"], key="input",
                               placeholder="Your AI assistant here! Ask me anything...",
                               label_visibility='hidden')
    return input_text

def new_chat():
    """
    clears session state and starts a new chat.
    :return:
    """
    save =[]
    for i in range(len(st.session_state['generated'])-1,-1,-1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state.entity_memory.store = {}
    st.session_state.entity_memory.buffer.clear()


st.title("Memory Bot")
api = st.sidebar.text_input("API-Key",type="password")
MODEL = st.sidebar.selectbox(label='model', options=['gpt-3.5-turbo','text-davinci-003','text-davinci-002', 'code-davinci-002'])
if api:
    llm = OpenAI(
        temperature = 0,
        openai_api_key=api,
        model_name=MODEL,
    )

    if 'entity_memory' not in st.session_state:
        st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=10)

    Conversation = ConversationChain(
        llm=llm,
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=st.session_state.entity_memory
    )
else:
    st.error("No API found")
    st.sidebar.button("New Chat", on_click=new_chat)

    user_input = get_text()

    if user_input:
        conversation_response = Conversation.run(input=user_input)
        output = conversation_response['choices'][0]['text'].strip()
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    with st.expander("Conversation"):
        for i in range(len(st.session_state['generated'])-1,-1,-1):
            st.info(st.session_state["past"][i])
            st.info(st.session_state["generated"][i],icon='')




