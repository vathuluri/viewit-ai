import random
from model import icons, df_prefix, get_answer
from streamlit_chat import message
import openai
import streamlit as st
st.set_page_config(page_title="Viewit Property Analyst", page_icon=random.choice(icons),
                   layout="centered", initial_sidebar_state="auto")
col1, col2, col3 = st.columns(3)

with col2:
    st.image("https://i.postimg.cc/Nfz5nZ8G/Logo.png", width=200)

# # Clear Session State Variables
# for key in st.session_state.keys():
#     del st.session_state[key]


if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''


def clear():
    st.session_state.user_input = st.session_state.widget
    st.session_state.widget = ''


# App Title
st.title('ViewIt Chatbot 0.3')


data_option = st.radio('Choose the data', ['pfraw.csv', 'real_estate1.csv'], 
                       key='radio_option', horizontal=True)

if data_option == 'pfraw.csv':
    df, PREFIX = df_prefix('pfraw.csv')
else:
    df, PREFIX = df_prefix('real_estate1.csv')


with st.expander("See the data being used"):
    st.write("Here's a sample of our transaction data")
    st.write(f"Total rows: {len(df)}")
    st.dataframe(df.head(10))


# App Sidebar
with st.sidebar:
    st.markdown(f"""
                # About
                This is version 0.3 of the Chatbot Assistant that will help you
                  look for your desired properties.
                
                # How to use
                Simply enter your query in the text field and the assistant 
                will help you out.
                """)


st.text_input("Ask a question: ", key='widget',
              placeholder='Ask a question...', on_change=clear)

# storing chat history
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

user_input = st.session_state.user_input

# Generate a response if input exists
if user_input:
    with st.spinner('Thinking...'):
        output = str(get_answer(question=user_input, prompt_prefix=PREFIX, df=df))

        # store chat
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

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
#     "Like what we're building? [Join the waitlist](https://tally.so/r/w4QW4r)")