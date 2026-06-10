from pathlib import Path

import pandas as pd


class UIIndexEngine:
    def __init__(self):
        """
        The Data Vigilante // Forensic UI Adequacy & Regressive Tax Model
        Statutory Baselines vs. 2026 Macroeconomic Realities
        """
        self.project_root = Path(__file__).resolve().parent
        self.datasource_path = self.project_root / "data" / "dmv_macro_baselines.csv"
        self.datasource_models = self._load_datasource_models()

    def _load_datasource_models(self):
        """Load the dashboard-facing datasource registry from the CSV baseline."""
        baselines = pd.read_csv(self.datasource_path)
        baselines = baselines.sort_values(["Jurisdiction", "Year"])

        latest_baselines = (
            baselines.sort_values("Year")
            .groupby("Jurisdiction", as_index=False)
            .tail(1)
            .set_index("Jurisdiction")
        )

        return {
            "dmv_macro_baselines": baselines,
            "open_datasource_models": {
                jurisdiction: frame.reset_index(drop=True)
                for jurisdiction, frame in baselines.groupby("Jurisdiction")
            },
            "latest_state_models": latest_baselines,
        }

    def list_datasources(self):
        """Return dashboard-ready datasource descriptors."""
        return [
            {
                "name": "dmv_macro_baselines",
                "type": "table",
                "rows": len(self.datasource_models["dmv_macro_baselines"]),
                "source": str(self.datasource_path),
                "models": "—",
            },
            {
                "name": "open_datasource_models",
                "type": "group",
                "rows": len(self.datasource_models["open_datasource_models"]),
                "models": ", ".join(sorted(self.datasource_models["open_datasource_models"].keys())),
                "source": str(self.datasource_path),
            },
        ]

    def get_dashboard_payload(self):
        """Return all datasource models in a dashboard-friendly package."""
        return {
            "datasources": self.list_datasources(),
            "baselines": self.datasource_models["dmv_macro_baselines"],
            "open_datasource_models": self.datasource_models["open_datasource_models"],
            "latest_state_models": self.datasource_models["latest_state_models"],
        }

    def compute_indices(self, part_time_earnings=250):
        """
        Calculates the strategic safety net metrics: BAI, WBI, and MIPI.
        """
        analysis_records = []

        latest_baselines = self.datasource_models["latest_state_models"]

        for state, metrics in latest_baselines.iterrows():
            weekly_housing = metrics["Weekly_Housing"]

            # 1. Benefit Adequacy Index (BAI)
            # Measures if max payout even clears localized weekly housing costs
            bai = metrics["Max_WBA"] / weekly_housing

            # 2. Regressive SUI Wage Base Index (WBI)
            # Measures how tiny a sliver of enterprise payroll is actually taxed
            wbi = metrics["Taxable_Wage_Base"] / metrics["Avg_Annual_Wage"]

            # 3. Multi-Income Penalty Index (MIPI)
            # Ratios the state's aggressive benefit clawbacks over resourceful side-hustles
            net_counted_income = max(0, part_time_earnings - 50)
            mipi = net_counted_income / metrics["Max_WBA"]

            analysis_records.append({
                "Jurisdiction": state,
                "Year": int(metrics["Year"]),
                "Adequacy Index (BAI)": round(bai, 2),
                "Wage Base Index (WBI)": round(wbi, 4),
                "Clawback Penalty (MIPI)": round(mipi, 2),
                "System Status": "CRITICAL DECAY" if bai < 1.0 else "STABLE"
            })

        return pd.DataFrame(analysis_records)


if __name__ == "__main__":
    print("Executing The Data Vigilante Multi-State Engine...\n")
    engine = UIIndexEngine()
    # Simulating a user earning $250/week from a fallback part-time job
    results_df = engine.compute_indices(part_time_earnings=250)
    print(results_df.to_markdown(index=False))
    print("\nAvailable datasource models:")
    print(pd.DataFrame(engine.list_datasources()).to_markdown(index=False))