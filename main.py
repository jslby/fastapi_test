from fastapi import FastAPI
import pandas as pd

fb_raw = pd.read_excel("fb_report.xlsx")
kt_raw = pd.read_csv("kt_report.csv", sep=";")

fb = fb_raw.iloc[:, 0:5]
fb.columns = ["creative", "spend", "impressions", "clicks", "cpc"]

kt = kt_raw.iloc[:, 0:4]
kt.columns = ["creative", "regs", "deps", "revenue"]

df = pd.merge(fb, kt, on="creative", how="left")
df["regs"] = df["regs"].fillna(0).astype(int)
df["deps"] = df["deps"].fillna(0).astype(int)
df["clicks"] = df["clicks"].fillna(0).astype(int)
df["cpc"] = df["cpc"].fillna(0)
df["impressions"] = df["impressions"].fillna(0).astype(int)


df["spend"] = df["spend"].round(2)
df["cpc"] = df["cpc"].round(2)
df["revenue"] = df["spend"].round(2)

df.to_csv(
    "result.csv",
    index=False,
    sep=";",
    decimal=",",
    encoding="utf-8-sig"
)

print("Готово")