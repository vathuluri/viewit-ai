import streamlit as st

if 'input' not in st.session_state:
    st.session_state.input = ''

def submit():
    st.session_state.input = st.session_state.widget
    st.session_state.widget = ''

st.text_input('Input', key='widget', on_change=submit)

st.write(f'Last submission: {st.session_state.input}')