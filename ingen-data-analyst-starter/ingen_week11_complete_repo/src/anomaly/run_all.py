"""Week 11 — run every detector on both public benchmarks and write the results table.

Split protocol (identical for every model, per the plan's success criteria):
  NAB  : train = all points BEFORE the first labelled anomaly window (a clean warm-up);
         test  = everything after. Mirrors baselining a Sentinel unit during commissioning
         and then running it live.
  SKAB : train = the shipped anomaly-free reference run (SKAB's intended clean baseline);
         test  = the valve1 experiment runs.
No labels are used during fitting — the detectors are unsupervised. Labels are used only to
evaluate, and to pick the operating point via the stated operational rule.

Outputs (data/week11/):
  results.csv               model x dataset x precision/recall/F1/AP/FAR/TTD/confusion
  pr_curves.csv             PR curve points per model x dataset
  adaptive_threshold.csv    fixed vs rolling-quantile vs EWMA on the best model
  dataset_licenses.csv      license + citation per dataset (success criterion)
  scores_<dataset>.csv      per-model scores on the test split (for charts)

Run:  python -m src.anomaly.run_all
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

from . import data_loader as dl
from .models import build_models
from .evaluate import evaluate_model, pr_curve_points, choose_threshold, RECALL_FLOOR
from .adaptive_threshold import compare as compare_thresholds
from .operational import frontier

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "week11"
DATA.mkdir(parents=True, exist_ok=True)


def _prep_nab():
    df = dl.load_nab()
    feats = dl.nab_features(df)
    first_window_start = min(s for s, _ in df.attrs["windows"])
    is_train = df["timestamp"] < first_window_start
    # drop rows whose rolling features are still warming up
    valid = feats.notna().all(axis=1)
    tr = is_train & valid
    te = (~is_train) & valid
    return {
        "name": "NAB machine_temperature",
        "X_train": feats[tr].to_numpy(),
        "X_test": feats[te].to_numpy(),
        "y_test": df.loc[te, "is_anomaly"].to_numpy(),
        "ts_test": df.loc[te, "timestamp"].to_numpy(),
        "n_train": int(tr.sum()), "n_test": int(te.sum()),
        "split_rule": f"train = points before first labelled window ({first_window_start:%Y-%m-%d %H:%M})",
    }


def _prep_skab():
    clean = dl.load_skab_clean()
    test = dl.load_skab()
    cols = dl.SKAB_SENSORS
    return {
        "name": "SKAB valve1",
        "X_train": clean[cols].to_numpy(),
        "X_test": test[cols].to_numpy(),
        "y_test": test["is_anomaly"].to_numpy(),
        "ts_test": test["datetime"].to_numpy(),
        "n_train": len(clean), "n_test": len(test),
        "split_rule": "train = SKAB shipped anomaly-free reference run",
    }


def main():
    datasets = [_prep_nab(), _prep_skab()]
    results, pr_rows, score_frames = [], [], {}

    for ds in datasets:
        print(f"\n=== {ds['name']} ===")
        print(f"  {ds['split_rule']}")
        print(f"  train={ds['n_train']:,} points (unlabelled)   test={ds['n_test']:,} points  "
              f"({ds['y_test'].mean()*100:.1f}% anomalous)")
        models = build_models(n_features=ds["X_train"].shape[1])
        sc = {"timestamp": pd.to_datetime(pd.Series(ds["ts_test"])), "is_anomaly": ds["y_test"]}
        for m in models:
            m.fit(ds["X_train"])
            scores = m.score(ds["X_test"])
            row = evaluate_model(m.name, ds["name"], ds["ts_test"], ds["y_test"], scores)
            results.append(row)
            sc[m.name] = scores
            rec, prec = pr_curve_points(ds["y_test"], np.nan_to_num(scores, nan=np.nanmin(scores)))
            for r, p in zip(rec, prec):
                pr_rows.append({"dataset": ds["name"], "model": m.name,
                                "recall": round(float(r), 4), "precision": round(float(p), 4)})
            flag = "" if row["met_recall_floor"] else "  [recall floor NOT met]"
            print(f"  {m.name:22s} P={row['precision']:.3f} R={row['recall']:.3f} "
                  f"F1={row['f1']:.3f} AP={row['avg_precision']:.3f} FAR={row['false_alarm_rate']:.3f} "
                  f"TTD={row['ttd_seconds']}s events={row['events_detected']}/{row['events_total']}{flag}")
        score_frames[ds["name"]] = pd.DataFrame(sc)

    res = pd.DataFrame(results)
    res.to_csv(DATA / "results.csv", index=False)
    pd.DataFrame(pr_rows).to_csv(DATA / "pr_curves.csv", index=False)
    dl.license_table().to_csv(DATA / "dataset_licenses.csv", index=False)
    for name, f in score_frames.items():
        f.to_csv(DATA / f"scores_{name.split()[0].lower()}.csv", index=False)

    # ---- adaptive threshold study on the best model of the richest dataset (NAB) ----
    nab_res = res[res.dataset == "NAB machine_temperature"].sort_values("f1", ascending=False)
    best_model = nab_res.iloc[0]["model"]
    fixed_thr = float(nab_res.iloc[0]["threshold"])
    sf = score_frames["NAB machine_temperature"]
    adapt = compare_thresholds(sf["timestamp"], sf["is_anomaly"], sf[best_model], fixed_thr)
    adapt.insert(0, "dataset", "NAB machine_temperature")
    adapt.insert(1, "model", best_model)
    adapt.to_csv(DATA / "adaptive_threshold.csv", index=False)

    print(f"\n=== Adaptive threshold study (model = {best_model}, NAB) ===")
    print(adapt[["scheme", "precision", "recall", "f1", "false_alarm_rate", "ttd_seconds"]].to_string(index=False))

    # ---- operational frontier: alert-level load at the stated recall floor ----
    fr = frontier(sf["is_anomaly"], sf[best_model], sf["timestamp"], recall_floor=RECALL_FLOOR)
    fr.insert(0, "dataset", "NAB machine_temperature"); fr.insert(1, "model", best_model)
    fr.to_csv(DATA / "operational_frontier.csv", index=False)
    print(f"\n=== Operational frontier (recall floor {RECALL_FLOOR:.0%}, alert-level) ===")
    print(fr[["persistence_readings", "threshold", "point_recall", "events_caught",
              "events_total", "false_alerts_per_day"]].to_string(index=False))
    print(f"\nSaved -> {DATA.relative_to(ROOT)}/  (results.csv, pr_curves.csv, adaptive_threshold.csv, dataset_licenses.csv)")
    return res, adapt


if __name__ == "__main__":
    main()
