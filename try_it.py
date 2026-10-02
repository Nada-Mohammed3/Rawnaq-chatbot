from search import search_perfumes
from generate_advice import generate_advice

print("=" * 50)
print("جربي شات بوت توصية العطور (اكتبي 'خروج' للإنهاء)")
print("=" * 50)

while True:
    query = input("\nسؤالك: ").strip()

    if query == "خروج":
        print("مع السلامة!")
        break

    if query == "":
        continue

    results = search_perfumes(query, top_k=3)

    advice = generate_advice(query, results)

    print("\n--- الرد ---")
    print(advice)
    print("-" * 50)