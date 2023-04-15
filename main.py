from modules.aho_corasick import search, visual_search


if __name__ == "__main__":
    text = "GACTACACA"
    substrings = ["ACAC", "AC", "A", "ACT", "GATC"]
    alphabet = ['A', 'C', 'G', 'T', 'N']
    res = visual_search(alphabet, text, substrings)
    print(res)

