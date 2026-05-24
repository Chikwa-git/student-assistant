"""Summarize a text or PDF using the configured model.

The function detects PDFs and extracts text before sending the
content to the model. Results are printed formatted for the terminal.
"""

from config import PROMPTS, MODEL
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader
from utils import format_response
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def summarize_text(argumento):
    """Summarize the content of a file (txt or PDF).

    Args:
        argumento: path to a text file or PDF to summarize.
    """
    if not os.path.exists(argumento):
        print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
        return

    file = os.path.splitext(argumento)

    if file[1].lower() == ".pdf":
        reader = PdfReader(argumento)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        file = text
    else:
        with open(argumento, "r", encoding="utf-8") as f:
            file = f.read()

    prompt = PROMPTS["resumir"]

    messages = [{"role": "system", "content": prompt},
                {"role": "user", "content": file}]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    print(format_response(response.choices[0].message.content))