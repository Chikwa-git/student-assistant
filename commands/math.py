"""Explain mathematical concepts using the configured model.

This module forwards the user input to the `matemática` prompt and then
prints the model output. A follow-up interaction allows clarification
questions from the user.
"""

from config import PROMPTS, MODEL
from dotenv import load_dotenv
from groq import Groq
from utils import format_response
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def explain_math(argumento):
    """Send a math question to the model and support follow-ups.

    Args:
        argumento: string with the mathematical question or topic.
    """
    prompt = PROMPTS["matemática"]

    messages = [{"role": "system", "content": prompt},
                {"role": "user", "content": argumento}]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    print(format_response(response.choices[0].message.content))

    messages.append({"role": "assistant", "content": response.choices[0].message.content})

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