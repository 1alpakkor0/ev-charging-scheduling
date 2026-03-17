from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Job:
    """
    An EV charging request modelled as a scheduling job.

    Attributes:
        id: Unique job identifier.
        r: Release time (arrival time).
        p: Processing time (required charging duration).
        D: Hard deadline (cannot be violated). Optional.
        d: Soft due date (can be violated, used for lateness/tardiness). Optional.
    """
    id: str
    r: float
    p: float
    D: Optional[float] = None
    d: Optional[float] = None


@dataclass
class ScheduledJob:
    """
    A scheduled instance of a job on a specific machine.
    """
    job: Job
    machine: int
    start: float
    finish: float


@dataclass
class ScheduleResult:
    """
    Output of a scheduling run.

    Attributes:
        scheduled: Jobs successfully scheduled.
        dropped: Jobs not served due to infeasibility.
        makespan: Maximum completion time among scheduled jobs.
        metrics: Dictionary of performance metrics.
    """
    scheduled: List[ScheduledJob]
    dropped: List[Job]
    makespan: float
    metrics: Dict[str, float]