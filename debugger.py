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
    probably are responsible for the {problem}""",
    expected_output= """In a structured format return the file paths that are related to the problem statement""",
    agent= navigator_agent
)

file_reader_tool = FileReadTool()

file_reader_agent = Agent(
    role = "File Reader",
    tools = [file_reader_tool],
    goal = "Read the contents of the files provided and find the part which is causing the stated {problem}",
    backstory = "You are a file reading agent that reads the content of the files provided and identifies the problem creating parts",
    llm = llm,
    verbose = False
)

file_reader_task = Task(
    description = "Read the content of the files provided and find out the part that is responsible for the problem",
    expected_output = """Return a structured output containing the file paths , the code snippets ,
    the location of the code snippets in the files, and why they may be responsible for the problem""",
    agent = file_reader_agent
)

resolution_agent = Agent(
    role = "Resolution agent",
    goal = "To provide a solution and shows implementation for the problematic code snippets in the files provided",
    backstory = "You are a resolution agent who provides solutions and their implementation",
    llm = llm,
    verbose = False
)

resolution_agent_task = Task(
    description= "Read and understand the problematic code snippets in the files and provide a solution respectively ",
    expected_output= """Return a structured explanation on how the problem can be resolved , 
    and provide a corrected version of the code snippets if possible """,
    agent = resolution_agent
)

debug_team = Crew(
    agents= [navigator_agent,file_reader_agent,resolution_agent],
    tasks = [navigator_agent_task,file_reader_task,resolution_agent_task],
    process = Process.sequential
)



if __name__ == "__main__":
    # print(code_files(r"C:\Users\DELL\OneDrive\Desktop\crewAI"))
    result = debug_team.kickoff(inputs={"folder_structure":code_files(input()),"problem":input()})
    print(result)