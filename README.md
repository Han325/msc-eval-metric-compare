# MSc SSE Individual Research Project Submission Details

This markdown document contains the details of the code artifiact submissions made for the MSc research project.

## About
This repository contains the python files that are used to compare the evaluation metrics from the report between the baseline and the enhanced tool. 

# Evaluation Metric Comparison Tool

Python scripts for analyzing and comparing test coverage between baseline and enhanced testing tools across multiple experimental runs.

## Files

- **`compare_dimeshift_v2.py`** - Coverage analysis for DimeShift application testing
- **`compare_retroboard_v2.py`** - Coverage analysis for Retroboard application testing

## Functionality

These tools analyze JavaScript test coverage data from automated testing experiments to compare the effectiveness of baseline vs enhanced testing approaches. They evaluate:

### Coverage Metrics
- **Branch Discovery**: Identifies which code branches each tool can reach
- **Coverage Consistency**: Measures how reliably each tool hits the same branches across runs
- **Unique Coverage**: Finds branches that only one tool discovers

### Performance Metrics (AUC Analysis)
- **Fault Discovery Score**: How well each tool finds bugs/faults
- **Coverage Growth Rate**: Speed of coverage accumulation over time
- **Final Coverage Percentage**: Total coverage achieved

## Usage

```bash
# Analyze DimeShift coverage data
python compare_dimeshift_v2.py

# Analyze Retroboard coverage data  
python compare_retroboard_v2.py
```

## Expected Directory Structure

```
project/
├── [app]-baseline-15-run-cc/     # Baseline tool results
│   ├── 1/                        # Run 1
│   │   ├── test[app]LLM_0/
│   │   │   └── coverage-final.json
│   │   ├── fault-auc.txt
│   │   └── results-auc.txt
│   └── ...                       # Runs 2-15
└── [app]-enhanced-15-run-cc/     # Enhanced tool results
    └── [same structure as baseline]
```

## Output

- **Console Summary**: Key metrics and comparison results
- **Detailed Report** (`coverage_comparison_report_[timestamp].md`): Comprehensive analysis with tables and insights
- **Test Files**: Copies relevant test files for manual inspection

## Key Features

- Loads coverage data from 15 experimental runs per tool
- Correctly identifies branches that were actually executed (hit_count > 0)
- Performs statistical analysis on fault discovery and coverage metrics
- Generates actionable insights about tool performance differences
- Copies test files for manual inspection of unique coverage patterns
