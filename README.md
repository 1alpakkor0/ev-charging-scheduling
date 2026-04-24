# EV Charging Scheduling Optimisation

This project focuses on designing and evaluating scheduling algorithms for Electric Vehicle (EV) charging systems with the primary objective of **minimising total flow time** while maintaining efficient charger utilisation and an acceptable served ratio.

The system models EV charging requests as scheduling jobs and applies different heuristic algorithms to analyse performance under various demand scenarios.

---

## Project Objectives

The main objectives of this project are:

- **Minimise Total Flow Time (Primary Objective)**  
  Reduce the total time vehicles spend in the system from arrival to completion.

- **Maximise Charger Utilisation**  
  Ensure charging stations are used efficiently with minimal idle time.

- **Maintain a Balanced Served Ratio**  
  Evaluate the trade-off between serving more vehicles and maintaining system efficiency.

---

## Problem Description

The EV charging scheduling problem is modelled using classical scheduling theory notation:

P | r_j, p_j, D_j | Σ(C_j − r_j)

Where:

- r_j: arrival time (release time)  
- p_j: charging duration (processing time)  
- D_j: hard deadline (must be satisfied)  
- C_j: completion time  

The objective is to minimise total flow time:

Σ(C_j − r_j)

---

## System Design

The system is built using a **list scheduling simulation framework**, where:

- Jobs (EV charging requests) arrive dynamically  
- Chargers (machines) process jobs  
- At each decision point, a scheduling rule selects the next job  

---

## Scheduling Algorithms Implemented

### 🔹 Classical Algorithms
- FCFS (First Come First Served)  
- SPT (Shortest Processing Time)  

### 🔹 Feasibility-Aware Algorithms
- SPT + Feasibility Filter  
- EDF (Earliest Deadline First) + Feasibility  
- Minimum Slack Time (MST) + Feasibility  
- Weighted Heuristic  

---

## Feasibility Constraint

A job is only scheduled if:

t + p_j ≤ D_j

This ensures that only jobs that can meet their deadlines are considered.

---

## Performance Metrics

The system evaluates algorithms using the following metrics:

- Total Flow Time → Primary optimisation objective  
- Average Waiting Time  
- Served Ratio → Number of jobs served / total jobs  
- Charger Utilisation  
- Deadline Violations  
- Tardiness and Lateness (optional)  

---

## Project Structure

```text
EV-CHARGING-SCHEDULING/
│
├── diagrams/                 # System diagrams
├── results/
│   ├── figures/             # Generated graphs
│   ├── experiment_results.csv
│   └── .gitkeep
│
├── src/
│   ├── __init__.py
│   ├── heuristics.py
│   ├── main.py
│   ├── metrics.py
│   ├── models.py
│   ├── plot_results.py
│   ├── scenarios.py
│   └── scheduler.py
│
├── README.md
└── requirements.txt

```

## Scenarios Tested

The system is evaluated under multiple conditions:

- Small Validation Scenario  
  Used to verify correctness and expected behaviour  

- Low Demand Scenario  
  System capacity exceeds demand  

- Peak Demand Scenario  
  High congestion and resource competition  

- Mixed Deadlines Scenario  
  Jobs with varying urgency levels  

---

## Results Summary

Key findings from the experiments:

- Feasibility-aware algorithms reduce **total flow time by over 50%**  
- Classical methods (FCFS, SPT):  
  - Serve all jobs  
  - But create congestion and delays  
- Feasibility-aware methods:  
  - Serve fewer jobs  
  - But significantly improve efficiency  
- Charger utilisation remains high even when jobs are filtered  

---

## Key Insight

> Minimising total flow time requires controlling system load, not just prioritising jobs.

Rejecting infeasible jobs improves:
- system stability  
- processing speed  
- overall performance  

---

## Graphs and Visualisation

The project generates graphs to visualise:

- Total Flow Time comparison  
- Served Ratio comparison  
- Charger Utilisation comparison  

Graphs are generated using:
- matplotlib  

---

## Technologies Used

- Python 3  
- dataclasses  
- heapq (priority queues)  
- math  
- matplotlib (for plotting)  
- draw.io (for diagrams)  

---

