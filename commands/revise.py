"""Review the given source file using the configured model.

This command reads the file at `argumento`, sends its contents to the
model using the `revisar` prompt and prints the formatted review. If the
file path does not exist a helpful message is printed.
"""

from config import PROMPTS, MODEL
from dotenv import load_dotenv
from groq import Groq
from utils import format_response
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def review_code(argumento):
    """Read a file and request a code review from the model.

    Args:
        argumento: filesystem path to a source file to review.
    """
    if not os.path.exists(argumento):
        print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
        return
    
    with open(argumento, "r", encoding="utf-8") as f:
        file = f.read()

    prompt = PROMPTS["revisar"]

    messages = [{"role": "system", "content": prompt},
                {"role": "user", "content": file}]

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