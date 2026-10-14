import pandas as pd
import requests
import io

url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
query = "SELECT * FROM ps WHERE default_flag = 1"

response = requests.get(url, params={"query": query, "format": "csv"})
planetary_systems = pd.read_csv(io.StringIO(response.text))

def column_test(pl_name, value):
    row = planetary_systems.loc[planetary_systems["pl_name"] == pl_name]
    print(row.loc[:, (row == value).any()].head())

print("Planet Radius [Jupiter Radius]")
column_test("2MASS J02192210-3925225 b", 1.44)
column_test("2MASS J0249-0557 c", 1.55)
column_test("2MASS J12073346-3932539 b", 1.40)

print("Planet Mass [Jupiter Mass]")
column_test("11 Com b", 15.464)
column_test("11 UMi b", 14.74)
column_test("14 And b", 3.559)

print("Eccentricity")
column_test("11 Com b", 0.238)
column_test("11 UMi b", 0.080)
column_test("14 And b", 0)

print("Spectral Type")
print(planetary_systems.loc[:, planetary_systems.isin(["G8 III", "K0 III", "K3 III"]).any()].head())

print("Stellar Effective Temperature [K]")
column_test("11 Com b", 4874)
column_test("11 UMi b", 4213)
column_test("14 And b", 4888)

print("Stellar Radius [Solar Radius]")
column_test("11 Com b", 13.76)
column_test("11 UMi b", 29.79)

print("Stellar Mass [Solar Mass]")
column_test("11 Com b", 2.09)
column_test("11 UMi b", 2.78)

print("Stellar Surface Gravity [whatever]")
column_test("11 Com b", 2.45)
column_test("11 UMi b", 1.93)

print("Distance [pc]")
column_test("11 Com b", 93.1846)
column_test("11 UMi b", 125.3210)

print("Date of Last Update")
print(planetary_systems.loc[:, planetary_systems.isin(["2023-09-19", "2018-09-04", "2026-03-26"]).any()].head())
# Two candidates: rowupdate and releasedate. It should be self-explanatory which one is which.

# Planet Mass [Jupiter Mass] gives two columns: pl_bmassj and pl_msinij. How much do they differ?
print(planetary_systems.loc[planetary_systems["pl_bmassj"] != planetary_systems["pl_msinij"]][["pl_name", "pl_bmassj", "pl_msinij"]])
# It seems like pl_msinij is mostly NaN, and when not indicates a lower bound for the mass. We're already choosing to ignore margins of error, so we can drop it.