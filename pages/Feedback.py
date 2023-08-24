import streamlit as st
from main import hide_made_by_streamlit
from trubrics.integrations.streamlit import FeedbackCollector

st.set_page_config(page_title='Feedback • ViewIt.AI', page_icon='📝', layout='wide')

collector = FeedbackCollector(
    component_name="general feedback",
    email=st.secrets["TRUBRICS_EMAIL"], # Store your Trubrics credentials in st.secrets:
    password=st.secrets["TRUBRICS_PASSWORD"], # https://blog.streamlit.io/secrets-in-sharing-apps/
)

# Add Viewit logo image to the center of page
col1, col2, col3 = st.columns(3)
with col2:
    st.image("https://i.postimg.cc/Nfz5nZ8G/Logo.png", width=200)


st.write('''
## Got suggestions?
## Or want to report a bug?
''')

st.subheader("We're here to listen.")

collector.st_feedback(
    feedback_type="textbox",
    model="gpt-4",
    user_id=None,   # TODO: Add this later on when implementing authentication
    open_feedback_label="Share your experience",
)

hide_made_by_streamlit()