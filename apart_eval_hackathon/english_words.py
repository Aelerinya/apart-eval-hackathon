from os.path import dirname

path = dirname(__file__) + "/english_words.txt"


def english_words_dataset() -> list[str]:
    with open(path, "r") as f:
        return f.read().lower().splitlines()


def random_words(count: int) -> list[str]:
    from random import sample

    return sample(english_words_dataset(), count)


if __name__ == "__main__":
    print(random_words(10))
