from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from crewai import LLM
import os

load_dotenv()

llm = LLM(model="gemini/gemini-3.1-flash-lite",api_key=os.getenv("GOOGLE_API_KEY"))

code_reader = Agent(
    role = "Code Reader",
    goal = """Decipher the language , intent , structure of the {code}""",
    backstory = "You are Code Reader who understands structure language and intent of the code",
    llm = llm,
    verbose = False
)

code_reader_task = Task(
    description = """Analyze the provided code and identify: 1) The Programming language,
    2) What the code is trying to do,3) the overall structure""",
    expected_output= "A Structured Summary with three labeled sections :Language ,Intent and Structure",
    agent=code_reader
)

bug_hunter = Agent(
    role = "Bug hunter",
    goal = "Find syntax errors,runtime errors,logical errors and other bugs in the {code}",
    backstory = "You are a code bug hunter who finds different mistakes in the code body",
    llm = llm,
    verbose = False
)

bug_hunter_task = Task(
    description= """Analyze the code and find 1) Syntax Errors,2) Logical Errors
    3)Runtime errors 4) Other bugs that ruin the code""",
    expected_output= """A structured output mentioning all the errors and where they occur in the code""",
    agent= bug_hunter
)

quality_reviewer = Agent(
    role = "Quality Reviewer",
    goal = "To check the overall quality of the code , the complexity , the readiness of the {code}",
    backstory = "You are a code reviewer that reviews different structural aspects of the code",
    llm =llm,
    verbose = False
)

quality_reviewer_task = Task(
    description = """Review the code and find 1) Quality of the code 2) Time complexity 
    3) General complexity 4) Readiness 5) Other viewing aspects""",
    expected_output= """A structure output mentioning 1) Quality 2)Complexity 3)Readniess 
    4) Some other major viewpoints""",
    agent = quality_reviewer
)

security_agent = Agent(
    role = "Security Agent",
    goal = "Report security vulrenabilities in the {code}",
    backstory = "You are a Security Agent that reports security vulnerabilities which can be exploited",
    llm = llm,
    verbose = False
)

security_agent_task = Task(
    description= """Scan the Code and search for security vulnerabilities that can be exploited
    or prove dangerous""",
    expected_output= """A structured output mentioning the security risks such as Injections,
    Hardcoded credentials,overflows, etc.""",
    agent = security_agent

)

checklist_compiler = Agent(
    role = " Checklist compiler",
    goal = "Compile all the results provided and sort them by priority",
    backstory = "You are a checklist compiler that sorts the problems by order of importance",
    llm = llm,
    verbose = False
)

checklist_compiler_task = Task(
    description = "Check the results provided and sort the errors/mistakes by priority for taking action against them",
    expected_output= """A structured Code review checklist that tells where exactly are the problems and rank them
    on the basis of resolving priority 1)  🔴 Critical (Fix First) 2) 🟡 Medium (Fix before shipping)
    3) 🟢 Low (Nice to Have) , try to output them in nice clean bullet points""",
    agent = checklist_compiler

)

crew = Crew(
    agents= [code_reader,bug_hunter,quality_reviewer,security_agent,checklist_compiler],
    tasks=  [code_reader_task,bug_hunter_task,quality_reviewer_task,security_agent_task,checklist_compiler_task],
    process = Process.sequential
)

def read():
    lines = []
    while True :
        line = input()
        if line=="END":
            break
        lines.append(line)

    user_input = "\n".join(lines)
    return user_input

def read_file(code):
   
    with open(code,"r") as file:
       txt = file.read()

    return txt


print("""Choose your option 
      1 for pasting the code
      2 for uploading a code file""")
option = input()

if(option=="1"):
    result = crew.kickoff(inputs={"code":read()})
elif(option=="2"):
    result =crew.kickoff(inputs={"code":read_file(input())})
else:
    print("No Such Option")


print(result)