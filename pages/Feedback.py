import streamlit as st
from utils import custom_css
from trubrics.integrations.streamlit import FeedbackCollector

try:
    st.set_page_config(page_title='Feedback • ViewIt.AI', page_icon='📝', layout='wide')
except:
    st.experimental_rerun()

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
### Or want to report a bug?
---
''')

st.subheader("We're here to listen.")

feed = collector.st_feedback(
    feedback_type="textbox",
    model="gpt-4",
    user_id=None,   # TODO: Add this later on when implementing authentication
    open_feedback_label="Share your experience",
)

with st.sidebar:
    # st.write("---")
    st.write(f'''
    <div class="social-icons">
        <a href="https://viewit.ae" class="icon viewit" aria-label="ViewIt"></a>
        <a href="https://github.com/viewitai" class="icon github" aria-label="GitHub"></a>
        <a href="https://facebook.com/View1T" class="icon facebook" aria-label="Facebook"></a>
        <a href="https://instagram.com/viewit.ae" class="icon instagram" aria-label="Instagram"></a>
        <a href="https://twitter.com/aeviewit" class="icon twitter" aria-label="Twitter"></a>
    </div>''', unsafe_allow_html=True)
    st.write('---')

    st.caption('© 2023 ViewIt. All rights reserved.')


custom_css()