import streamlit as st
import requests

st.title('Discover Agent 🔍')

query = st.text_input("Search...")
if query:
    body = {
        'query': query
    }
    response = requests.post('http://localhost:2911/get_answer', json=body)
    answer = response.json()['answer']
    st.subheader("Answer:")
    st.write(answer)