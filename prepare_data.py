import pandas as pd

file_path = "data/كتالوج_بيع_البرفانات_والمسكات.xlsx"

catalog = pd.read_excel(file_path, sheet_name="كتالوج البيع")
perfumes = pd.read_excel(file_path, sheet_name="البرفانات والمسكات")

catalog = catalog.rename(columns={"المنتج": "اسم_المنتج"})
perfumes = perfumes.rename(columns={"الاسم": "اسم_المنتج"})

perfumes_extra = perfumes[["اسم_المنتج", "درجة الحلاوة", "ملاحظات"]]
df = catalog.merge(perfumes_extra, on="اسم_المنتج", how="left")

print(f"عدد المنتجات بعد الدمج: {len(df)}")

DEFAULT_VALUES = {
    "النوع": "يناسب الجميع",
    "الموسم": "يصلح لكل المواسم",
    "التصنيف العطري": "تصنيف متنوع",
    "درجة الحلاوة": "على حسب اختيار العميل",
    "النوتات الرئيسية": "النوتات حسب اختيار العميل",
}

def is_incomplete(value):
    if pd.isna(value):
        return True
    text = str(value).strip()
    return text == "غير محدد" or "يحتاج" in text


def clean_column(df, column):
    default = DEFAULT_VALUES[column]
    df[column] = df[column].apply(lambda v: default if is_incomplete(v) else v)
    return df


for col in DEFAULT_VALUES:
    df = clean_column(df, col)


def build_embedding_text(row):
    parts = [
        str(row["النوع"]),
        str(row["الموسم"]),
        str(row["التصنيف العطري"]),
        str(row["النوتات الرئيسية"]),
        str(row["درجة الحلاوة"]),
    ]
    return " ".join(parts)


df["نص_البحث"] = df.apply(build_embedding_text, axis=1)

print(df[["اسم_المنتج", "نص_البحث"]].head(10))

df.to_excel("data/catalog_clean.xlsx", index=False)
print("\nتم حفظ الملف النظيف: data/catalog_clean.xlsx")