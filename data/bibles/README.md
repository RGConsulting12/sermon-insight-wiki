# Bundled Bible XML (Beblia format)

These files are copied from **[Beblia/Holy-Bible-XML-Format](https://github.com/Beblia/Holy-Bible-XML-Format)** (same structure: `<bible>` → `<testament>` → `<book number="1..66">` → `<chapter>` → `<verse>`).

| File | Translation (root `@translation`) |
|------|-------------------------------------|
| `EnglishKJBible.xml` | English KJV (marked Public Domain in source file) |
| `EnglishNIVBible.xml` | English NIV |
| `EnglishNKJBible.xml` | English NKJ 1982 (NKJV) |
| `EnglishNLTBible.xml` | English NLT |

## Important — copyright and distribution

Modern translations (**NIV, NKJV, NLT**, etc.) are normally **copyrighted** by their publishers. The upstream repository states *“Use at your own discretion”*; that does **not** replace publisher licenses. If this project is **public** on GitHub, verify that **hosting and redistributing** these XML files complies with the publisher terms for your use case. **KJV** is commonly treated as **public domain** in the US.

This folder exists so `sermon-insight-wiki` can supply **parallel passage text** to the LLM next to sermon evidence. You may remove any file you are not licensed to keep and adjust `SIW_BIBLE_TRANSLATIONS` in `.env`.
