import openai
import numpy as np
import pandas as pd
from openai.embeddings_utils import distances_from_embeddings
from main import df


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
        df=df,
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