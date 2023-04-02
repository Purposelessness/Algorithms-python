from modules.prefix_function import prefix_function


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
