# TEAM.md: the shared notebook

**Read this first, every time.** This file is how the people and AI assistants working on The Virtual Neuro Lab keep in step. None of the AI assistants remembers the others' conversations, so anything that matters goes here.

- **Owner and final say:** Romana. Nothing goes live and no decision is final until she approves it.
- **Team:** Romana (founder), Claude (Anthropic), ChatGPT (OpenAI).
- **Live site:** https://romananeuroscience-art.github.io/TheVirtualNeuroLab/
- **Last updated:** 2026-11-23 by Claude

---

## 1. What we are trying to do

**Now:** make the lab a proper **study tool** for learning how a real brain's wiring produces behaviour.

**Audience (decided 2026-11-23):** intro college neuroscience, and AP or high-school biology. The lab should cover what those syllabi teach, including the **human and rat brain**, not only the fly and the worm.

**Later:** a real business, such as paid licences for courses, schools or museums, and possibly a sale of the business one day. That only happens if the licensing question (section 4) is settled first.

## 2. How we work (rules)

1. **Never edit `main` directly.** Each task gets its own branch and comes in as a pull request.
2. **Only Romana merges.**
3. **One owner per task** (see section 5). Don't work on files that belong to someone else's open task.
4. **Every pull request gets reviewed by the other AI** before Romana merges. The review checks numbers against the data files, not just the wording.
5. **Update this file** when you start or finish a task, make a decision, or find a problem.
6. **Write for a non-scientist.** Plain words; explain every technical term the first time.

## 3. Things that must never be broken

- **Pre-registration files are never edited:** `experiments/*_preregistration*.json` and `discover/screen_preregistration.json`. They record what was decided *before* each experiment; changing them destroys the lab's credibility. New rules go in new files.
- **No API keys or secrets in the repo, ever.** `.env` stays git-ignored. "Ask Claude" only runs on Romana's own computer.
- **Simulation results are predictions, not facts about real flies.** Pages must say so where it matters.
- **Every number on a page must trace back to a data file in this repo.** Never type a number by hand that isn't in the data.
- **Rounding:** round from unrounded values, with halves rounding up. Never round a number that has already been rounded (this caused the Clavicle 83% vs 84% error).
- **Cite papers only for what they actually showed.** Example: Gordon & Scott 2009 described sugar-activated motor neurons; the name "MN9" came later. When unsure, check the paper or leave it out.
- **Don't compare raw synapse counts across datasets** (FlyWire, BANC, Male CNS). Each used a different automated synapse detector. Compare proportions.

## 4. Current state (2026-11-21)

**Works:**
- Neuron Silencing Screen (286 neurons, pre-run)
- Vivarium (24 taste mixes and antenna touch, pre-run)
- Calibration test and experiments round 1 (10 of 15 matched real flies)
- Lab notebook
- Parkinson's wiring map
- Fly Atlas
- Worm
- Guided tours on every page

**Checked on 2026-11-20 and 21:**
- All page numbers were checked against the data files and recounted from the raw FlyWire data. They hold.
- Citations were checked against the papers and the wording was corrected.
- One simulation ("Clavicle") was re-run independently and reproduced exactly (30.7 → 5.1 per second).

**Known limits** (say them honestly on the pages):
- The 30 repeats only measure simulation noise, not real uncertainty about the wiring or settings.
- The model misses single named neurons more often than group effects.
- No neuromodulators, learning, electrical synapses or body feedback.
- One female fly's brain.

**BLOCKER for any business:**
- FlyWire data is licensed **CC BY-NC 4.0 (non-commercial)**. A paid product or a sale likely needs FlyWire's permission and a lawyer's advice. Contact: flywire@princeton.edu.
- The Shiu et al. simulation code is MIT (commercial use allowed). The worm data is public domain.

## 5. Task list

| # | Task | Owner | Status |
|---|------|-------|--------|
| 1 | Write this file | Claude | Done |
| 2 | "Changes and corrections" page listing every fix, with dates (start with the 2026-11-20 and 21 claims check) | Claude | To do |
| 3 | Stress-test the 8 "needed" neurons: re-run under changed settings (synapse strength ±20%, 10% of transmitter labels flipped, weak links removed) and show a robustness score | Claude | To do |
| 4 | In-lab "Key ideas" page: connectome, model, 95% range, pre-registration, in plain words | ChatGPT | To do |
| 5 | "Download the numbers" button next to each result | ChatGPT | To do |
| 6 | Licence list for a lawyer: every data source, its licence, where it's used | Claude (draft) → Romana | To do |
| 7 | Email FlyWire about commercial use | Claude drafts, Romana sends | To do |
| 8 | Find 2–3 teachers of intro neuroscience or biology for a free pilot | Romana (AIs help find and draft) | To do |
| 9 | Rebuild-everything package: one command, pinned versions, missing input files, Zenodo archive | Claude | Later |
| 10 | Find a fly lab willing to test a prediction (CB0051, CB0192 #2, CB0501) | Romana (AIs draft) | After task 3 |
| 11 | **Neuron basics** module: one simulated neuron (resting potential, threshold, action potential, refractory period, excitatory and inhibitory synapses, summation). It's the core of AP Biology, it uses the same rules as the fly model, and it has no licensing issues. | Proposed, owner TBD | Proposed |
| 12 | **Human brain explorer**: 3D regions (lobes, brainstem, cerebellum, limbic system, basal ganglia), what each does, classic cases (H.M., Phineas Gage, Broca and Wernicke), region-to-region pathways. First find an atlas whose licence allows our use. | Proposed, owner TBD | Proposed |
| 13 | **Rat brain explorer**: Waxholm Space rat atlas (CC BY 4.0); hippocampus and memory (place cells, water maze), the reward circuit (links to the fly's dopamine and Parkinson's pages); region-to-region wiring (licence to check). | Proposed, owner TBD | Proposed |
| 14 | **Across species**: the same function in worm, fly, rat and human (e.g. reward, smell), and the "zoom levels" of what is mapped. Worm and fly are cell by cell, rat and human are by region; say clearly that these can't be compared like for like. | Proposed, owner TBD | Proposed |

## 6. Decisions made

- 2026-11-20: "Ask Claude" stays local-only. A public version would need a server middleman and a spending cap (deferred).
- 2026-11-21: For now the lab is a study tool, not a research tool (see the known limits in section 4).
- 2026-11-21: ChatGPT and Claude work through branches and pull requests, plus this file. Romana merges.
- 2026-11-23: Audience is intro college neuroscience plus AP and high-school biology; add human and rat brains (tasks 11-14, proposed order 11, 12, 13, 14).
- Facts for tasks 12-13: no neuron-by-neuron map exists for a whole rat or human brain. Rat and human content works at the level of regions, plus small detailed pieces (Blue Brain rat cortex model: CC BY-NC; H01 human cortex sample, about 1 mm³). Human Connectome Project raw data has restrictive terms (registration, no free re-sharing), so use published summary maps with clear licences.

## 7. Open questions for Romana

- Which customer do we aim at first? Suggested: intro neuroscience courses at universities or colleges.
- Should "Lab notebook" be added to the main menu?
- Should the Mac folder's git remote point to the new GitHub account?

## 8. Log

- 2026-11-21 (Claude): Created TEAM.md. Claims check done; fixes in commits of 2026-11-20 and 21.
- 2026-11-21 (Claude): PR #2 opened (corrections page). Stress test (task 3) run. Results: sugar predictions held in 7 of 7 perturbed versions. For drinking, 2 of 7 versions lost drinking entirely (untestable); of the other 5, Roundup #2 and Clavicle held in 5 of 5, CB0051, CB0501 and Rattle in 4 of 5, CB0192 #2 and Bract in 3 of 5. Not yet on any page.
- 2026-11-23 (Claude): Added syllabus audience and tasks 11-14 (proposed). ChatGPT's strategy PR #1 read; Claude's response drafted, awaiting Romana's OK to post.
