from openai.embeddings_utils import distances_from_embeddings
import numpy as np
import openai
import pandas as pd
import streamlit as st
from langchain.agents import create_pandas_dataframe_agent
from langchain import OpenAI
from prompts import *


@st.cache_data
def load_data(filename='pfraw.csv'):
    df = pd.read_csv(f"data/{filename}")
    return df


@st.cache_resource
def load_agent(df, temperature, prompt_prefix=SAMPLE_PROMPT_PREFIX):
    '''Loads the langchain datagrame agent for the specified dataframe.'''

    llm = OpenAI(temperature=0.2, model_name='text-davinci-003')
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

# =============== OLD MODEL =============== #


@st.cache_data
def load_old_data():
    '''Loads old web-scraped embeddings data'''
    df = pd.read_csv('processed/embeddings.csv', index_col=0)
    df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)
    return df


# df = load_old_data()


def create_context(question, df, maxlen=1800, size="ada"):
    '''
    Create a context for a question by finding the most similar context from the DataFrame
    '''

    # Get embeddings for question
    q_embeddings = openai.Embedding.create(
        input=question, engine="text-embedding-ada-002")['data'][0]['embedding']

    # Get distance from embeddings
    df['distances'] = distances_from_embeddings(
        q_embeddings, df['embeddings'].values, distance_metric='cosine')

    returns = []
    cur_len = 0

    # Sort by distance and add text to context till context is too long
    for i, row in df.sort_values('distances', ascending=True).iterrows():

        # Add length of text to current length
        cur_len += row['n_tokens'] + 4

        # If context too long, break
        if cur_len > maxlen:
            break

        # Else add it to the text being returned
        returns.append(row['text'])

    # Return context
    return '\n\n###\n\n'.join(returns)


def generate_response(
        df=load_old_data(),
        model="text-davinci-003",
        question="Hi, please introduce yourself",  # This is the default question
        max_len=1800,
        size='ada',
        debug=False,
        max_tokens=500,
        stop_sequence=None
):
    '''
    Answer a question based on the most similar context from DataFrame texts
    '''
    context = create_context(
        question,
        df,
        maxlen=max_len,
        size=size
    )

    # if debug enabled, print raw response
    if debug:
        print('Context:\n' + context)
        print('\n\n')

    try:
        # create Completion using question and context
        response = openai.Completion.create(
            prompt=f"""You are a virtual property assistant for the real estate company 'ViewIt'.
            Be friendly and welcoming and answer the question based on the context below.
            
            Context: {context}
            
            ---
            
            Question: {question}

            Answer: """,
            temperature=0.2,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        print(e)
        return ''
