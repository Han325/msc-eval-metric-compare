# Retroboard Coverage Comparison Report

**Generated:** 2025-08-18 13:39:17

**Baseline runs:** 15
**Enhanced runs:** 15

## 🚀 AUC Performance Analysis

### 🎯 Fault Discovery Performance

| Metric | Baseline | Enhanced | Difference |
|--------|----------|----------|------------|
| Average Score | 0.9469 | 0.9806 | +0.0336 |
| Std Deviation | 0.1611 | 0.0519 | -0.1092 |
| Min Score | 0.3750 | 0.8333 | +0.4583 |
| Max Score | 1.0000 | 1.0000 | +0.0000 |
| Data Points | 15 | 15 | - |

### 📈 Branch Coverage Growth (AUC)

| Metric | Baseline | Enhanced | Difference |
|--------|----------|----------|------------|
| Average AUC | 110.28 | 70.57 | -39.71 |
| Std Deviation | 26.51 | 22.52 | -3.99 |
| Min AUC | 79.84 | 25.51 | -54.34 |
| Max AUC | 165.69 | 120.24 | -45.45 |
| Data Points | 15 | 15 | - |

### 🎯 Final Branch Coverage

| Metric | Baseline | Enhanced | Difference |
|--------|----------|----------|------------|
| Average Coverage | 71.07% | 69.83% | -1.25% |
| Std Deviation | 1.76% | 2.11% | +0.34% |
| Min Coverage | 69.01% | 67.25% | -1.76% |
| Max Coverage | 74.27% | 74.27% | +0.00% |
| Data Points | 15 | 15 | - |

## 📊 Branch Discovery Summary

- **Total unique branches (Baseline):** 127
- **Total unique branches (Enhanced):** 128
- **Shared branches:** 127
- **Only in Enhanced:** 1
- **Only in Baseline:** 0

## 🎯 Discovery Advantage

### Branches found ONLY by Enhanced tool
**Count:** 1

- 📂 modules/board/session/sagas.js - Branch #6 (path 1) at Line 61, Col 2 (hit in 1/15 runs)

#### Detailed Run Analysis for Enhanced-Only Branches

**📂 modules/board/session/sagas.js - Branch #6 (path 1) at Line 61, Col 2**
- Hit in runs: [15]
- Test suites to examine: `retroboard-enhanced-15-run-cc/15/testretroboardLLM_0/`

**Pattern Analysis for this branch:**
- Average test length: 86.0 method calls
- Most frequent methods: renameBoardRetrospectivePage(9), createIdeasPostRetrospectivePage(8), goToMenuRetrospectivePage(8)
- Common parameters: boardNames0(9), ideasPosts0(8), id0(7)


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

