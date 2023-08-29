import streamlit as st

def custom_css():
    hide_streamlit_style = """
                <style>
                    footer {visibility: hidden;}
                    .viewerBadge_container__r5tak styles_viewerBadge__CvC9N {visibility: hidden;}
                    .social-icons {
                        display: flex;
                        flex-wrap: wrap;
                        justify-content: space-between;
                        align-items: center;
                        max-width: 100%; /* Adjust as needed */
                        width: 100%;
                        padding: 0 10px; 
                        /* Some padding to ensure icons aren't at the very edge on small devices */
                    }

                    .icon {
                        display: block;
                        width: 25px;
                        height: 25px;
                        margin: 5px;
                        /* Adjusted margin to make it symmetrical */
                        background-size: cover;
                        background-position: center;
                        transition: transform 0.3s;
                    }

                    .icon:hover {
                        transform: scale(1.1);
                    }

                    .viewit {
                        background-image: url('https://viewit.ae/_nuxt/img/viewit-logo-no-text.25ba9bc.png');
                    }

                    /* .github {
                        background-image: url('https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Github-1024.png');
                    } */

                    .facebook {
                        background-image: url('https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Facebook-1024.png');
                    }

                    .twitter {
                        background-image: url('https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Twitter-1024.png');
                    }

                    .instagram {
                        background-image: url('https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Instagram-1024.png');
                    }
                </style>
                """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
