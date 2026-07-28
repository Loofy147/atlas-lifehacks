# The Universal Leverage Atlas

A catalog of cross-domain leverage principles, filtered for four properties: well-supported by evidence, counterintuitive, generalizable across domains, and high-return for the effort of applying them. Each entry states the originating field, the core finding with its source, the mechanism underneath it, and translations into other domains. Where a popular version of a finding overstates the evidence, that's flagged rather than smoothed over — a catalog built on this criteria should survive the same scrutiny it asks other people's intuitions to survive.

This document has been restructured using the **From Abstraction to Implementation** methodology. For each mechanism in this atlas, we map it to one of the ten deepest recurring control classes (the **Eight Deep Moves** and **Two Meta-Moves**) and systematically answer the **Five Questions** of system design along with the **Six Practical Output** criteria.

---

## The Ten Deep Recurring Control Classes

1. **Slack / Headroom:** Keep capacity below the point where small spikes become system collapse (absorbing amplitude).
2. **Feedback / Observability:** Shorten the time between action and consequence (improving visibility).
3. **Threshold / Criterion:** Change when the system says "yes" (separating sensitivity from threshold).
4. **Redundancy / Fault Containment:** Do not let one component carry the whole load (controlled insurance).
5. **Decorrelation / Desynchronization:** Break timing correlation between otherwise independent agents (the jitter principle).
6. **Incentive Alignment:** Make the desired behavior the rational behavior (designing payoff structure).
7. **Risk Spreading / Bet-Hedging:** Spread exposure across uncorrelated bets over time (protecting against multiplicative ruin).
8. **Information Weighting / Signal Quality:** Prefer evidence that actually changes the model (weighting by likelihood ratio).
9. **Stop Rules / Reallocation (Meta-Move):** Leave when marginal value falls below alternatives (corrected persistence).
10. **Exploration Before Commitment (Meta-Move):** Generate information before locking in (prototyping/pre-mortems).

---

## 1. Queueing Theory — utilization near capacity destroys latency, not throughput

**Move Classification:** Move 1: Slack / Headroom

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Queues are exploding, response times are incredibly high, and delay cascades into systemic unresponsiveness and periodic collapse.
2. **Why is it happening?** Utilization is too close to capacity, leaving no headroom to absorb variability in arrival and service times. This variability compounds nonlinearly.
3. **What is the control knob?** Headroom / spare capacity (Utilization $ho$).
4. **What is the implementation?** Sizing server clusters/thread pools for tail load instead of average, leaving open blocks in a personal calendar, keeping financial reserves.
5. **What is the robustness test?** Subject the system to an unexpected 30% spike in request/arrival frequency or variance to verify if queue sizes and latencies remain bounded, or if the system cascades into total failure.

### Detailed Mechanism & Application
- **What the Mechanism Is:** In an M/M/1-type queue, expected wait time scales with $ho/(1-ho)$, where $ho$ is utilization. This is nonlinear — wait time barely rises from 50% to 70% utilization, then explodes approaching 100%. Running "full" doesn't mean slightly worse; it means qualitatively worse.
- **Why It Works:** Variability in arrival and service times compounds at high utilization because there's no slack to absorb it. At low utilization, a slow request just uses idle capacity. At high utilization, a slow request creates a queue that the next slow request stacks onto.
- **How It Fails:** It fails when the environment is completely deterministic and synchronized (i.e., variance is zero). In a perfectly scheduled, deterministic pipeline, utilization can reach 100% with zero wait time.
- **How to Implement It (Translations):**
  - *Personal:* An unscheduled day isn't wasted capacity, it's the buffer that keeps one bad meeting from cascading into a bad week.
  - *Business/ops:* Hospitals, call centers, and CPU schedulers all see cliff-like latency past ~80–85% utilization; staffing exactly to expected demand guarantees periodic collapse.
  - *Software:* Connection pools and thread pools sized to "average load" fail during any variance spike; size for the tail, not the mean.
- **How Far the Analogy Can Safely Extend:** This principle safely extends to any resource-constrained system subject to stochastic arrival or processing times, including human attention, computer hardware, physical logistics, and project planning.
- **Where the Analogy Breaks:** The analogy breaks when resources are not scarce, when request arrivals are perfectly scheduled and synchronized with processing capacity, or when requests can be rejected or dropped without penalty (e.g., lossy packet transmission).

---

## 2. Bayesian Statistics — weight evidence by likelihood ratio, not persuasiveness

**Move Classification:** Move 8: Information Weighting / Signal Quality

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Overreacting to low-value signal or persuasive stories, while being repeatedly surprised by unexpected outcomes because non-vivid but highly diagnostic evidence was ignored.
2. **Why is it happening?** Evaluating evidence based on its descriptiveness or persuasiveness rather than its mathematical diagnostic value, which is determined by the likelihood ratio.
3. **What is the control knob?** Likelihood ratio criteria (Surprise factor under competing hypotheses).
4. **What is the implementation?** Weighting evidence by the likelihood ratio: $P(	ext{evidence} \mid 	ext{true}) / P(	ext{evidence} \mid 	ext{false})$.
5. **What is the robustness test?** Introduce highly vivid, emotionally persuasive but common noise (high probability under both true and false hypotheses) to verify if the decision-making model successfully discounts it and maintains high accuracy.

### Detailed Mechanism & Application
- **What the Mechanism Is:** The correct measure of how much a piece of evidence should move your belief is $P(	ext{evidence} \mid 	ext{true}) / P(	ext{evidence} \mid 	ext{false})$ — not how compelling it sounds.
- **Why It Works:** Evidence that's *common* under both hypotheses (true and false) carries little information no matter how vivid it is. Evidence that's rare under the false hypothesis and common under the true one is diagnostic, even if it's a single unglamorous data point.
- **How It Fails:** It fails when the prior probabilities are exactly 0 or 1 (the model cannot learn), or when the conditional probabilities cannot be estimated with any reasonable precision.
- **How to Implement It (Translations):**
  - *Hiring:* "Hard-working" on a resume is true of almost every resume (high probability under both hypotheses) and moves nothing. A 300-commit GitHub history is rare among unqualified candidates and common among qualified ones — high likelihood ratio, real signal.
  - *Personal:* The operational question is "if this were false, how surprising would this evidence be?" If not very, it's not evidence.
  - *Media consumption:* Most news, meetings, and notifications are low-likelihood-ratio noise; the discipline is knowing which single observation would actually change your model.
- **How Far the Analogy Can Safely Extend:** This applies to all forms of inference and learning, from scientific research and legal trials to personal belief updates and machine learning model calibrations.
- **Where the Analogy Breaks:** The analogy breaks in purely deductive systems (such as mathematics), where evidence is binary and absolute rather than probabilistic, and in environments with complete, unquantifiable uncertainty (Knightian uncertainty) where conditional probabilities are undefined.

---

## 3. Control Theory — fix the sensor before the controller

**Move Classification:** Move 2: Feedback / Observability

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Erratic system behavior, continuous oscillation, or overshooting targets while effort is wasted optimizing decision logic or willpower in a state of blindness.
2. **Why is it happening?** Stale, absent, or low-resolution feedback data. Optimization of decision logic (controller) is useless if the system is feeding on noise.
3. **What is the control knob?** Measurement latency and feedback loop quality.
4. **What is the implementation?** Adding dashboards, continuous integration pipelines, telemetry, and establishing short feedback loops.
5. **What is the robustness test?** Introduce artificial delays or high noise into feedback data to see if the controller goes unstable, validating that sensor quality is indeed the gating factor.

### Detailed Mechanism & Application
- **What the Mechanism Is:** In engineered control systems, improving the feedback loop (better, faster measurement) typically yields more reliable performance gains than improving the controller's decision logic while flying blind.
- **Why It Works:** A controller — human or mechanical — cannot correct what it cannot see. Effort spent optimizing decisions made on stale or absent data is effort spent optimizing noise.
- **How It Fails:** It fails when the cost of measurement is higher than the value of the control, or when the measurement itself alters or destroys the system state (e.g., observer effect).
- **How to Implement It (Translations):**
  - *Personal habits:* Daily weigh-ins outperform willpower for weight management for the same reason unit tests outperform care for code correctness — the loop closes in a day instead of a season.
  - *Software:* Continuous integration and telemetry dashboards exist because "try to write better code" doesn't scale; "get an error signal in ten seconds" does.
  - *Organizations:* Teams without dashboards aren't undisciplined, they're uninstrumented — and no amount of discipline substitutes for instrumentation.
- **How Far the Analogy Can Safely Extend:** This applies to any adaptive system that adjusts its actions based on outcome data, including personal habits, engineering pipelines, financial portfolios, and organizational steering.
- **Where the Analogy Breaks:** The analogy breaks when system dynamics are chaotic and fundamentally unpredictable, meaning even perfect, instantaneous sensor data provides zero forward-looking control value, or when target outcomes are entirely static and require no steering.

---

## 4. Evolutionary Biology — bet-hedging (variance reduction over mean maximization)

**Move Classification:** Move 7: Risk Spreading / Bet-Hedging

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Catastrophic collapse or total ruin of a lineage, career, or organization during a high-variance shock, despite excellent average performance.
2. **Why is it happening?** Multiplicative compounding of outcomes over time. When compounding is multiplicative, a single zero or near-zero multiplier destroys the entire trajectory; arithmetic averages are irrelevant.
3. **What is the control knob?** Portfolio variance / uncommitted reserves.
4. **What is the implementation?** Keeping uncommitted fractions, delaying convergence, and maintaining backup plans or alternative strategies.
5. **What is the robustness test?** Subject the system to an environmental "extinction pulse" (e.g., zeroing out the dominant strategy's returns) to verify that the hedged fraction successfully preserves the system's continuity.

### Detailed Mechanism & Application
- **What the Mechanism Is:** Long-term lineage success depends on *geometric* mean fitness across generations, not arithmetic mean — and geometric means are catastrophically sensitive to variance. Organisms evolve to sacrifice average-case payoff for reduced variance: desert plants keep a fraction of seeds dormant every year (Cohen, 1966; Slatkin, 1974); bacteria maintain dormant "persister" subpopulations that survive antibiotic pulses precisely because they didn't commit to the dominant growth strategy. This is the same mathematics as the Kelly criterion in betting/finance.
- **Why It Works:** When outcomes compound multiplicatively over time, a single catastrophic loss cannot be averaged away by good years — it must be avoided structurally, by never betting everything on one outcome in the first place.
- **How It Fails:** It fails when the environment is completely static and risk-free, where the cost of holding dormant reserves represents pure wasted opportunity with no defensive benefit.
- **How to Implement It (Translations):**
  - *Personal/career:* Delaying convergence on one plan, keeping a second option alive past the point it feels efficient, is a rational bet-hedge, not indecision.
  - *Organizations:* Companies that kill competing internal ideas the moment a favorite emerges are optimizing arithmetic mean and exposed to catastrophic variance.
  - *This paper (self-referential):* Experiment 7's finding that Brooks' Law was robust because its representation was spread across nine dimensions instead of one is the same mechanism in a different costume — breadth as a hedge against any single dimension being reweighted away.
- **How Far the Analogy Can Safely Extend:** This applies to any compounding process over time where risk of ruin is non-zero, such as capital investment, long-term biological survival, strategic planning, and structural architecture.
- **Where the Analogy Breaks:** The analogy breaks when compounding is additive rather than multiplicative, where total loss in one period does not wipe out past gains, or when the system has a guaranteed bailout or reset button.

---

## 5. Network Science — weak ties outperform strong ties for novel information

**Move Classification:** Move 8: Information Weighting / Signal Quality

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Information stagnation, development of echo chambers, and missing out on novel opportunities, job openings, or cross-functional collaborations.
2. **Why is it happening?** Strong ties form dense, highly overlapping clusters where everyone knows the same information. Bridge connections to other clusters are carried by weak ties.
3. **What is the control knob?** Tie mix (ratio of bridge/weak ties to local/strong ties).
4. **What is the implementation?** Deliberately maintaining loose acquaintances, participating in cross-functional rotations, and setting up informal cross-team channels.
5. **What is the robustness test?** Cut off communications inside the core team and measure whether novel external info still reaches the team through their individual acquaintance bridges.

### Detailed Mechanism & Application
- **What the Mechanism Is:** Granovetter's classic 1973 sociology finding: close friends tend to know what you already know (their networks overlap heavily with yours); acquaintances bridge to entirely different clusters. Jobs, collaborations, and opportunities disproportionately arrive through weak ties.
- **Why It Works:** Information value comes from novelty, and novelty comes from structural distance. A strong tie is, almost by definition, someone whose information environment already overlaps with yours.
- **How It Fails:** It fails when the task requires high trust, intense resource sharing, or fast coordination, which weak ties lack the bandwidth or commitment to support.
- **How to Implement It (Translations):**
  - *Personal networking:* Maintaining a wide set of loose acquaintances is not a weaker substitute for close friendship, it's a different and complementary resource for a different purpose.
  - *Organizations:* Teams that only communicate within tight sub-groups develop internal echo chambers; deliberately weak cross-team ties (rotations, informal channels) are a structural fix, not a nice-to-have.
- **How Far the Analogy Can Safely Extend:** This applies to any information-routing network, including corporate communications, citation networks in academia, and computer routing protocols.
- **Where the Analogy Breaks:** The analogy breaks when the goal is execution rather than discovery. When a team needs to align on high-stakes, highly coordinated, or sensitive actions, strong ties are required to prevent coordination failure.

---

## 6. Reliability Engineering — near misses are undervalued data, and the value is destroyed by blame

**Move Classification:** Move 8: Information Weighting / Signal Quality

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Low reported rates of incident/failure data, followed by sudden, catastrophic, and completely unexpected major system accidents.
2. **Why is it happening?** A culture of blame increases the social and career cost of reporting errors, causing team members to raise their decision criterion for reporting a near miss until only unavoidable disasters are visible.
3. **What is the control knob?** Reporting criterion / cost of flagging anomalies.
4. **What is the implementation?** Creating blameless postmortems, implementing anonymous/protected reporting systems (like NASA's ASRS), and celebrating near misses as free lessons.
5. **What is the robustness test?** Introduce a non-fatal, human-caused anomaly to see if the team proactively reports and logs the incident, or if it is covered up.

### Detailed Mechanism & Application
- **What the Mechanism Is:** High-reliability industries (commercial aviation foremost) systematically study incidents that *almost* became accidents, not only accidents themselves, via voluntary, protected reporting systems (e.g., NASA's Aviation Safety Reporting System).
- **Why It Works:** A near miss contains almost all the causal information of a full failure, at zero cost. But this only works if reporting a near miss doesn't get the reporter punished — which connects directly to the signal detection point below: a blame culture doesn't reduce the true rate of near misses, it just raises the criterion for reporting them, and the graph looks identical to "things got safer" when nothing did.
- **How It Fails:** It fails when the "near miss" was caused by active, intentional sabotage or severe negligence that requires direct security or legal intervention rather than systemic study.
- **How to Implement It (Translations):**
  - *Personal:* A mistake caught five minutes before it mattered is a free lesson that a successful outcome would never have taught you.
  - *Organizations:* Blameless postmortems exist because the alternative — blame — doesn't reduce failures, it reduces *visibility* into failures.
- **How Far the Analogy Can Safely Extend:** This applies to all complex systems operating under high-risk environments, such as medicine, nuclear power, software infrastructure, and daily personal mistakes.
- **Where the Analogy Breaks:** The analogy breaks in strictly adversarial environments (e.g., warfare, competitive negotiations), where sharing your vulnerabilities or near-failure data leaks valuable tactical intelligence to opponents who will exploit it.

---

## 7. Signal Detection Theory — separate sensitivity from criterion

**Move Classification:** Move 3: Threshold / Criterion

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Apparent performance problems (e.g., "catching fewer bugs") are misdiagnosed as skill deficits, wasting training resources when the actual issue is a shift in the decision threshold.
2. **Why is it happening?** Failure to separate sensitivity ($d'$) — the genuine physical capability to distinguish signal from noise — from the criterion — the threshold level of evidence required before reporting "yes".
3. **What is the control knob?** Decision criterion (by changing the relative payoffs/costs of false positives vs. false negatives).
4. **What is the implementation?** Changing defaults, tuning diagnostic triggers, adjusting moderation policy, and redesigning false-alarm penalties.
5. **What is the robustness test?** Shift the cost of a false alarm (e.g., fine for a false positive) and verify that the sensitivity $d'$ remains constant, proving that threshold is independent of actual discriminative ability.

### Detailed Mechanism & Application
- **What the Mechanism Is:** Developed from 1950s–60s radar engineering (Tanner, Swets, Green), SDT formally splits detection performance into $d'$ (sensitivity — genuine ability to distinguish signal from noise) and *criterion* (the evidence threshold required before reporting "yes"). $d'$ is, by construction, unaffected by where the criterion is set.
- **Why It Works:** Most apparent "performance problems" are actually criterion shifts, not sensitivity losses — and the two require opposite fixes. More training and better data fix sensitivity. Changing the cost of a false alarm fixes criterion. Applying the first fix to the second problem (or vice versa) burns effort for nothing.
- **How It Fails:** It fails when the signal and noise distributions are completely identical (sensitivity $d' = 0$), meaning no threshold shift can ever yield diagnostic utility.
- **How to Implement It (Translations):**
  - *Organizations:* "We're catching fewer bugs/defects/risks" is frequently a criterion shift (people got scared to flag things) misdiagnosed as a sensitivity problem (people need more training) — see Entry 6.
  - *Diagnosis, forecasting, moderation:* Radiology, content moderation, and fraud detection all face the same tradeoff — the "right" criterion depends on the relative cost of false positives vs. false negatives, and is a policy choice, not a skill level.
  - *AI/ML:* Current interpretability research applies SDT directly to model calibration, separating a model's genuine discriminative ability from where its decision threshold happens to sit.
- **How Far the Analogy Can Safely Extend:** This applies to any classification or decision process under noise, including radar operations, medical diagnostics, credit scoring, legal trials, and content moderation.
- **Where the Analogy Breaks:** The analogy breaks when there is zero noise in the system, or when the signal is a deductive certainty, making the probabilistic frameworks of SDT irrelevant.

---

## 8. Distributed Systems — desynchronize retries with jitter, not just delay

**Move Classification:** Move 5: Decorrelation / Desynchronization

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Thundering herd failures: a recovering resource (server, database, manager) is hit by repeated, massive, synchronized spikes of requests, knocking it back down immediately.
2. **Why is it happening?** Cocoordinated timing correlation among otherwise independent clients. Standard delays (even exponential ones) keep the clients retrying in lockstep.
3. **What is the control knob?** Jitter (randomization of wait intervals).
4. **What is the implementation?** Introducing randomized jitter to retry logic, staggering deadline schedules, and staggering release times.
5. **What is the robustness test?** Force a server crash under high traffic and verify that retry requests arrive at a smooth, flat rate rather than a synchronized wave.

### Detailed Mechanism & Application
- **What the Mechanism Is:** Naive exponential backoff (wait 1s, 2s, 4s, 8s after each failure) leaves every failed client retrying in near-lockstep, so a recovering server gets hit by a synchronized wave — the "thundering herd." Adding randomized jitter to each wait interval spreads retries toward a roughly constant rate instead (documented in AWS's own architecture writeups on the pattern).
- **Why It Works:** The failure mode isn't the delay length, it's the correlation between clients. Fixing the average wait time without fixing the correlation makes the coordinated-spike problem worse, not better, because everyone still waits the "smart" amount of time — together.
- **How It Fails:** It fails when client request volume is so high that even perfectly flat, uncorrelated traffic exceeds the server's maximum possible capacity.
- **How to Implement It (Translations):**
  - *Personal/organizational:* Synchronized deadlines (everyone's report due Friday at 5pm) create the same thundering-herd effect on a manager's attention; staggering due times is jitter applied to a human system.
- **How Far the Analogy Can Safely Extend:** This applies to any distributed system where independent agents access a shared, limited-capacity resource, including computer networking, highway traffic, office hours, and project submissions.
- **Where the Analogy Breaks:** The analogy breaks when the shared resource has infinite capacity relative to request volume, or when clients can coordinate in real-time to form a perfect, zero-variance queue without needing random delays.

---

## 9. Behavioral Economics — defaults dominate stated preference

**Move Classification:** Move 6: Incentive Alignment

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Severe discrepancies between what people claim they want to do (stated preference) and what they actually do, resulting in low participation rates in valuable programs.
2. **Why is it happening?** Cognitive friction, decision fatigue, and the natural inertia of human behavior. People will take the path of least resistance.
3. **What is the control knob** Default choice architecture.
4. **What is the implementation?** Designing systems as opt-out rather than opt-in for highly valuable and ethically justified behaviors.
5. **What is the robustness test?** Increase the number of steps or the complexity of opting out to verify that default selection rates remain dominant under high friction.

### Detailed Mechanism & Application
- **What the Mechanism Is:** Johnson & Goldstein (2003, *Science*) compared organ-donation consent across European countries differing only in opt-in vs. opt-out defaults: opt-out countries reached ~99% effective consent; opt-in countries as low as single digits to twenties, with no evidence people's actual underlying willingness differed.
- **Why It Works:** Changing a default doesn't persuade anyone of anything; it redirects the inertia that was already present toward a different outcome.
- **How It Fails:** It fails when there is extreme, active resistance to the default choice, or when the cost of the default action is prohibitively high.
- **How to Implement It (Translations):**
  - *Personal systems:* Automatic transfers to savings beat "try to save more" for the same reason — the default absorbs the discipline you don't have to spend.
  - *Product design:* Opt-out beats opt-in for any behavior you can ethically justify defaulting people into.
- **How Far the Analogy Can Safely Extend:** This applies to any system designed for human choice, from software configurations and company retirement contributions to national public policy.
- **Where the Analogy Breaks:** The analogy breaks when choices are legally binding and require active, conscious, high-stake declarations, or when the population has highly polarized and deeply held convictions that override any default configuration.

---

## 10. Systems Engineering — N-1 contingency: no single component may be load-bearing for the whole

**Move Classification:** Move 4: Redundancy / Fault Containment

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** A single point of failure (one broken wire, one sick employee, one lost client) triggers a cascading, systemic collapse of the entire infrastructure.
2. **Why is it happening?** Fragile design that trusts individual components to remain 100% reliable, with zero redundant capacity or failover paths.
3. **What is the control knob?** Redundant pathways (N-1 or N-1-1 standards) / Load sharing.
4. **What is the implementation?** Designing grids to survive any single line loss; cross-training team members; diversifying personal income streams; having backup servers.
5. **What is the robustness test?** Deliberately disable the single highest-capacity component under peak system load to verify if the system maintains continuous, safe operations.

### Detailed Mechanism & Application
- **What the Mechanism Is:** Power grid reliability standards (NERC, ENTSO-E) require that the grid survive the loss of *any single* component — one line, one transformer, one generator — without cascading failure. More conservative grids plan for N-1-1 (a second failure before full recovery from the first).
- **Why It Works:** It formalizes "don't trust any single component to behave reliably under stress" as an enforceable engineering standard rather than an aspiration. Cascading blackouts almost never trace to "one thing failed" — they trace to N-1 not actually being enforced somewhere upstream.
- **How It Fails:** It fails when components have highly correlated failures (e.g., a systemic cyberattack or extreme environmental disaster that disables all backups simultaneously).
- **How to Implement It (Translations):**
  - *Organizations:* A team where one person's absence stops shipping has an unenforced N-1 violation, whether or not anyone's named it that.
  - *Personal finance/planning:* Single-income households, single clients, single suppliers are all N-1 violations by another name.
- **How Far the Analogy Can Safely Extend:** This applies to physical engineering, software system architectures, corporate operational design, and personal resource security.
- **Where the Analogy Breaks:** The analogy breaks when maintaining redundant capacity is mathematically or economically impossible (e.g., a startup operating under extreme cash constraints), or when the failover process itself introduces more failure modes than the redundancy prevents.

---

## 11. Human Reliability / Self-Regulation — implementation intentions

**Move Classification:** Move 2: Feedback / Observability (Pre-committing control loop)

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Constant failure to execute planned goals ("I'll exercise more"), leading to frustration, self-blame, and reliance on willpower that repeatedly fails under stress.
2. **Why is it happening?** Goal intentions require active, real-time cognitive processing and motivation at the moment of action. Noise, distraction, and willpower fatigue easily disrupt this loop.
3. **What is the control knob?** Cue-to-action coupling strength / decision overhead.
4. **What is the implementation?** Pre-committing decisions to specific environmental cues using "if-then" plans ("If it's 7am on a weekday, I put on running shoes before checking my phone").
5. **What is the robustness test?** Subject the individual to high cognitive fatigue or severe distraction at the trigger moment to verify if the planned action still initiates automatically.

### Detailed Mechanism & Application
- **What the Mechanism Is:** Gollwitzer & Sheeran's 2006 meta-analysis (94 studies, 8,000+ participants) found a medium-to-large effect (d = 0.65) of "if-then" planning on actual goal attainment, not just intention. Later meta-analyses (642 tests; a 2025 meta-analysis on pro-environmental behavior, d = 0.78 across 10,000+ participants) replicate and extend it.
- **Why It Works:** A goal intention ("I'll exercise more") relies on willpower recurring reliably at the moment of action. An implementation intention ("if it's 7am on a weekday, I put on running shoes before checking my phone") pre-commits the decision to a cue, removing it from competition with in-the-moment motivation.
- **How It Fails:** It fails when the specified environmental cue is too vague, rarely occurs, or is easily bypassed, or when the planned "then" response requires excessive steps.
- **How to Implement It (Translations):**
  - This is the human-cognition instance of "shorten and pre-commit the control loop," the same family as Entry 3.
- **How Far the Analogy Can Safely Extend:** This applies to any goal-oriented human behaviors, including habit formation, medical compliance, academic productivity, and environmental conservation.
- **Where the Analogy Breaks:** The analogy breaks in highly volatile or unpredictable scenarios where trigger cues cannot be defined in advance, requiring adaptive, real-time reasoning rather than pre-programmed responses.

---

## 12. Educational Psychology — productive failure

**Move Classification:** Move 10: Exploration Before Commitment

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Fragile expertise: students/users perform well on structured, routine tests but completely fail to adapt their knowledge to novel problems or out-of-distribution scenarios.
2. **Why is it happening?** Receiving clean, well-structured instruction first bypasses the exploratory phase, preventing the creation of representational scaffolding of the problem's underlying constraints.
3. **What is the control knob?** Length of the unguided exploration phase prior to receiving instruction.
4. **What is the implementation?** Designing exercises where learners must attempt to solve a problem *before* they are taught the correct method, allowing them to fail constructively.
5. **What is the robustness test?** Present the learner with a novel, transfer-level problem that looks different from the training set to measure their structural adaptive capacity.

### Detailed Mechanism & Application
- **What the Mechanism Is:** Manu Kapur's research program shows students who attempt to solve a problem *before* receiving instruction (and mostly fail) subsequently learn the correct method better than students given well-structured instruction first.
- **Why It Works:** Unsuccessful attempts build representational scaffolding — a felt sense of the problem's structure — that makes the eventual correct method land on prepared ground instead of a blank surface.
- **How It Fails:** It fails when the initial challenge is so discouraging or difficult that it causes severe anxiety and complete learner disengagement, or when correct instruction is never provided afterward, cementing incorrect methods.
- **How to Implement It (Translations):**
  - *Prototyping:* The research-backed version of "ship early and imperfectly" — starting before you're ready isn't just motivationally useful, it measurably improves what you learn once the "correct" answer arrives.
- **How Far the Analogy Can Safely Extend:** This applies to educational curricula, software engineering prototyping, professional training, and UI onboarding.
- **Where the Analogy Breaks:** The analogy breaks when the cost of failure is fatal (e.g., flight school, nuclear operations), or when the correct solution is highly arbitrary and counterintuitive, offering no structural insights through exploration.

---

## 13. Decision Science — the pre-mortem (prospective hindsight, correctly stated)

**Move Classification:** Move 10: Exploration Before Commitment

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Projects repeatedly fail late due to obvious, severe risks that many team members were quietly worried about but never felt permitted to speak up about during reviews.
2. **Why is it happening?** Traditional "what could go wrong" prompts trigger social filters and optimistic hedging to avoid looking unsupportive. Assuming certainty of failure flips the social pressure.
3. **What is the control knob?** Temporal framing / assumption of failure certainty.
4. **What is the implementation?** Running a pre-mortem: "Assume the project has failed completely. Write down the exact history of how and why it happened."
5. **What is the robustness test?** Run a standard pros/cons review and a pre-mortem in parallel on the same project with different groups to see which uncovers more critical, actionable risks.

### Detailed Mechanism & Application
- **What the Mechanism Is:** Mitchell, Russo & Pennington (1989) found that framing a future outcome as *certain* rather than merely possible increased the quantity and concreteness of reasons people generated for it (~30% more reasons, twice as many concrete/actionable ones) — not, as commonly mis-cited, a 30% gain in accuracy. A more direct test of the actual premortem technique (Veinott et al., 2010; 178 participants) found it reduced overconfidence roughly twice as much as standard pros/cons methods.
- **Why It Works:** "What could go wrong" invites hedged, socially cautious answers. "This already failed, why" grants permission to say the specific, concrete thing people were already quietly worried about.
- **How It Fails:** It fails when the organization has such a severe fear culture that even hypothetical failure histories are punished, or when the generated risks are completely ignored by decision-makers.
- **How to Implement It (Translations):**
  - *Strategic Planning:* Prior to launching a new business product or career pivot, force the team to write a detailed, highly specific history of its ultimate failure.
- **How Far the Analogy Can Safely Extend:** This applies to any planned group or individual actions under uncertainty, from launching software features and company strategy to personal choices.
- **Where the Analogy Breaks:** The analogy breaks in environments of absolute predictability where outcomes are deterministic, or in highly chaotic contexts where failures are purely driven by unpredictable "black swan" external events.

---

## 14. Medicine / High-Stakes Procedure — checklists catch omission, not incompetence

**Move Classification:** Move 4: Redundancy / Fault Containment

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** High-expertise teams make routine, catastrophic errors (e.g., leaving a sponge inside a patient, skipping a standard software security check) under routine stress or fatigue.
2. **Why is it happening?** Human working memory is highly fragile and vulnerable to distraction. Expertise does not prevent memory lapse; checklists provide a redundant cognitive backup.
3. **What is the control knob?** Checklist adoption and psychological buy-in.
4. **What is the implementation?** Creating highly structured checklists with mandatory verification pauses (like the WHO Surgical Safety Checklist).
5. **What is the robustness test?** Introduce distraction or noise during the procedure to verify if crucial safety checks are still performed consistently.

### Detailed Mechanism & Application
- **What the Mechanism Is:** The WHO Surgical Safety Checklist (Haynes et al., 2009, *NEJM*), tested across eight hospitals worldwide, was associated with complication rates falling from 11.0% to 7.0% and in-hospital deaths from 1.5% to 0.8%. **Caveat:** A later Ontario-wide rollout found no significant reduction — the effect depends heavily on genuine team buy-in, not merely posting a checklist.
- **Why It Works:** Expertise doesn't protect against memory lapses under routine or stress; checklists don't add expertise, they catch the specific failure mode expertise doesn't fix.
- **How It Fails:** It fails when treated as a bureaucratic, check-the-box exercise without true team alignment, leading to mindless compliance rather than safety.
- **How to Implement It (Translations):**
  - *Aviation & Engineering:* Pre-flight and deployment checklists prevent senior staff from omitting fundamental steps during fatigue.
- **How Far the Analogy Can Safely Extend:** This applies to any procedural task where execution accuracy must approach 100% and steps can be written down in advance.
- **Where the Analogy Breaks:** The analogy breaks in fast-moving, highly fluid tactical situations (e.g., active military combat, acute emergency resuscitation) where reading a checklist would cause fatal delays.

---

## 15. Sociology of Influence — people underestimate compliance and how much they're liked

**Move Classification:** Move 8: Information Weighting / Signal Quality

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Extreme social hesitation, over-caution in networking, and under-asking for support, jobs, or funding due to fear of rejection.
2. **Why is it happening?** Systematic, directional cognitive bias in social prediction: people overestimate the social cost of asking and underestimate compliance and conversation partner ratings.
3. **What is the control knob?** Ask-frequency / initiating rate.
4. **What is the implementation?** Deliberately initiating more requests, collaborations, and conversations than feels safe.
5. **What is the robustness test?** Track predicted outcomes vs. actual outcomes in a social log to measure and calibrate the gap between expectation and reality.

### Detailed Mechanism & Application
- **What the Mechanism Is:** Flynn and Bohns's research program finds people underestimate by roughly half how likely strangers are to comply with direct requests. The "liking gap" (Boothby, Cooney, Sandstrom & Clark, 2018) finds people consistently underestimate how much conversation partners liked them.
- **Why It Works:** Both are systematic, directional miscalibrations in social prediction — not general pessimism, but a specific, measurable, exploitable error in modeling other people's responses to you.
- **How It Fails:** It fails when requests are exceptionally costly, inappropriate, or made in highly hostile or adversarial social environments.
- **How to Implement It (Translations):**
  - *Personal:* Deliberately asking for things you expect refusal on, and initiating more conversations/collaborations than feel "safe," are both direct corrections for a mapped bias.
- **How Far the Analogy Can Safely Extend:** This applies to professional networking, startup fundraising, sales, negotiation, and making friends.
- **Where the Analogy Breaks:** The analogy breaks in strictly transactional, automated, or highly formal environments where relationships are irrelevant and interactions are governed by cold market pricing.

---

## 16. Ecology — indirect/bottleneck leverage, and a live caution about overclaiming it

**Move Classification:** Move 2: Feedback / Observability (observing indirect cascade effects)

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Direct interventions on visible symptoms produce negligible or counterproductive effects, while upstream constraints are completely missed.
2. **Why is it happening?** Complex networks have dense, indirect causal links (like trophic cascades), meaning the highest-leverage point is often several steps removed from the symptom.
3. **What is the control knob?** Upstream bottleneck constraint identification.
4. **What is the implementation?** Analyzing system dynamics to find the bottleneck upstream; verifying primary literature before acting on popular claims.
5. **What is the robustness test?** Apply a temporary, localized shock to the hypothesized upstream bottleneck and measure the downstream cascade to see if it behaves as predicted.

### Detailed Mechanism & Application
- **What the Mechanism Is:** Trophic cascades — where a top predator's effect propagates indirectly through multiple levels of an ecosystem — are real and documented in many systems. The popular version of the flagship example (Yellowstone wolves reshaping rivers via elk behavior) is currently disputed in the primary literature: Ripple et al. (2025) claimed one of the strongest cascades ever recorded (~1,500% increase in willow crown volume); a rebuttal (Hobbs, Cooper, MacNulty and colleagues, ScienceDirect, Oct. 2025, ongoing into 2026) found the analysis used a tautological volume model, unmatched plots, and omitted human hunting as a confound. As of mid-2026 the dispute is unresolved; most ecologists agree *some* cascade occurred, not what the viral-video version claims about magnitude or mechanism.
- **Why It Works:** In a system with many interacting variables, the highest-leverage intervention point is often not the symptom you can see but an upstream constraint several steps removed from it.
- **How It Fails:** It fails when we act on speculative or unverified causal cascade models without verifying the primary evidence, leading to unintended systemic side-effects.
- **How to Implement It (Translations):**
  - *Debugging Systems:* "What's the bottleneck upstream" remains a good question to ask of any complex system; it just shouldn't be answered with a citation that's currently being argued about in the primary literature.
- **How Far the Analogy Can Safely Extend:** This applies to any network of interacting variables, such as organizational workflows, software systems, public health, and environmental policy.
- **Where the Analogy Breaks:** The analogy breaks in simple, linear systems where direct effects are dominant and there are no network feedback loops.

---

## 17. Mechanism Design — the revelation principle

**Move Classification:** Move 6: Incentive Alignment

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Strategic lying, information asymmetry, and participants gaming the system to extract advantages, leading to massive inefficiency.
2. **Why is it happening?** The rules of the system make strategic dishonesty more rational than truthfulness. Participants operate under conflicting payoffs.
3. **What is the control knob?** System payoff rules and outcome rules.
4. **What is the implementation?** Designing direct, truthful mechanisms where honesty is the dominant strategy (e.g., second-price Vickrey auctions).
5. **What is the robustness test?** Introduce highly strategic, self-interested agents to see if honesty remains their mathematically optimal strategy under the designed rules.

### Detailed Mechanism & Application
- **What the Mechanism Is:** (Myerson, 1979, 1982) For a wide class of mechanism-design problems, any outcome achievable by *any* mechanism — however indirect or strategic — can also be achieved by a direct, truthful mechanism in which participants simply report their private information honestly. This lets a designer restrict the entire search for good mechanisms to truthful ones, without loss of generality.
- **Why It Works:** It mathematically aligns individual self-interest with global truthfulness, eliminating the payoff for strategic misrepresentation.
- **How It Fails:** It fails exactly at its stated boundaries: it does not solve *moral hazard* (hidden actions post-facto); it requires the designer to *commit* to the outcome rule in advance; it assumes communication is free and unrestricted; and it does not prevent collusion between agents.
- **How to Implement It (Translations):**
  - *Org design:* Instead of trying to catch dishonesty, redesign the payoff so honesty is each person's dominant strategy (the logic behind second-price auctions: bidding your true value is always at least as good as bidding anything else).
  - *Personal:* If you keep needing to verify someone's claims, the fix might be the incentive structure they're operating under, not their character.
- **How Far the Analogy Can Safely Extend:** This applies to any system involving resource allocation, information aggregation, or contract drafting with multiple self-interested participants.
- **Where the Analogy Breaks:** The analogy breaks when participants can easily form collusive agreements to game the system together, or when the primary issue is performance monitoring (moral hazard) rather than truthful reporting.

---

## 18. Threshold Cryptography — Shamir secret sharing, and its static blind spot

**Move Classification:** Move 4: Redundancy / Fault Containment

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** A distributed security system is quietly compromised over time, even though no single location was ever breached simultaneously.
2. **Why is it happening?** The security scheme assumes a static snapshot of authority, leaving it vulnerable to a patient "mobile adversary" who compromises shares sequentially over time.
3. **What is the control knob?** Share refresh frequency.
4. **What is the implementation?** Implementing *proactive* secret sharing, periodically refreshing all shares so old compromised copies go stale.
5. **What is the robustness test?** Simulate a slow-moving adversary who compromises individual shares one by one over several months to verify if the periodic refresh successfully keeps the secret safe.

### Detailed Mechanism & Application
- **What the Mechanism Is:** (Shamir, 1979) A secret can be split into *n* shares such that any *k* reconstruct it exactly, while any *k-1* reveal provably zero information about it — not "hard to guess," mathematically zero.
- **Why It Works:** It uses polynomial interpolation to split authority such that partial information is completely useless, requiring a defined threshold for reconstruction.
- **How It Fails:** It fails under a "mobile adversary" who compromises different shares one at a time over an extended period. The guarantee is a static snapshot, not a lifetime guarantee.
- **How to Implement It (Translations):**
  - *Org/key management:* Splitting authority so no single person can act alone only holds if trust doesn't erode across everyone at the same slow rate with nobody re-checking — rotating who holds authority is the organizational version of refreshing shares.
  - *Personal:* A "second opinion" only protects you if it's genuinely independent, not the same source consulted twice under a different name.
- **How Far the Analogy Can Safely Extend:** This applies to human delegation of authority, distributed secure storage, consensus-based workflows, and digital key management.
- **Where the Analogy Breaks:** The analogy breaks when the adversary can compromise the threshold number of shares ($k$) simultaneously, or when the individuals holding the shares collude.

---

## 19. Information Theory — Shannon capacity, and the latency you pay to approach it

**Move Classification:** Move 4: Redundancy / Fault Containment

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** High rate of misunderstandings in remote communication, or severe project delays due to writing extremely long, exhaustive technical specifications.
2. **Why is it happening?** Error-free transmission over a noisy channel requires structured redundancy, which mathematically demands longer blocklengths, causing a direct latency penalty.
3. **What is the control knob?** Message blocklength / structured redundancy.
4. **What is the implementation?** Explicitly trading speed for accuracy: writing longer, highly redundant technical specifications when error cannot be tolerated; accepting latency to ensure correct alignment.
5. **What is the robustness test?** Inject high noise/distraction into the communication loop and verify if the message is still decoded with zero errors, and measure the delay.

### Detailed Mechanism & Application
- **What the Mechanism Is:** (Shannon, 1948) Every noisy channel has a maximum rate (capacity) below which structured redundancy — error-correcting coding, not just transmitting slower — can drive error probability toward zero.
- **Why It Works:** Structured redundancy groups information into larger blocks (blocklength) to protect the message against localized noise bursts.
- **How It Fails:** It fails under finite-blocklength constraints. Polyanskiy, Poor & Verdú (2010) formalized the finite-blocklength gap: achievable rate falls short of capacity by an amount shrinking only as $\sim 1/\sqrt{	ext{blocklength}}$. Arbitrarily low error and arbitrarily low latency cannot both be had at once.
- **How to Implement It (Translations):**
  - *Communication:* Over-explaining does reduce misunderstanding, but only if you accept it taking longer — a single low-latency message cannot simultaneously be maximally redundant.
  - *Documentation:* A spec written for zero ambiguity is necessarily longer than one written for speed; the tradeoff is quantifiable, not a style preference.
- **How Far the Analogy Can Safely Extend:** This applies to any channel transmitting information under noise, including radio frequencies, written documentation, software APIs, and team instructions.
- **Where the Analogy Breaks:** The analogy breaks in completely noiseless channels, where capacity can be reached instantly with zero latency, or when errors do not matter and can be easily bypassed.

---

## 20. Aviation Safety — Crew Resource Management and the authority gradient

**Move Classification:** Move 3: Threshold / Criterion

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Junior team members clearly see critical dangers or errors made by senior leaders but stay silent, leading to preventable, catastrophic accidents.
2. **Why is it happening?** A steep authority gradient makes challenging a leader socially costly, raising the decision criterion for junior staff to speak up.
3. **What is the control knob?** Cockpit authority gradient flatness.
4. **What is the implementation?** Training teams in Crew Resource Management (CRM), utilizing structured callouts, and flatting the feedback loop in reviews.
5. **What is the robustness test?** Deliberately introduce an obvious, safe error into a senior leader's work during a simulation to see if junior members immediately challenge it.

### Detailed Mechanism & Application
- **What the Mechanism Is:** A string of 1970s crashes (Eastern 401, United 173, Tenerife) traced to a steep authority gradient where junior crew did not forcefully challenge a captain who had missed danger. CRM, adopted in 1981, restructures cockpit communication to flatten that gradient.
- **Why It Works:** It lowers the criterion (social cost) for junior staff to speak up, making their observations visible to the controller (the captain) in real-time.
- **How It Fails:** It is difficult to isolate CRM's statistical impact from concurrent technological improvements (like weather radar or autopilot), and it fails if leadership is actively hostile and toxic.
- **How to Implement It (Translations):**
  - *Organizations:* If junior staff routinely see problems senior staff miss, the deficit usually isn't in junior staff's *sensitivity* — it's whether the structure makes speaking up costly, i.e. their *criterion*.
  - *Meetings:* Explicitly inviting disagreement from the most junior person present is a deliberate authority-gradient flattener.
- **How Far the Analogy Can Safely Extend:** This applies to any high-stakes, collaborative decision-making environment, such as operating rooms, nuclear plants, corporate boards, and software reviews.
- **Where the Analogy Breaks:** The analogy breaks in fast-moving tactical scenarios where immediate, top-down command and absolute obedience are required to survive a split-second hazard.

---

## 21. Market Microstructure — the Kyle model: informed trades must be camouflaged to be profitable

**Move Classification:** Move 8: Information Weighting / Signal Quality

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Executing a large strategic action or asking a highly specific question immediately tips off the market or negotiating counterparty, moving the price or terms against you.
2. **Why is it happening?** The pattern, timing, and size of actions leak strategic information independent of their content, which counterparties constantly monitor.
3. **What is the control knob?** Strategic order size / camouflage ratio with noise traders.
4. **What is the implementation?** Breaking up large requests into small, staggered pieces; blending strategic actions with normal noise traffic; limiting immediate urgency.
5. **What is the robustness test?** Run a large strategic move under high visibility vs. highly camouflaged conditions to measure and compare the adverse pricing/negotiation impact.

### Detailed Mechanism & Application
- **What the Mechanism Is:** (Kyle, 1985) A trader with private information trades against a market maker who sees only total order flow. The informed trader's rational strategy is to deliberately *limit* trade size and blend with uninformed noise traders — trading too aggressively reveals the information and moves the price against them before they can profit.
- **Why It Works:** It prevents the market maker from distinguishing strategic information from random noise, allowing the insider to capture value slowly.
- **How It Fails:** Kyle is a stylized, single-period model. Applying its precise predictions unmodified to modern, highly fragmented high-frequency markets is a misuse.
- **How to Implement It (Translations):**
  - *Negotiation:* Revealing full interest or urgency too fast is the human version of trading too large — it moves the other side's position against you before you can act on your advantage.
  - *Organizations:* Unusually specific, large-scope questions asked all at once often signal someone already knows more than they're stating — the shape of the ask carries information on its own.
- **How Far the Analogy Can Safely Extend:** This applies to negotiation, data querying, competitive business strategy, and information privacy.
- **Where the Analogy Breaks:** The analogy breaks when the counterparty has zero pricing power, or when the information is already public and carries no strategic advantage.

---

## 22. Behavioral Ecology — the marginal value theorem, and why almost nobody follows it exactly

**Move Classification:** Move 9: Stop Rules / Reallocation

### The Five Questions (From Abstraction to Implementation)
1. **What is the observable symptom?** Remaining in declining projects, jobs, or relationships long after their value has dropped below alternatives, or quitting too early due to minor local dips.
2. **Why is it happening?** Human intuition naturally compares the current patch's performance to its own past history rather than comparing its *local* marginal return to the *global* environmental average.
3. **What is the control knob?** Exit criterion based on environmental return baseline.
4. **What is the implementation?** Establishing stop-loss rules; leaving a project or job the moment its local rate of return drops below your honest global alternative average.
5. **What is the robustness test?** Track the actual local marginal return over time against an objective environmental average to verify if exit timing matches the MVT optimum.

### Detailed Mechanism & Application
- **What the Mechanism Is:** (Charnov, 1976) In a patchy environment, the reward-maximizing rule is: leave your current patch when its *local* rate of return drops to the *average* rate available across the whole environment — not when the patch is empty, not on a fixed timer.
- **Why It Works:** It mathematically maximizes long-term rate of return by taking into account transit/searching costs between patches.
- **How It Fails:** It is only valid when the forager has perfect knowledge of environmental statistics. Real foragers (insects, humans) deviate due to uncertainty, risk sensitivity, and temporal discounting.
- **How to Implement It (Translations):**
  - *Careers, relationships, projects:* "Leave when it's worse than your honest average elsewhere" is the correctly-stated version of "know when to quit" — the intuitive version compares the current patch to its own past, which is precisely the bias the animal literature documents.
  - *Ties this Atlas together:* MVT (Entry 22) tells you when to leave a patch; bet-hedging (Entry 4) tells you not to have committed everything to one patch to begin with.
- **How Far the Analogy Can Safely Extend:** This applies to strategic project reallocation, career transition planning, financial asset management, and biological foraging.
- **Where the Analogy Breaks:** The analogy breaks when the search or transit costs between patches are infinite, or when the entire environment consists of only a single patch.

---

## Open leverage-mining targets

All six of the prioritized targets above are now entered. Remaining candidates for future rounds: zero-knowledge proofs (revealing that you know something without revealing the thing itself — a template for credentialing and trust-minimization), non-equilibrium thermodynamics and entropy production (why maintaining order anywhere requires exporting disorder somewhere else), Jane Jacobs's urban-systems observations (mixed-use density and "eyes on the street" as emergent safety mechanisms), and auction theory beyond Kyle/Myerson specifically (winner's curse, common-value vs. private-value bidding errors).

---

*Every entry above traces to a real citation, checked rather than assumed — two entries (the ceramics-class "quantity beats quality" story, and the popularized 30%-accuracy version of the premortem finding) were checked and rejected/corrected during the research for this Atlas, and one (Yellowstone) was checked and kept with a live caveat attached. That filtering is itself part of what "well-supported by evidence" has to mean for a catalog like this to be worth trusting.*
