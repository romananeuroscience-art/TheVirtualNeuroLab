# Visual learning curriculum — proposed foundation

**Status:** draft architecture for Claude + ChatGPT review. Not a claim that the modules are implemented.

Audience: introductory college neuroscience and AP/high-school biology. Anchor the actual standards and course outlines in a reviewed coverage matrix; do not claim complete syllabus coverage without checking each objective.

## Lesson contract
Every published lesson must provide:
1. An explicit learning objective and prerequisite.
2. A scientifically grounded visual with labels and accessible text alternative.
3. A learner-controlled interaction, not just a passive animation.
4. A prediction or experiment and an explanation of the result.
5. A short formative assessment with feedback.
6. References, attribution and license status.
7. An explicit distinction between biological observations, simplified models, and predictions.

## Recommended sequence
1. Neuron basics vertical slice: membrane potential, threshold, spikes, refractory period, excitatory/inhibitory synapses and summation.
2. Human brain regional explorer and cases.
3. Rat brain regional explorer with licensed atlas.
4. Across-species comparison using existing fly/worm experiences.

**Modeling caution:** A leaky integrate-and-fire spike is an event, not a biophysically resolved action-potential waveform. Use separate explanatory visuals for ion-channel phases, clearly labeled as conceptual.

## Collaboration protocol
- Claude and ChatGPT exchange critiques in PR comments, with evidence and alternatives.
- Approved work is implemented on task branches; no agent commits to main.
- Human founder alone approves merges, releases and scope changes.
- CI checks objective metadata; human review remains necessary for science, accessibility and licensing.
- No API keys in repository. Claude Code automation requires a separately configured runner, GitHub permissions and secrets; it is **not** enabled by this PR.
- Never modify preregistration records automatically.

See `learning/curriculum.json` for the initial scope and `learning/modules/` for lesson contracts.
