---
layout: post
author: Veronica White
title: Which Statistical Test should I use? An Overview
tags: statistics skill 
# need both visible 1 and published false to not publish post
published: true
visible: 0
---

Collaborative work with organizations often involves analyzing whatever data is available. These analyses can often lead to satistical testing to help understand and communicate what the data tells you about the organization’s processes. With so many statistical tests and methods out there, it’s essential to choose the right one(s) for your study.

Before you start, consider how these frequentist statistics (i.e., statistical methods that estimate p-values) play a role in your study. The American Statistician Association has written two statements that highlight the concerns, considerations, and alternative/supplementary approaches when conducting scientific studies that utilize frequentist statistics (see [[1]](#r1), [[2]](#r2)). 

Suppose you have decided to go ahead and use frequentist statistics and, more specifically, hypothesis testing for your study. In that case, the next natural question is, what test do you use? To choose a test, you must describe both the purpose of the test and the data you are analyzing which are outlined as the following:
1. **Defining the test’s purpose** (i.e., what is your null hypothesis). If your 
    - *How many groups?*: This could be 1, 2, or >3 groups. 
        - A single group involves comparing your entire dataset to some external standard. For example, consider you wish to compare the length of stay on average length for knee surgery at a specific hospital to the clinically expected mean length of stay time. This example would involve comparing the single mean of your sample data to a known population mean value. 
        - Two groups could involve a control group and an intervention group. Alternatively, the two groups could be defined by two specific categories your data falls into (e.g., people who drink coffee every day and those who don’t). 
        - Comparing data across three or more groups could involve a control group and multiple intervention groups. Alternatively, it could be three or more specific categories your data falls into (e.g., broadway musical, off-broadway musicals, off-off-broadway musicals, etc.)
    - *If multiple groups, are the groups independent or paired?*: paired or matched data typically 
2. **Describing your data**
    - *Continuous, discrete, ordinal, vs. categorical data*: The outcome variable that you wish to compare might be continuous (e.g., lbs/oz), discrete (e.g., number of children), ordinal (e.g., Likert scale), or categorical (e.g., shoe brands) (see [[3]](#r3) for a description of data types). 
    - *parametric vs. non-parametric*: The resulting outcome variable may follow a normal distribution (i.e., parametric) or a non-parametric distribution. In other words, are you assuming your data follows a normal distribution? If yes, it is best to support this assumption through the use of a visual inspection followed by a Shapiro-Wilk test (see [[4]](#r4)) for more information). If your data fails normality testing, you can use a non-parametric test. 
        - Can I always use a non-parametric test and skip checking for normality? Short answer, you can, but it will result in higher p-values than if you used a parametric test. Long answer, see [[5]](#r5) 

Now that both the test’s purpose and data are well defined, you are ready to choose a test—table 1 summarizes when to use various hypothesis tests. Additional information on choosing a statistical test and on the various statistical tests can be found in ([[6]](#r6),[[7]](#r7)). 

#### **<u>Table 1</u>**: Summary of Hypothesis testing, Purpose of test vs. Characteristics of Outcome Variables. (Adapted from [[6]](#r6))

{:.DataTable}

| **<u>Purpose of Test</u>**                                      | **Continuous and normal data** | **Continuous, non-normal data OR non-continuous, discrete or ordinal data** | **Non-continuous, categorical data**                    |
|:----------------------------------------------------------------|:--------------------------------------:|:------------------------------------------------:|:---------------------------------------------------------------:|
| **Compare 1 mean with a population value**     |One sample z-test/t-test<sup>[a](#f1)</sup>|      One sample z-test/ t-test <sup>[a](#f1)</sup>               |              One sample z-test/ exact binomial test           |
|-----------------------------------------------------------------|----------------------------------------|--------------------------------------------------|-----------------------------------------------------------------|
| **Compare 2 independent groups**                                | Independent samples z-test/ t-test<sup>[a](#f1)</sup> | Mann-Whitney U/ Wilcoxon Sum of ranks<sup>[b](#f2)</sup>  | Chi-squared test or Fisher’s exact test<sup>[c](#f3)</sup> |
|-----------------------------------------------------------------|----------------------------------------|--------------------------------------------------|-----------------------------------------------------------------|
| **Compare 2 paired groups**                                     |              Paired t-test             |       Wilcoxon signed ranks test/ sign test  | McNemar’s test                             |
|-----------------------------------------------------------------|----------------------------------------|--------------------------------------------------|-----------------------------------------------------------------|
| **Compare 3 or more independent groups**                        | One-way Analysis of Variance      |                Kruskal Wallis test               |           Chi-squared test or ordinal chi-squared test          |    
|-----------------------------------------------------------------|----------------------------------------|--------------------------------------------------|-----------------------------------------------------------------|
| **Compare 3 or more paired groups**                             | Repeated measures Analysis of variance |                   Friedman test                  |                            Cochrane Q                           |
|-----------------------------------------------------------------|----------------------------------------|--------------------------------------------------|-----------------------------------------------------------------|

footnotes:<br/>
<a name="f1"><sup>a</sup></a>: If the sample size is small (e.g., n < 30), use a t-test. <br/>
<a name="f2"><sup>b</sup></a>: The Mann-Whitney U test is the same as conducting the Wilcoxon Sum of ranks test, see [[8]](#r8) <br/>
<a name="f2"><sup>b</sup></a>: See [[9]](#r9) for a disscussion on using a chi squred vs fisher test https://www.datascienceblog.net/post/statistical_test/contingency_table_tests/ <br/>

Each test can be implemented using various software such as Excel, R, SPSS, and STATA. My personal favorite is R, and a guide for implementing the various tests discussed is in [[10]](#r10)). Are we all done? Not quite, re-read [[2]](#r2) and read [[11]](#r11) for interpretation and best practices of reporting p-values.

### References
<a name="r1">[1]</a> R. L. Wasserstein and N. A. Lazar, “The ASA Statement on p-Values: Context, Process, and Purpose,” The American Statistician, vol. 70, no. 2, pp. 129–133, Apr. 2016, doi: [10.1080/00031305.2016.1154108](10.1080/00031305.2016.1154108). <br/>
<a name="r2">[2]</a> R. L. Wasserstein, A. L. Schirm, and N. A. Lazar, “Moving to a World Beyond ‘p < 0.05,’” The American Statistician, vol. 73, no. sup1, pp. 1–19, Mar. 2019, doi: [10.1080/00031305.2019.1583913](10.1080/00031305.2019.1583913).<br/>
<a name="r3">[3]</a> “Types of Statistical Data: Numerical, Categorical, and Ordinal,” dummies. https://www.dummies.com/article/academics-the-arts/math/statistics/types-of-statistical-data-numerical-categorical-and-ordinal-169735 (accessed Feb. 07, 2022).<br/>
<!-- <a name="r3">[3]</a> J.-B. du Prel, B. Röhrig, G. Hommel, and M. Blettner, “Choosing Statistical Tests,” Dtsch Arztebl Int, vol. 107, no. 19, pp. 343–348, May 2010, doi: 10.3238/arztebl.2010.0343. -->
<a name="r4">[4]</a>  “Which statistical test should you use? | XLSTAT Support Center.” https://help.xlstat.com/s/article/which-statistical-test-should-you-use?language=en_US (accessed Feb. 07, 2022). <br/>
<a name="r5">[5]</a>“Parametric and Non-parametric tests for comparing two or more groups | Health Knowledge.” https://www.healthknowledge.org.uk/public-health-textbook/research-methods/1b-statistical-methods/parametric-nonparametric-tests (accessed Feb. 07, 2022). <br/>
<a name="r6">[6]</a> Wills, A. Research Methods and Statistics. Online Course Acessed 2/2/2022.](http://www.bristol.ac.uk/medical-school/media/rms/red/which_test.html) <br/>
<a name="r7">[7]</a>A. Ghasemi, and S. Zahediasl. "Normality tests for statistical analysis: a guide for non-statisticians." International journal of endocrinology and metabolism 10, no. 2 (2012): 486. doi: [10.5812/ijem.3505](10.5812/ijem.3505) <br/>
<a name="r8">[8]</a> “Mann–Whitney U test,” Wikipedia. Jan. 31, 2022. Accessed: Feb. 07, 2022. [Online]. Available: https://en.wikipedia.org/w/index.php?title=Mann%E2%80%93Whitney_U_test&oldid=1069150075 <br/>
<a name="r9">[9]</a> “Testing Independence: Chi-Squared vs Fisher’s Exact Test,” Oct. 17, 2018. https://www.datascienceblog.net/post/statistical_test/contingency_table_tests/ (accessed Feb. 07, 2022). <br/>
<a name="r10">[10]</a> TJ Murphy. biostats538@gmail.com Department of Pharmacology and Chemical Biology, School of Medicine, Emory University, Atlanta, GA, JABSTB: Statistical Design and Analysis of Experiments with R. Accessed: Feb. 01, 2022. [Online]. Available: https://tjmurphy.github.io/jabstb/index.html <br/>
<a name="r11">[11]</a> J. Storopoli. "Bayesian Statistics with Julia and Turing". *p-values*. 2021. [https://storopoli.io/Bayesian-Julia/pages/2_bayes_stats/#p-values](https://storopoli.io/Bayesian-Julia/pages/2_bayes_stats/#p-values) 
<!-- chi squred ved fisher test https://www.datascienceblog.net/post/statistical_test/contingency_table_tests/  -->

<!-- book http://140.117.153.69/ctdr/files/857_1734.pdf  -->