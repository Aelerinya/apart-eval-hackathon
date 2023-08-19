import os
from typing import cast
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

drop_number_samples = pd.read_csv("data/drop_number_not_football_samples.csv")
drop_span_samples = pd.read_csv("data/drop_span_not_football_samples.csv")
with open("data/drop_ltm_decomposition.txt", "r", encoding="utf-8") as f:
    prompt_decomposition = f.read()
with open("data/drop_ltm_solving.txt", "r", encoding="utf-8") as f:
    prompt_solving = f.read()

Target = float | str


def generate_prompt(row: pd.Series) -> tuple[str, Target]:
    prompt = f"{prompt_decomposition}\n\n{prompt_solving}\n\n"
    prompt += f"Q: {row['passage']} {row['question']}\nA:"
    target = cast(float, row["number"]) if "number" in row else cast(str, row["span"])
    return prompt, target


def main() -> None:
    # print(len(drop_number_samples))
    # print(len(drop_span_samples))
    # print(len(prompt_decomposition))
    # print(len(prompt_solving))
    prompt, target = generate_prompt(drop_number_samples.iloc[0])
    print(prompt)
    print(target)
    print(60 * "=")

    prompt, target = generate_prompt(drop_span_samples.iloc[0])
    print(prompt)
    print(target)


if __name__ == "__main__":
    main()
