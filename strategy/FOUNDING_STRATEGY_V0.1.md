# The Virtual Neuro Lab — Founding Product & Business Strategy (v0.1)

**Status:** Proposal for Claude's critique and Romana's approval. Not a final decision.  
**Planning window:** November 2026–May 2027 (six months).  
**Founder / final authority:** Romana.  
**Authors / reviewers:** ChatGPT proposes; Claude independently critiques and revises; Romana decides.

## Shared starting point

Today the lab is a **study tool** with precomputed neuroscience demonstrations, guided tours, and a scientifically documented fruit-fly simulation. It is **not yet a validated general-purpose research platform**. Our destination, however, serves **both students and researchers**. Do not confuse today's claims with tomorrow's ambitions.

**Six-month objective:** deliver an education-first product with a genuinely usable, transparently limited research workflow; obtain pilot feedback from both user groups; establish whether a commercially licensable, financially sustainable venture is feasible.

## Product vision: two modes, one scientific foundation

### Study Mode
- Guided concepts, anatomy, pathways, and experiment walkthroughs.
- A learner can formulate a hypothesis, choose a perturbation, run or select a reproducible simulation, inspect results, and explain limitations.
- Clear distinction between published biological observations, computational predictions, and illustrative examples.
- Instructor-friendly exercises, assessment, and exportable learning artifacts.

### Research Mode
- Explicitly labeled **exploratory computational research**, not a validated substitute for in-vivo experiments.
- Select datasets, neuron sets, perturbations, model parameters and seeds; inspect provenance and uncertainties.
- Reproducible run manifest, downloadable raw results, comparison of runs, citations and limitations.
- Gradual expansion of models only after independent validation and clear scope statements.

### Shared engine and platform
- A versioned scientific engine with validated inputs, pinned dependencies, repeatable outputs, and tests.
- Separation of user interface, job execution, datasets, experiment metadata, and exported artifacts.
- Hosted simulations require architecture and cost/security design; GitHub Pages currently cannot run the Python engine server-side.
- AI tutor/research assistant should cite actual lab data and sources, never invent runs or results. Public deployment needs privacy, safety and API cost controls.

## Market and commercial hypotheses (not facts)

**Initial institutional buyer hypothesis:** undergraduate neuroscience/biology course instructors or departments, who may use both teaching and introductory research capabilities. **Second pilot segment:** computational neuroscience researchers exploring connectome perturbations.

Test willingness to pay, procurement constraints, accessibility, curriculum fit, and researcher reproducibility requirements before choosing pricing. Potential business models to evaluate: departmental annual license, instructor/course license, hosted usage-based research compute, and service/support contracts. No revenue forecast without evidence.

## Non-negotiable licensing and scientific gates

- TEAM.md identifies FlyWire data as CC BY-NC 4.0. **Do not launch paid access or assume derivative commercial rights** until the actual licensing chain is reviewed, permission or alternative licensing is obtained where needed, and qualified legal advice is sought.
- Inventory all datasets, code, imagery, weights, model outputs, dependencies, and attribution requirements.
- Preserve preregistration files, source traceability, numerical rounding rules, and published-data versus prediction distinctions.
- Publish model failure cases and robustness limits, including sensitivity to parameters and dataset coverage.
- Research Mode is a workflow label, not a claim of clinical, biological, or predictive validity.

## Six-month milestones and evidence gates

| Month | Product milestone | Business/science evidence required |
|---|---|---|
| 1 | Joint architecture and product specification; prioritized backlog; initial UI prototype | License inventory; 6–10 discovery conversations across educators and researchers; baseline reproducibility audit |
| 2 | Study Mode improved; Research Mode minimal experiment configuration prototype | Technical feasibility of running experiments; initial usability sessions; license permission outreach |
| 3 | End-to-end experiment run or explicitly precomputed fallback, result comparisons, exportable manifests/data | Independent rerun checks; parameter sensitivity tests; honest validation report |
| 4 | Two audience-specific pilot experiences and onboarding | Small educator/student pilot and at least one researcher workflow evaluation; documented feedback |
| 5 | Iterate on bottlenecks; institutional demo; deployment/security/cost plan | Willingness-to-pay interviews; licensing decision path; realistic unit-cost estimates |
| 6 | Pilot-ready release candidate, documentation, demonstrations, founder decision package | Evidence-based go/no-go on commercialization, target market, validation, and next investment |

**Scope guard:** If licensing or model validity blocks paid/research claims, preserve an educational or internal pilot and do not represent it as commercial or validated research deployment.

## Collaboration protocol — not task assignment by default

1. Each substantive proposal is posted as a branch/PR or versioned discussion document.
2. Claude and ChatGPT each respond with: **agree / challenge / alternative / evidence needed**. No rubber-stamping.
3. Maintain a decision register with competing options, risks, founder decision, and review date.
4. Only after Romana approves the strategy do we assign engineering and business tasks.
5. Claude and ChatGPT cannot message each other autonomously; Romana can ask each to read and respond to the same GitHub PR. Neither assistant merges to main.
6. No silent edits to TEAM.md, preregistrations, or live product.

## Specific questions for Claude — please challenge this proposal

1. Is a two-mode UI on one shared engine achievable in six months given the actual repository? What smaller viable architecture would you propose?
2. Which existing demos can become genuinely configurable, reproducible experiments first? Which data files or compute requirements are missing?
3. Where do you disagree with prioritizing institutional educators as the initial buyer while building researcher workflows concurrently?
4. What are the top three technical/scientific failure risks and objective acceptance tests?
5. How should we handle the FlyWire non-commercial license while validating demand without making impermissible commercial use?
6. What should we cut or defer to make the six-month target credible?
7. Propose a revised plan and explicitly mark disagreements for Romana rather than simply accepting this draft.

## Questions reserved for Romana

- Approve or revise the six-month objective and the education-first commercialization hypothesis.
- Decide the first pilot audience(s) after reviewing both AI perspectives.
- Approve any external contact, expenditure, deployment, pricing, licensing commitment, or merge.

## Review record

- 2026-11-21 — ChatGPT: initial proposal drafted for independent Claude critique. No implementation or business decision authorized.
