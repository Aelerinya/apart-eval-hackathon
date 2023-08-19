import openai
from dotenv import load_dotenv

load_dotenv()


# Q, "transformer, language"
# A: The last letter of "transformer" is "r". The last letter of "language" is "e". Concatenating "r", "e" leads to "re". So, "transformer, language" outputs "re".
# R: "re"

# Q: "transformer, language, vision"

base_prompt = """
Q: "think, machine"
A: The last letter of "think" is "k". The last letter of "machine" is "e". Concatenating "k", "e" leads to "ke". So, "think, machine" outputs "ke".
R: "ke"

Q: "think, machine, learning"
A: "think, machine" outputs "ke". The last letter of "learning" is "g". Concatenating "ke", "g" leads to "keg". So, "think, machine, learning" outputs "keg".
R: "keg"
"""


def prompt_last_letters(
    words: list[str], preprompt: str = base_prompt
) -> tuple[str, str]:
    wordlist = ", ".join(words)
    prompt = preprompt + f'\n\nQ: "{wordlist}"\n'
    # print("Prompt:")
    # print(prompt)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    answer: str = completion.choices[0].message.content
    print("Answer:")
    print(answer)
    result: str = answer.split("R: ")[1].strip('"')
    # print("Result:", result)
    return result, prompt + answer


def least_to_most_last_letters(words: list[str]) -> str:
    prompt = base_prompt
    for i in range(2, len(words) + 1):
        subsequence = words[:i]
        print("Subsequence:", subsequence)
        result, context = prompt_last_letters(subsequence, prompt)
        print("Result:", result)
        prompt = context
    print("Final prompt:")
    print(prompt)
    return result


def last_letters(words: list[str]) -> str:
    last_letters = [word[-1] for word in words]
    return "".join(last_letters)


if __name__ == "__main__":
    words = [
        "transformer",
        "language",
        "vision",
        "learning",
        # "machine",
        # "think",
        # "ai",
        # "robot",
        # "human",
        # "computer",
        # "intelligence",
        # "artificial",
        # "neural",
        # "network",
        # "deep",
        # "learning",
        # "supervised",
        # "unsupervised",
        # "reinforcement",
        # "learning",
    ]
    result = least_to_most_last_letters(words)
    expected = last_letters(words)
    print("Expected:", expected)
    print("Result:", result)
    print(f"The answer is {'correct' if result == expected else 'incorrect'}.")
