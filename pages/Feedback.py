import streamlit as st
from Chat import hide_made_by_streamlit
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
    width = 25
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        # https://cdn4.iconfinder.com/data/icons/liberty/46/Earth-1024.png
        st.write(f'''<center>
                <a href='https://viewit.ae'>
                    <img src="https://viewit.ae/_nuxt/img/viewit-logo-no-text.25ba9bc.png" 
                        alt="viewit-landing" width="{width}">
                </a></center>
                ''', unsafe_allow_html=True)

    with c2:
        st.write(f'''<center>
                <a href='https://github.com/viewitai'>
                    <img src="https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Github-1024.png" 
                        alt="github" width="{width}">
                </a></center>
                ''', unsafe_allow_html=True)

    with c3:
        st.write(f'''<center>
                <a href='https://www.facebook.com/View1T'>
                    <img src="https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Facebook-1024.png" 
                        alt="facebook" width="{width}">
                </a></center>
                ''', unsafe_allow_html=True)

    with c4:
        st.write(f'''<center>
                <a href='https://instagram.com/viewit.ae'>
                    <img src="https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Instagram-1024.png" 
                        alt="instagram" width="{width}">
                </a></center>
                ''', unsafe_allow_html=True)

    with c5:
        st.write(f'''<center>
                <a href='https://twitter.com/aeviewit'>
                    <img src="https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Twitter-1024.png" 
                        alt="twitter" width="{width}">
                </a></center>
                ''', unsafe_allow_html=True)
    st.write('---')

    st.caption('© 2023 ViewIt. All rights reserved.')


hide_made_by_streamlit()