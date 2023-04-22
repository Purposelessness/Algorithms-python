import pydotplus as pdot
from PIL import Image
import glob, os

debug = True
messy = True

class AhoCorasick:
    class Node:
        def __init__(self):
            self.term: bool = False
            self.link: int = -1
            self.up: int = 0
            self.to: dict[int, int] = {}
            self.children = set()
            self.depth: int = 0

    def __init__(self, alphabet: list):
        self.tries: list[AhoCorasick.Node] = []
        self.alphabet = set(alphabet)
        self.tries.append(self.Node())

    def search(self, text: str, substrings: list[str]) -> dict[str, list[int]]:
        substrings_dict: dict[str, list[int]] = {}
        for s in substrings:
            substrings_dict[s] = []
        v = 0
        for i in range(len(text)):
            c = ord(text[i])
            v = self.tries[v].to[c]
            u = v
            while u != 0:
                if self.tries[u].term:
                    s = text[i - self.tries[u].depth + 1 : i + 1]
                    if substrings_dict.__contains__(s):
                        substrings_dict[s].append(i - self.tries[u].depth + 1)
                u = self.tries[u].up
        return substrings_dict

    def search_masked(self, text: str, substring: str, mask: str) -> list[int]:
        subs_map: dict[str, list[int]] = {}
        subs_count: int = 0
        j = -1
        for i in range(len(substring)):
            if substring[i] == mask:
                if j < i - 1:
                    s = substring[j + 1 : i]
                    if not subs_map.__contains__(s):
                        subs_map[s] = []
                    subs_map[s].append(j + 1)
                    subs_count += 1
                j = i
        if j != len(substring) - 1:
            s = substring[j + 1:]
            if not subs_map.__contains__(s):
                subs_map[s] = []
            subs_map[s].append(j + 1)
            subs_count += 1
        if debug:
            print(f"Substrings in {substring} divided by mask:\n{subs_map}")

        occurences_count: list[int] = [0] * len(text)
        v = 0
        for i in range(len(text)):
            c = ord(text[i])
            v = self.tries[v].to[c]
            u = v
            while u != 0:
                if self.tries[u].term:
                    s_len = self.tries[u].depth
                    s = text[i - s_len + 1 : i + 1]
                    if subs_map.__contains__(s):
                        for z in subs_map[s]:
                            if (index := i - s_len - z + 1) >= 0:
                                occurences_count[index] += 1
                                if debug:
                                    print(f"Found substring {s} on position "
                                          f"{i - s_len + 1}")
                                    print("Occurense in template on position " 
                                          f"{index}")
                                    print(occurences_count)
                u = self.tries[u].up
        ans: list[int] = []
        for i in range(len(text) - len(substring) + 1):
            if occurences_count[i] == subs_count:
                ans.append(i)
        if debug:
            for i in range(len(occurences_count)):
                if i in ans:
                    print(f"\033[32m{occurences_count[i]}\033[0m", end='')
                else:
                    print(f"{occurences_count[i]}", end='')
            print('')
        return ans

    def add(self, s: str) -> None:
        v = 0
        for c in s:
            c = ord(c)
            if not self.tries[v].to.__contains__(c):
                self.tries.append(self.Node())
                self.tries[v].to[c] = len(self.tries) - 1
            u = self.tries[v].to[c]
            self.tries[v].children.add(c)
            self.tries[u].depth = self.tries[v].depth + 1
            v = u
        self.tries[v].term = True

    def resolve(self) -> None:
        t = self.tries
        for c in self.alphabet:
            c = ord(c)
            if not t[0].to.__contains__(c):
                t[0].to[c] = 0

        q = [0]
        while len(q) > 0:
            v = q.pop(0)
            for c in self.alphabet:
                c = ord(c)
                u = t[v].to[c]
                if t[u].link != -1:
                    continue
                if v == 0:
                    t[u].link = 0
                    t[u].up = 0
                else:
                    t[u].link = t[t[v].link].to[c]
                    if t[t[u].link].term:
                        t[u].up = t[u].link
                    else:
                        t[u].up = t[t[u].link].up
                for d in self.alphabet:
                    d = ord(d)
                    if t[u].to.__contains__(d):
                        continue
                    t[u].to[d] = t[t[u].link].to[d]
                q.append(u)

    @staticmethod
    def create_node(name: str, is_term: bool = False) -> pdot.Node:
        node = pdot.Node(name)
        node.set("style", "filled")
        node.set('fillcolor', 'white' if is_term else 'lightgray')
        return node

    @staticmethod
    def create_edge(src: str, dest: str, link: bool = False,
                    label: str = "", color: str = "") -> pdot.Edge:
        edge = pdot.Edge(src, dest)
        if link:
            edge.set('style', 'dashed')
            edge.set("arrowsize", 0.7)
        if label != "":
            edge.set("xlabel", label)
        if color != "":
            edge.set("color", color)
        return edge

    def get_graph(self) -> tuple[pdot.Dot, dict[int, pdot.Node]]:
        g = pdot.Dot(graph_type="digraph", strict=True)
        g.set("dpi", 144)

        t: list[AhoCorasick.Node] = self.tries
        q: list[tuple[int, str]] = []
        m: dict[int, str] = {0: ""}
        m_node: dict[int, pdot.Node] = {}
        ranks: dict[int, list[pdot.Node]] = {}

        node = self.create_node("")
        m_node[0] = node
        ranks[0] = [node]
        for c in self.alphabet:
            c = ord(c)
            v = t[0].to[c]
            if v != 0:
                m[v] = chr(c)
                q.append((v, chr(c)))
                g.add_edge(self.create_edge('', chr(c), label=chr(c)))
        while len(q) > 0:
            (v, s) = q.pop(0)
            if not ranks.__contains__(t[v].depth):
                ranks[t[v].depth] = []
            node = self.create_node(s, t[v].term)
            ranks[t[v].depth].append(node)
            m_node[v] = node
            g.add_edge(self.create_edge(s, m[t[v].up], link=True,
                                        color='dimgray'))
            if t[v].up != t[v].link:
                g.add_edge(self.create_edge(s, m[t[v].link], link=True, 
                                            color='lightgray'))
            for c in self.alphabet:
                c = ord(c)
                u = t[v].to[c]
                if t[u].depth > t[v].depth:
                    m[u] = s + chr(c)
                    q.append((u, s + chr(c)))
                    g.add_edge(self.create_edge(s, s + chr(c), label=chr(c)))
                # Too messy image...
                # elif messy and v != u and u != 0:
                #     edge = pdot.Edge(s, m[u])
                #     edge.set('label', chr(c))
                #     g.add_edge(edge)

        subgraph_index = 0
        for rank in ranks.keys():
            subgraph = pdot.Subgraph(str(subgraph_index))
            subgraph_index += 1
            for node in ranks[rank]:
                subgraph.add_node(node)
            subgraph.set("rank", "same")
            g.add_subgraph(subgraph)

        return (g, m_node)

    @staticmethod
    def select_node(graph: pdot.Dot, node: pdot.Node, frames_list: list):
        node.set('color', 'blue')
        node.set('fontcolor', 'blue')
        node.set('shape', 'rect')
        AhoCorasick.save_frame(graph, frames_list)

    @staticmethod
    def save_frame(graph: pdot.Dot, frames_list: list) -> None:
        num = len(frames_list)
        graph.write(f'{num}_tmp.png', format='png')
        frame = Image.open(f'{num}_tmp.png')
        frames_list.append(frame)

    @staticmethod
    def goto_node(graph: pdot.Dot, src: pdot.Node, dest: pdot.Node, frame_list: list) -> None:
        src.set('color', 'black')
        src.set('fontcolor', 'black')
        src.set('shape', 'ellipse')
        edges = graph.get_edge(src.get_name(), dest.get_name())
        if len(edges) > 0:
            edge = edges[0]
            edge.set('color', 'blue')
            edge.set('arrowsize', 1.3)
            AhoCorasick.save_frame(graph, frame_list)
            edge.set('color', 'black')
            edge.set('arrowsize', 1)
        dest.set('color', 'blue')
        dest.set('fontcolor', 'blue')
        dest.set('shape', 'rect')
        AhoCorasick.save_frame(graph, frame_list)

    def visual_search(self, text: str, substrings: list[str]) -> dict[str, list[int]]:
        (g, m) = self.get_graph()
        g.write('finite_state_machine.png', format='png')
        old_img = Image.open('finite_state_machine.png')
        img = Image.new(old_img.mode, (old_img.size[0], old_img.size[1] + 50), 'white')
        img.paste(old_img, (0, 0))
        img.save('finite_state_machine.png')
        frames_list: list[Image.Image] = []

        substrings_dict: dict[str, list[int]] = {}
        for s in substrings:
            substrings_dict[s] = []
        v = 0
        self.select_node(g, m[0], frames_list)
        for i in range(len(text)):
            c = text[i]
            c = ord(c)
            prev = v
            v = self.tries[v].to[c]
            self.goto_node(g, m[prev], m[v], frames_list)
            u = v
            while u != 0:
                if self.tries[u].term:
                    s = text[i - self.tries[u].depth + 1 : i + 1]
                    if substrings_dict.__contains__(s):
                        substrings_dict[s].append(i - self.tries[u].depth + 1)
                u = self.tries[u].up

        frames_list[0].save(
            '1.gif',
            save_all=True,
            append_images=frames_list[1:],
            optimize=True,
            duration=1000,
            loop=0
        )
        for f in glob.glob('*_tmp.png'):
            os.remove(f)

        return substrings_dict


def search(alphabet: list, text: str, substrings: list[str]) -> dict[str, list[int]]:
    solution = AhoCorasick(alphabet)
    for s in substrings:
        solution.add(s)
    solution.resolve()
    return solution.search(text, substrings)

def visual_search(alphabet: list, text: str, substrings: list[str]) -> dict[str, list[int]]:
    solution = AhoCorasick(alphabet)
    for s in substrings:
        solution.add(s)
    solution.resolve()
    return solution.visual_search(text, substrings)

def search_masked(alphabet: list, text: str, substring: str, mask: str) -> list[int]:
    solution = AhoCorasick(alphabet)
    substrings: list[str] = list(filter(lambda x: x != "", substring.split(mask)))
    for s in substrings:
        solution.add(s)
    solution.resolve()
    return solution.search_masked(text, substring, mask)

def visual_search_masked(alphabet: list, text: str, substring: str, mask: str) -> list[int]:
    solution = AhoCorasick(alphabet)
    substrings: list[str] = list(filter(lambda x: x != "", substring.split(mask)))
    for s in substrings:
        solution.add(s)
    solution.resolve()
    (g, m) = solution.get_graph()
    g.write('finite_state_machine.png', format='png')
    return solution.search_masked(text, substring, mask)

