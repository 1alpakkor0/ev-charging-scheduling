from __future__ import annotations
from typing import List, Tuple

from models import Job


def scenario_small_validation() -> Tuple[List[Job], int]:
    """
    Small scenario for manual validation.
    """
    jobs = [
        Job("EV1", r=10.00, p=2.00, D=13.00, d=12.50),
        Job("EV2", r=10.00, p=2.00, D=13.00, d=12.00),
        Job("EV3", r=10.50, p=1.50, D=13.00, d=12.75),
        Job("EV4", r=11.00, p=1.00, D=12.50, d=12.25),
    ]
    m = 2
    return jobs, m


def scenario_low_demand() -> Tuple[List[Job], int]:
    jobs = [
        Job("EV1", r=8.00, p=1.0, D=10.0, d=9.5),
        Job("EV2", r=8.50, p=1.5, D=11.0, d=10.5),
        Job("EV3", r=9.00, p=1.0, D=11.5, d=11.0),
    ]
    m = 2
    return jobs, m


def scenario_peak_demand() -> Tuple[List[Job], int]:
    jobs = [
        Job("EV1", r=8.00, p=2.0, D=11.0, d=10.5),
        Job("EV2", r=8.10, p=1.5, D=10.5, d=10.0),
        Job("EV3", r=8.20, p=1.0, D=10.0, d=9.75),
        Job("EV4", r=8.30, p=2.5, D=12.0, d=11.5),
        Job("EV5", r=8.40, p=1.0, D=9.8, d=9.5),
        Job("EV6", r=8.50, p=1.2, D=10.8, d=10.5),
    ]
    m = 2
    return jobs, m


def scenario_mixed_deadlines() -> Tuple[List[Job], int]:
    jobs = [
        Job("EV1", r=9.00, p=1.5, D=11.00, d=10.75),
        Job("EV2", r=9.10, p=0.8, D=10.20, d=10.10),
        Job("EV3", r=9.20, p=2.0, D=12.00, d=11.75),
        Job("EV4", r=9.50, p=1.0, D=10.80, d=10.60),
        Job("EV5", r=10.00, p=0.7, D=10.90, d=10.80),
    ]
    m = 2
    return jobs, m