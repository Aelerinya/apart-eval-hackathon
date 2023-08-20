from last_letter_least_to_most import Result
import pickle

with open("last_letter_least_to_most.pickle", "rb") as f:
    result: list[Result] = pickle.load(f)
    failures = [r for r in result if not r.success]
    for failure in failures:
        print(failure.words)
    print(failures[1].final_context)
