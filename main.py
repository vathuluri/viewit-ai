import os
import openai
import streamlit as st
from model import df_prefix, agent
from datetime import datetime
from streamlit_chat import message

st.set_page_config(page_title="Viewit Property Analyst", page_icon="📊")

col1, col2, col3 = st.columns(3)

with col2:
    st.image("https://i.postimg.cc/Nfz5nZ8G/Logo.png", width=200)

# Clear Session State Variables
def clear_session_states():
    for key in st.session_state.keys():
        del st.session_state[key]


# ViewIt OpenAI API key
openai.organization = st.secrets['org']
openai.api_key = st.secrets['api_key']


if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''


def clear():
    st.session_state.user_input = st.session_state.widget
    st.session_state.widget = ''


# App Title
st.title('ViewIt Chatbot')

df, PREFIX = df_prefix('reidin_new.csv')


with st.expander("Show data"):
    st.write(f"Total rows: {len(df)}")
    st.dataframe(df)


if st.button('Clear session state'):
    clear_session_states()

st.info('Click to reset session states', icon='🛈')

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

st.text_input("Ask a question: ", key='widget',
              placeholder='Ask a question...', on_change=clear)


# storing chat history
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

user_input = st.session_state['user_input']

datenow = datetime.now().strftime("%Y_%m_%d")

# Generate a response if input exists
if user_input:
    user_log = f"\nUser [{datetime.now().strftime('%H:%M:%S')}]: " + user_input
    print(user_log)

    with st.spinner('Thinking...'):
        try:
            output = str(agent.run(user_input))
            response_log = f"Bot [{datetime.now().strftime('%H:%M:%S')}]: " + output
            print(response_log)
            # store chat
            st.session_state.past.append(user_input)
            st.session_state.generated.append(output)

        except:
            st.write("⚠️ Oops! Looks like you ran into an error. Try refreshing the page.")

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True,
                avatar_style='thumbs', key=str(i)+'_user')
        message(st.session_state['generated'][i], key=str(i))


st.write("---")
st.caption(
    """Made by Hamdan Mohammad. [GitHub](https://github.com/hamdan-27) | 
    [Instagram](https://instagram/hxm.dxn_)""")
# st.caption(
#     "Like what we're building? [Join the waitlist]()")