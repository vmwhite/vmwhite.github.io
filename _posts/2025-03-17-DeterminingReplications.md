---
layout: post
author: Veronica White
title: How many samples are needed? Finding N for Confidence Intervals and Prediction Intervals using the Benforrioni Correction
tags: statistics skill 
# need both visible 1 and published false to not publish post
published: false
visible: 1
---
When conducting simulation studies, you'll often need to determine the number of samples you need to achieve a certain level of confidence in your resutling analysis or calibration. 

**sample with a replacement for confidence intervals  central limit theorem:**
https://www.statisticshowto.com/probability-and-statistics/normal-distributions/central-limit-theorem-definition-examples/

https://www.socscistatistics.com/tests/samplesize/default.aspx

if you are testing multiple hypotheses, you will want to use the Bonferroni correction:
$$\alpha = \frac{p}{m}$$
where $\alpha$ is the resulting confidence level to test at. $p$ is the desired confidence level you want to test for (1-.95%) and $m$ is the number of hypotheses you test. For example, if you were testing 12 different hypotheses and desired a 95% confidence level then the correction would change to:
$$\alpha = \frac{0.05}{12} = 0.004166$$


we would then use this $\alpha$ to calculate out Z value. the Z-score can be calculated from the $\alpha$:

https://www.socscistatistics.com/tests/ztest/zscorecalculator.aspx <- calculte Z from alpha (aka P). For example for an $\alpha$ of $0.004166$, $Z= 2.63831$
Note: as alpha gets closer to 0, Z increases

We are now ready to calculate our desired convenience interval using the final equation:
$$\bar{\mu} \plusminus Z_{\frac{\alpha}{2}}\frac{\sigma}{\sqrt{n}}$$
where $\bar{\mu}$ is the sample mean, $Z_{\frac{\alpha}{2}}$ is the Z score, $\sigma$ is the Standard Deviation, and $n$ is the number of samples. 



The cons of using the Bonferroni correction for larger sample sizes is when we are testing a large number of tests or if those hypotheses are positively correlated, we run the risk of receiving false negatives (i.e., risk not observing statistical significance where it does exisit). Need to increase N to reduce false negatives. 

-------------- Seperate for determining sample size for RCT or social study -------- 

**Sample with out replacement via finaite population correction:**
https://select-statistics.co.uk/blog/importance-effect-sample-size/
https://select-statistics.co.uk/calculators/sample-size-calculator-population-mean/
https://www.smartsurvey.co.uk/survey-tools/sample-size-calculator
https://www.statisticshowto.com/finite-population-correction-factor/

if you are unsure of the calcualtion use $N=100,000$ since larger values do not effect the sample size much following that. The sample size can be calculated via:

$n = \frac{\frac{Z^2p(1-p)}{e^2}}{1+\frac{Z^2p(1-p)}{e^2N}}$
where $Z$ is the Z score, $p$ is the population proportion, $e$ is the margin of error, and $N$ is the population size


factor in drop out rate after finding ideal sample adjsut for potential drop out rate so that you still meet desired significance. 


When conducting simulation studies—or designing empirical analyses more broadly—you will often face the question:

**How many samples do I need to achieve a desired level of confidence in my results?**

This question arises in calibration, performance comparison, uncertainty quantification, and hypothesis testing. The answer depends on *how* you are sampling, *what* you are estimating, and *how many* statistical tests you are running simultaneously.

This post walks through:
1. Sample size determination for confidence intervals under repeated sampling  
2. Adjustments needed when testing multiple hypotheses (Bonferroni correction)  
3. A brief contrast with finite-population sampling (e.g., surveys or RCTs)

---

## Sampling With Replacement: Confidence Intervals and the Central Limit Theorem

In many simulation settings, samples are drawn **with replacement**. Under fairly mild conditions, the **Central Limit Theorem (CLT)** applies, allowing us to construct confidence intervals for the mean using a normal approximation.

If the sample size is sufficiently large, the sampling distribution of the sample mean is approximately normal, regardless of the underlying distribution.

Helpful references:
- Central Limit Theorem overview:  
  https://www.statisticshowto.com/probability-and-statistics/normal-distributions/central-limit-theorem-definition-examples/
- Sample size intuition:  
  https://www.socscistatistics.com/tests/samplesize/default.aspx

---

## Multiple Hypotheses and the Bonferroni Correction

If you are testing **multiple hypotheses simultaneously**, the probability of making at least one Type I error (false positive) increases. To control the **family-wise error rate**, a common (and conservative) adjustment is the **Bonferroni correction**.

The corrected significance level is:

\[
\alpha = \frac{p}{m}
\]

where:
- \( p \) is the desired overall significance level (e.g., 0.05 for 95% confidence),
- \( m \) is the number of hypotheses being tested.

### Example

Suppose you are testing **12 hypotheses** and want an overall confidence level of **95%**:

\[
\alpha = \frac{0.05}{12} = 0.004166
\]

This adjusted \( \alpha \) is then used to compute the corresponding **Z-score**.

A Z-score calculator can be found here:  
https://www.socscistatistics.com/tests/ztest/zscorecalculator.aspx

For \( \alpha = 0.004166 \), the corresponding Z-score is approximately:

\[
Z \approx 2.64
\]

> **Note:** As \( \alpha \) decreases, the Z-score increases—meaning wider confidence intervals unless the sample size increases.

---

## Confidence Interval Formula

Once the adjusted Z-score is determined, the confidence interval for the mean is:

\[
\bar{\mu} \pm Z_{\alpha/2}\frac{\sigma}{\sqrt{n}}
\]

where:
- \( \bar{\mu} \) is the sample mean,
- \( Z_{\alpha/2} \) is the Z-score corresponding to the adjusted significance level,
- \( \sigma \) is the standard deviation,
- \( n \) is the number of samples.

This equation makes the tradeoff explicit:
- Smaller \( \alpha \) → larger Z → wider interval  
- Larger \( n \) → narrower interval  

If you want to maintain precision while correcting for multiple tests, **you must increase \( n \)**.

---

## A Caution on Bonferroni

While simple and widely used, the Bonferroni correction can be **overly conservative**, especially when:
- The number of hypotheses is large, or
- Hypotheses are positively correlated.

In these cases, the correction increases the risk of **Type II errors (false negatives)**—failing to detect real effects. In simulation studies, this often means needing substantially larger sample sizes to preserve power.

---

## Sampling Without Replacement: Finite Population Settings

In contrast to simulation, many **survey studies, RCTs, or social science applications** involve sampling **without replacement** from a finite population.

In these cases, a **finite population correction (FPC)** may be appropriate.

Helpful references:
- Effect size and sample size intuition:  
  https://select-statistics.co.uk/blog/importance-effect-sample-size/
- Population mean sample size calculator:  
  https://select-statistics.co.uk/calculators/sample-size-calculator-population-mean/
- Finite population correction explanation:  
  https://www.statisticshowto.com/finite-population-correction-factor/

If the population size is unknown or very large, it is common to assume:
\[
N = 100{,}000
\]
Larger values beyond this have little effect on the resulting sample size.

The sample size formula with finite population correction is:

\[
n = \frac{\frac{Z^2 p(1-p)}{e^2}}{1 + \frac{Z^2 p(1-p)}{e^2 N}}
\]

where:
- \( Z \) is the Z-score,
- \( p \) is the population proportion,
- \( e \) is the margin of error,
- \( N \) is the population size.

---

## Accounting for Dropout and Attrition

In applied studies, the **calculated sample size is rarely the final number recruited**. You should always inflate the initial sample to account for expected:
- Dropout
- Nonresponse
- Missing data

This ensures that the *effective* sample size still meets your desired confidence or power targets.

---

## Example: Accounting for Dropout and Attrition

In practice, the sample size you *calculate* is rarely the sample size you *end up with*. Attrition due to dropout, nonresponse, missing data, or unusable observations is common in both simulation experiments and real-world studies.

To account for this, you should **inflate your initial sample size** so that the *final analyzed sample* still meets your desired confidence or precision requirements.

### Simple Adjustment Formula

Let:
- \( n_{\text{required}} \) = sample size required by your statistical formula  
- \( r \) = expected dropout rate (as a proportion)

Then the adjusted sample size is:

\[
n_{\text{adjusted}} = \frac{n_{\text{required}}}{1 - r}
\]

### Example

Suppose your confidence interval calculations (after applying a Bonferroni correction) indicate that you need:

\[
n_{\text{required}} = 1{,}200
\]

Based on prior experience, you expect a **20% dropout rate**:

\[
r = 0.20
\]

Then the adjusted sample size is:

\[
n_{\text{adjusted}} = \frac{1{,}200}{1 - 0.20} = \frac{1{,}200}{0.80} = 1{,}500
\]

This means you should plan to generate or recruit **1,500 samples** so that approximately **1,200 usable observations** remain after attrition.

---

### Why This Matters

Failing to account for dropout can lead to:
- Wider-than-expected confidence intervals
- Loss of statistical power
- Increased risk of false negatives, especially when using conservative corrections like Bonferroni

In simulation studies, attrition may arise from discarded runs, unstable warm-up periods, or convergence failures. In empirical studies, it may result from participant withdrawal or missing outcomes. In either case, planning for attrition *up front* is far easier than trying to recover power after the fact.

---

### Rule of Thumb

- **10–15%**: optimistic / well-controlled studies  
- **20–30%**: typical for many applied settings  
- **30%+**: plan carefully and justify assumptions  

When in doubt, err on the side of a slightly larger initial sample—especially if running simulations where additional replications are relatively inexpensive.

---

## Takeaway

- Simulation studies typically rely on **sampling with replacement** and CLT-based confidence intervals.
- Multiple hypothesis testing requires correcting \( \alpha \), often via Bonferroni.
- Bonferroni increases required sample sizes to maintain precision and power.
- Finite-population settings require different formulas and assumptions.
- Always plan for attrition.

If you’re designing a simulation or study and unsure which framework applies, that decision alone often determines whether your sample size estimate is reasonable—or wildly optimistic.