import pandas as pd
import streamlit as st
# from langchain.agents import create_pandas_dataframe_agent
from langchain import OpenAI, LLMChain
from prompts import *
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.tools.python.tool import PythonAstREPLTool

icons = "😎,😶‍🌫️,🤯,👾,🤖,👽,🦾,🕵️,✨,👓,🕶️,🔑,🗝️,🩻,🔍,💡,📈,📊,📍,📎,🌏,🏙️,🏡,🏠,🏢,🏬,🌇".split(',')

@st.cache_data
def load_data(filename) -> pd.DataFrame:
    df = pd.read_csv(f"data/{filename}")
    if 'Record Date' in df.columns:
        df['Record Date'] = pd.to_datetime(df['Record Date'])
    elif 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    return df


# @st.cache_resource
def create_pandas_dataframe_agent(
    llm,
    df: pd.DataFrame,
    prefix: str = REIDIN_PREFIX,
    suffix: str = SUFFIX,
    input_variables = None,
    verbose: bool = False,
    memory: ConversationBufferMemory = ConversationBufferMemory(memory_key="chat_history")
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
    llm = OpenAI(temperature=0.25, model_name="text-davinci-003", openai_api_key=st.secrets['api_key']),
    df= load_data('new_reidin_data.csv'),
    prefix=REIDIN_PREFIX,
    verbose=True
)


@st.cache_resource
def load_agent(df, temperature, prompt_prefix=SAMPLE_PROMPT_PREFIX, model='text-davinci-003'):
    '''Loads the langchain dataframe agent for the specified dataframe.'''

    llm = OpenAI(temperature=temperature, model_name=model, openai_api_key=st.secrets['api_key'], verbose=True)
    agent = create_pandas_dataframe_agent(llm=llm, df=df, prefix=prompt_prefix)
    return agent


def get_answer(question, prompt_prefix, df, model='text-davinci-003', temperature=0.2):
    agent = load_agent(df=df, temperature=temperature,
                       prompt_prefix=prompt_prefix, model=model)
    response = agent.run(question)
    return response


prefix_mapping = {
    'pfraw.csv': SAMPLE_PROMPT_PREFIX,
    'real_estate1.csv': PROMPT_PREFIX,
    'new_reidin_data.csv': REIDIN_PREFIX
}


@st.cache_data(show_spinner=False)
def df_prefix(filename):
    df = load_data(filename)

    if filename in prefix_mapping:
        PREFIX = prefix_mapping[filename]

    return df, PREFIX