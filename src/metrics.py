from __future__ import annotations
from typing import Dict, List

from models import Job, ScheduledJob


def compute_metrics(
    all_jobs: List[Job],
    scheduled: List[ScheduledJob],
    dropped: List[Job],
    m: int
) -> Dict[str, float]:
    """
    Compute the main performance metrics for a schedule.
    """
    served = scheduled
    n_served = len(served)
    n_total = len(all_jobs)

    sum_C = sum(sj.finish for sj in served)
    sum_flow = sum((sj.finish - sj.job.r) for sj in served)
    sum_p = sum(sj.job.p for sj in served)

    # Waiting time: Wj = (Cj - rj) - pj
    sum_wait = sum_flow - sum_p
    avg_wait = (sum_wait / n_served) if n_served > 0 else 0.0
    avg_flow = (sum_flow / n_served) if n_served > 0 else 0.0
    avg_C = (sum_C / n_served) if n_served > 0 else 0.0

    hard_misses = 0
    for sj in served:
        if sj.job.D is not None and sj.finish > sj.job.D + 1e-9:
            hard_misses += 1

    lateness = []
    tardiness = []
    for sj in served:
        if sj.job.d is None:
            continue
        L = sj.finish - sj.job.d
        lateness.append(L)
        tardiness.append(max(0.0, L))

    Lmax = max(lateness) if lateness else 0.0
    sumT = sum(tardiness) if tardiness else 0.0

    if served:
        horizon_start = min(sj.start for sj in served)
        horizon_end = max(sj.finish for sj in served)
        total_capacity = m * (horizon_end - horizon_start)
        used = sum(sj.job.p for sj in served)
        utilisation = used / total_capacity if total_capacity > 1e-9 else 0.0
    else:
        utilisation = 0.0

    return {
        "n_total": float(n_total),
        "n_served": float(n_served),
        "n_dropped": float(len(dropped)),
        "served_ratio": (n_served / n_total) if n_total > 0 else 0.0,
        "sum_C": sum_C,
        "avg_C": avg_C,
        "sum_flow": sum_flow,
        "avg_flow": avg_flow,
        "sum_wait": sum_wait,
        "avg_wait": avg_wait,
        "hard_deadline_misses": float(hard_misses),
        "Lmax": Lmax,
        "sum_tardiness": sumT,
        "utilisation": utilisation,
    }