import heapq
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def get_similarity(query, strings):
    query_emb = model.encode(query)
    sentence_embs = model.encode(strings)
    scores = model.similarity(query_emb, sentence_embs)[0]

    return [(s, score.item()) for s, score in zip(strings, scores)]

def get_n_most_similar(query, strings, size):
    return heapq.nlargest(size, get_similarity(query, strings), key=lambda pair: pair[1])

def get_most_similar(query, strings):
    return get_n_most_similar(query, strings, 1)[0]