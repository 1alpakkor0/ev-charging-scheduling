from __future__ import annotations
import csv
import os
from typing import Callable, Dict, Tuple

from heuristics import (
    key_fcfs,
    key_spt,
    key_edf,
    key_min_slack,
    make_key_weighted,
)
from scheduler import list_schedule
from scenarios import (
    scenario_small_validation,
    scenario_low_demand,
    scenario_peak_demand,
    scenario_mixed_deadlines,
)


def print_schedule_result(name: str, result) -> None:
    print(f"\n=== {name} ===")
    print(
        f"served: {int(result.metrics['n_served'])}, "
        f"dropped: {int(result.metrics['n_dropped'])}, "
        f"sum_flow: {result.metrics['sum_flow']:.3f}, "
        f"avg_wait: {result.metrics['avg_wait']:.3f}, "
        f"utilisation: {result.metrics['utilisation']:.3f}"
    )

    for sj in sorted(result.scheduled, key=lambda x: (x.machine, x.start)):
        print(
            f"  M{sj.machine}: {sj.job.id} "
            f"start={sj.start:.2f} finish={sj.finish:.2f}"
        )

    if result.dropped:
        dropped_ids = [job.id for job in result.dropped]
        print(f"  Dropped: {dropped_ids}")


def save_results_to_csv(csv_path: str, rows: list[dict]) -> None:
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    if not rows:
        return

    fieldnames = list(rows[0].keys())
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_experiment_set():
    scenarios = {
        "small_validation": scenario_small_validation,
        "low_demand": scenario_low_demand,
        "peak_demand": scenario_peak_demand,
        "mixed_deadlines": scenario_mixed_deadlines,
    }

    methods: Dict[str, Tuple[Callable, bool]] = {
        "FCFS": (key_fcfs, False),
        "SPT": (key_spt, False),
        "SPT+feas": (key_spt, True),
        "EDF+feas": (key_edf, True),
        "MinSlack+feas": (key_min_slack, True),
        "Weighted(alpha=0.7)+feas": (make_key_weighted(alpha=0.7), True),
    }

    rows = []

    for scenario_name, scenario_fn in scenarios.items():
        jobs, m = scenario_fn()
        print(f"\n\n######## Scenario: {scenario_name} ########")

        for method_name, (key_fn, use_filter) in methods.items():
            result = list_schedule(jobs, m, key_fn, use_deadline_filter=use_filter)
            print_schedule_result(method_name, result)

            row = {
                "scenario": scenario_name,
                "method": method_name,
                "machines": m,
                "n_total": result.metrics["n_total"],
                "n_served": result.metrics["n_served"],
                "n_dropped": result.metrics["n_dropped"],
                "served_ratio": result.metrics["served_ratio"],
                "sum_C": result.metrics["sum_C"],
                "avg_C": result.metrics["avg_C"],
                "sum_flow": result.metrics["sum_flow"],
                "avg_flow": result.metrics["avg_flow"],
                "sum_wait": result.metrics["sum_wait"],
                "avg_wait": result.metrics["avg_wait"],
                "hard_deadline_misses": result.metrics["hard_deadline_misses"],
                "Lmax": result.metrics["Lmax"],
                "sum_tardiness": result.metrics["sum_tardiness"],
                "utilisation": result.metrics["utilisation"],
                "makespan": result.makespan,
            }
            rows.append(row)

    save_results_to_csv("results/experiment_results.csv", rows)
    print("\nResults saved to results/experiment_results.csv")


if __name__ == "__main__":
    run_experiment_set()