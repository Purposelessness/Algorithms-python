from modules.aho_corasick import search, visual_search, search_masked, visual_search_masked
from string import ascii_lowercase


if __name__ == "__main__":
    alphabet = ['A', 'C', 'G', 'T', 'N']
    
    # first task
    text = input()
    substrings = []
    n = int(input())
    for i in range(n):
        substrings.append(input())
    res = search(alphabet, text, substrings)
    ans: list[tuple[int, int]] = []
    i = 0
    for k in res.keys():
        for j in res[k]:
            ans.append((j, i))
        i += 1
    ans.sort()
    for p in ans:
        print(p[0] + 1, p[1] + 1)
    res = visual_search(alphabet, text, substrings)

    # second task
    # text = input()
    # substring = input()
    # mask = input()
    # res = visual_search_masked(alphabet, text, substring, mask)
    # print(' '.join(list(map(lambda x: str(x + 1), res))))

