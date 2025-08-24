# Coverage Comparison Report

**Generated:** 2025-08-17 08:06:30

**Baseline runs:** 15
**Enhanced runs:** 15

## 🚀 AUC Performance Analysis

### 🎯 Fault Discovery Performance

| Metric | Baseline | Enhanced | Difference |
|--------|----------|----------|------------|
| Average Score | 0.6255 | 0.6709 | +0.0454 |
| Std Deviation | 0.0650 | 0.0565 | -0.0084 |
| Min Score | 0.4722 | 0.5833 | +0.1111 |
| Max Score | 0.7143 | 0.8000 | +0.0857 |
| Data Points | 15 | 15 | - |

### 📈 Branch Coverage Growth (AUC)

| Metric | Baseline | Enhanced | Difference |
|--------|----------|----------|------------|
| Average AUC | 49.43 | 41.38 | -8.05 |
| Std Deviation | 32.65 | 14.14 | -18.51 |
| Min AUC | 28.02 | 19.12 | -8.90 |
| Max AUC | 161.46 | 68.03 | -93.43 |
| Data Points | 15 | 15 | - |

### 🎯 Final Branch Coverage

| Metric | Baseline | Enhanced | Difference |
|--------|----------|----------|------------|
| Average Coverage | 40.22% | 38.88% | -1.34% |
| Std Deviation | 1.22% | 2.45% | +1.22% |
| Min Coverage | 38.61% | 32.78% | -5.83% |
| Max Coverage | 42.59% | 41.39% | -1.20% |
| Data Points | 15 | 15 | - |

## 📊 Branch Discovery Summary

- **Total unique branches (Baseline):** 465
- **Total unique branches (Enhanced):** 466
- **Shared branches:** 464
- **Only in Enhanced:** 2
- **Only in Baseline:** 1

## 🎯 Discovery Advantage

### Branches found ONLY by Enhanced tool
**Count:** 2

- 📂 app/template_manager.js - Branch #1 (path 0) at Line 16, Col 3 (hit in 1/15 runs)
- 📂 app/template_manager.js - Branch #24 (path 0) at Line 156, Col 35 (hit in 7/15 runs)

#### Detailed Run Analysis for Enhanced-Only Branches

**📂 app/template_manager.js - Branch #1 (path 0) at Line 16, Col 3**
- Hit in runs: [3]
- Test suites to examine: `dimeshift-enhanced-15-run-cc/3/testdimeshiftLLM_0/`

**Pattern Analysis for this branch:**
- Average test length: 100.0 method calls
- Most frequent methods: goToAddWalletPageWalletPage(9), editAddWalletPage(8), goToGoalsPageWalletPage(6)
- Common parameters: id0(10), walletNames0(8), id1(7)

**📂 app/template_manager.js - Branch #24 (path 0) at Line 156, Col 35**
- Hit in runs: [9, 10, 11, 12, 13, 14, 15]
- Test suites to examine: `dimeshift-enhanced-15-run-cc/9/testdimeshiftLLM_0/, 10/testdimeshiftLLM_0/, 11/testdimeshiftLLM_0/, 12/testdimeshiftLLM_0/, 13/testdimeshiftLLM_0/, 14/testdimeshiftLLM_0/, 15/testdimeshiftLLM_0/`

**Pattern Analysis for this branch:**
- Average test length: 101.1 method calls
- Most frequent methods: editAddWalletPage(63), goToAddWalletPageWalletPage(57), goToSetTotalPageTransactionsPage(40)
- Common parameters: id0(91), walletNames0(63), amount0(30)


### Branches found ONLY by Baseline tool
**Count:** 1

- 📂 app/views/dialogs/wallet_accesses.js - Branch #5 (path 0) at Line 72, Col 2 (hit in 1/15 runs)

## 📊 Consistency Advantage

### Branches Enhanced hits more consistently (≥10 runs vs <5 runs)
**Count:** 3

- 📂 app/template_manager.js - Branch #0 (path 1) at Line 14, Col 3
  - Enhanced: 14/15 runs, Baseline: 3/15 runs
- 📂 app/template_manager.js - Branch #1 (path 1) at Line 16, Col 3
  - Enhanced: 14/15 runs, Baseline: 3/15 runs
- 📂 app/template_manager.js - Branch #2 (path 1) at Line 18, Col 3
  - Enhanced: 14/15 runs, Baseline: 3/15 runs

### Branches Baseline hits more consistently (≥10 runs vs <5 runs)
**Count:** 7

- 📂 app.js - Branch #3 (path 0) at Line 62, Col 2
  - Baseline: 15/15 runs, Enhanced: 4/15 runs
- 📂 app/models/wallets_access.js - Branch #2 (path 1) at Line 14, Col 140
  - Baseline: 14/15 runs, Enhanced: 3/15 runs
- 📂 app/views/dialogs/remove_access.js - Branch #0 (path 0) at Line 10, Col 2
  - Baseline: 15/15 runs, Enhanced: 4/15 runs
- 📂 app/views/dialogs/remove_access.js - Branch #1 (path 0) at Line 16, Col 2
  - Baseline: 15/15 runs, Enhanced: 4/15 runs
- 📂 app/views/dialogs/wallet_accesses.js - Branch #0 (path 1) at Line 12, Col 2
  - Baseline: 15/15 runs, Enhanced: 4/15 runs
- 📂 app/views/dialogs/wallet_accesses.js - Branch #1 (path 1) at Line 18, Col 2
  - Baseline: 15/15 runs, Enhanced: 4/15 runs
- 📂 app/views/dialogs/wallet_accesses.js - Branch #6 (path 0) at Line 78, Col 2
  - Baseline: 10/15 runs, Enhanced: 4/15 runs

📁 **Test files copied to:** `test_files_for_inspection/` for manual inspection

