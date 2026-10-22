import random
import re
from datetime import datetime

# ---------- Predefined responses (keyword -> list of possible replies) ----------
RESPONSES = {
    "greeting": {
        "keywords": ["hello", "hi", "hey", "good morning", "good evening"],
        "replies": ["Hi!", "Hello there!", "Hey! Nice to see you."],
    },
    "how_are_you": {
        "keywords": ["how are you", "how's it going", "how do you do"],
        "replies": ["I'm fine, thanks!", "Doing great, thanks for asking!"],
    },
    "thanks": {
        "keywords": ["thanks", "thank you"],
        "replies": ["You're welcome!", "No problem!", "Happy to help!"],
    },
    "joke": {
        "keywords": ["joke", "funny", "make me laugh"],
        "replies": [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why did the Python programmer wear glasses? He couldn't C!",
            "How many programmers does it take to change a light bulb? None, it's a hardware problem.",
        ],
    },
    "bot_name": {
        "keywords": ["your name", "who are you"],
        "replies": ["I'm PyBot, a simple rule-based chatbot."],
    },
}

HELP_TEXT = """You can try:
  - hello / how are you / thanks
  - my name is <your name>   (I'll remember it)
  - what is my name
  - what time is it / what is the date
  - tell me a joke
  - calculate 5 + 3          (supports + - * /)
  - history                  (shows our conversation)
  - help / bye"""


# ---------- Helper functions ----------
def normalize(text):
    """Lowercase the text and strip extra spaces/punctuation at the ends."""
    return text.strip().lower().rstrip("!?.")


def contains_keyword(message, keywords):
    """Check if any keyword appears as a whole word/phrase in the message."""
    for word in keywords:
        if re.search(r"\b" + re.escape(word) + r"\b", message):
            return True
    return False


def calculate(message):
    """Handle messages like 'calculate 12 * 4'."""
    match = re.search(r"(-?\d+\.?\d*)\s*([+\-*/])\s*(-?\d+\.?\d*)", message)
    if not match:
        return "Try something like: calculate 5 + 3"

    a, op, b = float(match.group(1)), match.group(2), float(match.group(3))

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    else:
        if b == 0:
            return "I can't divide by zero!"
        result = a / b

    # Show whole numbers without the trailing .0
    result = int(result) if result == int(result) else round(result, 4)
    return f"The answer is {result}."


def get_reply(message, memory):
    """Decide the chatbot's reply. 'memory' stores info like the user's name."""
    # 1. Remember the user's name
    name_match = re.search(r"my name is (\w+)", message)
    if name_match:
        memory["name"] = name_match.group(1).capitalize()
        return f"Nice to meet you, {memory['name']}!"

    # 2. Recall the user's name
    if "what is my name" in message or "who am i" in message:
        if "name" in memory:
            return f"Your name is {memory['name']}."
        return "I don't know your name yet. Tell me with 'my name is ...'"

    # 3. Time and date
    if "time" in message:
        return "The time is " + datetime.now().strftime("%I:%M %p") + "."
    if "date" in message or "today" in message:
        return "Today's date is " + datetime.now().strftime("%d %B %Y") + "."

    # 4. Calculator
    if message.startswith("calculate"):
        return calculate(message)

    # 5. Help
    if message == "help":
        return HELP_TEXT

    # 6. Keyword-based replies
    for category in RESPONSES.values():
        if contains_keyword(message, category["keywords"]):
            return random.choice(category["replies"])

    # 7. Fallback
    return random.choice([
        "Sorry, I don't understand that. Type 'help' to see what I can do.",
        "Hmm, I'm not sure about that. Try 'help'.",
    ])


def show_history(history):
    """Print the conversation so far."""
    if not history:
        print("PyBot: We haven't talked yet.")
        return
    print("PyBot: Here's our conversation:")
    for speaker, text in history:
        print(f"  {speaker}: {text}")


# ---------- Main chat loop ----------
def chatbot():
    memory = {}
    history = []
    exit_words = ["bye", "exit", "quit"]

    print("PyBot: Hello! I'm PyBot. Type 'help' to see what I can do.")

    while True:
        user_input = input("You: ")
        message = normalize(user_input)

        if message == "":
            print("PyBot: Please type something.")
            continue

        if message in exit_words:
            name = memory.get("name", "")
            print(f"PyBot: Goodbye{', ' + name if name else ''}!")
            break

        if message == "history":
            show_history(history)
            continue

        reply = get_reply(message, memory)
        print("PyBot:", reply)

        history.append(("You", user_input))
        history.append(("PyBot", reply))


if __name__ == "__main__":
    chatbot()