import os
import pickle
import re
from textwrap import dedent
from typing import cast, NamedTuple

from cachier import cachier
from dotenv import load_dotenv
import openai
from openai.openai_object import OpenAIObject

load_dotenv()


class DropSampleNumber(NamedTuple):
    section_id: str
    query_id: str
    passage: str
    question: str
    number: float


class DropSampleSpan(NamedTuple):
    section_id: str
    query_id: str
    passage: str
    question: str
    span: str


DropSample = DropSampleNumber | DropSampleSpan


class DropSamples(NamedTuple):
    fb_number: list[DropSampleNumber]
    fb_span: list[DropSampleSpan]
    nfb_number: list[DropSampleNumber]
    nfb_span: list[DropSampleSpan]


openai.api_key = os.environ["OPENAI_API_KEY"]


def load_prompt_decomposition() -> str:
    with open("data/drop_ltm_decomposition.txt", "r", encoding="utf-8") as f:
        prompt_decomposition = f.read()
    return prompt_decomposition


def load_prompt_solving() -> str:
    with open("data/drop_ltm_solving.txt", "r", encoding="utf-8") as f:
        prompt_solving = f.read()
    return prompt_solving


def load_drop_samples() -> DropSamples:
    with open("data/drop_samples.pkl", "rb") as f:
        drop_samples = pickle.load(f)
    assert "DropSamples" in str(type(drop_samples))
    return cast(DropSamples, drop_samples)


prompt_decomposition = load_prompt_decomposition()
prompt_solving = load_prompt_solving()
drop_samples = load_drop_samples()


@cachier()
def generate_prompt(ds: DropSample) -> str:
    return dedent(
        f"""\
        "{prompt_decomposition}
        
        {prompt_solving}
        
        
        Q: {ds.passage} {ds.question}
        A: """
    )


# @cachier()
def parse_decomposed_questions_on_quote(l: str) -> list[str]:
    assert "\n" not in l
    assert "need to know" in l
    matches = []
    pat = re.compile(r'(?<=")[^"]+(?=")')
    curr_i = l.index("need to know")
    while True:
        match = pat.search(l, curr_i)
        if match is None:
            break
        matches.append(match.group())
        curr_i = match.span()[1] + 2
    return matches


@cachier()
def decompose_question(ds: DropSample) -> tuple[OpenAIObject, list[str] | None]:
    prompt = dedent(
        f"""\
        {prompt_decomposition}
        
        {ds.passage}
        Q: {ds.question}
        A: """
    )
    messages = [{"role": "user", "content": prompt}]
    completion = cast(
        OpenAIObject,
        openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages),
    )
    decomposition_line = next(
        (
            l
            for l in completion.choices[0].message.content.split("\n")
            if "need to know" in l
        ),
        None,
    )
    subquestions = (
        parse_decomposed_questions_on_quote(cast(str, decomposition_line))
        if decomposition_line is not None
        else None
    )
    return completion, subquestions


@cachier()
def answer_subquestion(prompt: str) -> tuple[OpenAIObject, str]:
    completion = cast(
        OpenAIObject,
        openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
        ),
    )
    answer: str = completion.choices[0].message.content
    return completion, answer


@cachier()
def answer_subquestions(
    qs: tuple[str, ...], ds: DropSample
) -> tuple[list[OpenAIObject], str]:
    prompt = dedent(
        f"""\
        {prompt_solving}

        {ds.passage}"""
    )
    completions = []
    for q in qs + (ds.question,):
        prompt += f"\n\nQ: {q}\nA: "
        completion, answer = answer_subquestion(prompt)
        completions.append(completion)
        prompt += answer
    return completions, prompt


def remove_commas_from_numerals(s: str) -> str:
    return re.sub(r"(?<=\d),(?=\d)", "", s)


def test_response(final_prompt: str, ds: DropSample, *, verbose: bool = False) -> bool:
    if isinstance(ds, DropSampleSpan):
        target = ds.span
    else:
        target = re.sub(r"\.0+\b", "", str(ds.number))
    last_answer = remove_commas_from_numerals(final_prompt[final_prompt.rfind("A:") :])
    result = target in last_answer
    if verbose:
        print(f"{last_answer = }\n{target = }\n{result = }")
    return result


def main() -> None:
    p = prompt_decomposition + "\n\n" + prompt_solving
    for i, l in enumerate(p.split("\n")):
        if "need to know" in l:
            parsed = parse_decomposed_questions_on_quote(l)
            print(f"[{i}] {l}\n{parsed}\n")


if __name__ == "__main__":
    main()
