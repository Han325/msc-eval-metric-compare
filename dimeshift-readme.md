# Coverage Analysis Methodology

## Overview

This document describes the methodology for comparing branch coverage between two testing tools (baseline vs enhanced) across multiple test runs to evaluate discovery capabilities and consistency.

## Data Collection

### Test Setup
- **Baseline tool runs:** 15 independent executions
- **Enhanced tool runs:** 15 independent executions  
- **Coverage measurement:** Istanbul.js branch coverage reports (`coverage-final.json`)
- **Target application:** Same web application for all runs

### File Structure
```
dimeshift-baseline-15-run-cc/
├── 1/testdimeshiftLLM_0/coverage-final.json
├── 2/testdimeshiftLLM_0/coverage-final.json
...
├── 15/testdimeshiftLLM_0/coverage-final.json

dimeshift-enhanced-15-run-cc/
├── 1/testdimeshiftLLM_0/coverage-final.json
├── 2/testdimeshiftLLM_0/coverage-final.json
...
├── 15/testdimeshiftLLM_0/coverage-final.json
```

## Branch Identification

### Branch Key Structure
Each unique branch is identified by a tuple:
```
(file_path, branch_id, path_index)
```

Where:
- **file_path:** JavaScript file location (e.g., `app/views/dialogs/add_profit.js`)
- **branch_id:** Unique identifier within the file (e.g., `"1"`, `"2"`)
- **path_index:** Specific path within the branch (e.g., true/false path: 0 or 1)

### Data Extraction
From each `coverage-final.json`:
1. **branchMap:** Contains branch metadata including line/column locations
2. **b:** Contains hit counts for each branch path
3. **Hit detection:** Branch path is considered "hit" if `hit_count > 0`

## Union Calculation Methodology

### Definition of Tool Coverage
**Union of a tool = Set of all unique branches that the tool successfully executes (hit_count > 0) across all its runs**

### Mathematical Formulation

For a tool with runs R₁, R₂, ..., R₁₅:

```
Union_tool = ⋃(i=1 to 15) {branches with hit_count > 0 in run Rᵢ}
```

### Critical Design Decision
- **Included:** Branches with hit_count > 0 in at least one run
- **Excluded:** Branches with hit_count = 0 in all runs (even if they exist in the JSON structure)

**Rationale:** A branch that is never executed should not count as "covered" by a tool, regardless of whether it appears in the coverage report structure.

## Comparison Metrics

### 1. Discovery Analysis

**Intersection (Shared Branches):**
```
Shared = Union_baseline ∩ Union_enhanced
```

**Unique Discovery:**
```
Only_Enhanced = Union_enhanced - Union_baseline
Only_Baseline = Union_baseline - Union_enhanced
```

**Discovery Advantage:**
```
Net_Discovery = |Only_Enhanced| - |Only_Baseline|
```

### 2. Frequency Analysis

For each branch, track hit frequency across runs:
```
Frequency_tool(branch) = Number of runs where hit_count > 0
```

### 3. Consistency Analysis

**Purpose:** Among shared branches, identify which tool provides more reliable coverage.

**Methodology:**
For each branch in the intersection, compare hit frequencies:

```python
if enhanced_frequency >= threshold_high and baseline_frequency <= threshold_low:
    # Enhanced more consistent
elif baseline_frequency >= threshold_high and enhanced_frequency <= threshold_low:
    # Baseline more consistent
```

**Threshold Parameters:**
- `threshold_high`: Minimum runs for "consistent" (e.g., ≥10 runs)  
- `threshold_low`: Maximum runs for "inconsistent" (e.g., <5 runs)

**Interpretation:**
- **Enhanced more consistent:** Enhanced reliably hits branches that baseline hits sporadically
- **Baseline more consistent:** Baseline reliably hits branches that enhanced hits sporadically

## Results Interpretation

### Summary Statistics
- **Total unique branches per tool:** Size of each union
- **Shared branches:** Size of intersection
- **Discovery counts:** Size of unique sets

### Key Findings Format
1. **Discovery Advantage:** Count and details of branches only one tool finds
2. **Consistency Advantage:** Count and details of branches one tool hits more reliably
3. **Trade-off Analysis:** What each tool gains/loses relative to the other

### Example Results Interpretation

Given results:
- Baseline: 465 unique branches
- Enhanced: 469 unique branches  
- Shared: 464 branches
- Only Enhanced: 5 branches
- Only Baseline: 1 branch

**Interpretation:**
- Enhanced discovers 5 code paths that baseline never reaches across all 15 runs
- Baseline finds 1 code path that enhanced never reaches  
- Net discovery advantage: +4 branches for enhanced tool
- 464 branches can be reached by both tools (98.9% overlap)

## Limitations and Considerations

### Variability Factors
- Test execution timing and randomness
- Network conditions and system load
- Non-deterministic application behavior
- Tool-specific generation strategies

### Methodological Assumptions
- Multiple runs capture tool behavior better than single runs
- Branch coverage is a meaningful proxy for test effectiveness
- Hit frequency indicates reliability of coverage
- Union-based aggregation appropriately represents tool capabilities

## Technical Implementation

### Data Processing Pipeline
1. **File Discovery:** Automatically locate all coverage files
2. **JSON Parsing:** Extract branch data using Istanbul.js format
3. **Union Calculation:** Aggregate unique hit branches per tool
4. **Intersection Analysis:** Calculate shared and unique branches
5. **Frequency Calculation:** Count hits per branch across runs
6. **Report Generation:** Format results for analysis

### Quality Assurance
- Error handling for missing or corrupted files
- Validation of JSON structure consistency
- Verification of branch key uniqueness
- Cross-checking of mathematical relationships (e.g., union sizes)