from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from crewai import LLM
from crewai_tools import FileReadTool
import os

load_dotenv()

llm = LLM(model="gemini/gemini-3.1-flash-lite",api_key=os.getenv("GOOGLE_API_KEY"))

def code_files(folder_path):
    file_list = []
    for root,dirs,files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in ['.venv', '__pycache__','.git']]
        for file in files:
            file_list.append(os.path.join(root,file))

    return "\n".join(file_list)

navigator_agent = Agent(
    role = "Navigating agent",
    goal = "To select files from the {folder_structure} which can contain the possible {problem}",
    backstory = """You are a navigating agent that navigates through folder files and selects
    the problematic ones""",
    llm = llm,
    verbose = False
)

navigator_agent_task = Task(
    description= """Navigate the {folder_structure} and select the files which 
    probably are responsible for the {problem}, never read the file contents and do not guess or invent what the files might contain""",
    expected_output= """In a structured format return the file paths that are related to the problem statement and nothing else.""",
    agent= navigator_agent
)

def build_debug_team(folder_path):
    file_reader_tool = FileReadTool(base_dir= folder_path)

    file_reader_agent = Agent(
        role = "File Reader",
        tools = [file_reader_tool],
        goal = "Read the contents of the files provided and find the part which is causing the stated {problem}",
        backstory = "You are a file reading agent that reads the content of the files provided and identifies the problem creating parts",
        llm = llm,
        verbose = False
    )

    file_reader_task = Task(
        description="""Read the content of the files provided and find the exact lines responsible for the problem. 
        Use the full, exact file path provided by the previous agent when calling the file reading tool — 
        do not shorten, modify, or use only the filename. 
        Quote the code verbatim, character-for-character, with no changes.""",
        expected_output="""A structured output containing: the file path, the exact original line(s) of code copied word-for-word from the file, the line number if visible, and a brief explanation of why this line may be causing the problem.""",
        agent=file_reader_agent
    )
    resolution_agent = Agent(
        role = "Resolution agent",
        goal = "To provide a solution and shows implementation for the problematic code snippets in the files provided",
        backstory = "You are a resolution agent who provides solutions and their implementation",
        llm = llm,
        verbose = False
    )

    resolution_agent_task = Task(
        description="Using the exact problematic line(s) identified, provide the smallest possible fix. Do not rewrite, restructure, or 'improve' any other part of the file. Only change what is broken.",
        expected_output="""A structured output showing: the original broken line, the corrected line, and a one-sentence explanation of the fix. Do not output the entire file — only the specific line(s) changed.""",
        agent=resolution_agent
    )

    debug_team = Crew(
        agents = [navigator_agent,file_reader_agent,resolution_agent],
        tasks = [navigator_agent_task,file_reader_task,resolution_agent_task],
        process = Process.sequential
    )

    return debug_team


if __name__ == "__main__":

    # print(code_files(r"C:\Users\DELL\html-css-js-template"))
    folder_path = input()
    debug_team = build_debug_team(folder_path)
    result = debug_team.kickoff(inputs={"folder_structure":code_files(folder_path),"problem":input()})
    print(result)
    # The button on my page looks unstyled — no background color, padding, or rounded corners are showing up.