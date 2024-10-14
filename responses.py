from random import choice, randint

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == "":
        return "You do be silent"
    elif "hello" in lowered:
        return "Hey there!"
    elif "how are you" in lowered:
        return "I'm doing good, thanks for asking!"
    elif "bye" in lowered:
        return "Goodbye!"
    elif "roll dice" in lowered:
        return f"You rolled: {randint(1, 6)}"
    else:
        return choice([
            "I'm not sure I understand...",
            "What does that mean?",
            "I'm not programmed to answer that..."
        ])

