import pandas as pd, numpy as np, sys, os
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test
from scipy import stats
D, O = sys.argv[1], sys.argv[2]
x = pd.read_csv(f"{D}/HiSeqV2.gz", sep="\t", index_col=0)
surv = pd.read_csv(f"{D}/SKCM_survival.txt", sep="\t")
st = x.columns.str[13:15]
x = x.loc[:, st.isin(["01", "06"])]
pat = x.columns.str[:12]
# one sample per patient: the primary tumor if there is one
order = sorted(x.columns, key=lambda c: (c[:12], c[13:15]))
keep = pd.Series(order).groupby(pd.Series(order).str[:12]).first().values
x = x[keep]
cyt = x.loc[["GZMA", "PRF1"]].mean()
s = pd.DataFrame({"sample": cyt.index, "patient": cyt.index.str[:12],
                  "sample_type": np.where(cyt.index.str[13:15] == "01", "primary", "metastasis"), "cyt": cyt.values.round(4)})
med = s.cyt.median()
s["group"] = np.where(s.cyt > med, "high", "low")
sv = surv[["sample", "OS", "OS.time"]].dropna()
s = s.merge(sv, on="sample", how="left")
s.rename(columns={"OS": "os_event", "OS.time": "os_days"}, inplace=True)
bad = ~(s.os_days > 0)
s.loc[bad, ["os_days", "os_event"]] = np.nan
s.to_csv(f"{O}/scores.tsv", sep="\t", index=False)
m = s.dropna(subset=["os_days", "os_event"])
m = m[m.os_days > 0]
cph = CoxPHFitter().fit(pd.DataFrame({"T": m.os_days, "E": m.os_event, "high": (m.group == "high").astype(int)}), "T", "E")
r = cph.summary.loc["high"]
lr = logrank_test(m.os_days[m.group == "high"], m.os_days[m.group == "low"], m.os_event[m.group == "high"], m.os_event[m.group == "low"])
km = {}
for g in ("high", "low"):
    k = KaplanMeierFitter().fit(m.os_days[m.group == g] / 365.25, m.os_event[m.group == g])
    km[g] = k.median_survival_time_
pd.DataFrame([{"term": "cyt_high_vs_low", "HR": round(r["exp(coef)"], 3), "CI_low": round(r["exp(coef) lower 95%"], 3),
               "CI_high": round(r["exp(coef) upper 95%"], 3), "p": float(f"{r['p']:.2g}"), "logrank_p": float(f"{lr.p_value:.2g}"),
               "n": len(m), "events": int(m.os_event.sum()), "n_high": int((m.group == "high").sum()), "n_low": int((m.group == "low").sum()),
               "median_os_high_years": round(km["high"], 1), "median_os_low_years": round(km["low"], 1), "cyt_median": round(med, 3)}]
             ).to_csv(f"{O}/cox.tsv", sep="\t", index=False)
genes = ["CD8A", "CD8B", "GZMA", "GZMB", "PRF1", "IFNG", "CXCL9", "CXCL10", "CD274", "LAG3", "FOXP3", "MITF", "TYR", "MLANA"]
h = x.loc[genes, s["sample"]]
h.index.name = "gene"
h.round(3).to_csv(f"{O}/heatmap.tsv", sep="\t")
s[["sample", "group"]].to_csv(f"{O}/samples.tsv", sep="\t", index=False)
xx = x.loc[(x > 1).mean(axis=1) > 0.2]
hi, lo = xx.loc[:, s["sample"][s.group == "high"]], xx.loc[:, s["sample"][s.group == "low"]]
t, p = stats.ttest_ind(hi, lo, axis=1, equal_var=False)
de = pd.DataFrame({"gene": xx.index, "log2fc": (hi.mean(1) - lo.mean(1)).round(3).values, "p": p})
de["p"] = de.p.map(lambda v: float(f"{v:.3g}"))
de.to_csv(f"{O}/de.tsv", sep="\t", index=False)
print(pd.read_csv(f"{O}/cox.tsv", sep="\t").T)
print(s.groupby(["group", "sample_type"]).size())
print(de.sort_values("p").head(8))
