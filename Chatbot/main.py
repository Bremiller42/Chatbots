import os
import json
from difflib import get_close_matches

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "knowledge_base.json")

def load_knowledge_base(file_path: str) -> dict:                # Loading all previous interactions from JSON
    with open(file_path, 'r') as file:
        data: dict = json.load(file)

    return data


def save_knowledge_base(file_path: str, data: dict):            # Saves all interactions to JSON
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)    # n is amount of respones, cutoff is accuracy
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]


def chat_bot():
    knowledge_base: dict = load_knowledge_base(file_path)

    while True:
        user_input: str = input("You: ")
        if user_input.lower() == 'quit':
            break
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f"Bot: {answer}")
        else:
            print("Bot: I Don't understand, can you teach me?")
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base(file_path, knowledge_base)
                print("Bot: Thank you I learned a new response")

if __name__ == "__main__":
    chat_bot()



