import pandas as pd
import streamlit as st
from langchain import LLMChain
from langchain.tools.python.tool import PythonAstREPLTool
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory

# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=msgs, memory_key="chat_history")


@st.cache_data
def load_data(filename) -> pd.DataFrame:
    df = pd.read_csv(f"data/{filename}")
    df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%Y", dayfirst=True)

    return df


# @st.cache_resource
def create_pandas_dataframe_agent(
        llm,
        df: pd.DataFrame,
        prefix: str,
        suffix: str,
        format_instructions: str,
        verbose: bool,
        **kwargs) -> AgentExecutor:
    """Construct a pandas agent from an LLM and dataframe."""

    if not isinstance(df, pd.DataFrame):
        raise ValueError(f"Expected pandas object, got {type(df)}")

    input_variables = ["df", "input", "chat_history", "agent_scratchpad"]

    tools = [PythonAstREPLTool(locals={"df": df})]

    prompt = ZeroShotAgent.create_prompt(
        tools=tools,
        prefix=prefix,
        suffix=suffix,
        format_instructions=format_instructions,
        input_variables=input_variables
    )
    partial_prompt = prompt.partial(df=str(df.head()))

    llm_chain = LLMChain(
        llm=llm,
        prompt=partial_prompt
    )
    tool_names = [tool.name for tool in tools]

    agent = ZeroShotAgent(llm_chain=llm_chain,
                          allowed_tools=tool_names, verbose=verbose)

    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=verbose,
        memory=memory,
        **kwargs
    )


def custom_css():
    hide_streamlit_style = """
                <style>
                    footer {visibility: hidden;}
                    .viewerBadge_container__r5tak styles_viewerBadge__CvC9N {visibility: hidden;}
                    .social-icons {
                        display: flex;
                        flex-wrap: wrap;
                        justify-content: space-between;
                        align-items: center;
                        max-width: 100%; /* Adjust as needed */
                        width: 100%;
                        padding: 0 10px; 
                        /* Some padding to ensure icons aren't at the very edge on small devices */
                    }

                    .icon {
                        display: block;
                        width: 25px;
                        height: 25px;
                        margin: 5px;
                        /* Adjusted margin to make it symmetrical */
                        background-size: cover;
                        background-position: center;
                        transition: transform 0.3s;
                    }

                    .icon:hover {
                        transform: scale(1.1);
                    }

                    .viewit {
                        background-image: url('https://viewit.ae/_nuxt/img/viewit-logo-no-text.25ba9bc.png');
                    }

                    .github {
                        background-image: url('https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Github-1024.png');
                    }

                    .facebook {
                        background-image: url('https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Facebook-1024.png');
                    }

                    .twitter {
                        background-image: url('https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Twitter-1024.png');
                    }

                    .instagram {
                        background-image: url('https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Instagram-1024.png');
                    }
                </style>
                """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
