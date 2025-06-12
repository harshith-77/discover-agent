import streamlit as st
from helper import helper
import logging

st.title('Discover Agent 🔍')

query = st.text_input("Search...")
if query:
    print("Sending to generate the answer")
    answers = helper.generate(query)
    for answer in answers:
        answer.pretty_print()
    answer = answers[-1].content
    print("Sending response")
    st.subheader("Answer:")
    st.write(answer)
