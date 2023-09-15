from typing import NamedTuple, Optional, cast
import openai
from dotenv import load_dotenv
from tqdm import trange
import pickle

from english_words import random_words

load_dotenv()


class Prediction(NamedTuple):
    success: bool
    words: list[str]
    answer: Optional[str]
    completion: str


class Result(NamedTuple):
    words: list[str]
    subsequence_predictions: list[Prediction]
    final_predictions: list[Prediction]
    final_context: str


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
) -> tuple[Prediction, str]:
    wordlist = ", ".join(words)
    prompt = preprompt + f'\n\nQ: "{wordlist}"\n'
    while True:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                request_timeout=5,
            )
            break
        except Exception as e:
            print(e)
            if input("Continue ? (y/n)") != "y":
                raise e

    completion: str = cast(str, completion.choices[0].message.content)
    try:
        answer: str = completion.strip('". \n')
        answer = answer[answer.rfind('"') + 1 :]
        assert answer.isalpha()
    except:
        return Prediction(False, words, None, completion), prompt + completion

    expected = last_letters(words)
    return (
        Prediction(expected == answer, words, answer, completion),
        prompt + completion,
    )


def least_to_most_last_letters(words: list[str], *, bar) -> Result:
    bar.write(f"Words: {words}")
    prompt = base_prompt

    subsequence_predictions: list[Prediction] = []
    final_predictions: list[Prediction] = []

    final_prediction, final_prompt = prompt_last_letters(words, prompt)
    final_predictions.append(final_prediction)

    for i in range(2, len(words)):
        subsequence = words[:i]
        bar.write(f"Subsequence: {subsequence}")
        subsequence_prediction, new_prompt = prompt_last_letters(subsequence, prompt)
        subsequence_predictions.append(subsequence_prediction)
        prompt = new_prompt
        bar.write(f"Prediction: {subsequence_prediction}")

        final_prediction, final_prompt = prompt_last_letters(words, new_prompt)
        final_predictions.append(final_prediction)
        bar.write(f"Final prediction: {final_prediction}")

    return Result(
        words=words,
        subsequence_predictions=subsequence_predictions,
        final_predictions=final_predictions,
        final_context=final_prompt,
    )


def last_letters(words: list[str]) -> str:
    last_letters = [word[-1] for word in words]
    return "".join(last_letters)


if __name__ == "__main__":
    results: list[Result] = []
    bar = trange(100)
    for i in bar:
        words = random_words(7)
        result = least_to_most_last_letters(words, bar=bar)
        results.append(result)

    with open("last_letter_least_to_most.pickle", "wb") as f:
        pickle.dump(results, f)
