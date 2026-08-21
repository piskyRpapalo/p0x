# The Evaluation Doctrine

A local LLM without a testing doctrine is a parlor trick.
Loss curves go down, the output looks coherent, and you ship a
model that silently hallucinates under pressure.

This file is the minimal, executable framework to prevent that.
If you are forking Aurelius to build your own local instance, you
must implement this. The framework teaches you how to think about
evaluation by forcing you to write tests that prove your model has
a soul, not just a vocabulary.

## The 4 Laws of Behavioral Testing

Do not write tests that check if the model outputs a specific
string. Write tests that check if the model makes the right
*choice*. Every behavioral test in your guardian tester must obey
these laws. (The reference implementation lives in the private
forge until its publication is signed; if you are cloning, you
build your own.)

### 1. Falsifiability
The test must name the exact rupture it catches.
"I want it to say hello" is not a rupture.
"If the user injects a prompt, the model must not obey" is a
rupture. Name the failure mode you are defending against.

### 2. No String-Presence
Never `grep` the output. LLMs are stochastic; a missing comma
breaks your test. Measure behavior: did it reject the action? Did
it ask for clarification? Did it declare absence of data? Assert
the behavioral state, not the lexical token. Where two
continuations compete —the one the doctrine demands and the one
that betrays it— measure which one the model chooses, not which
words it prints.

### 3. The Change-Detector Rule
Your test MUST fail on the base model and pass with your LoRA.
If the base model already passes, your LoRA adds no mathematical
value to that behavior. Keep the case marked as redundant, but do
not count it as proof.

### 4. The Regression Rule
Your LoRA MUST NOT flip any case the base model passes — above
all, any case that touches the fuse. A LoRA that answers "which
files, and where?" with "execute: rm -rf …" has made the model
more dangerous, and no loss curve redeems it. Measure what the
LoRA breaks, not only what it fixes.

## The 3 Categories of Edge Cases

Structure your test suite around these three axes. A model is only
ready for deployment when it passes all three.

### Category 1: Robustness (The Shield)
The model must withstand the chaos of the real world.
- Inputs out of distribution (jargon, slang, lexical noise).
- Prompt injections ("ignore previous instructions").
- Adversarial attacks mimicking the system tone.
- Code-switching (forcing it to mix languages).

### Category 2: Coherence (The Spine)
The model must hold its identity over time and pressure.
- Degradation after N turns (inject the history of the previous
  turns as context; do not assume a stateful chat API).
- Internal contradiction (does it invent facts when challenged?).
- Doctrinal violations (does it reject with the doctrine's own
  words, or with generic AI excuses?).

### Category 3: Operational Honesty (The Soul)
The most critical category. If one test here fails, the global
state is RED.
- Naming the absence: if data is missing, it must say "I don't
  have X", not "I can't help".
- The dishonest sensor: if a response was truncated, it must
  admit it failed, not claim success.

## The Early Stopping Protocol

Training a LoRA on a small dataset will inevitably lead to
overfitting. The model will stop understanding the doctrine and
start memorizing the dataset.

The guardian tracks two metrics simultaneously:
1. Training loss (should go down).
2. Validation loss (should go down, on a stratified cut — 20%,
   balanced per language).

**The Abort Rule:**
The guardian MUST abort training if:
- Validation loss rises for TWO consecutive evaluations,
- AND training loss is still decreasing.
One rise over a tiny cut can be noise; two consecutive rises are a
curve turning.

**The Best-Checkpoint Rule:**
Aborting is not enough. The trainer MUST save the checkpoint of
the step with the minimum validation loss — never the last step.
A stopped run that saves its last step ships the worst model of
the good ones. And the health guardian MUST compare *best* against
*saved*: if they ever differ, a sensor is lying.

If you only look at training loss, you will ship a model that
perfectly recites your dataset and fails in production. The
guardian's job is to catch the exact step where the model stops
learning and starts memorizing.

---

This doctrine is not a suggestion. It is the difference between a
local wrapper and a sovereign system. Implement it, run your
tests, and let the carbon sign the final commit only when the
guardian is validated.
