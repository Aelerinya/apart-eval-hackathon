import os
from dotenv import load_dotenv

load_dotenv()

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]




def main() -> None:
    ...

if __name__ == "__main__":
    main()
