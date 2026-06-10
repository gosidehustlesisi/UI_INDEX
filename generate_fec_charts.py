import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams['figure.dpi'] = 150

# Load FEC data
with open('data/political/fec_funding_profiles.json') as f:
    fec_data = json.load(f)

df = pd.DataFrame(fec_data)

# Chart 1: Total Receipts by Member (sorted)
df_sorted = df.sort_values('total_receipts', ascending=True)
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#1f77b4' if s == 'MD' else '#ff7f0e' for s in df_sorted['state']]
ax.barh(range(len(df_sorted)), df_sorted['total_receipts'], color=colors, alpha=0.8)
ax.set_yticks(range(len(df_sorted)))
ax.set_yticklabels([f"{r['name']} ({r['state']})" for _, r in df_sorted.iterrows()], fontsize=10)
ax.set_xlabel('Total Receipts ($)', fontsize=12)
ax.set_title('Total Campaign Receipts — UI-Relevant Committee Members\n(FEC API, Real-Time)', fontsize=14, fontweight='bold')
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#1f77b4', label='Maryland'), Patch(facecolor='#ff7f0e', label='Virginia')]
ax.legend(handles=legend_elements, loc='lower right')
plt.tight_layout()
plt.savefig('figures/11_fec_total_receipts.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved figures/11_fec_total_receipts.png")

# Chart 2: Business vs Labor Contributions (stacked)
fig, ax = plt.subplots(figsize=(10, 6))
x = range(len(df))
width = 0.6
ax.bar(x, df['business_contributions'], width, label='Business/Industry', color='crimson', alpha=0.8)
ax.bar(x, df['labor_contributions'], width, bottom=df['business_contributions'], label='Labor Unions', color='steelblue', alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels([f"{r['name']}\n({r['state']})" for _, r in df.iterrows()], fontsize=9, rotation=15, ha='right')
ax.set_ylabel('Contributions ($)', fontsize=12)
ax.set_title('Business vs Labor Contributions to UI Committee Members\n(FEC Schedule A, Itemized ≥$500)', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig('figures/12_fec_business_vs_labor.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved figures/12_fec_business_vs_labor.png")

# Chart 3: Individual vs PAC vs Business (normalized %)
fig, ax = plt.subplots(figsize=(10, 6))
for i, (_, r) in enumerate(df.iterrows()):
    total = r['individual_contributions'] + r['pac_contributions'] + r['business_contributions']
    if total > 0:
        indiv_pct = r['individual_contributions'] / total * 100
        pac_pct = r['pac_contributions'] / total * 100
        biz_pct = r['business_contributions'] / total * 100
    else:
        indiv_pct = pac_pct = biz_pct = 0
    ax.barh(i, indiv_pct, color='forestgreen', alpha=0.8, label='Individual' if i == 0 else '')
    ax.barh(i, pac_pct, left=indiv_pct, color='darkorange', alpha=0.8, label='PAC' if i == 0 else '')
    ax.barh(i, biz_pct, left=indiv_pct + pac_pct, color='crimson', alpha=0.8, label='Business/Industry' if i == 0 else '')

ax.set_yticks(range(len(df)))
ax.set_yticklabels([f"{r['name']} ({r['state']})" for _, r in df.iterrows()], fontsize=10)
ax.set_xlabel('Percentage of Total Contributions', fontsize=12)
ax.set_title('Contribution Source Mix — UI Committee Members\n(FEC API, Real-Time)', fontsize=14, fontweight='bold')
ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig('figures/13_fec_contribution_mix.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved figures/13_fec_contribution_mix.png")

print(f"\n✅ Generated 3 FEC charts from {len(df)} member profiles")
