from crew import crew
import streamlit as st

st.set_page_config(page_title="Code reviewer", page_icon="🤖")

st.title("Code Reviewer")

option = st.radio("Choose input method", ["Paste Code", "Upload File"])

if option=="Paste Code":
    code_paste=st.text_area("Paste your code here")
    if st.button("Code review"):
        result = crew.kickoff(inputs={"code":code_paste})
        st.write(result.raw)

else :
    code_file= st.file_uploader("Upload a code file")
    if code_file is not None:
        code_txt = code_file.read().decode("utf-8")
        if st.button("Code Review"):
            result = crew.kickoff(inputs={"code":code_txt})
            st.write(result.raw)