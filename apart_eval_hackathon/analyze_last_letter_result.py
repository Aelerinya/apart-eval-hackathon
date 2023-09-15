from last_letter_least_to_most import Result, Prediction
import pickle

with open("last_letter_least_to_most.pickle", "rb") as f:
    result: list[Result] = pickle.load(f)
    # failures = [r for r in result if not r.success]
    # for failure in failures:
    #     print(failure.words)
    # print(failures[1].final_context)
    # for r in result:
    #     print(r.words)
    #     for i in range(len(r.subsequence_predictions)):
    #         print(
    #             "Final",
    #             r.final_predictions[i].success,
    #             r.final_predictions[i].answer or r.final_predictions[i].completion,
    #         )
    #         print(
    #             "Sub",
    #             r.subsequence_predictions[i].success,
    #             r.subsequence_predictions[i].answer
    #             or r.subsequence_predictions[i].completion,
    #         )
    #     print("Final", r.final_predictions[-1].success, r.final_predictions[-1].answer)
    dip = (
        str(i)
        + repr(r.words)
        + "\n"
        + r.final_predictions[4].completion
        + "\n"
        + r.final_context
        for i, r in enumerate(result)
        if r.final_predictions[3].success
        and not r.final_predictions[4].success
        and r.final_predictions[5].success
    )
    print(*dip, sep="\n====================\n")
    # print(len(list(dip)))
    # print(result[96].final_context)
    # print(result[96].final_predictions[1].completion)
