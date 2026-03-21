from __future__ import annotations
import os
import pandas as pd
import matplotlib.pyplot as plt


RESULTS_CSV = "results/experiment_results.csv"
FIGURES_DIR = "results/figures"


def ensure_output_dir() -> None:
    os.makedirs(FIGURES_DIR, exist_ok=True)


def save_bar_chart(df: pd.DataFrame, scenario: str, metric: str, ylabel: str, filename: str) -> None:
    scenario_df = df[df["scenario"] == scenario].copy()
    scenario_df = scenario_df.sort_values(metric)

    plt.figure(figsize=(8, 5))
    plt.bar(scenario_df["method"], scenario_df[metric])
    plt.xlabel("Scheduling algorithm")
    plt.ylabel(ylabel)
    plt.title(f"{ylabel} for scenario: {scenario}")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, filename), dpi=300)
    plt.close()


def generate_all_metric_figures(df: pd.DataFrame) -> None:
    scenarios = df["scenario"].unique()

    for scenario in scenarios:
        save_bar_chart(
            df, scenario,
            metric="sum_flow",
            ylabel="Total flow time",
            filename=f"{scenario}_sum_flow.png"
        )

        save_bar_chart(
            df, scenario,
            metric="avg_wait",
            ylabel="Average waiting time",
            filename=f"{scenario}_avg_wait.png"
        )

        save_bar_chart(
            df, scenario,
            metric="utilisation",
            ylabel="Charger utilisation",
            filename=f"{scenario}_utilisation.png"
        )

        save_bar_chart(
            df, scenario,
            metric="served_ratio",
            ylabel="Served ratio",
            filename=f"{scenario}_served_ratio.png"
        )

        save_bar_chart(
            df, scenario,
            metric="hard_deadline_misses",
            ylabel="Hard deadline misses",
            filename=f"{scenario}_deadline_misses.png"
        )


def generate_overall_comparison(df: pd.DataFrame) -> None:
    grouped = df.groupby("method", as_index=False).mean(numeric_only=True)

    save_bar_chart(
        grouped.assign(scenario="all"),
        scenario="all",
        metric="sum_flow",
        ylabel="Average total flow time across scenarios",
        filename="overall_sum_flow.png"
    )

    save_bar_chart(
        grouped.assign(scenario="all"),
        scenario="all",
        metric="avg_wait",
        ylabel="Average waiting time across scenarios",
        filename="overall_avg_wait.png"
    )

    save_bar_chart(
        grouped.assign(scenario="all"),
        scenario="all",
        metric="utilisation",
        ylabel="Average charger utilisation across scenarios",
        filename="overall_utilisation.png"
    )


def main() -> None:
    ensure_output_dir()
    df = pd.read_csv(RESULTS_CSV)

    generate_all_metric_figures(df)
    generate_overall_comparison(df)

    print(f"Figures saved in: {FIGURES_DIR}")


if __name__ == "__main__":
    main()