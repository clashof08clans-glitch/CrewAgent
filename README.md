# CrewAI Code Assistant Suite

A multi-agent AI toolkit built with [CrewAI](https://www.crewai.com/) for reviewing code and debugging entire project folders — all through one Streamlit app.

## Features

**🔍 Code Reviewer** — 5-agent pipeline (Code Reader → Bug Hunter, Quality Reviewer & Security Agent in parallel → Checklist Compiler) that reviews pasted or uploaded code and outputs a 🔴/🟡/🟢 prioritized checklist, downloadable as markdown.

**🐛 Project Debugger** — 3-agent pipeline (Navigator → File Reader → Resolution Agent) that takes a folder path + a plain-English problem description, locates the likely buggy file(s), and proposes a minimal fix.

## Tech Stack
- CrewAI + LiteLLM (`gemini/gemini-3.1-flash-lite`)
- Streamlit UI
- `FileReadTool` scoped to a runtime `base_dir` for safe file access

## Setup
```bash
git clone <your-repo-url>
cd crewAI
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
Add your key to `.env`:
```
GOOGLE_API_KEY=your_api_key_here
```
Run:
```bash
streamlit run app.py
```

## Project Structure
```
crewAI/
├── app.py         # Streamlit UI
├── crew.py         # Code Reviewer pipeline
├── debugger.py      # Project Debugger pipeline
└── requirements.txt
```

## License
MIT