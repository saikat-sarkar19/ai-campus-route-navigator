# CU Technology Campus AI Route Navigator

**Assignment X_03 | AI/ML Laboratory | B.Tech. 5th Semester**

An AI-based campus navigation system for the University of Calcutta (CU) Technology Campus. This system models the campus layout as a weighted graph, implements two distinct pathfinding agents (**PATHFINDER** using Greedy Best-First Search and **ORBIT** using A* Search), enforces domain-specific rules (the Special CSE Routing Constraint), and evaluates their computational behavior across multiple routing scenarios.

---

## 🏗️ Project Architecture & OOP Structure

The project is structured into modular Python components following Object-Oriented Programming (OOP) principles and file separation:

```text
campus-navigator/
├── main.py           # User interface (CLI & interactive route prompt)
├── campus_map.py     # Graph representation, Location nodes, SearchState, CSE rules
├── search.py         # Search implementations: Greedy Best-First Search & A* Search
├── agents.py         # Agent classes: PathfinderAgent & OrbitAgent
├── experiment.py     # Automated benchmark experiment suite & result logging
├── campus.json       # External JSON data store for campus graph (nodes, edges, weights)
├── results.csv       # Saved experimental routing metrics and comparison
└── README.md         # Comprehensive documentation and experimental observations
```

---

## 🧠 Navigation Agents & Algorithms

### 1. PATHFINDER Agent (Greedy Best-First Search)
- **Evaluation Function:** \( f(n) = h(n) \)
- **Behavior:** Always expands the node that appears closest to the destination in terms of straight-line (Euclidean) distance, ignoring accumulated travel cost \( g(n) \).
- **Pros/Cons:** Fast frontier expansion, but susceptible to suboptimal routes and heuristic traps.

### 2. ORBIT Agent (A* Search)
- **Evaluation Function:** \( f(n) = g(n) + h(n) \)
- **Behavior:** Combines the actual walking cost traveled so far \( g(n) \) with the estimated Euclidean distance remaining \( h(n) \).
- **Pros/Cons:** Guarantees finding the optimal (shortest cost) route when used with an admissible heuristic.

---

## 🔒 Special CSE Routing Rule & State Representation

The campus includes a restricted CSE Zone consisting of:
- `CSE Laboratory`
- `CSE_AKC Seminar Hall`
- `CSE_Reflxon Room`

### Access Rules:
1. **Entry Rule:** To enter any CSE-labelled location, the route MUST follow:
   $$\text{Tower 2 Front/Rear Entry} \rightarrow \text{Lift Area} \rightarrow \text{CSE Location}$$
2. **Inside Rule:** Once the `Lift Area` is crossed during entry, only CSE-labelled locations may be visited until returning to `Lift Area`.
3. **Exit Rule:** To exit to the rest of the campus, the route MUST follow:
   $$\text{CSE Location} \rightarrow \text{Lift Area} \rightarrow \text{Tower 2 Front/Rear Entry} \rightarrow \text{Other Campus Locations}$$

### State Machine Implementation (`campus_map.py`):
Search states are tracked as `SearchState(node_name, cse_mode)` with four explicit modes:
- `OUTSIDE`: Standard navigation outside CSE zone.
- `READY_TO_ENTER`: At `Lift Area` via `Tower 2 Front/Rear Entry` (allowed to enter CSE zone).
- `INSIDE`: Inside CSE zone; only CSE nodes or `Lift Area` can be visited.
- `EXITING`: At `Lift Area` coming from CSE zone; must transition to `Tower 2 Front/Rear Entry`.

---

## 📊 Experimental Results (`results.csv`)

| Route | Agent | Path | Cost (m) | Nodes Explored | Execution Time | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **Reception → Library** | PATHFINDER | Reception → Garden Area → Library | 215.0 | 3 | 0.000092 s | Identical |
| | ORBIT | Reception → Garden Area → Library | 215.0 | 3 | 0.000052 s | Identical |
| **Canteen → New Building 2** | PATHFINDER | Canteen → Reception → Garden Area → New Building 2 | 265.0 | 4 | 0.000023 s | **Suboptimal** |
| | ORBIT | Canteen → Reception → Auditorium Hall → New Building 2 | **235.0** | 4 | 0.000021 s | **Optimal** |
| **Entry Gate 1 → CSE Laboratory** | PATHFINDER | Entry Gate 1 → Reception → Garden Area → Lift Area → Tower 2 Front Entry → Lift Area → CSE Lab | 335.0 | 7 | 0.000037 s | **Constraint Trap** |
| | ORBIT | Entry Gate 1 → Reception → CRNN Centre → Tower 2 Front Entry → Lift Area → CSE Lab | **250.0** | 6 | 0.000027 s | **Optimal Path** |
| **Auditorium Hall → CSE_AKC Hall** | PATHFINDER | Auditorium Hall → Tower 2 Front Entry → Lift Area → CSE_AKC Seminar Hall | 115.0 | 4 | 0.000021 s | Identical |
| | ORBIT | Auditorium Hall → Tower 2 Front Entry → Lift Area → CSE_AKC Seminar Hall | 115.0 | 4 | 0.000019 s | Identical |
| **Library → Canteen** | PATHFINDER | Library → Lift Area → Tower 2 Front Entry → CRNN Centre → Reception → Canteen | 245.0 | 6 | 0.000084 s | Alternative |
| | ORBIT | Library → Lift Area → Tower 2 Front Entry → CRNN Centre → Power Area → Canteen | 250.0 | 6 | 0.000034 s | Alternative |

---

## 🔍 Core Observations & Analysis (PART 9)

### 1. Does Greedy Best-First Search always find the shortest route?
**No.** Greedy Best-First Search (\(f(n) = h(n)\)) does **not** guarantee finding the shortest route. Because it evaluates nodes purely based on estimated distance to the destination, it is easily tricked by paths that initially head straight toward the goal but accumulate high physical edge costs. For example, in the `Canteen → New Building 2` route, PATHFINDER chose a path costing **265.0 m**, whereas ORBIT found the optimal path costing **235.0 m**.

### 2. How does A* use the distance already travelled?
A* Search balances the greedy heuristic with past experience using \( f(n) = g(n) + h(n) \). The \( g(n) \) component represents the exact cumulative walking distance from the start node to the current node. If a branch starts accumulating high path distance, its total evaluation score \( f(n) \) increases, causing A* to deprioritize it in the frontier and explore alternative, shorter overall paths.

### 3. When do the two agents choose different paths?
The agents diverge under two main conditions:
1. **Heuristic vs. Total Cost Conflict:** When a visually direct neighbor has a low \( h(n) \) but is connected via high-weight edges or circuitous connections.
2. **Constrained Gateways:** When entering/exiting restricted areas (like the CSE zone), Greedy Best-First takes the nearest gateway node regardless of whether it meets rule preconditions, forcing extra backtracking steps later.

### 4. How does the heuristic affect their behaviour?
The Euclidean distance heuristic \( h(n) \) provides directional bias:
- In **PATHFINDER**, \( h(n) \) acts as the sole driver. If \( h(n) \) misleads the search into a local minimum or invalid constraint path, PATHFINDER cannot recover efficiently.
- In **ORBIT**, \( h(n) \) serves as an admissible guide. Because Euclidean distance is straight-line distance, \( h(n) \le g^*(n) \), satisfying admissibility and consistency, ensuring A* guarantees path optimality.

### 5. What happens when the CSE constraint restricts possible routes?
When navigating into the CSE zone (e.g., `Entry Gate 1 → CSE Laboratory`):
- **PATHFINDER** greedily moved from `Reception` to `Garden Area` and then `Lift Area` because `Garden Area` was closer straight-line to `CSE Laboratory`. However, reaching `Lift Area` via `Garden Area` violates the CSE entry condition (`Tower 2 Front/Rear Entry → Lift Area`). Consequently, PATHFINDER was forced to loop from `Lift Area` out to `Tower 2 Front Entry` and back into `Lift Area`, inflating the route cost to **335.0 m**.
- **ORBIT** accounted for the state constraints and total path cost, choosing `Reception → CRNN Centre → Tower 2 Front Entry → Lift Area → CSE Laboratory` directly for an optimal cost of **250.0 m** (a savings of **85 meters**).

---

## 🚀 How to Run the Project

### Interactive Mode:
```bash
python main.py
```
Or specify start and destination directly:
```bash
python main.py "Entry Gate 1" "CSE Laboratory"
```

### Run Automated Experiments:
```bash
python experiment.py
```
This generates `results.csv` with full experimental data.
