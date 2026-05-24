"""Explain a concept by sending the user input to the model.

This module sends the user's prompt to the model using the
`explicar` prompt template and prints a formatted response. After the
initial reply the user can ask follow-up questions in a short loop.
"""

from config import PROMPTS, MODEL
from dotenv import load_dotenv
from groq import Groq
from utils import format_response
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def explain_concept(argumento):
    """Send a concept question to the model and interact for follow-ups.

    Args:
        argumento: question or topic text to explain.
    """
    prompt = PROMPTS["explicar"]

    messages = [{"role": "system", "content": prompt},
                {"role": "user", "content": argumento}]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    # Print formatted assistant answer
    print(format_response(response.choices[0].message.content))

    messages.append({"role": "assistant", "content": response.choices[0].message.content})

    # Short interactive loop for clarifying questions.
    while True:
        question = input("\nFicou alguma dúvida? (s/n) ").strip().lower()

        if question == "s":
            user_question = input("\nQual é a sua dúvida? ")
            messages.append({"role": "user", "content": user_question})

            follow_up_response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )

            print("\n" + format_response(follow_up_response.choices[0].message.content))
            messages.append({"role": "assistant", "content": follow_up_response.choices[0].message.content})
        elif question == "n":
            print("Ótimo! Se tiver mais dúvidas no futuro, é só perguntar.")
            break
        else:
            print("Resposta inválida. Por favor, responda com 's' ou 'n'.")