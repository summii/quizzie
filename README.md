# Quizzie - A Trivia Game

A command-line trivia game that generates questions using Ollama's Mistral model.

## Prerequisites

- Python 3.8 or higher
- uv package manager
- Ollama with Mistral model installed

## Installation

1. First, install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repository:
```bash
git clone <repository-url>
cd quizzie
```

3. Create a virtual environment and install dependencies using uv:
```bash
uv venv
uv pip install rich requests
```

4. Make sure Ollama is running with Mistral model:
```bash
ollama run mistral
```

## Running the Game

1. Activate the virtual environment:
```bash
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

2. Run the game:
```bash
uv run quizzie.py
```

## How to Play

1. When prompted, type 'yes' to start playing
2. Choose a category from the available options
3. Answer the trivia questions
4. Type 'no' when you want to end the game

## Features

- Multiple categories: History, Geography, Arts, Sports
- AI-generated questions about India using Mistral
- Intelligent answer checking
- Colorful command-line interface

## Dependencies

- rich: For beautiful command-line interface
- requests: For API calls to Ollama
- Ollama: For generating questions using Mistral model
