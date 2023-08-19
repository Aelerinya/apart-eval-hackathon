from typing import NamedTuple, cast
import openai
from dotenv import load_dotenv

from apart_eval_hackathon.english_words import random_words

load_dotenv()

Result = NamedTuple(
    "Result", [("success", bool), ("words", list[str]), ("final_context", str), ("answers", list[str])])

base_prompt = """
Q: "think, machine"
A: The last letter of "think" is "k". The last letter of "machine" is "e". Concatenating "k", "e" leads to "ke". So, "think, machine" outputs "ke".

Q: "think, machine, learning"
A: "think, machine" outputs "ke". The last letter of "learning" is "g". Concatenating "ke", "g" leads to "keg". So, "think, machine, learning" outputs "keg".

Q: "transformer, language"
A: The last letter of "transformer" is "r". The last letter of "language" is "e". Concatenating: "r", "e"
leads to "re". So, "transformer, language" outputs "re".
Q: "transformer, language, vision"
A: "transformer, language" outputs "re". The last letter of "vision" is "n". Concatenating: "re", "n" leads
to "ren". So, "transformer, language, vision" outputs "ren".
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
    answer: str = cast(str, completion.choices[0].message.content)
    # print("Answer:")
    # print(answer)
    result: str = answer.strip('". \n')
    result = result[result.rfind('"') + 1:]
    assert result.isalpha()
    # print("Result:", result)
    return result, prompt + answer


def least_to_most_last_letters(words: list[str]) -> Result:
    print("Words:", words)
    prompt = base_prompt
    result = ""
    answers: list[str] = []
    expected = ""
    for i in range(2, len(words) + 1):
        subsequence = words[:i]
        print("Subsequence:", subsequence)
        result, context = prompt_last_letters(subsequence, prompt)
        print("Result:", result)
        answers.append(result)
        prompt = context
        expected = last_letters(subsequence)
        if result != expected:
            print("Failure after", i, "words")
            break
    else:
        print("Success")

    # print("Final prompt:")
    # print(prompt)
    return Result(success=result == expected, words=words, answers=answers, final_context=prompt)


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
    # result = least_to_most_last_letters(words)
    # print(result)
    # print(prompt_last_letters(["think", "machine"]))

    results: list[Result] = []
    for i in range(10):
        words = random_words(10)
        result = least_to_most_last_letters(words)
        results.append(result)

    # save as pickle
    import pickle
    with open("last_letter_least_to_most.pickle", "wb") as f:
        pickle.dump(results, f)
