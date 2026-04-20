from sentence_transformers import SentenceTransformer
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def GetSimilarity(query, strings):
    query_emb = model.encode(query)
    sentence_embs = model.encode(strings)
    scores = model.similarity(query_emb, sentence_embs)[0]
    
    return [(s, score.item()) for s, score in zip(strings, scores)]

def GetMostSimilar(query, strings):
    return max(GetSimilarity(query, strings), key=lambda pair: pair[1])

result = GetMostSimilar("It was a sunny day", [
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium.",
])

print(result)