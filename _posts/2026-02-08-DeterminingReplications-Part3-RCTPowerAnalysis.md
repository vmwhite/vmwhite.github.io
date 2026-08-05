---
layout: post
author: Veronica White
title: "How Many Samples Are Needed? Part 3: Power Analysis for RCTs"
subtitle: Sizing samples around statistical power instead of confidence-interval width
tags: statistics skill
# need both visible 1 and published false to not publish post
published: false
visible: 1
---
This is **Part 3 of a 3-part series**:
- [Part 1: Infinite Populations]({% post_url 2026-08-05-DeterminingReplications-Part1-InfinitePopulations %}) — sampling with replacement and the CLT
- [Part 2: Finite Populations]({% post_url 2026-02-07-DeterminingReplications-Part2-FinitePopulations %}) — sampling without replacement and the finite population correction
- **Part 3: Power Analysis for RCTs** *(this post)* — sizing samples around statistical power instead of confidence-interval width

[Part 1]({% post_url 2026-08-05-DeterminingReplications-Part1-InfinitePopulations %}) and [Part 2]({% post_url 2026-02-07-DeterminingReplications-Part2-FinitePopulations %}) sized samples around a target **confidence interval width**—how precisely you can pin down a mean or proportion. But when the question is comparative—"does the treatment group outperform the control group?"—the more natural framework is **statistical power**: the probability of detecting a real effect, if one truly exists. This is the standard approach for sizing **randomized controlled trials (RCTs)** and other A/B-style comparisons.

## Type I and Type II Errors

Every hypothesis test balances two kinds of mistakes:

|                     | $H_0$ is True         | $H_0$ is False          |
|---------------------|------------------------|--------------------------|
| **Reject $H_0$**    | Type I error ($\alpha$) | Correct (Power, $1-\beta$) |
| **Fail to reject $H_0$** | Correct              | Type II error ($\beta$) |

- $\alpha$ is the false positive rate—the same significance level used in Parts 1 and 2 (and, if you're testing multiple hypotheses, the same one that gets Bonferroni-corrected).
- $\beta$ is the false negative rate: the probability of failing to detect a real effect.
- **Power** is $1 - \beta$: the probability of correctly detecting an effect that truly exists. A common target is **80% power** ($\beta = 0.20$), though 90% is used when missing a real effect is costly.

Where Parts 1 and 2 asked "how many samples do I need for a precise estimate?", power analysis asks **"how many samples do I need to reliably detect a difference of a given size?"**

## Effect Size

Power analysis requires you to specify, in advance, the smallest effect you care about detecting. The standardized effect size for comparing two group means is **Cohen's $d$**[[1]](#r1):

$$
d = \frac{\mu_1 - \mu_2}{\sigma}
$$

where $\mu_1, \mu_2$ are the two group means and $\sigma$ is the (pooled) standard deviation. As a rough convention, Cohen suggests $d = 0.2$ is a small effect, $d = 0.5$ is medium, and $d = 0.8$ is large—but domain knowledge or pilot data should always take precedence over these generic benchmarks.

## Sample Size for Comparing Two Means

For a two-sample test comparing independent group means with equal group sizes, the required sample size **per group** is:

$$
n = \frac{2(Z_{\alpha/2} + Z_{\beta})^2}{d^2}
$$

where:
- $ Z_{\alpha/2} $ is the Z-score for your (possibly Bonferroni-corrected) significance level, as in [Part 1]({% post_url 2026-08-05-DeterminingReplications-Part1-InfinitePopulations %}),
- $ Z_{\beta} $ is the Z-score corresponding to your target power (e.g., for 80% power, $Z_\beta \approx 0.84$; for 90% power, $Z_\beta \approx 1.28$),
- $ d $ is Cohen's effect size.

Note the shape of this formula: it looks just like the confidence-interval sample size equation from Part 1, except the single $Z_{\alpha/2}$ term is replaced with $(Z_{\alpha/2} + Z_\beta)$. Solving for power, rather than for interval width, simply adds a second Z-score term to the same underlying logic.

#### Example

Suppose you're running a two-arm RCT and want to detect a **medium effect** ($d = 0.5$) at $\alpha = 0.05$ (two-sided, so $Z_{\alpha/2} \approx 1.96$) with **80% power** ($Z_\beta \approx 0.84$):

$$
n = \frac{2(1.96 + 0.84)^2}{0.5^2} = \frac{2(2.8)^2}{0.25} = \frac{15.68}{0.25} \approx 63
$$

You would need approximately **63 participants per group** (126 total) to detect this effect with 80% power.

> **Note:** If you are testing multiple hypotheses and apply a Bonferroni correction as in [Part 1]({% post_url 2026-08-05-DeterminingReplications-Part1-InfinitePopulations %}), $Z_{\alpha/2}$ increases—which increases $n$ *and* makes it harder to hold power constant. Correcting for multiplicity without adjusting your sample size is one of the most common ways an RCT ends up underpowered.

## Combining With Parts 1 and 2

Power analysis doesn't replace the earlier posts in this series—it's a different lens on the same sample size problem, and the same considerations still apply:

- If you are testing multiple outcomes or subgroups, the Bonferroni-adjusted $\alpha$ from [Part 1]({% post_url 2026-08-05-DeterminingReplications-Part1-InfinitePopulations %}) feeds directly into $Z_{\alpha/2}$ above.
- If you are sampling without replacement from a finite population (e.g., all eligible patients at a clinic), apply the finite population correction from [Part 2]({% post_url 2026-02-07-DeterminingReplications-Part2-FinitePopulations %}) to the $n$ computed here.
- Always **inflate for expected dropout**, exactly as described in [Part 2]({% post_url 2026-02-07-DeterminingReplications-Part2-FinitePopulations %})—an underpowered trial due to attrition is functionally the same problem as an underpowered trial due to a miscalculated $n$.

For more complex designs (unequal group sizes, paired designs, ANOVA, regression-based effects), the same $\alpha$/$\beta$/effect-size logic applies, but the formulas change. Tools like G\*Power[[2]](#r2), or the `pwr` package in R, handle these cases without requiring you to derive each formula by hand.

## Summary

- Power analysis sizes a study around the probability of **detecting a real effect** ($1-\beta$), rather than around confidence-interval width.
- It requires specifying a target effect size (e.g., Cohen's $d$) in advance.
- The sample size formula mirrors the confidence-interval formula from Part 1, with an added $Z_\beta$ term for power.
- Bonferroni corrections, finite population corrections, and dropout inflation all still apply—power analysis composes with, rather than replaces, the tools from [Part 1]({% post_url 2026-08-05-DeterminingReplications-Part1-InfinitePopulations %}) and [Part 2]({% post_url 2026-02-07-DeterminingReplications-Part2-FinitePopulations %}).

Across this three-part series, the underlying message is the same: "how many samples do I need?" always depends on *how* you're sampling, *what* you're estimating or comparing, and *how many* tests you're running simultaneously. Get those three questions right, and the sample size formula is the easy part.

### References
<a name="r1">[1]</a> J. Cohen, *Statistical Power Analysis for the Behavioral Sciences*, 2nd ed. Hillsdale, NJ: Lawrence Erlbaum Associates, 1988. <br/>
<a name="r2">[2]</a> F. Faul, E. Erdfelder, A.-G. Lang, and A. Buchner, "G*Power: A flexible statistical power analysis program," *Behavior Research Methods*, vol. 39, pp. 175–191, 2007. [Online]. Available: https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower<br/>
