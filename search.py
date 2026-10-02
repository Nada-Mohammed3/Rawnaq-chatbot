from sentence_transformers import SentenceTransformer
import chromadb
import numpy as np

model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="perfumes")

SEASON_ANCHORS = {
    "صيفي": "عطر مناسب لأجواء الصيف والحر",
    "شتوي": "عطر مناسب لأجواء الشتاء والبرد",
    "خريفي": "عطر مناسب لأجواء الخريف",
    "ربيعي": "عطر مناسب لأجواء الربيع",
}

_season_names = list(SEASON_ANCHORS.keys())
_season_embeddings = model.encode(list(SEASON_ANCHORS.values()))

SEASON_SIMILARITY_THRESHOLD = 0.45


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def detect_season(user_query):
    """
    يكتشف الموسم المقصود من سؤال المستخدم بالمعنى (مش بمطابقة كلمة)،
    فبيشتغل مع أي لغة يكتب بيها المستخدم.
    """
    query_embedding = model.encode([user_query])[0]

    best_season = None
    best_score = 0

    for season, season_embedding in zip(_season_names, _season_embeddings):
        score = cosine_similarity(query_embedding, season_embedding)
        if score > best_score:
            best_score = score
            best_season = season

    if best_score >= SEASON_SIMILARITY_THRESHOLD:
        return best_season
    return None


def matches_season(product_season, target_season):
    if not product_season:
        return False
    return (
        target_season in str(product_season)
        or "كل المواسم" in str(product_season)
    )


def search_perfumes(user_query, top_k=3):
    detected_season = detect_season(user_query)

    query_embedding = model.encode([user_query]).tolist()

    initial_k = 20 if detected_season else top_k

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=initial_k,
    )

    all_matches = []
    for i in range(len(results["ids"][0])):
        all_matches.append({
            "product": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })

    if not detected_season:
        return all_matches[:top_k]

    filtered = [
        m for m in all_matches
        if matches_season(m["product"].get("الموسم"), detected_season)
    ]

    if len(filtered) >= top_k:
        return filtered[:top_k]

    remaining = [m for m in all_matches if m not in filtered]
    return (filtered + remaining)[:top_k]


if __name__ == "__main__":
    for query in ["عايز عطر دافي للشتا", "night summer perfume", "un parfum d'été"]:
        results = search_perfumes(query, top_k=3)
        print(f"سؤال المستخدم: {query}\n")
        for rank, match in enumerate(results, start=1):
            product = match["product"]
            print(f"{rank}. {product['اسم_المنتج']} | الموسم: {product['الموسم']}")
        print("-" * 50)