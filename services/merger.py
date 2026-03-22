import pandas as pd
from io import BytesIO

def merge_reports(fb_files: list[bytes], kt_file: bytes) -> bytes:
    fb_list = []

    for file in fb_files:
        df = pd.read_excel(BytesIO(file)).iloc[:, 0:4]
        df.columns = ["creative", "spend", "impressions", "clicks"]
        fb_list.append(df)

    fb_raw = pd.concat(fb_list, ignore_index=True)

    fb_grouped = (
        fb_raw
        .groupby("creative")
        .agg({
            "spend":        "sum",
            "impressions":  "sum",
            "clicks":       "sum"
        })
        .reset_index()
    )

    kt_raw = pd.read_csv(BytesIO(kt_file), sep=";").iloc[:, 0:4]
    kt_raw.columns = ["creative", "regs", "deps", "revenue"]

    result = pd.merge(fb_grouped, kt_raw, on="creative", how="left").sort_values("spend", ascending=False)

    result["regs"] = result["regs"].fillna(0).astype(int)
    result["deps"] = result["deps"].fillna(0).astype(int)
    result["clicks"] = result["clicks"].fillna(0).astype(int)
    result["impressions"] = result["impressions"].fillna(0).astype(int)

    result["spend"] = result["spend"].round(2)
    result["revenue"] = result["spend"].round(2)

    output = BytesIO()
    result.to_csv(output, index=False, sep=";", decimal=",", encoding="utf-8-sig")

    return output.getvalue()