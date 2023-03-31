def kmp(string: str, word: str) -> list[int]:
    ans: list[int] = []
    pi = prefix_function(word)
    w = 0
    for s in range(len(string)):
        while w > 0 and string[s] != word[w]:
            w = pi[w - 1]
        if string[s] == word[w]:
            w += 1
            if w == len(word):
                ans.append(s - w + 1)
                w = pi[w - 1]
    return ans


def prefix_function(word: str) -> list[int]:
    pi = [0] * len(word)
    j = 0
    i = 1
    while i < len(word):
        if word[i] == word[j]:
            pi[i] = j + 1
            i += 1
            j += 1
        elif j == 0:
            pi[i] = 0
            i += 1
        else:
            j = pi[j - 1]
    return pi
