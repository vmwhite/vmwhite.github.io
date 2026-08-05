---
layout: post
author: Veronica White
title: "How Many Samples Are Needed? Part 1: Infinite Populations"
subtitle: Finding N for confidence intervals using the Central Limit Theorem and the Bonferroni correction
tags: statistics skill
# need both visible 1 and published false to not publish post
published: false
visible: 1
---
When conducting simulation studies—or designing empirical analyses more broadly—you will often face the question:

> **"How many samples do I need to achieve a desired level of confidence in my results?"**

This question arises in calibration, performance comparison, uncertainty quantification, and hypothesis testing. The answer depends on *how* you are sampling, *what* you are estimating, and *how many* statistical tests you are running simultaneously.

This is **Part 1 of a 4-part series**:
- **Part 1: Infinite Populations** *(this post)* — sampling with replacement and the CLT
- [Part 2: Finite Populations]({% post_url 2026-02-07-DeterminingReplications-Part2-FinitePopulations %}) — sampling without replacement and the finite population correction
- [Part 3: Power Analysis for RCTs]({% post_url 2026-02-08-DeterminingReplications-Part3-RCTPowerAnalysis %}) — sizing samples around statistical power instead of confidence-interval width
- [Part 4: Prediction Intervals]({% post_url 2026-08-08-DeterminingReplications-Part4-PredictionIntervals %}) — sizing samples around statistical power instead of confidence-interval width

### Sampling With Replacement: Infinite Population Settings

In many simulation settings, samples are drawn **with replacement**. Under fairly mild conditions, the **Central Limit Theorem (CLT)** applies, allowing us to construct confidence intervals for the mean using a normal approximation. If the sample size is sufficiently large, the sampling distribution of the sample mean is approximately normal, regardless of the underlying distribution[[1]](#r1). Therefore we can use what we know about the Normal distribution to estimate our desired sample size. 

#### Margin of Error, Standard Error, and Solving for N

Before layering on the Bonferroni correction, it's worth being precise about where the $Z_{\alpha/2}\sigma/\sqrt{n}$ term below actually comes from, since it's the piece you ultimately solve for $n$.

The **standard error (SE)** of the sample mean measures how much the sample mean is expected to bounce around the true population mean, purely due to sampling variability:
$$
SE = \frac{\sigma}{\sqrt{n}}
$$
Unlike $\sigma$, which is a fixed property of the population, $SE$ shrinks as $n$ grows—more samples average out noise.

The **margin of error (e)** is the half-width of the confidence interval, i.e., how far from the true mean your estimate could plausibly land at your chosen confidence level:
$$
e = Z_{\alpha/2} \cdot SE = Z_{\alpha/2}\frac{\sigma}{\sqrt{n}}
$$

So margin of error and standard error are related but not the same thing: $SE$ is a property of your sampling design, while margin of error scales $SE$ by however many standard errors ($Z_{\alpha/2}$) you need to reach your target confidence level.

Rearranging this equation for $n$ gives the sample size formula:
$$
n = \left(\frac{Z_{\alpha/2}\,\sigma}{e}\right)^2
$$

This is the equation you're actually solving every time you ask "how many samples do I need?" Three inputs go in:
- $ \sigma $: an estimate of the population standard deviation,
- $ e $: the margin of error you're willing to accept,
- $ Z_{\alpha/2} $: determined by your desired confidence level (and the Bonferroni correction, if applicable—see below).

##### Choosing a Reasonable Margin of Error and $\sigma$

$n$ is highly sensitive to both $e$ and $\sigma$ (note it scales with $\sigma^2$ and $1/e^2$), so it's worth being deliberate about both:

- **Margin of error ($e$)** should be set relative to the scale of what you're measuring and how the result will be used—e.g., $\pm 5$ percentage points may be acceptable for an exploratory analysis, but far too wide for a calibration check where small biases matter. Smaller $e$ always means larger $n$.
- **$\sigma$** is rarely known exactly ahead of time. In order of preference:
  1. Use $\sigma$ from a pilot run or prior comparable data.
  2. Use a conservative (larger) published estimate for a similar population or process.
  3. As a rough rule of thumb, if you can bound the likely range of your data, $\sigma \approx \text{range} / 4$ (from the empirical rule that ~95% of data falls within 2 standard deviations of the mean).
- Because $n$ scales with $\sigma^2$, moderately **overestimating** $\sigma$ is the safer failure mode—you may run somewhat more replications than strictly necessary, but you won't end up underpowered. Underestimating $\sigma$ risks a confidence interval wider than intended.

##### Example

Suppose a pilot run of your simulation suggests $\sigma \approx 10$, and you want a 95% CI ($Z_{\alpha/2} \approx 1.96$) no wider than $\pm 2$ (so $e = 2$):
$$
n = \left(\frac{1.96 \times 10}{2}\right)^2 = (9.8)^2 \approx 97
$$
So roughly **97 replications** are needed to achieve that precision—before any correction for multiple hypotheses, which we turn to next.

#### Multiple Hypotheses and the Bonferroni Correction

If you are testing **multiple hypotheses simultaneously**, the probability of making at least one Type I error (false positive) increases. To control the **family-wise error rate**, a common (and conservative) adjustment is the **Bonferroni correction**. This adjusted $\alpha$ is then used to compute the corresponding **Z-score**. A Z-score calculator can be found at [[3]](#r3).


The corrected significance level is:
$$
\alpha = \frac{p}{m}
$$
where:
- $p$ is the desired overall significance level (e.g., 0.05 for 95% confidence),
- $m$ is the number of hypotheses being tested.

##### Example

Suppose you are testing **12 hypotheses** and want an overall confidence level of **95%**:
$$\alpha = \frac{0.05}{12} = 0.004166$$
Then for an $\alpha = 0.004166$, the corresponding Z-score is approximately, $Z \approx 2.64$
> **Note:** As $\alpha$ decreases, the Z-score increases—meaning wider confidence intervals unless the sample size increases.

Once the adjusted Z-score is determined, the confidence interval for the mean is:
$$
\bar{\mu} \pm Z_{\alpha/2}\frac{\sigma}{\sqrt{n}}
$$

where:
- $ \bar{\mu} $ is the sample mean,
- $ Z_{\alpha/2} $ is the Z-score corresponding to the adjusted significance level,
- $ \sigma $ is the standard deviation,
- $ n $ is the number of samples.

The term $Z_{\alpha/2}\sigma/\sqrt{n}$ is exactly the margin of error $e$ from above—Bonferroni doesn't change the formula, it only changes which $Z_{\alpha/2}$ you plug into it. This equation makes the tradeoff explicit:
- Smaller $ \alpha $ → larger $Z$ → wider interval (larger $e$) for the same $n$
- Larger $ n $ → narrower interval (smaller $e$) for the same $Z$

If you want to maintain the *same* margin of error while correcting for multiple tests, **you must increase the number of samples, $n$**, using the corrected $Z_{\alpha/2}$ in the sample-size formula above:
$$
n = \left(\frac{Z_{\alpha/2,\,\text{corrected}}\,\sigma}{e}\right)^2
$$
Continuing the earlier example: correcting for 12 hypotheses raised $Z_{\alpha/2}$ from 1.96 to about 2.64. Holding $\sigma = 10$ and $e = 2$ fixed, the required sample size grows from 97 to:
$$
n = \left(\frac{2.64 \times 10}{2}\right)^2 = (13.2)^2 \approx 175
$$
So testing 12 hypotheses at a fixed precision requires roughly **175 replications** instead of 97—an increase of nearly 80%, purely from correcting for multiplicity.

##### A Caution on Bonferroni

While simple and widely used, the Bonferroni correction can be **overly conservative**, especially when:
- The number of hypotheses is large, or
- Hypotheses are positively correlated.

In these cases, the correction increases the risk of **Type II errors (false negatives)**—failing to detect real effects. In simulation studies, this often means needing substantially larger sample sizes to preserve power.

## Summary

- Simulation studies typically rely on **sampling with replacement** and CLT-based confidence intervals.
- Multiple hypothesis testing requires correcting $ \alpha $, often via Bonferroni.
- Bonferroni increases required sample sizes to maintain precision and power.

Up next, in [Part 2]({% post_url 2026-02-07-DeterminingReplications-Part2-FinitePopulations %}), we'll look at what changes when you're sampling **without replacement** from a finite population—as is common in surveys and RCTs.

### Tools
link to my tool.  see [[2]](#r2) for a useful tool to estimate study sample size of binary data 


### References
<a name="r1">[1]</a> "Central Limit Theorem: Definition and Examples," Statistics How To. Accessed: Feb. 06, 2026. [Online]. Available: https://www.statisticshowto.com/probability-and-statistics/normal-distributions/central-limit-theorem-definition-examples/ <br/>
<a name="r2">[2]</a> J. Stangroom, "Sample Size Calculator," Social Science Statistics. Accessed: Feb. 06, 2026. [Online]. Available: https://www.socscistatistics.com/utilities/samplesize/calculator/ <br/>
<a name="r3">[3]</a> J. Stangroom, "Z-Score Calculator," Social Science Statistics. Accessed: Feb. 06, 2026. [Online]. Available: https://www.socscistatistics.com/tests/zscore/calculator/<br/>
