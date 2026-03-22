from fastapi import FastAPI
import pandas as pd

fb_raw = pd.read_excel("fb_report.xlsx").iloc[:, 0:4]
fb_raw.columns = ["creative", "spend", "impressions", "clicks"]


kt_raw = pd.read_csv("kt_report.csv", sep=";").iloc[:, 0:4]
kt_raw.columns = ["creative", "regs", "deps", "revenue"]

fb = (
    fb_raw
    .groupby("creative")
    .agg({
        "spend":        "sum",
        "impressions":   "sum",
        "clicks":       "sum"
    })
    .reset_index()
)


df = pd.merge(fb, kt_raw, on="creative", how="left")
df["regs"] = df["regs"].fillna(0).astype(int)
df["deps"] = df["deps"].fillna(0).astype(int)
df["clicks"] = df["clicks"].fillna(0).astype(int)
df["impressions"] = df["impressions"].fillna(0).astype(int)


df["spend"] = df["spend"].round(2)
df["revenue"] = df["spend"].round(2)

df.to_csv(
    "result.csv",
    index=False,
    sep=";",
    decimal=",",
    encoding="utf-8-sig"
)

print("Готово")