import re
from konlpy.tag import Okt
from collections import Counter
import networkx
import itertools

def xplit(*delimiters):
    return lambda value: re.split('|'.join([re.escape(delimiter) for delimiter in delimiters]), value)

class Sentence:
    @staticmethod
    def co_occurence(sentence1, sentence2):
        p = sum((sentence1.bow & sentence2.bow).values())
        q = sum((sentence1.bow | sentence2.bow).values())
        return p / q if q else 0

    def __init__(self, text, index=0):
        self.okt = Okt()
        self.index = index
        self.text = text
        self.nouns = self.okt.nouns(self.text)
        self.bow = Counter(self.nouns)

    def __eq__(self, another):
        return hasattr(another, 'index') and self.index == another.index

    def __hash__(self):
        return self.index


def get_sentences(text):
    candidates = xplit('. ', '? ', '! ', '\n', '.\n')(text.strip())
    sentences = []
    index = 0
    for candidate in candidates:
        candidate = candidate.strip()
        if len(candidate) != 0:
            sentences.append(Sentence(candidate, index))
            index += 1
    return sentences


def build_graph(sentences):
    graph = networkx.Graph()
    graph.add_nodes_from(sentences)
    pairs = list(itertools.combinations(sentences, 2))
    for eins, zwei in pairs:
        graph.add_edge(eins, zwei, weight=Sentence.co_occurence(eins, zwei))
    return graph


def summarize(text, limit=3):
    results = []
    sentences = get_sentences(text)
    graph = build_graph(sentences)
    pagerank = networkx.pagerank(graph, weight='weight')
    reordered = sorted(pagerank, key=pagerank.get, reverse=True)

    for sentence in reordered[:limit]:
        results.append(sentence.text)
    
    return results