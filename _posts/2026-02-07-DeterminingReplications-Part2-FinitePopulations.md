---
layout: post
author: Veronica White
title: "How Many Samples Are Needed? Part 2: Finite Populations"
subtitle: Finding N when sampling without replacement using the finite population correction
tags: statistics skill
# need both visible 1 and published false to not publish post
published: false
visible: 1
---
This is **Part 2 of a 3-part series**:
- [Part 1: Infinite Populations]({% post_url 2026-08-05-DeterminingReplications-Part1-InfinitePopulations %}) — sampling with replacement and the CLT
- **Part 2: Finite Populations** *(this post)* — sampling without replacement and the finite population correction
- [Part 3: Power Analysis for RCTs]({% post_url 2026-02-08-DeterminingReplications-Part3-RCTPowerAnalysis %}) — sizing samples around statistical power instead of confidence-interval width

In [Part 1]({% post_url 2026-08-05-DeterminingReplications-Part1-InfinitePopulations %}), we assumed sampling **with replacement**, which is typical in simulation studies where the CLT applies directly. But many **survey studies, RCTs, and social science applications** instead sample **without replacement** from a finite population. In these cases, a **finite population correction (FPC)** may be appropriate.

## Sampling Without Replacement: Finite Population Settings

When you sample without replacement, each draw slightly reduces the uncertainty remaining in the population relative to sampling with replacement. As the sample size $n$ approaches the population size $N$, this effect becomes substantial, and ignoring it will lead you to overestimate the sample size you actually need. The FPC scales the sample size down to reflect this.

Helpful references:
- Effect size and sample size intuition: [[1]](#r1)
- Population proportion sample size calculator: [[2]](#r2)
- Finite population correction explanation: [[3]](#r3)

If the population size is unknown or very large, it is common to assume:
$$
N = 100{,}000
$$
Larger values beyond this have little effect on the resulting sample size.

The sample size formula with finite population correction is:

$$
n = \frac{\frac{Z^2 p(1-p)}{e^2}}{1 + \frac{Z^2 p(1-p)}{e^2 N}}
$$

where:
- $ Z $ is the Z-score (adjusted for multiple comparisons via Bonferroni, if applicable—see [Part 1]({% post_url 2026-08-05-DeterminingReplications-Part1-InfinitePopulations %})),
- $ p $ is the estimated population proportion,
- $ e $ is the margin of error,
- $ N $ is the population size.

### What Is the Estimated Proportion ($p$)?

This formula is built for **categorical outcomes**—the fraction of the population that falls into a category of interest (e.g., the proportion of survey respondents who answer "yes," or the proportion of patients who experience a side effect). $p$ is your best guess, going in, at that fraction.

$p$ plays the same role here that $\sigma$ played in [Part 1]({% post_url 2026-08-05-DeterminingReplications-Part1-InfinitePopulations %}): it's the variability estimate that drives the sample size. For a single binary (Bernoulli) observation, the variance is $p(1-p)$, so the standard error of a sample proportion is:
$$
SE_p = \sqrt{\frac{p(1-p)}{n}}
$$
which is the direct proportion-analog of $SE = \sigma/\sqrt{n}$ from Part 1, with $\sqrt{p(1-p)}$ standing in for $\sigma$. Multiplying by $Z_{\alpha/2}$ gives the margin of error $e = Z_{\alpha/2}\sqrt{p(1-p)/n}$, and solving for $n$ (ignoring the FPC for a moment) recovers the numerator of the formula above: $n = Z^2p(1-p)/e^2$.

> **Note:** If you don't have a prior estimate of $p$, use $p = 0.5$. This is the most conservative choice, since $p(1-p)$ is maximized at $p = 0.5$, yielding the largest (safest) required sample size.

#### Example: Plugging Into the Calculator

Say you're surveying patients at a clinic ($N = 100{,}000$, per the assumption above) and don't have a prior estimate of the proportion who will report a particular symptom, so you use the conservative default $p = 0.5$. You want a 95% confidence level ($Z_{\alpha/2} \approx 1.96$) with a margin of error of $e = 5\% = 0.05$.

Plugging $Z = 1.96$, $p = 0.5$, $e = 0.05$, $N = 100{,}000$ into the calculator at [[2]](#r2) (or the formula above by hand):
$$
n = \frac{\frac{1.96^2 \times 0.5(1-0.5)}{0.05^2}}{1 + \frac{1.96^2 \times 0.5(1-0.5)}{0.05^2 \times 100{,}000}} = \frac{384.16}{1.0038} \approx 383
$$
So you'd need approximately **383 respondents**. Notice the numerator alone (384) is the classic "infinite population" result from Part 1—the FPC only shaves off about 2 respondents here, since 383 is a tiny fraction of a 100,000-person population. This is the same point made below: the FPC only matters once your sample size becomes a non-trivial fraction of $N$.

As $N \to \infty$, the denominator approaches 1 and this formula reduces to the infinite-population case from Part 1—which is exactly what we'd expect, since the FPC only matters when your sample is a non-trivial fraction of the population.

## Accounting for Dropout and Attrition

In applied studies, the **calculated sample size is rarely the final number recruited**. You should always inflate the initial sample to account for expected:
- Dropout
- Nonresponse
- Missing data

This ensures that the *effective* sample size still meets your desired confidence or precision targets.

### Simple Adjustment Formula

Let:
- $ n_{\text{required}} $ = sample size required by your statistical formula
- $ r $ = expected dropout rate (as a proportion)

Then the adjusted sample size is:

$$
n_{\text{adjusted}} = \frac{n_{\text{required}}}{1 - r}
$$

#### Example

Suppose your confidence interval calculations (after applying a Bonferroni correction, as in [Part 1]({% post_url 2026-08-05-DeterminingReplications-Part1-InfinitePopulations %})) indicate that you need:

$$
n_{\text{required}} = 1{,}200
$$

Based on prior experience, you expect a **20% dropout rate**:

$$
r = 0.20
$$

Then the adjusted sample size is:

$$
n_{\text{adjusted}} = \frac{1{,}200}{1 - 0.20} = \frac{1{,}200}{0.80} = 1{,}500
$$

This means you should plan to recruit **1,500 samples** so that approximately **1,200 usable observations** remain after attrition.

Failing to account for dropout can lead to:
- Wider-than-expected confidence intervals
- Loss of statistical power
- Increased risk of false negatives, especially when using conservative corrections like Bonferroni

In simulation studies, attrition may arise from discarded runs, unstable warm-up periods, or convergence failures. In empirical studies, it may result from participant withdrawal or missing outcomes. In either case, planning for attrition *up front* is far easier than trying to recover power after the fact.

As a rough guide:
- **10–15%**: optimistic / well-controlled studies
- **20–30%**: typical for many applied settings
- **30%+**: plan carefully and justify assumptions

When in doubt, err on the side of a slightly larger initial sample—especially if running simulations where additional replications are relatively inexpensive.

## Summary

- Sampling **without replacement** from a finite population requires the finite population correction (FPC).
- As $N \to \infty$, the FPC formula reduces to the infinite-population case from Part 1.
- The calculated sample size should be **inflated to account for expected attrition**, so that the final analyzed sample still meets your target precision or power.

Up next, in [Part 3]({% post_url 2026-02-08-DeterminingReplications-Part3-RCTPowerAnalysis %}), we'll shift from confidence-interval width to **statistical power**—the framework most commonly used to size RCTs and other comparative studies.

### References
<a name="r1">[1]</a> "The Importance of Effect Size and Sample Size," Select Statistical Consultants. Accessed: Feb. 07, 2026. [Online]. Available: https://select-statistics.co.uk/blog/importance-effect-sample-size/ <br/>
<a name="r2">[2]</a> "Sample Size Calculator for a Population Proportion," Select Statistical Consultants. Accessed: Feb. 07, 2026. [Online]. Available: https://select-statistics.co.uk/calculators/sample-size-calculator-population-proportion/ <br/>
<a name="r3">[3]</a> "Finite Population Correction Factor," Statistics How To. Accessed: Feb. 07, 2026. [Online]. Available: https://www.statisticshowto.com/finite-population-correction-factor/<br/>
