# ViewIt Chatbot_v0.3

This chatbot now reads tabular data directly, for question answering.

Contains a webcrawler to crawl the domain and scrape the data, which is then used to create embeddings and context for the AI model.

Check the guide on [how to clone a repository.](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

_It is recommmended to create a virtual environment and install the requirements specified in the `requirements.txt` file in the following manner:_

    $ pip3 install -r requirements.txt

---
### 1. `main.py`

Runs the chatbot on the streamlit interface. Simply navigate to thid directory on your cli and run:

    $ streamlit run main.py

[Official Streamlit Documentation](https://docs.streamlit.io/)

---
### 2. `terminal_chatbot.py`

Runs the QA feature on the jupyter notebook. Reads the DataFrame from CSV and defines the question answering function.

Simply call the `agent.run()` method and pass the question to generate responses.