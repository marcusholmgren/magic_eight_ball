import random
import time

def magic_8_ball():
    """
    A simple Magic 8-Ball game that provides answers to user questions.
    """
    answers = [
        "The answer is unclear",
        "Uncertain at this time",
        "I have no idea",
        "Absolutely yes!",
        "Ask again later",
        "Emphatically No!",
        "Signs point to yes, definitely!",
        "My sources say no, but they've been wrong before.",
        "Reply hazy, try again after a coffee.",
        "It is decidedly so.",
        "Outlook not so good, maybe ask your cat?",
        "You may rely on it.",
        "Error 404: Future not found."
    ]

    print("--- Magic 8-Ball ---")
    print("Ask me a question, and I will tell you your future. (Type 'quit' to exit)")

    while True:
        question = input("\nYour question: ")

        if question.lower() == 'quit':
            print("Goodbye!")
            break

        if not question.strip():
            print("You must ask a question!")
            continue

        print("Thinking...")
        time.sleep(1)  # A small delay to simulate thinking

        chosen_answer = random.choice(answers)
        print(f"\nAnswer: {question}? ... {chosen_answer}")


if __name__ == "__main__":
    magic_8_ball()
