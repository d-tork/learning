# DevOps
From the IQT Conference

Conference notes / developer techniques / big data practices

DevOps is accelerated software build lifecycles. **DataOps** does the same via orchestration of a
data pipeline. 

## Tamr - a framework for working with dirty data at scale
Mark Marinelli 

A little detour took me to a synopsis of one of Tamr's presentations, which pointed to 
[Snorkel](https://dawn.cs.stanford.edu/2017/05/08/snorkel): a "weak supervision" model for 
labeling large datasets for training. Some key words or concepts:

> **Data programming** (to include a link to a blog post and NIPS paper): users focus on writing
> a set of labeling functions, which are just small functions that programmatically label data.
> The labels they produce are noisy and could conflict with each other. However, we then **model 
> this noise** by learning a generative model of the labeling process, effectively synthesizing the
labels created by the labeling functions. We can then use this new label set to train a 
_noise-aware_ end discriminative model (such as a neural network) with higher accuracy.

## Waterfall vs. Agile
| Waterfall | Agile |
| --------- | ----- |
| | Bottom-up: users drive specs |
| | Learn from use: emergent feature set |
| | Distributed: loosely-coupled, scalable |
| QA: manual testing | Continuous integration: automated testing |
| Traditional SDLC (dev/test/prod) | Modern DevOps: continuous delivery |

### The wrong process:
1. modeling exercise
2. write ETL rules
3. testing
4. delivery
5. go back and fix based on feedback

### The right process:
1. deliver value, something to use, at each step
2. feedback at every step
* automation can help!

Metadata catalog vs. warehouse: a catalog tells you where to find what you want

Systematic treatment of feedback: Jira, not emails or sticky notes! (the owners/developers decide
_if_ it's a problem and how to solve it). 

## Getting started - Quick Win
1. Define a high-value, data-rich project that will demand a complex solution
2. Decouple monolithic processes; wrap components in APIs, expose as services

Avoid: "single platform" trap - don't overestimate what a single piece of software can do; focus on 
a thoughtfully designed ecosystem of loosely coupled best of breed tools

### Cataloging by source (vs. publishing)
* manually: type of data, sample, who knows about it
* automated: 
    - inspection
    - someone just checking/verifying it
    - breath over depth: i.d. where you can focus your energy

