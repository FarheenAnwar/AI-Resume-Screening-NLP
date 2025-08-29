from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def match(jd_embedding, resume_embeddings):
    results = []

    # Ensure jd_embedding is 2D
    jd_embedding = np.squeeze(jd_embedding)
    if jd_embedding.ndim == 1:
        jd_embedding = jd_embedding.reshape(1, -1)

    for filename, emb in resume_embeddings.items():
        emb = np.squeeze(emb)
        if emb.ndim == 1:
            emb = emb.reshape(1, -1)

        score = cosine_similarity(jd_embedding, emb)[0][0]
        results.append((filename, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results
