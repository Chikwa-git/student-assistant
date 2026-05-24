# Student Assistant CLI

A command-line study assistant powered by Groq (Llama 3.3 70B), built to support learning in programming and AI topics. Designed for personal use during CS50AI and beyond.

## Features

| Command | Description |
|---|---|
| `explicar` | Explains a programming or AI concept didactically |
| `revisar` | Reviews a code file and provides structured feedback |
| `resumir` | Summarizes a `.txt` or `.pdf` study material |
| `erro` | Interprets a Python/C error message and guides debugging |
| `matematica` | Explains math concepts applied to programming and AI |

All commands support a follow-up loop — after each response, you can keep asking questions with full conversation context.

## Requirements

- Python 3.10+
- Groq API key (free tier at [console.groq.com](https://console.groq.com))

## Installation

```bash
git clone https://github.com/Chikwa-git/student-assistant
cd student-assistant
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_api_key_here
```

## Usage

```bash
# Explain a concept
python study.py explicar "what is a Bayesian network"

# Review a code file
python study.py revisar /path/to/your/file.py

# Summarize a study material
python study.py resumir /path/to/notes.pdf

# Analyze an error message
python study.py erro "TypeError: unsupported operand type(s) for +: 'int' and 'str'"

# Explain a math concept
python study.py matematica "what is conditional probability"
```

## Project Structure

```
student-assistant/
├── study.py          # Entry point, argument parsing
├── config.py         # API config, model, system prompts
├── utils.py          # Terminal formatting utilities
├── commands/
│   ├── explain.py
│   ├── revise.py
│   ├── summarize.py
│   ├── error.py
│   └── math.py
├── .env              # API key (not committed)
└── requirements.txt
```

## Tech Stack

- [Groq API](https://console.groq.com) — Llama 3.3 70B inference
- [python-dotenv](https://pypi.org/project/python-dotenv/) — environment variable management
- [pypdf](https://pypi.org/project/pypdf/) — PDF text extraction

## About

Built as a personal productivity tool while studying CS50AI. Part of a broader portfolio that includes [Radar Político](https://github.com/Chikwa-git/political-tracker) and [DataComex](https://github.com/Chikwa-git/DataComex).
