import streamlit as st

st.markdown('## Example: This is a markdown header')
with open('example.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()
    st.markdown(markdown_content, unsafe_allow_html=True)
