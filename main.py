import openai
from openai.embeddings_utils import distances_from_embeddings
# from creds import api_key
import pandas as pd
import numpy as np
from streamlit_chat import message
import streamlit as st

# read the already created embeddings csv
df = pd.read_csv('processed/embeddings.csv', index_col=0)
df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)

# ViewIt OpenAI API key
openai.organization = st.secrets['org']
openai.api_key = st.secrets['api_key']
# openai.api_key = api_key

def create_context(question, df, maxlen=1800, size="ada"):
    '''
    Create a context for a question by finding the most similar context from the DataFrame
    '''

    # Get embeddings for question
    q_embeddings = openai.Embedding.create(input=question, engine="text-embedding-ada-002")['data'][0]['embedding']

    # Get distance from embeddings
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')

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


def get_input():
    input_text = st.text_input("Ask a question: ", key='input', value="Hi",
                               placeholder='Ask a question...')
    return input_text


def generate_response(
        df=df,
        model= "text-davinci-003",
        question = "Hi, please introduce yourself", # This is the default question
        max_len = 1800,
        size = 'ada',
        debug = False,
        max_tokens = 500,
        stop_sequence = None
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
            prompt= f"""You are a virtual property broker for the real estate company 'ViewIt'. Be friendly and welcoming and answer the question based on the context below.
            
            Context: {context}
            
            ---
            
            Question: {question}
            Answer: """,
            temperature=0,
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
    


# App Title
st.title('ViewIt Chatbot 2.0')

# App Sidebar
with st.sidebar:
    st.markdown(f"""
                # About
                This is version 2 of the Chatbot Assistant that will help you look for your desired properties.

                
                # How does it work
                Simply enter your query in the text field and the assistant will help you out.
                """)

# storing chat history
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

user_input = get_input()

# Generate a response if input exists
if user_input:
    output = str(generate_response(df=df, model='text-davinci-003', question=user_input))

    # store chat
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i)+'_user')
        message(st.session_state['generated'][i], key=str(i))
