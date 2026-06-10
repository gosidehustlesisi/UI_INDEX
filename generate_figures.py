import csv
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

# Set style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 150

# Load data
DATA_PATH = Path(__file__).parent / "data" / "dmv_macro_baselines.csv"
records = []
with open(DATA_PATH, "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        records.append({
            "Jurisdiction": row["Jurisdiction"],
            "Year": int(row["Year"]),
            "Max_WBA": float(row["Max_WBA"]),
            "Taxable_Wage_Base": float(row["Taxable_Wage_Base"]),
            "Avg_Annual_Wage": float(row["Avg_Annual_Wage"]),
            "Weekly_Housing": float(row["Weekly_Housing"]),
        })

# Compute indices
for rec in records:
    rec["BAI"] = rec["Max_WBA"] / rec["Weekly_Housing"]
    rec["WBI"] = rec["Taxable_Wage_Base"] / rec["Avg_Annual_Wage"]
    net_counted = max(0, 250 - 50)
    rec["MIPI"] = net_counted / rec["Max_WBA"]
    rec["Housing_Gap"] = rec["Weekly_Housing"] - rec["Max_WBA"]

df = pd.DataFrame(records)

# Ensure figures directory exists
FIG_DIR = Path(__file__).parent / "figures"
FIG_DIR.mkdir(exist_ok=True)

# Chart 1: BAI Decay Trajectory
fig, ax = plt.subplots(figsize=(10, 6))
for jurisdiction in df["Jurisdiction"].unique():
    sub = df[df["Jurisdiction"] == jurisdiction].sort_values("Year")
    ax.plot(sub["Year"], sub["BAI"], marker="o", linewidth=2.5, markersize=8, label=jurisdiction)

ax.axhline(1.0, color="red", linestyle="--", linewidth=1.5, alpha=0.7, label="Adequacy Threshold (1.0)")
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Benefit Adequacy Index (BAI)", fontsize=12)
ax.set_title("BAI Decay Trajectory: 2010 → 2026", fontsize=14, fontweight="bold")
ax.legend(title="Jurisdiction", loc="upper right")
ax.set_ylim(0.5, 1.5)
plt.tight_layout()
plt.savefig(FIG_DIR / "01_bai_decay_trajectory.png", dpi=150, bbox_inches="tight")
plt.close()

# Chart 2: WBI Stagnation
fig, ax = plt.subplots(figsize=(10, 6))
for jurisdiction in df["Jurisdiction"].unique():
    sub = df[df["Jurisdiction"] == jurisdiction].sort_values("Year")
    ax.plot(sub["Year"], sub["WBI"], marker="s", linewidth=2.5, markersize=8, label=jurisdiction)

ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Regressive Wage Base Index (WBI)", fontsize=12)
ax.set_title("WBI Stagnation: Flat SUI Caps vs. Rising Wages", fontsize=14, fontweight="bold")
ax.legend(title="Jurisdiction", loc="upper right")
plt.tight_layout()
plt.savefig(FIG_DIR / "02_wbi_stagnation.png", dpi=150, bbox_inches="tight")
plt.close()

# Chart 3: MIPI Clawback Severity
fig, ax = plt.subplots(figsize=(10, 6))
for jurisdiction in df["Jurisdiction"].unique():
    sub = df[df["Jurisdiction"] == jurisdiction].sort_values("Year")
    ax.plot(sub["Year"], sub["MIPI"], marker="^", linewidth=2.5, markersize=8, label=jurisdiction)

ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Multi-Income Penalty Index (MIPI)", fontsize=12)
ax.set_title("MIPI Clawback Severity at $250 Side-Hustle Earnings", fontsize=14, fontweight="bold")
ax.legend(title="Jurisdiction", loc="upper right")
plt.tight_layout()
plt.savefig(FIG_DIR / "03_mipi_clawback.png", dpi=150, bbox_inches="tight")
plt.close()

# Chart 4: Housing Cost vs. WBA Gap
fig, ax = plt.subplots(figsize=(10, 6))
x_pos = range(len(df))
width = 0.35

years = df["Year"].unique()
jurisdictions = df["Jurisdiction"].unique()

# Grouped bar chart: WBA vs Housing per jurisdiction-year
for i, jurisdiction in enumerate(jurisdictions):
    sub = df[df["Jurisdiction"] == jurisdiction].sort_values("Year")
    x = [j * 3 + i * width for j in range(len(sub))]
    ax.bar([xi - width/2 for xi in x], sub["Max_WBA"], width, label=f"{jurisdiction} WBA", alpha=0.8)
    ax.bar([xi + width/2 for xi in x], sub["Weekly_Housing"], width, label=f"{jurisdiction} Housing", alpha=0.6)

ax.set_xticks([j * 3 + width/2 for j in range(len(years))])
ax.set_xticklabels(years)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Weekly Amount ($)", fontsize=12)
ax.set_title("Housing Cost vs. Maximum Weekly Benefit: The Growing Gap", fontsize=14, fontweight="bold")
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig(FIG_DIR / "04_housing_vs_wba_gap.png", dpi=150, bbox_inches="tight")
plt.close()

print(f"✅ Generated 4 charts in {FIG_DIR}")
print("Files:")
for f in sorted(FIG_DIR.iterdir()):
    print(f"  {f.name}")
