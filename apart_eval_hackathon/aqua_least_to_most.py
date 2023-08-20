from datasets import load_dataset
import pandas as pd
import nltk.data

openai.api_key = os.environ["OPENAI_API_KEY"]

decomposition_prompt = """
Q: A company produces 420 units of a particular computer component every month, at a production cost to the company of $110 per component, and sells all of the components by the end of each month. What is the minimum selling price per component that will guarantee that the yearly profit (revenue from sales minus production costs) will be at least $626,400?
A)7, B)8, C)10, D)11, E)12
A: To answer the question "What is the minimum selling price per component that will guarantee that the yearly profit (revenue from sales minus production costs) will be at least $626,400?", we need to know: "How many units does the company produce yearly?", "What would have to be the revenue per unit for the yearly revenue to be at least $626,400?", "What would the price have to be to include the 100$ cost and the desired revenue?"
"""


def main():
    dataset = load_dataset("aqua_rat")
    df = pd.DataFrame(dataset["test"])


if __name__ == "__main__":
    main()
