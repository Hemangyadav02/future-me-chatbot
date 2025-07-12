"""
chatbot.py – Future Me: GPT-3.5 Career Counselling Chatbot
"""

import openai
import os
import time
from dotenv import load_dotenv

# --- Load environment variables from .env ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Check if API key is loaded
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found. Did you create a .env file?")
    exit(1)

openai.api_key = api_key

# --- System prompt: initial instruction to GPT ---
system_prompt = {
    "role": "system",
    "content": (
        "You are 'Future Me', a top-tier AI career counsellor for students aged 16–25. "
        "You give personalized, friendly, and structured guidance with 4–6 bullet points or steps. "
        "Support answers with real tools (Coursera, Kaggle, GitHub), job advice, motivation, and roadmap breakdowns."
    )
}

# --- Memory of the conversation ---
messages = [system_prompt]

# --- Typing animation before bot responds ---
def typing_animation():
    print("Future Me is typing", end="", flush=True)
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print("\n")

# --- Save each chat to file ---
def save_to_log(user_input, bot_reply):
    with open("chatlog.txt", "a", encoding="utf-8") as file:
        file.write(f"User: {user_input}\n")
        file.write(f"Future Me: {bot_reply}\n\n")

# --- Ask GPT-3.5 and get a reply ---
def get_response(user_input):
    messages.append({"role": "user", "content": user_input})
    typing_animation()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ✅ updated to 3.5
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0.3
        )
        reply = response['choices'][0]['message']['content']
        messages.append({"role": "assistant", "content": reply})
        save_to_log(user_input, reply)
        return reply
    except Exception as e:
        return f"⚠️ Error: {e}"

# --- Clean user input for roadmap prompts ---
def clean_career_input(raw_input):
    career = raw_input.lower().split("roadmap")[-1].strip()
    for prefix in ["to become a", "to be a", "become a", "a", "an"]:
        if career.startswith(prefix):
            career = career[len(prefix):].strip()
    return career or "data scientist"

# --- Choose bot personality ---
def choose_personality():
    print("\nChoose your counsellor's personality:")
    print("1. Friendly Mentor\n2. Professional Recruiter\n3. Visionary Guide")
    choice = input("Enter 1, 2, or 3: ").strip()
    if choice == "2":
        messages[0]["content"] = messages[0]["content"].replace("friendly", "professional recruiter")
    elif choice == "3":
        messages[0]["content"] = messages[0]["content"].replace("friendly", "visionary guide")
    else:
        messages[0]["content"] = messages[0]["content"].replace("friendly", "friendly mentor")

# --- Main chatbot loop ---
def main():
    print("\n🎓 Welcome to Future Me – Your AI Career Counsellor")
    print("Type 'exit' to quit, or 'clear chat' to reset the session.\n")

    choose_personality()
    print("\n✅ Ready! Ask me anything about your career.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("👋 Goodbye! Keep building your future. 🚀")
            break

        elif user_input.lower() == "clear chat":
            print("🧹 Chat memory cleared!\n")
            global messages
            messages = [system_prompt]
            continue

        elif "score my resume" in user_input.lower():
            user_input = (
                "Please score my resume as if I'm a 3rd-year student applying for internships. "
                "Give me 5 detailed, actionable improvement tips. Mention actual phrases, bullet structures, or sections I should add."
            )

        elif "roadmap" in user_input.lower():
            career = clean_career_input(user_input)
            user_input = (
                f"Give me a 5-step practical roadmap to become a {career}. "
                f"Include tools, platforms, projects, and milestones I can follow."
            )

        bot_reply = get_response(user_input)
        print(f"\nFuture Me: {bot_reply}\n")

if __name__ == "__main__":
    main()
