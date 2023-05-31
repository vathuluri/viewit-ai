import openai
import pandas as pd
import streamlit as st
from langchain.agents import create_pandas_dataframe_agent
from langchain import OpenAI
from prompts import *

icons = "😎,😶‍🌫️,🤯,👾,🤖,👽,🦾,🕵️,🤹,✨,👓,🕶️,🔑,🗝️,🩻,📽️,📷,🔍,🔎,💡,📈,📊,📍,📎,🌏,🏙️,🏡,🏠,🏢,🏬,🌇".split(',')

# ViewIt OpenAI API key
openai.organization = st.secrets['org']
openai.api_key = st.secrets['api_key']


@st.cache_data
def load_data(filename='pfraw.csv'):
    df = pd.read_csv(f"data/{filename}")
    return df


@st.cache_resource
def load_agent(df, temperature, prompt_prefix=SAMPLE_PROMPT_PREFIX):
    '''Loads the langchain datagrame agent for the specified dataframe.'''

    llm = OpenAI(temperature=0.2, model_name='text-davinci-003', openai_api_key=st.secrets['api_key'])
    agent = create_pandas_dataframe_agent(llm=llm, df=df, prefix=prompt_prefix)
    return agent


def get_answer(question, prompt_prefix, df, temperature=0.2):
    agent = load_agent(df=df, temperature=temperature,
                       prompt_prefix=prompt_prefix)
    response = agent.run(question)
    return response


prefix_mapping = {
    'pfraw.csv': SAMPLE_PROMPT_PREFIX,
    'real_estate1.csv': PROMPT_PREFIX
}

@st.cache_data
def df_prefix(filename):
    df = load_data(filename)

    if filename in prefix_mapping:
        PREFIX = prefix_mapping[filename]

    return df, PREFIX
