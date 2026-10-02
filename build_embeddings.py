import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

df = pd.read_excel("data/catalog_clean.xlsx")
print(f"عدد المنتجات: {len(df)}")

print("جاري تحميل الموديل...")
model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
print("تم تحميل الموديل بنجاح")

texts = df["نص_البحث"].tolist()
embeddings = model.encode(texts, show_progress_bar=True)
print(f"شكل المتجهات: {embeddings.shape}")  # المفروض يطبع (54, 768) تقريباً

client = chromadb.PersistentClient(path="./chroma_db")

try:
    client.delete_collection("perfumes")
except Exception:
    pass

collection = client.create_collection(name="perfumes")

# ٥) تخزين المتجهات + البيانات الأصلية لكل منتج في القاعدة
collection.add(
    ids=[str(i) for i in df.index],                 # معرّف فريد لكل منتج
    embeddings=embeddings.tolist(),                   # المتجه الرقمي
    documents=texts,                                    # النص الأصلي (نص_البحث)
    metadatas=df.to_dict(orient="records"),            # كل بيانات المنتج (الاسم، السعر، إلخ)
)

print(f"\nتم تخزين {collection.count()} منتج في قاعدة البيانات المتجهية بنجاح")