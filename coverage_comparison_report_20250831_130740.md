# Retroboard Coverage Comparison Report

**Generated:** 2025-08-31 13:07:40

**Baseline runs:** 20
**Enhanced runs:** 20

## 🚀 AUC Performance Analysis

### 🎯 Fault Discovery Performance

| Metric | Baseline | Enhanced | Difference |
|--------|----------|----------|------------|
| Average Score | 0.9602 | 0.9854 | +0.0252 |
| Std Deviation | 0.1403 | 0.0454 | -0.0949 |
| Min Score | 0.3750 | 0.8333 | +0.4583 |
| Max Score | 1.0000 | 1.0000 | +0.0000 |
| Data Points | 20 | 20 | - |

### 📈 Branch Coverage Growth (AUC)

| Metric | Baseline | Enhanced | Difference |
|--------|----------|----------|------------|
| Average AUC | 104.19 | 69.32 | -34.86 |
| Std Deviation | 25.96 | 21.49 | -4.47 |
| Min AUC | 62.91 | 25.51 | -37.40 |
| Max AUC | 165.69 | 120.24 | -45.45 |
| Data Points | 20 | 20 | - |

### 🎯 Final Branch Coverage

| Metric | Baseline | Enhanced | Difference |
|--------|----------|----------|------------|
| Average Coverage | 70.91% | 69.36% | -1.55% |
| Std Deviation | 2.01% | 2.05% | +0.03% |
| Min Coverage | 67.25% | 66.67% | -0.58% |
| Max Coverage | 74.85% | 74.27% | -0.58% |
| Data Points | 20 | 20 | - |

## 🔬 Statistical Significance Analysis

| Metric | p-value | A₁₂ (Enhanced vs. Baseline) | Conclusion |
|:---|:---:|:---:|:---|
| **Fault Discovery Score** | 0.345 | 0.522 | Not Statistically Significant |
| **Branch Coverage Growth (AUC)** | **0.000** | 0.115 | **Significant**, with a **large** effect size in favor of **Baseline**. |
| **Final Branch Coverage** | 0.993 | 0.275 | Not significant, but a **large effect size** trend was observed. |

*The **p-value** indicates statistical significance (p < 0.05 is significant).*
*The **A₁₂ effect size** measures the probability that a random run from 'Enhanced' will outperform a random run from 'Baseline'. 0.5 is no difference, >0.5 favors Enhanced.*

## 🐞 Unique Fault Discovery Analysis

- **Total unique fault types (Baseline):** 1
- **Total unique fault types (Enhanced):** 1
- **Shared fault types found by both:** 1
- **Fault types found ONLY by Enhanced:** 0
- **Fault types found ONLY by Baseline:** 0

### Fault Types Found ONLY by Enhanced Tool

*None found.*

### Fault Types Found ONLY by Baseline Tool

*None found.*

## 📊 Branch Discovery Summary

- **Total unique branches (Baseline):** 128
- **Total unique branches (Enhanced):** 128
- **Shared branches:** 128
- **Only in Enhanced:** 0
- **Only in Baseline:** 0

## 🎯 Discovery Advantage

### Branches found ONLY by Enhanced tool
**Count:** 0


### Branches found ONLY by Baseline tool
**Count:** 0

*None found*

## 📊 Consistency Advantage

### Branches Enhanced hits more consistently (≥10 runs vs <5 runs)
**Count:** 0

*None found*

### Branches Baseline hits more consistently (≥10 runs vs <5 runs)
**Count:** 0

*None found*

📁 **Test files copied to:** `test_files_for_inspection/` for manual inspection

