# DCIT 313: Introduction to Artificial Intelligence
**University of Ghana — Department of Computer Science**  
*Practical Laboratory Series & Coursework Portfolio*

---

## 📚 Repository Overview
This repository contains the complete, rigorous implementations and laboratory reports for **DCIT 313: Introduction to Artificial Intelligence**.

Each lab is structured as an independent module containing executed Jupyter notebooks, standalone test suites, dataset assets, and academic laboratory reports aligned with the course's 20-mark evaluation rubrics.

```
DCIT313-Artificial-Intelligence/
├── README.md                                  # Repository overview and guide
├── .gitignore                                 # Python and Jupyter gitignore
├── Lab1-Intelligent-Agents-and-GenAI/         # Lecture 1 Practical Pack
│   ├── DCIT313_Lecture1_Student_Notebook_Reviewed.ipynb  # Executed notebook
│   ├── DCIT313_Lecture1_Student_Lab_Reviewed.docx        # Original manual
│   ├── DCIT313_L1_Student_Claims.csv                     # Completed claims audit
│   ├── LAB1_REPORT.md                                    # Comprehensive report
│   └── test_lab1.py                                      # Unit test suite
└── Lab2-Problem-Solving-and-Heuristic-Search/ # Lecture 2 Practical Pack
    ├── DCIT313_L2_Student_Notebook.ipynb                 # Executed notebook
    ├── DCIT313_Lecture2_Student_Lab_Manual.docx          # Original manual
    ├── README_Student.txt                                # Lab instructions
    ├── synthetic_route_edges.csv                         # Directed edge network
    ├── synthetic_heuristics.csv                          # Heuristic values
    ├── grid_map.txt                                      # 6x6 obstacle grid map
    ├── LAB2_REPORT.md                                    # Comprehensive report
    └── test_lab2.py                                      # Unit test suite
```

---

## 🏛️ Architectural Decision: Single Repository Structure
### *Why One Repository Instead of Multiple Repositories?*
1. **Course Cohesion & Clean Organization:** Both assignments are core progressive milestones in the same semester-long course (**DCIT 313**). Consolidating all lab assignments under a single repository prevents GitHub profile fragmentation and provides a structured portfolio of coursework.
2. **Simplified Academic Submission:** Course instructors and Teaching Assistants can evaluate and clone a single URL containing all lecture labs rather than juggling multiple disconnected repositories.
3. **Reproducibility & Shared Testing:** Standardized Python environments and uniform testing conventions ensure that grading scripts and CI checks run consistently across all labs.

---

## 🔬 Lab 1: Intelligent Agents & GenAI Literacy
**Focus:** PEAS Agent Modeling, Simple Reflex Logic, Cost-Sensitive Evaluation, and Source Grounding.

### Key Deliverables & Results
1. **PEAS Agent Formulation:** Complete specification for an intelligent campus shuttle assistant, including environmental uncertainties, failure mode analysis, and fail-safe minimum departure buffers.
2. **Light-Control Reflex Agent:**
   - Implemented `lighting_agent(occupied, light_lux)` enforcing strict thresholding (`< 300` lux).
   - Implemented `safer_lighting_agent` with input type/range validation, safely trapping unphysical inputs (`None`, $-2$, $\text{NaN}$) into `"MANUAL_REVIEW"`.
3. **Decision Cost Analysis (Spam Filtering):**
   - Assessed two agents across $N=1,000$ emails with asymmetric loss: $C_{FP} = 50, C_{FN} = 10$.
   - **Agent A:** $\text{Accuracy} = 98.80\%, \text{Recall} = 99.88\%, \text{Cost} = 560\text{ units}$.
   - **Agent B:** $\text{Accuracy} = 96.20\%, \text{Recall} = 95.25\%, \text{Cost} = 380\text{ units}$.
   - **Conclusion:** **Agent B is preferred** due to zero false positives, demonstrating that raw accuracy is inadequate under asymmetric error consequences.
   - **Sensitivity Analysis:** Derived algebraic tie threshold $\frac{C_{FP}}{C_{FN}} = \frac{37}{11} \approx 3.3636$.
4. **GenAI Evidence Audit:** Audited all 12 claims in `DCIT313_L1_Student_Claims.csv` against the simulated fact sheet with exact quotation evidence.
5. **Prompt Injection & Security:** Evaluated indirect prompt injection defenses and designed an evidence-grounded system prompt.

---

## 🧭 Lab 2: Problem Solving & Heuristic Search
**Focus:** State-Space Graph Search, Uninformed Search (BFS, DFS), Heuristic Search (UCS, Greedy, A*), and Admissibility/Consistency Auditing.

### Performance Summary Table (Campus Referral Network)
| Algorithm | Returned Route | Total Cost | Nodes Expanded | Search Characteristics |
| :--- | :--- | :---: | :---: | :--- |
| **BFS** | `['S', 'A', 'C', 'G']` | **14.0** | 7 | Fewest hops (3 hops); ignores weights; suboptimal cost. |
| **DFS** | `['S', 'A', 'C', 'D', 'E', 'G']` | **10.0** | 6 | LIFO exploration; non-optimal; depth-first path. |
| **UCS** | `['S', 'B', 'D', 'E', 'G']` | **9.0** | 7 | Cost-optimal; explores all states below optimal cost. |
| **Greedy** | `['S', 'B', 'E', 'G']` | **11.0** | 4 | Myopic; fast (4 expansions); trapped in suboptimal route. |
| **A\*** | `['S', 'B', 'D', 'E', 'G']` | **9.0** | **5** | **Cost-optimal; prunes branches $A$ and $C$; minimal expansions.** |

### Key Deliverables & Results
1. **Formal Problem Formulation:** Formal 5-tuple $\langle S, s_0, A(s), T(s,a), \text{Goal}(s), c(s,a,s') \rangle$.
2. **Standard Library Implementation:** Fully implemented BFS, UCS, Greedy, and A* using only `collections.deque` and `heapq`, featuring lazy deletion for stale heap entries.
3. **Heuristic Admissibility & Consistency Audit:**
   - Computed exact true remaining costs $h^*(n)$ using reverse UCS propagation.
   - Proved original heuristic is strictly admissible ($h \le h^*$) and consistent ($\Delta h \le c$).
   - Demonstrated that setting $h(B) = 7.0$ introduces a consistency violation on edge $B \to D$ ($7.0 > 1.0 + 4.0 = 5.0$) and destroys A* optimality guarantees.
4. **6×6 Grid A\* Pathfinding:** Proved Manhattan distance is an admissible relaxation on orthogonal grids; returned optimal 10-step route expanding only 11 nodes.
5. **Robustness Suites:** Verified termination on disconnected graphs, zero-cost edge loops, and runtime rejection of negative-weight edges.

---

## 🚀 Running the Notebooks and Tests

### Prerequisites
- Python 3.10+
- Only Python standard library required (no `numpy`, `pandas`, or external ML packages needed).
- Jupyter Notebook / VS Code / JupyterLab.

### Running Unit Tests
```bash
# Test Lab 1
python Lab1-Intelligent-Agents-and-GenAI/test_lab1.py

# Test Lab 2
python Lab2-Problem-Solving-and-Heuristic-Search/test_lab2.py
```

### Viewing Executed Notebooks
Open either:
- `Lab1-Intelligent-Agents-and-GenAI/DCIT313_Lecture1_Student_Notebook_Reviewed.ipynb`
- `Lab2-Problem-Solving-and-Heuristic-Search/DCIT313_L2_Student_Notebook.ipynb`

All cells have been executed and saved with full output traces, tables, and assertions intact.

---

## 📜 Academic Integrity & GenAI Disclosure
Generative AI was used for template scaffolding, notebook JSON generation, and LaTeX formatting. All code logic, mathematical proofs, cost trade-off derivations, graph search hand traces, and claim audit quotes were independently verified for academic rigor and adherence to University of Ghana course standards.
