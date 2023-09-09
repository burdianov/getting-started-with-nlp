import os
import codecs


def read_in(folder) -> list[str]:
    absolute_path = os.path.join(os.getcwd(), folder)
    files: list[str] = os.listdir(absolute_path)
    a_list: list[str] = []
    for a_file in files:
        if not a_file.startswith("."):
            f = codecs.open(
                os.path.join(absolute_path, a_file),
                "r",
                encoding="ISO-8859-1",
                errors="ignore",
            )
            a_list.append(f.read())
            f.close()
    return a_list


spam_list = read_in("./datasets/enron1/spam")
ham_list = read_in("./datasets/enron1/ham")

print(len(spam_list))
print(len(ham_list))

print(spam_list[0])
print(ham_list[0])
