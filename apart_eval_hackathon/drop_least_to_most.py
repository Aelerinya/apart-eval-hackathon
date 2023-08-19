import openai
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()


openai.api_key = os.environ["OPENAI_API_KEY"]

drop_number_samples = pd.read_csv("drop_number_samples.csv")
drop_span_samples = pd.read_csv("drop_span_samples.csv")


def main() -> None:
    print(drop_number_samples)
    print(drop_span_samples)


if __name__ == "__main__":
    main()
