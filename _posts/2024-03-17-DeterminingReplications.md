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


