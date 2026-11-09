# University of Ghana — Department of Computer Science
## DCIT 313: Introduction to Artificial Intelligence
### Lecture 2 Laboratory Report: Problem Solving and Heuristic Search

---

## 1. Intended Learning Outcomes & Scope
This laboratory demonstrates competency in state-space formulation, uninformed search, cost-sensitive search, and informed heuristic search:
1. Formulating a deterministic graph search problem as a formal 5-tuple.
2. Tracing and implementing Breadth-First Search (BFS), Uniform-Cost Search (UCS), Greedy Best-First Search, and A* using Python's standard library.
3. Conducting rigorous heuristic audits for admissibility ($h(n) \le h^*(n)$) and consistency/monotonicity ($h(u) \le c(u, v) + h(v)$).
4. Implementing 4-connected grid pathfinding using the Manhattan distance heuristic.
5. Evaluating edge-case robustness (unreachable goals, zero-cost edges, and negative-weight rejection).

---

## 2. Activity A — Problem Formulation: Campus Referral Network

### Formal 5-Tuple Specification
- **State Space ($S$):** $S = \{S, A, B, C, D, E, G\}$, representing key campus junctions:
  - $S$: Campus gate (Start)
  - $A$: Library junction
  - $B$: Market road
  - $C$: Student hostel
  - $D$: Main junction
  - $E$: Clinic road
  - $G$: District hospital (Goal)
- **Initial State ($s_0$):** $s_0 = S$.
- **Action Set ($A(s)$):** Legal directed edges departing from node $s$:
  - $A(S) = \{A, B\}$
  - $A(A) = \{C, D\}$
  - $A(B) = \{D, E\}$
  - $A(C) = \{D, G\}$
  - $A(D) = \{E, G\}$
  - $A(E) = \{G\}$
  - $A(G) = \emptyset$ (Terminal goal node)
- **Transition Function ($T(s, a)$):** Deterministic successor state mapping: $T(s, a) = a$.
- **Goal Test ($\text{Goal}(s)$):** Evaluates whether $s == G$.
- **Step-Cost Function ($c(s, a, s')$):** Abstract non-negative weights from `synthetic_route_edges.csv`.

### Modeling Assumptions & Real-World Limitations
1. **Sufficiency of "Current Node" State:** The environment is static, fully observable, deterministic, and Markovian. The cheapest route from any junction depends exclusively on the current node, independent of how the agent arrived there.
2. **Real-World State Augmentations:**
   - **Time-Dependent Traffic:** Edge costs fluctuate dynamically with time of day; the state space must be augmented to $(s, t)$ where $t$ is the current time.
   - **Energy / Fuel Constraints:** For an electric vehicle or battery-operated transport, state must track remaining state of charge $(s, \text{SoC})$.
3. **Hop Count vs. Route Cost:** Minimizing hops is **not** equivalent to minimizing path cost when edge weights vary. BFS finds the shallowest path ($S \to A \to C \to G$, 3 hops) but incurs a high cost of 14, whereas UCS finds a 4-hop path ($S \to B \to D \to E \to G$) costing only 9.

---

## 3. Activity B & C — Search Algorithm Hand Traces

### Directed Network Topology
- $S \to A (2), S \to B (4)$
- $A \to C (2), A \to D (5)$
- $B \to D (1), B \to E (4)$
- $C \to D (2), C \to G (10)$
- $D \to E (1), D \to G (5)$
- $E \to G (3)$
- $G$: terminal

### Activity B — BFS Trace (Alphabetical Successors, Mark on Enqueue)
| Pop # | Node Popped | Frontier Queue After Expansion | Discovered / Parent Pointers | Observation |
| :---: | :---: | :--- | :--- | :--- |
| **1** | $S$ | $[A, B]$ | $S: \text{None}, A: S, B: S$ | Enqueue $A, B$ |
| **2** | $A$ | $[B, C, D]$ | $C: A, D: A$ | Enqueue $C, D$ |
| **3** | $B$ | $[C, D, E]$ | $E: B$ | $D$ already discovered via $A$; enqueue $E$ |
| **4** | $C$ | $[D, E, G]$ | $G: C$ | $D$ discovered; enqueue $G$ |
| **5** | $D$ | $[E, G]$ | — | $E, G$ already discovered |
| **6** | $E$ | $[G]$ | — | $G$ already discovered |
| **7** | $G$ | $[]$ | — | **Goal Test on Pop:** Goal reached! |

- **Reconstructed BFS Route:** $S \to A \to C \to G$
- **Total Edge Count:** 3 hops
- **Total Weighted Cost:** $2 + 2 + 10 = \mathbf{14.0}$
- **Expansion Order:** $[S, A, B, C, D, E, G]$ (7 nodes)

---

### Activity C — UCS Trace (Priority $g(n)$, Stale Entry Discard)
| Pop # | Node Popped | Cost $g$ at Pop | Priority Queue Frontier | Updates to $\text{best\_g}$ & Parent |
| :---: | :---: | :---: | :--- | :--- |
| **1** | $S$ | 0.0 | $[(2, A), (4, B)]$ | $\text{best\_g}[S]=0, \text{best\_g}[A]=2, \text{best\_g}[B]=4$ |
| **2** | $A$ | 2.0 | $[(4, B), (4, C), (7, D)]$ | $\text{best\_g}[C]=4, \text{best\_g}[D]=7$ |
| **3** | $B$ | 4.0 | $[(4, C), (5, D), (7, D), (8, E)]$ | Relax $B \to D$: $4+1=5 < 7 \implies \text{best\_g}[D]=5, P[D]=B$; $\text{best\_g}[E]=8$ |
| **4** | $C$ | 4.0 | $[(5, D), (7, D), (8, E), (14, G)]$ | $C \to D: 4+2=6 \not< 5$; $\text{best\_g}[G]=14$ |
| **5** | $D$ | 5.0 | $[(6, E), (7, D), (8, E), (10, G), (14, G)]$ | Relax $D \to E: 5+1=6 < 8 \implies \text{best\_g}[E]=6$; Relax $D \to G: 5+5=10 < 14 \implies \text{best\_g}[G]=10$ |
| **6** | $E$ | 6.0 | $[(7, D), (8, E), (9, G), (10, G), (14, G)]$ | Relax $E \to G: 6+3=9 < 10 \implies \text{best\_g}[G]=9$ |
| — | $D$ | 7.0 | — | **Stale entry** ($7 > \text{best\_g}[D]=5$); discard |
| — | $E$ | 8.0 | — | **Stale entry** ($8 > \text{best\_g}[E]=6$); discard |
| **7** | $G$ | 9.0 | — | **Goal Test on Pop:** Goal reached! |

- **Reconstructed UCS Route:** $S \to B \to D \to E \to G$
- **Total Edge Count:** 4 hops
- **Total Weighted Cost:** $4 + 1 + 1 + 3 = \mathbf{9.0}$ (Cost-Optimal)
- **Expansion Order:** $[S, A, B, C, D, E, G]$ (7 nodes)

---

## 4. Activity D — Heuristic Proof & Consistency Audit

### Ground Truth Least-Cost-to-Goal ($h^*(n)$)
Using backward propagation from goal $G$:
- $h^*(G) = 0$
- $h^*(E) = c(E, G) = 3$
- $h^*(D) = \min(c(D, E) + h^*(E), c(D, G)) = \min(1 + 3, 5) = \mathbf{4}$
- $h^*(C) = \min(c(C, D) + h^*(D), c(C, G)) = \min(2 + 4, 10) = \mathbf{6}$
- $h^*(B) = \min(c(B, D) + h^*(D), c(B, E) + h^*(E)) = \min(1 + 4, 4 + 3) = \mathbf{5}$
- $h^*(A) = \min(c(A, C) + h^*(C), c(A, D) + h^*(D)) = \min(2 + 6, 5 + 4) = \mathbf{8}$
- $h^*(S) = \min(c(S, A) + h^*(A), c(S, B) + h^*(B)) = \min(2 + 8, 4 + 5) = \mathbf{9}$

### Admissibility Audit Table
| Node ($n$) | Given $h(n)$ | True $h^*(n)$ | Admissible ($h(n) \le h^*(n)$)? | Example Edge Consistency Check |
| :---: | :---: | :---: | :---: | :--- |
| **$S$** | 8.0 | 9.0 | **Yes** ($8 \le 9$) | $h(S)=8 \le c(S,B)+h(B)=4+4=8$ |
| **$A$** | 8.0 | 8.0 | **Yes** ($8 \le 8$) | $h(A)=8 \le c(A,C)+h(C)=2+6=8$ |
| **$B$** | 4.0 | 5.0 | **Yes** ($4 \le 5$) | $h(B)=4 \le c(B,D)+h(D)=1+4=5$ |
| **$C$** | 6.0 | 6.0 | **Yes** ($6 \le 6$) | $h(C)=6 \le c(C,D)+h(D)=2+4=6$ |
| **$D$** | 4.0 | 4.0 | **Yes** ($4 \le 4$) | $h(D)=4 \le c(D,E)+h(E)=1+3=4$ |
| **$E$** | 3.0 | 3.0 | **Yes** ($3 \le 3$) | $h(E)=3 \le c(E,G)+h(G)=3+0=3$ |
| **$G$** | 0.0 | 0.0 | **Yes** ($0 \le 0$) | Terminal ($h(G) = 0$) |

**Conclusion on Original Heuristic:** Admissible across all states. Zero consistency violations across all 11 directed edges.

### Deliberately Inadmissible Modification: $h(B) = 7.0$
- **Admissibility Check:** $h(B) = 7.0 > h^*(B) = 5.0$. **Inadmissible** (overestimates remaining cost by 2.0 units).
- **Consistency Check:** For directed edge $B \to D$ ($c=1.0$):
  $$h(B) = 7.0, \quad c(B, D) + h(D) = 1.0 + 4.0 = 5.0 \implies 7.0 > 5.0 \quad (\mathbf{VIOLATION!})$$
- **Theoretical Guarantee Lost:** Monotonicity is broken. A* with graph search without reopening can pop a node prematurely through an overestimated branch and fail to return the optimal cost.

---

## 5. Activity E — 6×6 Obstacle Grid Search

### Grid Topology
```
S . . . . .
. # # # . .
. . . # . .
. # . . . .
. # . # # .
. . . . . G
```
- Start: $(0, 0)$
- Destination: $(5, 5)$
- Inaccessible cells (`#`): $(1,1), (1,2), (1,3), (2,3), (3,1), (4,1), (4,3), (4,4)$
- Legal movements: Orthogonal 4-connectivity (Up, Down, Left, Right) with unit cost 1.0.

### Admissibility Proof of Manhattan Distance
The Manhattan distance heuristic is defined as:
$$h((r, c)) = |r - r_{\text{goal}}| + |c - c_{\text{goal}}|$$
Under 4-connected unit-cost movements, each horizontal move changes $c$ by at most 1, and each vertical move changes $r$ by at most 1. In a barrier-free relaxation, the minimum number of steps required to reach $(r_{\text{goal}}, c_{\text{goal}})$ is exactly $|r - r_{\text{goal}}| + |c - c_{\text{goal}}|$. Any obstacles (`#`) can only force detours, strictly increasing the true step count $h^*((r,c)) \ge h((r,c))$. Thus, Manhattan distance is a mathematically proven lower bound (admissible and consistent).

### Grid A* Output
- **Optimal Route (10 steps):**
  $$(0,0) \to (0,1) \to (0,2) \to (0,3) \to (0,4) \to (0,5) \to (1,5) \to (2,5) \to (3,5) \to (4,5) \to (5,5)$$
- **Total Weighted Path Cost:** **10.0**
- **Nodes Expanded:** **11 nodes** (expanded only the nodes on the direct optimal trajectory).

---

## 6. Activity F — Comprehensive Results & Comparative Analysis

### Comprehensive Algorithm Comparison Table
| Algorithm | Returned Route | Total Cost | Nodes Expanded | Execution Characteristics |
| :--- | :--- | :---: | :---: | :--- |
| **BFS** | `['S', 'A', 'C', 'G']` | **14.0** | 7 | Shallowest path (3 hops); ignores weights; suboptimal cost. |
| **DFS** | `['S', 'A', 'C', 'D', 'E', 'G']` | **10.0** | 6 | Deep exploration; non-optimal; sensitive to child order. |
| **UCS** | `['S', 'B', 'D', 'E', 'G']` | **9.0** | 7 | Cost-optimal; explores all frontiers below optimal cost. |
| **Greedy** | `['S', 'B', 'E', 'G']` | **11.0** | 4 | Extremely fast; myopic; traps into suboptimal path. |
| **A\*** | `['S', 'B', 'D', 'E', 'G']` | **9.0** | **5** | **Cost-optimal; prunes branches $A$ and $C$; fewest optimal expansions.** |

### Robustness & Invariant Validations
1. **Unreachable Goal Test:** In a disconnected graph, the priority queue exhausts all reachable components and terminates safely returning `path = None` and $\text{cost} = \infty$ without infinite loops.
2. **Zero-Cost Edge Invariant:** Introducing an edge with $c=0.0$ does not induce infinite cycling; UCS/A* maintain non-decreasing priorities and find the optimal route.
3. **Negative Edge Cost Invariant:** The algorithms strictly validate non-negative edge weights upon invocation, throwing a `ValueError` if any negative cost is detected, preventing cyclic infinite negative loops.

---

## 7. Reflection: The Engineer’s Perspective
- **Transitioning from Classroom Model to Real Deployment:** In emergency referral routing, edge costs cannot remain static scalars. Costs must incorporate continuous traffic telemetry, road surface conditions, weather, and time of day. Probabilistic arrival models (e.g., Markov Decision Processes) would be required to handle stochastic delays.
- **When is a Shorter-in-Hops Route Preferred?** In physical vehicular routing, every extra turn or junction transition increases mechanical wear, risk of collisions, and navigational confusion. A 3-hop route with cost 10 may be preferred over a complex 7-hop maze with cost 9 to minimize driver cognitive load and junction accident exposure.
- **Admissibility Proof vs. Empirical Testing:** Testing $h(n) \le h^*(n)$ on sample graphs proves correctness only for those specific instances. An engineering proof establishes mathematical lower-bound guarantees across all possible state configurations (e.g. Euclidean or Manhattan triangle inequality).

---

## 8. Academic Integrity & GenAI Disclosure
- **Tool Used:** Generative AI was utilized for boilerplate code formatting, table generation, and LaTeX formatting.
- **Independent Verification:** All algorithm implementations (deque-based BFS, priority-queue UCS/Greedy/A*, grid converter, and DFS), state traces, mathematical lower bound proofs, and consistency calculations were independently derived, executed, and validated against the course rubric.
