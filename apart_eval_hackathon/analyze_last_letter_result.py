from last_letter_least_to_most import Result
import pickle

with open("last_letter_least_to_most.pickle", "rb") as f:
    result: list[Result] = pickle.load(f)
    print(result)
