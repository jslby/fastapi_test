from fastapi import FastAPI
import pandas as pd


fb_raw = pd.read_excel("fb_report.xlsx")
kt_raw = pd.read_csv("kt_report.csv", sep=";")

fb = fb_raw.iloc[:, 0:5]
fb.columns = ["creative", "spend", "impressions", "clicks", "cpc"]

kt = kt_raw.iloc[:, 0:4]
kt.columns = ["creative", "regs", "deps", "revenue"]

df = pd.merge(fb, kt, on="creative", how="left")

df.to_csv("result.csv", index=False)

print("Готово")