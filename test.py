import streamlit as st

if 'something' not in st.session_state:
    st.session_state.something = ''

def submit():
    st.session_state.something = st.session_state.widget
    st.session_state.widget = ''

st.text_input('Something', key='widget', on_change=submit)

st.write(f'Last submission: {st.session_state.something}')