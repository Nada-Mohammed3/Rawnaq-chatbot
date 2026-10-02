from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from search import search_perfumes
from generate_advice import generate_advice

app = FastAPI(title="Perfume Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    query: str
    exclude: list[str] = []  

def format_product(product_dict):
    """يجهز بيانات منتج واحد بشكل مبسط للفرونت إند"""
    return {
        "name": product_dict["اسم_المنتج"],
        "type": product_dict["النوع"],
        "season": product_dict["الموسم"],
        "scent_family": product_dict["التصنيف العطري"],
        "price_premium_50ml": product_dict.get("بريميوم 50 مل"),
    }


@app.post("/ask")
def ask(request: AskRequest):
    """
    يستقبل سؤال المستخدم + قايمة المنتجات المستبعدة (اللي عرضناها قبل كده)،
    ويرجع منتج واحد + نصيحة عنه، وبيانات منتجين احتياطيين (من غير نصيحة) للاستخدام لاحقاً
    """
    results = search_perfumes(request.query, top_k=10)


    filtered = [
        match for match in results
        if match["product"]["اسم_المنتج"] not in request.exclude
    ]


    if not filtered:
        return {
            "query": request.query,
            "product": None,
            "advice": "للأسف مفيش عطور تانية تناسب طلبك في الوقت الحالي.",
            "other_products": [],
            "has_more": False,
        }


    top_match = filtered[0]

    backup_matches = filtered[1:3]

    advice = generate_advice(request.query, [top_match])

    return {
        "query": request.query,
        "product": format_product(top_match["product"]),
        "advice": advice,
        "other_products": [format_product(m["product"]) for m in backup_matches],
        "has_more": len(backup_matches) > 0,
    }


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Perfume Recommendation API is running!"}