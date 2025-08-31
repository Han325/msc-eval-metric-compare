# Dimeshift Coverage Comparison Report

**Generated:** 2025-08-31 13:07:32

**Baseline runs:** 20
**Enhanced runs:** 20

## 🚀 AUC Performance Analysis

### 🎯 Fault Discovery Performance

| Metric | Baseline | Enhanced | Difference |
|--------|----------|----------|------------|
| Average Score | 0.6344 | 0.6691 | +0.0347 |
| Std Deviation | 0.0698 | 0.0595 | -0.0104 |
| Min Score | 0.4722 | 0.5833 | +0.1111 |
| Max Score | 0.7143 | 0.8000 | +0.0857 |
| Data Points | 20 | 20 | - |

### 📈 Branch Coverage Growth (AUC)

| Metric | Baseline | Enhanced | Difference |
|--------|----------|----------|------------|
| Average AUC | 46.37 | 38.12 | -8.26 |
| Std Deviation | 28.58 | 14.30 | -14.28 |
| Min AUC | 28.02 | 16.73 | -11.29 |
| Max AUC | 161.46 | 68.03 | -93.43 |
| Data Points | 20 | 20 | - |

### 🎯 Final Branch Coverage

| Metric | Baseline | Enhanced | Difference |
|--------|----------|----------|------------|
| Average Coverage | 40.33% | 38.91% | -1.43% |
| Std Deviation | 1.15% | 2.15% | +0.99% |
| Min Coverage | 38.61% | 32.78% | -5.83% |
| Max Coverage | 42.59% | 41.39% | -1.20% |
| Data Points | 20 | 20 | - |

## 🔬 Statistical Significance Analysis

| Metric | p-value | A₁₂ (Enhanced vs. Baseline) | Conclusion |
|:---|:---:|:---:|:---|
| **Fault Discovery Score** | 0.098 | 0.620 | Not significant, but a **small effect size** trend was observed. |
| **Branch Coverage Growth (AUC)** | 0.155 | 0.405 | Not significant, but a **small effect size** trend was observed. |
| **Final Branch Coverage** | 0.992 | 0.280 | Not significant, but a **large effect size** trend was observed. |

*The **p-value** indicates statistical significance (p < 0.05 is significant).*
*The **A₁₂ effect size** measures the probability that a random run from 'Enhanced' will outperform a random run from 'Baseline'. 0.5 is no difference, >0.5 favors Enhanced.*

## 🐞 Unique Fault Discovery Analysis

- **Total unique fault types (Baseline):** 12
- **Total unique fault types (Enhanced):** 12
- **Shared fault types found by both:** 10
- **Fault types found ONLY by Enhanced:** 2
- **Fault types found ONLY by Baseline:** 2

### Fault Types Found ONLY by Enhanced Tool

- `http://webapp:8080/api/wallets/2/accesses/ - Failed to load resource: the server responded with a status of 500 (Internal Server Error)`
- `http://webapp:8080/api/wallets/undefined - Failed to load resource: the server responded with a status of 500 (Internal Server Error)`

### Fault Types Found ONLY by Baseline Tool

- `http://webapp:8080/api/users/7/wallets - Failed to load resource: the server responded with a status of 500 (Internal Server Error)`
- `http://webapp:8080/api/users/8/wallets - Failed to load resource: the server responded with a status of 500 (Internal Server Error)`

## 📊 Branch Discovery Summary

- **Total unique branches (Baseline):** 466
- **Total unique branches (Enhanced):** 473
- **Shared branches:** 465
- **Only in Enhanced:** 8
- **Only in Baseline:** 1

## 🎯 Discovery Advantage

### Branches found ONLY by Enhanced tool
**Count:** 8

- 📂 app/abstract/page.js - Branch #10 (path 0) at Line 60, Col 8 (hit in 1/20 runs)
- 📂 app/abstract/page.js - Branch #18 (path 0) at Line 113, Col 2 (hit in 1/20 runs)
- 📂 app/abstract/page.js - Branch #9 (path 1) at Line 58, Col 3 (hit in 1/20 runs)
- 📂 app/template_manager.js - Branch #1 (path 0) at Line 16, Col 3 (hit in 1/20 runs)
- 📂 app/views/header.js - Branch #1 (path 1) at Line 22, Col 2 (hit in 1/20 runs)
- 📂 app/views/pages/wallet.js - Branch #15 (path 1) at Line 154, Col 3 (hit in 1/20 runs)
- 📂 app/views/pages/wallet.js - Branch #16 (path 0) at Line 158, Col 10 (hit in 1/20 runs)
- 📂 app/views/pages/wallets.js - Branch #5 (path 0) at Line 47, Col 2 (hit in 1/20 runs)

#### Detailed Run Analysis for Enhanced-Only Branches

**📂 app/abstract/page.js - Branch #10 (path 0) at Line 60, Col 8**
- Hit in runs: [18]
- Test suites to examine: `dimeshift-enhanced-20-run-cc/18/testdimeshiftLLM_0/`

**Pattern Analysis for this branch:**
- Average test length: 103.0 method calls
- Most frequent methods: goToAddWalletPageWalletPage(9), editAddWalletPage(8), goToTrashPageWalletPage(8)
- Common parameters: id0(13), walletNames0(7), goals0, walletNames0(5)

**📂 app/abstract/page.js - Branch #18 (path 0) at Line 113, Col 2**
- Hit in runs: [18]
- Test suites to examine: `dimeshift-enhanced-20-run-cc/18/testdimeshiftLLM_0/`

**Pattern Analysis for this branch:**
- Average test length: 103.0 method calls
- Most frequent methods: goToAddWalletPageWalletPage(9), editAddWalletPage(8), goToTrashPageWalletPage(8)
- Common parameters: id0(13), walletNames0(7), goals0, walletNames0(5)

**📂 app/abstract/page.js - Branch #9 (path 1) at Line 58, Col 3**
- Hit in runs: [18]
- Test suites to examine: `dimeshift-enhanced-20-run-cc/18/testdimeshiftLLM_0/`

**Pattern Analysis for this branch:**
- Average test length: 103.0 method calls
- Most frequent methods: goToAddWalletPageWalletPage(9), editAddWalletPage(8), goToTrashPageWalletPage(8)
- Common parameters: id0(13), walletNames0(7), goals0, walletNames0(5)

**📂 app/template_manager.js - Branch #1 (path 0) at Line 16, Col 3**
- Hit in runs: [3]
- Test suites to examine: `dimeshift-enhanced-20-run-cc/3/testdimeshiftLLM_0/`

**Pattern Analysis for this branch:**
- Average test length: 100.0 method calls
- Most frequent methods: goToAddWalletPageWalletPage(9), editAddWalletPage(8), goToGoalsPageWalletPage(6)
- Common parameters: id0(10), walletNames0(8), id1(7)

**📂 app/views/header.js - Branch #1 (path 1) at Line 22, Col 2**
- Hit in runs: [18]
- Test suites to examine: `dimeshift-enhanced-20-run-cc/18/testdimeshiftLLM_0/`

**Pattern Analysis for this branch:**
- Average test length: 103.0 method calls
- Most frequent methods: goToAddWalletPageWalletPage(9), editAddWalletPage(8), goToTrashPageWalletPage(8)
- Common parameters: id0(13), walletNames0(7), goals0, walletNames0(5)

**📂 app/views/pages/wallet.js - Branch #15 (path 1) at Line 154, Col 3**
- Hit in runs: [18]
- Test suites to examine: `dimeshift-enhanced-20-run-cc/18/testdimeshiftLLM_0/`

**Pattern Analysis for this branch:**
- Average test length: 103.0 method calls
- Most frequent methods: goToAddWalletPageWalletPage(9), editAddWalletPage(8), goToTrashPageWalletPage(8)
- Common parameters: id0(13), walletNames0(7), goals0, walletNames0(5)

**📂 app/views/pages/wallet.js - Branch #16 (path 0) at Line 158, Col 10**
- Hit in runs: [18]
- Test suites to examine: `dimeshift-enhanced-20-run-cc/18/testdimeshiftLLM_0/`

**Pattern Analysis for this branch:**
- Average test length: 103.0 method calls
- Most frequent methods: goToAddWalletPageWalletPage(9), editAddWalletPage(8), goToTrashPageWalletPage(8)
- Common parameters: id0(13), walletNames0(7), goals0, walletNames0(5)

**📂 app/views/pages/wallets.js - Branch #5 (path 0) at Line 47, Col 2**
- Hit in runs: [18]
- Test suites to examine: `dimeshift-enhanced-20-run-cc/18/testdimeshiftLLM_0/`

**Pattern Analysis for this branch:**
- Average test length: 103.0 method calls
- Most frequent methods: goToAddWalletPageWalletPage(9), editAddWalletPage(8), goToTrashPageWalletPage(8)
- Common parameters: id0(13), walletNames0(7), goals0, walletNames0(5)


### Branches found ONLY by Baseline tool
**Count:** 1

- 📂 app/views/dialogs/wallet_accesses.js - Branch #5 (path 0) at Line 72, Col 2 (hit in 1/20 runs)

## 📊 Consistency Advantage

### Branches Enhanced hits more consistently (≥10 runs vs <5 runs)
**Count:** 3

- 📂 app/template_manager.js - Branch #0 (path 1) at Line 14, Col 3
  - Enhanced: 19/20 runs, Baseline: 3/20 runs
- 📂 app/template_manager.js - Branch #1 (path 1) at Line 16, Col 3
  - Enhanced: 19/20 runs, Baseline: 3/20 runs
- 📂 app/template_manager.js - Branch #2 (path 1) at Line 18, Col 3
  - Enhanced: 19/20 runs, Baseline: 3/20 runs

### Branches Baseline hits more consistently (≥10 runs vs <5 runs)
**Count:** 3

- 📂 app/models/wallets_access.js - Branch #2 (path 1) at Line 14, Col 140
  - Baseline: 18/20 runs, Enhanced: 3/20 runs
- 📂 app/views/dialogs/wallet_accesses.js - Branch #6 (path 0) at Line 78, Col 2
  - Baseline: 14/20 runs, Enhanced: 4/20 runs
- 📂 app/views/pages/plans.js - Branch #13 (path 1) at Line 302, Col 2
  - Baseline: 11/20 runs, Enhanced: 3/20 runs

📁 **Test files copied to:** `test_files_for_inspection/` for manual inspection

