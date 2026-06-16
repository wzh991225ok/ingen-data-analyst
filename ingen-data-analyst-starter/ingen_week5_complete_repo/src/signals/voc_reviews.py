"""Task 3 — Voice-of-customer mining (review topic modelling).

Real source: public review/comment datasets for each vertical (e.g., app-store reviews
for education/eldercare apps, G2/Capterra-style reviews for security products, forum
threads). Given a CSV of reviews per vertical with a `text` column, this module:
  1. cleans + vectorises with TF-IDF (English stopwords, 1-2 grams),
  2. clusters with KMeans into k themes,
  3. labels each theme by its top TF-IDF terms,
  4. extracts the most negative ("pain-point") reviews per theme as examples.

Output: data/week05/pain_points_long.csv (vertical, theme, top_terms, size, example)
and a per-vertical taxonomy markdown is written by build_reports.py.

Network: review corpora are normally supplied as files. This module ships a small,
clearly-labelled SAMPLE corpus so the pipeline runs end-to-end; replace
data/week05/reviews_<vertical>.csv with a real export to analyse live data.
The manifest records, per vertical, whether a real file or the sample was used.
"""
from __future__ import annotations
import re
import pandas as pd
from . import base
from .sample_reviews import SAMPLE_REVIEWS

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

_NEG = {"won't","can't","cannot","not","never","fails","failed","broke","broken","stuck",
        "expensive","slow","confusing","crash","crashes","poor","bad","hard","difficult",
        "disconnect","battery","drains","glitch","buggy","useless","frustrating","noisy",
        "drops","lag","delay","unreliable","error","errors","return","refund","stopped"}


def _load_reviews(vertical):
    """Real reviews file if present, else the labelled sample. Returns (df, mode)."""
    f = base.DATA / f"reviews_{vertical}.csv"
    if f.exists():
        df = pd.read_csv(f)
        if "text" in df.columns and len(df):
            return df[["text"]].dropna(), "file"
    return pd.DataFrame({"text": SAMPLE_REVIEWS[vertical]}), "sample"


def _neg_score(text):
    toks = re.findall(r"[a-z']+", text.lower())
    return sum(1 for t in toks if t in _NEG)


def mine(k: int = 5):
    rows = []
    mode_overall = "sample"
    for vert, (product, _) in base.VERTICALS.items():
        df, mode = _load_reviews(vert)
        if mode == "file":
            mode_overall = "file"
        texts = df["text"].astype(str).tolist()
        n = len(texts)
        kk = max(2, min(k, n // 3)) if n >= 6 else 2
        vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1, max_df=0.9)
        X = vec.fit_transform(texts)
        terms = vec.get_feature_names_out()
        km = KMeans(n_clusters=kk, random_state=42, n_init=10).fit(X)
        labels = km.labels_
        centroids = km.cluster_centers_
        for c in range(kk):
            top_idx = centroids[c].argsort()[::-1][:6]
            top_terms = ", ".join(terms[i] for i in top_idx)
            members = [texts[i] for i in range(n) if labels[i] == c]
            # top-3 most negative members as representative pain-point examples (spec: >=3 per theme)
            ex = sorted(members, key=_neg_score, reverse=True)[:3]
            ex = [e[:240] for e in ex]
            while len(ex) < 3:
                ex.append("")
            rows.append({"vertical": vert, "product": product, "theme_id": c + 1,
                         "top_terms": top_terms, "size": len(members),
                         "example_1": ex[0], "example_2": ex[1], "example_3": ex[2], "mode": mode})
        base.record_manifest({"task": "voice_of_customer", "vertical": vert,
                              "source": ("reviews file" if mode == "file" else "labelled sample corpus"),
                              "mode": ("network" if mode == "file" else "offline-fallback"),
                              "reviews": n, "themes": kk})
    out = pd.DataFrame(rows)
    path = base.DATA / "pain_points_long.csv"
    out.to_csv(path, index=False)
    print(f"  voice_of_customer -> {path.relative_to(base.ROOT)} ({len(out)} themes, mode={mode_overall})")
    return out


if __name__ == "__main__":
    mine()
