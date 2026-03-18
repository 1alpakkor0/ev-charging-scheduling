from __future__ import annotations
from typing import Callable, Optional, Tuple
import math

from models import Job


def feasible_if_started_now(job: Job, t: float) -> bool:
    """
    Returns True if job can start at time t and still satisfy its hard deadline.
    """
    if job.D is None:
        return True
    return (t + job.p) <= job.D + 1e-9


def slack(job: Job, t: float) -> float:
    """
    Slack relative to hard deadline:
        slack = D - t - p

    Smaller slack means higher urgency.
    If no hard deadline exists, return infinity.
    """
    if job.D is None:
        return float("inf")
    return job.D - t - job.p


def key_fcfs(job: Job, t: float) -> Tuple[float, str]:
    """
    First Come First Served:
    prioritise earliest arrival time.
    """
    return (job.r, job.id)


def key_spt(job: Job, t: float) -> Tuple[float, float, str]:
    """
    Shortest Processing Time:
    prioritise smallest charging duration.
    """
    return (job.p, job.r, job.id)


def key_edf(job: Job, t: float) -> Tuple[float, float, float, str]:
    """
    Earliest Deadline First:
    prioritise smallest hard deadline D.
    If no deadline exists, treat as infinity.
    """
    D = job.D if job.D is not None else float("inf")
    return (D, job.p, job.r, job.id)


def key_min_slack(job: Job, t: float) -> Tuple[float, float, float, str]:
    """
    Minimum Slack Time:
    prioritise smallest slack.
    """
    return (slack(job, t), job.p, job.r, job.id)


def make_key_weighted(alpha: float, eps: float = 1e-3) -> Callable[[Job, float], Tuple[float, str]]:
    """
    Weighted trade-off between short jobs and urgent jobs.

    Score:
        score = alpha * (1 / p) + (1 - alpha) * (1 / (slack + eps))

    Higher score is better, so we return negative score for min().
    alpha close to 1 => prioritise short jobs more
    alpha close to 0 => prioritise urgent jobs more
    """
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha must be between 0 and 1")

    def key(job: Job, t: float) -> Tuple[float, str]:
        inv_p = 1.0 / max(job.p, eps)
        s = slack(job, t)
        inv_slack = 0.0 if math.isinf(s) else 1.0 / max(s + eps, eps)
        score = alpha * inv_p + (1.0 - alpha) * inv_slack
        return (-score, job.id)

    return key