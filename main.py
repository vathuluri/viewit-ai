import openai
import pandas as pd
import streamlit as st
from datetime import datetime
# from langchain.agents import create_pandas_dataframe_agent
from prompts import *
from langchain import OpenAI, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.tools.python.tool import PythonAstREPLTool
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory

try:
    st.set_page_config(page_title="Viewit Property Analyst", page_icon="📊")
except Exception as e:
    st.toast(str(e))
    st.toast("Psst. Try refreshing the page.", icon="👀")

# ViewIt OpenAI API key
openai.organization = st.secrets['org']
openai.api_key = st.secrets['api_key']

# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=msgs, memory_key="chat_history")


prefix_mapping = {
    'new_reidin_data.csv': REIDIN_PREFIX,
    'reidin_new.csv': REIDIN_PREFIX
}


#@st.cache_data
def df_prefix(filename):
    df = load_data(filename)

    if filename in prefix_mapping:
        PREFIX = prefix_mapping[filename]

    return df, PREFIX

#@st.cache_data
def load_data(filename) -> pd.DataFrame:
    df = pd.read_csv(f"data/{filename}")
    if 'Record Date' in df.columns:
        df['Record Date'] = pd.to_datetime(df['Record Date'], format="%d-%M-%Y").dt.date
    elif 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True).dt.date
    return df


# @st.cache_resource
def create_pandas_dataframe_agent(
    llm,
    df: pd.DataFrame,
    prefix: str = REIDIN_PREFIX,
    suffix: str = SUFFIX,
    input_variables = None,
    verbose: bool = False,
    # memory: ConversationBufferMemory = ConversationBufferMemory(memory_key="chat_history")
    memory = memory
) -> AgentExecutor:
    """Construct a pandas agent from an LLM and dataframe."""

    if not isinstance(df, pd.DataFrame):
        raise ValueError(f"Expected pandas object, got {type(df)}")
    if input_variables is None:
        input_variables = ["df", "input", "chat_history", "agent_scratchpad"]
    tools = [PythonAstREPLTool(locals={"df": df})]
    prompt = ZeroShotAgent.create_prompt(
        tools, prefix=prefix, suffix=suffix, input_variables=input_variables
    )
    partial_prompt = prompt.partial(df=str(df.head()))
    llm_chain = LLMChain(
        llm=llm,
        prompt=partial_prompt
    )
    tool_names = [tool.name for tool in tools]
    agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names, verbose=verbose)
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=verbose,
        memory=memory
    )


agent = create_pandas_dataframe_agent(
    llm = OpenAI(temperature=0.1, model_name="text-davinci-003", openai_api_key=st.secrets['api_key']),
    df= load_data('reidin_new.csv'),
    prefix=REIDIN_PREFIX,
    verbose=True,
    memory=memory
)


col1, col2, col3 = st.columns(3)

with col2:
    st.image("https://i.postimg.cc/Nfz5nZ8G/Logo.png", width=200)


# Give the user a surprise 
welcome_msg = ''
datenow = datetime.now().strftime("%d/%m")
if datenow == "30/04":
    st.baloons()
    welcome_msg = "It's my birthdaayyy!"
else:
    # st.snow()
    # welcome_msg = "I hope I've cooled you down in this unforgiving weather :)."
    welcome_msg = ""

if len(msgs.messages) == 0:
    msgs.add_ai_message(welcome_msg + " How can I help you today?")


# if 'user_input' not in st.session_state:
#     st.session_state['user_input'] = ''

# def clear():
#     st.session_state.user_input = st.session_state.widget
#     st.session_state.widget = ''


# App Title
st.title('ViewIt Chatbot')

df, PREFIX = df_prefix('reidin_new.csv')


with st.expander("Show data"):
    st.write(f"Total rows: {len(df)}")
    st.dataframe(df)


# # Clear Session State Variables
# def clear_session_states():
#     for key in st.session_state.keys():
#         st.session_state[key] = ''


# if st.button('Clear session state'):
#     clear_session_states()

# App Sidebar
with st.sidebar:
    st.markdown(f"""
                # About
                This Chatbot Assistant that will help you
                  look for your desired properties.
                
                # How to use
                Simply enter your query in the text field and the assistant 
                will help you out.

                # Data
                Uses Reidin Property Data.
                
                Source: http://reidin.com

                """)

    
    with st.expander("Commonly asked questions"):
        st.write(
            """
            - Give me a summary of all properties, what percentage are apartments?
            - Which location has the largest number of sales?
            - Give me a summary of the the top 10 most expensive properties excluding price per sq ft, what are the 3 the most reliable predictors of price? Explain your answer
            - Which developer made the cheapest property and how much was it? How many properties have they sold in total and what is the price range?
            - What percentage capital appreciation would I make if I bought an average priced property in the meadows in 2020 and sold it in 2023?
            - What does sales type mean?
            """
        )
    
    st.markdown('###### ©️ Hamdan Mohammad')

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type, avatar="🤖").write(msg.content)

# If user inputs a new prompt, generate and draw a new response
if user_input := st.chat_input('Ask away'):
    st.chat_message("human", avatar="😃").write(user_input)
    
    user_log = f"\nUser [{datetime.now().strftime('%H:%M:%S')}]: " + user_input
    print(user_log)
    
    # Note: new messages are saved to history automatically by Langchain during run
    with st.spinner('Thinking...'):
        try:
            response = agent.run(user_input)

        except Exception as e:
            response = str(e)
            if response.startswith("Could not parse LLM output: `"):
                response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
            
        st.chat_message("ai", avatar="🤖").write(response)
    
    response_log = f"Bot [{datetime.now().strftime('%H:%M:%S')}]: " + response
    print(response_log)

# # storing chat history
# if 'generated' not in st.session_state:
#     st.session_state['generated'] = []

# if 'past' not in st.session_state:
#     st.session_state['past'] = []

# user_input = st.session_state['user_input']


# Generate a response if input exists
# if user_input:
#     user_log = f"\nUser [{datetime.now().strftime('%H:%M:%S')}]: " + user_input
#     print(user_log)

#     with st.spinner('Thinking...'):
#         # try:
#             output = str(agent.run(user_input))
#             response_log = f"Bot [{datetime.now().strftime('%H:%M:%S')}]: " + output
#             print(response_log)
#             # store chat
#             st.session_state.past.append(user_input)
#             st.session_state.generated.append(output)

        # except:
        #     st.write("⚠️ Oops! Looks like you ran into an error. Try asking another question or refresh the page.")

# if st.session_state['generated']:
#     for i in range(len(st.session_state['generated'])-1, -1, -1):
#         message(st.session_state['past'][i], is_user=True,
#                 avatar_style='thumbs', key=str(i)+'_user')
#         message(st.session_state['generated'][i], key=str(i))

st.write("---")
st.caption(
    """Made by Hamdan Mohammad. [GitHub](https://github.com/hamdan-27) | 
    [Instagram](https://instagram/hxm.dxn_)""")