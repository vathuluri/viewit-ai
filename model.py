import pandas as pd
import streamlit as st
from langchain.agents import create_pandas_dataframe_agent
from langchain import OpenAI
from prompts import *

icons = "😎,😶‍🌫️,🤯,👾,🤖,👽,🦾,🕵️,✨,👓,🕶️,🔑,🗝️,🩻,🔍,💡,📈,📊,📍,📎,🌏,🏙️,🏡,🏠,🏢,🏬,🌇".split(',')

@st.cache_data
def load_data(filename) -> pd.DataFrame:
    df = pd.read_csv(f"data/{filename}")
    if 'Record Date' in df.columns:
        df['Record Date'] = pd.to_datetime(df['Record Date'])
    elif 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    return df


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