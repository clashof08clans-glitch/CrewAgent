from crew import crew
import streamlit as st
from debugger import code_files , build_debug_team
st.set_page_config(page_title="Code reviewer", page_icon="🤖")

st.title("Code Reviewer")

action = st.radio("Choose the Action",["Review Code", "Debug Folder"])
if action == "Review Code":
    option = st.radio("Choose input method", ["Paste Code", "Upload File"])

    if option=="Paste Code":
        code_paste=st.text_area("Paste your code here")
        if st.button("Code review"):
            result = crew.kickoff(inputs={"code":code_paste})
            st.write(result.raw)
            st.download_button(label="Review file download",data= result.raw,file_name="review.md")

    else :
        code_file= st.file_uploader("Upload a code file")
        if code_file is not None:
            code_txt = code_file.read().decode("utf-8")
            if st.button("Code Review"):
                result = crew.kickoff(inputs={"code":code_txt})
                st.write(result.raw)
                st.download_button(label="Review file download",data= result.raw,file_name="review.md")

else :
    folder_path = st.text_input("Paste your folder path here")
    problem = st.text_area("Your problem statement")
    if st.button("Upload folder path And problem "):
        debug_team = build_debug_team(folder_path)
        result = debug_team.kickoff(inputs={"folder_structure":code_files(folder_path),"problem":problem})
        st.write(result.raw)
    