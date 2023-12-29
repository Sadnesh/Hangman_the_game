"""take a word from the dictonary and ask user to guess the word and provide the word's no count only and mark how many words the user provided
cannot provide same letter twice 
cannot have more than 6 guesses"""

# from functools import partial # we can import this as well
import random as ran

hangman_states = [
    """
    +---+
    |   |
        |
        |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
        |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
    |   |
        |
        |
    =========
    """,
    """
    +---+
    |   |
    O   |
   /|   |
        |
        |
    =========
    """,
    r"""
    +---+
    |   |
    O   |
   /|\  |
        |
        |
    =========
    """,
    r"""
    +---+
    |   |
    O   |
   /|\  |
   /    |
        |
    =========
    """,
    r"""
    +---+
    |   |
    O   |
   /|\  |
   / \  |
        |
    =========
    """,
]


def index_generator():
    index = ran.randrange(0, 370105)
    # index = ran.randrange(0, 10)
    return index


def word_generator(dic):
    index = index_generator()
    line = dic[index].strip()
    if len(line) >= 3:
        return line
    else:
        return word_generator(dic)


def display_used(used_letters, dic_word):
    for i in used_letters:
        if not i in dic_word:
            print(f"\x1b[9m{i}\x1b[m", end=" ")


def display(word_count):
    for letter, found in word_count:
        if found:
            print(letter, end=" ")
        else:
            print("_", end=" ")
    print("\n")


def checker(user_letter, item):
    return (item[0], 1) if user_letter == item[0] or item[1] == 1 else (item[0], 0)


def partial(fir, *args, **kwargs):
    # return lambda x: fir(x, *args, **kwargs)

    def _inner(x):
        return fir(*args, x, **kwargs)

    return _inner


def body_displayer(n):
    print(hangman_states[n])


def main():
    n = 0
    dic = open("dictonary.txt", "r").readlines()
    dic_word = ""
    used_letters = []
    dic_word = word_generator(dic)
    word_count = [(i, 0) for i in dic_word]
    display(word_count)
    display_used(used_letters, dic_word)
    body_displayer(0)
    while True:
        guess_letter = input("\nEnter your guess (same letter not allowed twice):  \n")
        if not guess_letter in used_letters:
            used_letters.append(guess_letter)

            if guess_letter in dic_word:
                # word_count = [(i, 1) if guess_letter == i[0] else (i, 0) for i in word_count]
                word_count = list(map(partial(checker, guess_letter), word_count))
                body_displayer(n)
            else:
                print("Bro you suck\a")
                n += 1
                body_displayer(n)
                if n == len(hangman_states) - 1:
                    print("You are doomed")
                    print(f"BTW the actual answer was {dic_word}")
                    break
            # De Morgan's law is used here---
            # if not any([i[1] != 1 for i in word_count]):
            # if any([i[1] != 1 for i in word_count]) == False:
            # if all([i[1] == 1 for i in word_count]):
            if len(list(filter(lambda x: x[1] != 1, word_count))) == 0:
                print(f"You did it and the word was {dic_word}")
                break
        else:
            print(
                "How many times do I have to tell you, you can't use same letter twice!"
            )

        display(word_count)
        display_used(used_letters, dic_word)


if __name__ == "__main__":
    main()
