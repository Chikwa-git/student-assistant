"""Interactive helper to interpret Python tracebacks using the model.

This function sends the provided `argumento` (expected to be an error
traceback or error message) to the configured model and prints a
formatted response. After the initial answer it enters a short
interactive loop that lets the user ask follow-up questions.
"""

from config import PROMPTS, MODEL
from dotenv import load_dotenv
from groq import Groq
from utils import format_response
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def interpret_error(argumento):
    """Send an error traceback to the model and interact with the user.

    Args:
        argumento: string containing the traceback or error context.
    """
    prompt = PROMPTS["erro"]

    messages = [{"role": "system", "content": prompt},
                {"role": "user", "content": argumento}]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    # Print initial formatted assistant response
    print(format_response(response.choices[0].message.content))

    # Keep conversation history for follow-ups
    messages.append({"role": "assistant", "content": response.choices[0].message.content})

    # Interactive follow-up loop.
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