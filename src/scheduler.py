from __future__ import annotations
from typing import Callable, List, Tuple
import heapq

from models import Job, ScheduledJob, ScheduleResult
from heuristics import feasible_if_started_now
from metrics import compute_metrics


def list_schedule(
    jobs: List[Job],
    m: int,
    key_fn: Callable[[Job, float], Tuple],
    use_deadline_filter: bool = True,
) -> ScheduleResult:
    """
    Event-driven non-preemptive list scheduling for identical parallel machines.

    Parameters:
        jobs: List of jobs to schedule.
        m: Number of identical machines (chargers).
        key_fn: Heuristic priority function.
        use_deadline_filter: If True, only consider jobs that can still meet hard deadlines.

    Returns:
        ScheduleResult
    """
    if m <= 0:
        raise ValueError("Number of machines m must be positive")

    jobs_sorted = sorted(jobs, key=lambda j: (j.r, j.id))
    n = len(jobs_sorted)

    # Machine availability heap: (available_time, machine_id)
    machine_heap = [(0.0, i) for i in range(m)]
    heapq.heapify(machine_heap)

    t = 0.0
    idx = 0
    available: List[Job] = []
    scheduled: List[ScheduledJob] = []
    dropped: List[Job] = []

    def push_arrivals(up_to_t: float) -> None:
        nonlocal idx
        while idx < n and jobs_sorted[idx].r <= up_to_t + 1e-9:
            available.append(jobs_sorted[idx])
            idx += 1

    while idx < n or available:
        avail_time, mid = heapq.heappop(machine_heap)
        t = max(t, avail_time)

        push_arrivals(t)

        if not available and idx < n:
            next_r = jobs_sorted[idx].r
            t = max(t, next_r)
            push_arrivals(t)

        feasible_jobs = available
        if use_deadline_filter:
            feasible_jobs = [j for j in available if feasible_if_started_now(j, t)]

        if not feasible_jobs:
            still_available = []
            for j in available:
                # If infeasible now under a hard deadline, it will remain infeasible later.
                if j.D is not None and (t + j.p) > j.D + 1e-9:
                    dropped.append(j)
                else:
                    still_available.append(j)
            available = still_available

            heapq.heappush(machine_heap, (t, mid))
            continue

        chosen = min(feasible_jobs, key=lambda j: key_fn(j, t))
        available.remove(chosen)

        start = max(t, chosen.r)
        finish = start + chosen.p

        scheduled.append(
            ScheduledJob(
                job=chosen,
                machine=mid,
                start=start,
                finish=finish
            )
        )

        heapq.heappush(machine_heap, (finish, mid))

    makespan = max((sj.finish for sj in scheduled), default=0.0)
    metrics = compute_metrics(jobs, scheduled, dropped, m)
    return ScheduleResult(
        scheduled=scheduled,
        dropped=dropped,
        makespan=makespan,
        metrics=metrics
    )