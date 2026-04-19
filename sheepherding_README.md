# Sheepherding Puzzle — A* Search

An implementation of the A* search algorithm applied to a sheepherding puzzle, built in Python using an informed search framework.

The puzzle involves herding an unlimited field of sheep into two fixed-capacity pens (A and B) using the lowest-cost sequence of moves.

---

## The Problem

Given:
- **Pen A** with capacity `Amax`
- **Pen B** with capacity `Bmax`
- An **unbounded field** of sheep
- A **goal state** (target sheep in each pen)

Find the **lowest-cost sequence of moves** to reach the goal.

---

## Actions and Costs

| Action | Cost |
|------|------|
| Field → Pen A | 60s |
| Field → Pen B | 60s |
| Pen → Field | 5s |
| Pen A ↔ Pen B | 30s |

---

## A* Search

The search uses:

f(n) = g(n) + h(n)

- g(n) = actual cost from start  
- h(n) = estimated cost to goal  

The fringe is maintained using binary insertion, improving efficiency over linear insertion.

---

## Heuristic

h(n) = (|a - a_goal| + |b - b_goal|) × 5

- Based on Manhattan distance  
- Uses minimum possible move cost (5s)  
- Guarantees admissibility → optimal solutions  

### Heuristic Comparison

| Heuristic | Multiplier | Property | Result |
|----------|----------|--------|--------|
| Conservative | ×5 | Admissible | Optimal |
| Aggressive | ×39 | Not guaranteed admissible | Faster, may be suboptimal |

---

## State Representation

Each state stores:
- a_sheep
- b_sheep
- field_sheep

Equality is based only on pen values.

Important:
If a == b then hash(a) must equal hash(b)

Fixing this was critical to prevent invalid paths.

---

## Project Structure

sheepherding_puzzle/
├── README.md
├── report/
│   └── sheepherding_A_grade_report_merged.docx
├── src/
│   ├── Main.py
│   └── aips/
│       ├── search.py
│       └── informed/
│           └── search.py

---

## Running the Code

python src/Main.py

Default parameters:

Amax = 9
Bmax = 15
A0   = 0
B0   = 0
An   = 0
Bn   = 12

---

## Example Output (Simplified)

Cost: 2430.0

Pen A: 0, Pen B: 0
→ Move 15 sheep to Pen B
→ Move 9 sheep to Pen A
→ ...
→ Goal reached

---

## Data Structures Used

| Structure | Role |
|----------|------|
| Priority Queue | Fringe ordering |
| HashMap | Visited tracking |
| Linked List | Path reconstruction |
| Binary insertion | Efficient ordering |

---

## Coursework Report

See report/sheepherding_report.docx for full write-up.

---

## Improvements

- Fixed hashing bug
- Removed globals
- Improved heuristic
- Validated outputs

---

## Motivation

Originally coursework, later refined to improve correctness and design.
