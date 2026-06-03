#!/usr/bin/env python3
"""Study 5 modality x disclosure-depth analysis (FILTER ON: filter_$ == 1).

Uses the disclosure scores already in the file: DD_S (0-3), DD_L (0-6),
and WC (word count). Compares VR vs Text, raw and adjusted for word count.
"""
import json
import numpy as np
import pandas as pd
import pyreadstat
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statsmodels.miscmodels.ordinal_model import OrderedModel

SRC = "/root/.claude/uploads/df0dbb36-4d78-424d-bd29-c1d29cdf89f4/819687d3-AI_Companions__Study_5__no_attention_checks.sav"
VR, TEXT = 1, 2

df, meta = pyreadstat.read_sav(SRC)
n_total = len(df)
# ---- APPLY FILTER ----
d = df[df["filter_$"] == 1].copy()
n_filter = len(d)
d = d.dropna(subset=["DD_S", "DD_L", "WC", "Condition"]).copy()
d["modality"] = d["Condition"].map({VR: "VR", TEXT: "Text"})
vr, tx = d[d.Condition == VR], d[d.Condition == TEXT]
R = {"n_total": n_total, "n_after_filter": n_filter, "n_excluded_by_filter": n_total - n_filter,
     "n_analysed": len(d), "n_vr": len(vr), "n_text": len(tx)}


def mw(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    a = a[~np.isnan(a)]; b = b[~np.isnan(b)]
    u, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    rb = 1 - 2 * u / (len(a) * len(b))
    return dict(vr_mean=a.mean(), vr_med=float(np.median(a)), vr_sd=a.std(ddof=1),
                tx_mean=b.mean(), tx_med=float(np.median(b)), tx_sd=b.std(ddof=1),
                U=float(u), p=float(p), r=float(rb))


R["R1"] = mw(vr.DD_S, tx.DD_S)
R["R2"] = mw(vr.DD_L, tx.DD_L)
R["WC"] = mw(vr.WC, tx.WC)
R["spearman_wc_r2"] = dict(zip(("rho", "p"), [float(x) for x in stats.spearmanr(d.WC, d.DD_L)]))

# ---- ordinal regression: depth ~ text + word count ----
d["text"] = (d.Condition == TEXT).astype(float)
d["wc_z"] = (d.WC - d.WC.mean()) / d.WC.std()


def ordreg(y):
    m = OrderedModel(d[y], d[["text", "wc_z"]], distr="logit").fit(method="bfgs", disp=False)
    out = {}
    for term in ["text", "wc_z"]:
        ci = m.conf_int().loc[term]
        out[term] = dict(OR=float(np.exp(m.params[term])), p=float(m.pvalues[term]),
                         ci=[float(np.exp(ci[0])), float(np.exp(ci[1]))])
    return out


R["ord_R1"] = ordreg("DD_S")
R["ord_R2"] = ordreg("DD_L")
json.dump(R, open("study5_results.json", "w"), indent=2)
print(json.dumps(R, indent=2))

# ============ FIGURES ============
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
C = {"VR": "#4C72B0", "Text": "#DD8452"}

fig, ax = plt.subplots(figsize=(7, 4.2))
ct = pd.crosstab(d.modality, d.DD_S, normalize="index") * 100
levels = sorted(d.DD_S.dropna().unique())
x = np.arange(len(levels)); w = 0.38
ax.bar(x - w / 2, [ct.loc["VR"].get(l, 0) for l in levels], w, label="VR", color=C["VR"])
ax.bar(x + w / 2, [ct.loc["Text"].get(l, 0) for l in levels], w, label="Text", color=C["Text"])
ax.set_xticks(x); ax.set_xticklabels([f"{int(l)}" for l in levels])
ax.set_ylabel("% of participants"); ax.set_xlabel("Disclosure depth DD_S (0-3)")
ax.set_title("Study 5: Disclosure depth by modality (filter on)"); ax.legend(title="Modality")
fig.tight_layout(); fig.savefig("s5_fig1_depth_by_modality.png", dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(6, 4.2))
data = [tx.DD_L.values, vr.DD_L.values]
bp = ax.boxplot(data, widths=0.55, patch_artist=True, tick_labels=["Text", "VR"])
for patch, k in zip(bp["boxes"], ["Text", "VR"]):
    patch.set_facecolor(C[k]); patch.set_alpha(0.55)
for i, (vals, k) in enumerate(zip(data, ["Text", "VR"]), 1):
    ax.scatter(np.random.normal(i, 0.06, len(vals)), vals, s=14, color=C[k], alpha=0.6, zorder=3)
ax.set_ylabel("Disclosure depth DD_L (0-6)")
ax.set_title("Study 5: finer-grained depth by modality")
fig.tight_layout(); fig.savefig("s5_fig2_R2_box.png", dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 4.2))
for k, g in d.groupby("modality"):
    j = g.DD_L + np.random.normal(0, 0.08, len(g))
    ax.scatter(g.WC, j, s=22, alpha=0.6, color=C[k], label=k)
ax.set_xlabel("Participant word count"); ax.set_ylabel("Disclosure depth DD_L (0-6)")
ax.set_title("Study 5: more words ≠ deeper disclosure"); ax.legend(title="Modality")
fig.tight_layout(); fig.savefig("s5_fig3_wordcount_vs_depth.png", dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(5, 4.2))
ax.bar(["VR", "Text"], [vr.WC.mean(), tx.WC.mean()], yerr=[vr.WC.sem(), tx.WC.sem()],
       capsize=6, color=[C["VR"], C["Text"]], alpha=0.85)
ax.set_ylabel("Mean word count"); ax.set_title("Study 5: word count by modality")
fig.tight_layout(); fig.savefig("s5_fig4_wordcount.png", dpi=150); plt.close(fig)
print("\nfigures + study5_results.json written")
