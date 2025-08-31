#!/usr/bin/env python3

import json
import sys
import os
from pathlib import Path
from collections import defaultdict
import datetime
import re
import statistics
import shutil

# NEW IMPORTS FOR STATISTICAL ANALYSIS
import pingouin as pg
import pandas as pd


def load_all_coverage_files(base_dir, tool_name):
    """
    Load all coverage files for a given tool from the directory structure.
    Returns a list of (run_number, coverage_data) tuples.
    """
    coverage_files = []
    tool_dir = Path(base_dir) / f"dimeshift-{tool_name}-20-run-cc"
    
    if not tool_dir.exists():
        print(f"Error: Directory {tool_dir} not found", file=sys.stderr)
        return []

    for run_num in range(1, 21):  # 1 to 20
        coverage_file = tool_dir / str(run_num) / "testdimeshiftLLM_0" / "coverage-final.json"
        
        if coverage_file.exists():
            try:
                with open(coverage_file, 'r') as f:
                    coverage_data = json.load(f)
                coverage_files.append((run_num, coverage_data))
                print(f"✅ Loaded {tool_name} run {run_num}")
            except json.JSONDecodeError as e:
                print(f"⚠️  Error parsing {coverage_file}: {e}", file=sys.stderr)
            except Exception as e:
                print(f"⚠️  Error loading {coverage_file}: {e}", file=sys.stderr)
        else:
            print(f"⚠️  Missing: {coverage_file}")
    
    return coverage_files

def extract_branches_from_run(coverage_data):
    """
    Extract all branches from a single coverage run.
    Returns a dict of {(file_path, branch_id, path_index): hit_count}
    """
    branches = {}
    
    for file_path, file_data in coverage_data.items():
        branch_map = file_data.get('branchMap', {})
        branch_hits = file_data.get('b', {})
        
        for branch_id, branch_meta in branch_map.items():
            hits = branch_hits.get(branch_id, [])
            
            for path_index, hit_count in enumerate(hits):
                branch_key = (file_path, branch_id, path_index)
                branches[branch_key] = hit_count
    
    return branches

def aggregate_tool_coverage(coverage_files):
    """
    Aggregate coverage across all runs for a tool.
    This version CORRECTLY defines the union as branches that were actually HIT.
    """
    # This set will store keys ONLY for branches with hit_count > 0 in at least one run.
    union_of_hit_branches = set()
    
    # This will store all defined branches and their hit counts across all runs.
    # {branch_key: [run1_hits, run2_hits, ...]}
    frequency_data = defaultdict(lambda: [0] * len(coverage_files))
    run_map = {run_num: i for i, (run_num, _) in enumerate(coverage_files)}
    
    for run_num, coverage_data in coverage_files:
        run_branches = extract_branches_from_run(coverage_data)
        run_index = run_map[run_num]
        
        for branch_key, hit_count in run_branches.items():
            # Store the hit count for this run
            frequency_data[branch_key][run_index] = hit_count
            
            # **THE FIX IS HERE:** Only add to the union set if it was actually covered.
            if hit_count > 0:
                union_of_hit_branches.add(branch_key)
    
    # Calculate hit frequency (how many runs hit each branch)
    hit_frequency = {}
    for branch_key, hit_counts in frequency_data.items():
        hit_frequency[branch_key] = sum(1 for count in hit_counts if count > 0)
    
    # Return the CORRECT union set
    return union_of_hit_branches, frequency_data, hit_frequency

def parse_fault_auc_file(file_path):
    """
    Parse fault-auc.txt file to extract the fault discovery score.
    Returns the final score (float) or None if parsing fails.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Look for the final score line
        score_match = re.search(r"Your Test Suite's Discovery Score:\s*([0-9\.]+)", content)
        if score_match:
            return float(score_match.group(1))
        
        # Fallback: look for the calculation line
        calc_match = re.search(r"Final Score = .+ = ([0-9\.]+)", content)
        if calc_match:
            return float(calc_match.group(1))
            
        return None
    except Exception as e:
        print(f"⚠️  Error parsing fault AUC file {file_path}: {e}")
        return None

def parse_results_auc_file(file_path):
    """
    Parse results-auc.txt file to extract branch coverage AUC and final coverage.
    Returns tuple (final_coverage, auc_value) or (None, None) if parsing fails.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract final branch coverage
        coverage_match = re.search(r"Final Branch Coverage:\s*([0-9\.]+)%", content)
        final_coverage = float(coverage_match.group(1)) if coverage_match else None
        
        # Extract AUC value
        auc_match = re.search(r"AUC \(Branch Coverage vs\. Time\):\s*([0-9\.]+)", content)
        auc_value = float(auc_match.group(1)) if auc_match else None
        
        return final_coverage, auc_value
    except Exception as e:
        print(f"⚠️  Error parsing results AUC file {file_path}: {e}")
        return None, None

def load_auc_data(base_dir, tool_name):
    """
    Load AUC data for a given tool from both fault-auc.txt and results-auc.txt files.
    Returns dict with run data.
    """
    tool_dir = Path(base_dir) / f"dimeshift-{tool_name}-20-run-cc"
    auc_data = {
        'fault_scores': [],
        'branch_coverage_final': [],
        'branch_coverage_auc': [],
        'run_numbers': []
    }
    
    for run_num in range(1, 21):
        run_dir = tool_dir / str(run_num)
        
        # Parse fault-auc.txt
        fault_file = run_dir / "fault-auc.txt"
        if fault_file.exists():
            fault_score = parse_fault_auc_file(fault_file)
            if fault_score is not None:
                auc_data['fault_scores'].append(fault_score)
                auc_data['run_numbers'].append(run_num)
        
        # Parse results-auc.txt  
        results_file = run_dir / "results-auc.txt"
        if results_file.exists():
            final_cov, auc_val = parse_results_auc_file(results_file)
            if final_cov is not None:
                auc_data['branch_coverage_final'].append(final_cov)
            if auc_val is not None:
                auc_data['branch_coverage_auc'].append(auc_val)
    
    print(f"📊 {tool_name.capitalize()} AUC data: {len(auc_data['fault_scores'])} fault scores, {len(auc_data['branch_coverage_auc'])} coverage AUCs")
    return auc_data

# --- NEW FUNCTIONS FOR UNIQUE FAULT ANALYSIS ---

def normalize_fault_line(line):
    """
    Removes transient parts of a fault string, like timestamps, to group similar faults.
    """
    # This regex finds and removes "?_=[any sequence of digits]" from the line.
    return re.sub(r'\?_=\d+', '', line)

def parse_unique_faults_file(file_path):
    """
    Parse a unique_faults.txt file and return a set of NORMALIZED fault strings.
    """
    faults = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Exclude header/footer and empty lines
                if line and not line.startswith("---"):
                    # NORMALIZE the line before adding it to the set
                    normalized_line = normalize_fault_line(line)
                    faults.add(normalized_line)
    except Exception as e:
        print(f"⚠️  Error parsing unique faults file {file_path}: {e}")
    return faults

def load_all_unique_faults(base_dir, tool_name):
    """
    Load and aggregate all unique faults for a given tool across all runs.
    """
    tool_dir = Path(base_dir) / f"dimeshift-{tool_name}-20-run-cc"
    aggregated_faults = set()
    
    if not tool_dir.exists():
        # This case is handled by the coverage loader, but good practice to check
        return aggregated_faults

    for run_num in range(1, 21):
        fault_file = tool_dir / str(run_num) / "unique_faults.txt"
        if fault_file.exists():
            run_faults = parse_unique_faults_file(fault_file)
            aggregated_faults.update(run_faults)
        else:
            print(f"⚠️  Missing unique faults file: {fault_file}")
            
    print(f"🐞 {tool_name.capitalize()} unique faults: Found {len(aggregated_faults)} unique fault types across all runs.")
    return aggregated_faults

# --- END OF NEW FUNCTIONS ---

# --- MODIFIED FUNCTION ---
def calculate_auc_statistics(data_list):
    """Calculate mean, median, std dev, IQR, min, max for a list of values."""
    if not data_list:
        return {'mean': 0, 'median': 0, 'std': 0, 'iqr': 0, 'min': 0, 'max': 0, 'count': 0}
    
    stats_dict = {
        'mean': statistics.mean(data_list),
        'median': statistics.median(data_list),
        'min': min(data_list),
        'max': max(data_list),
        'count': len(data_list)
    }
    
    if len(data_list) > 1:
        stats_dict['std'] = statistics.stdev(data_list)
        # IQR requires at least two points to calculate quantiles
        try:
            quantiles = statistics.quantiles(data_list, n=4)
            stats_dict['iqr'] = quantiles[2] - quantiles[0]
        except statistics.StatisticsError:
             stats_dict['iqr'] = 0
    else:
        stats_dict['std'] = 0
        stats_dict['iqr'] = 0
    
    return stats_dict

def format_branch_info(branch_key, baseline_coverage=None, enhanced_coverage=None):
    """
    Format branch information for display.
    """
    file_path, branch_id, path_index = branch_key
    
    # Try to get location info from either coverage data
    location_info = "Unknown location"
    
    for coverage_files in [baseline_coverage, enhanced_coverage]:
        if coverage_files:
            for run_num, coverage_data in coverage_files:
                if file_path in coverage_data:
                    branch_map = coverage_data[file_path].get('branchMap', {})
                    if branch_id in branch_map:
                        locations = branch_map[branch_id].get('locations', [])
                        if path_index < len(locations):
                            loc = locations[path_index]
                            location_info = f"Line {loc['start']['line']}, Col {loc['start']['column']}"
                            break
            if location_info != "Unknown location":
                break
    
    return f"📂 {file_path} - Branch #{branch_id} (path {path_index}) at {location_info}"
    

def analyze_test_patterns(run_numbers, tool_name):
    """Analyze patterns in test suites for given runs."""
    patterns = {
        'method_calls': defaultdict(int),
        'parameters': defaultdict(int),
        'test_lengths': []
    }
    
    for run in run_numbers:
        test_file = f"dimeshift-{tool_name}-20-run-cc/{run}/testdimeshiftLLM_0/main/ClassUnderTestApogen_ESTest.java"
        
        if os.path.exists(test_file):
            try:
                with open(test_file, 'r') as f:
                    content = f.read()
                
                # Extract method calls
                method_calls = re.findall(r'classUnderTestApogen0\.(\w+)\(([^)]*)\)', content)
                patterns['test_lengths'].append(len(method_calls))
                
                for method, params in method_calls:
                    patterns['method_calls'][method] += 1
                    if params.strip():
                        patterns['parameters'][params.strip()] += 1
            except Exception as e:
                print(f"⚠️  Could not analyze test file for run {run}: {e}")

    return patterns


def copy_relevant_test_files(only_in_enhanced, enhanced_files, enhanced_hit_freq):
    """Copy test files for manual inspection, grouped by branch."""
    import shutil
    
    # Create main output directory
    output_dir = Path("test_files_for_inspection")
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n📁 Copying test files to {output_dir}/ for manual inspection...")
    
    copied_files = []
    for branch in sorted(only_in_enhanced):
        file_path, branch_id, path_index = branch
        
        # Create branch-specific folder
        clean_filename = file_path.replace('/', '_').replace('.js', '')
        branch_folder = output_dir / f"branch{branch_id}path{path_index}_{clean_filename}"
        branch_folder.mkdir(exist_ok=True)
        
        # Find which runs hit this branch
        hitting_runs = []
        for run_num, coverage_data in enhanced_files:
            run_branches = extract_branches_from_run(coverage_data)
            if branch in run_branches and run_branches[branch] > 0:
                hitting_runs.append(run_num)
        
        # Copy all test files for this branch into its folder
        for run in hitting_runs:
            source_file = f"dimeshift-enhanced-20-run-cc/{run}/testdimeshiftLLM_0/main/ClassUnderTestApogen_ESTest.java"
            if os.path.exists(source_file):
                dest_file = branch_folder / f"run{run}_test.java"
                
                try:
                    shutil.copy2(source_file, dest_file)
                    copied_files.append(dest_file)
                except Exception as e:
                    print(f"⚠️  Could not copy {source_file}: {e}")
    
    print(f"✅ Copied {len(copied_files)} test files to {output_dir}/")
    return output_dir

# --- NEW FUNCTION FOR STATISTICAL ANALYSIS (BUG FIXED) ---
def run_and_format_stat_tests(baseline_data, enhanced_data):
    """
    Runs Mann-Whitney U and calculates A12 effect size for all metrics,
    and returns a formatted Markdown table. (A12 calculation is now corrected)
    """
    if not all(k in baseline_data and k in enhanced_data for k in ['fault_scores', 'branch_coverage_auc', 'branch_coverage_final']):
        return "## 🔬 Statistical Significance Analysis\n\n- Data missing for statistical analysis.\n"
        
    results = []
    n1 = len(enhanced_data['fault_scores'])
    n2 = len(baseline_data['fault_scores'])
    
    # 1. Fault Discovery (Higher is better for Enhanced)
    mwu_fault = pg.mwu(x=enhanced_data['fault_scores'], y=baseline_data['fault_scores'], alternative='greater')
    p_val_fault = mwu_fault['p-val'].iloc[0]
    # Correct A12 = U / (n1 * n2). For 'greater', U is the number of times X > Y.
    u_val_fault = mwu_fault['U-val'].iloc[0]
    a12_fault = u_val_fault / (n1 * n2)
    results.append({
        'Metric': 'Fault Discovery Score', 'p-value': p_val_fault, 'A12': a12_fault, 
        'Interpretation': 'Higher is better'
    })
    
    # 2. Branch Coverage Growth (AUC) (LOWER is better for Enhanced)
    mwu_auc = pg.mwu(x=enhanced_data['branch_coverage_auc'], y=baseline_data['branch_coverage_auc'], alternative='less')
    p_val_auc = mwu_auc['p-val'].iloc[0]
    # For 'less', U is the number of times X < Y.
    u_val_auc = mwu_auc['U-val'].iloc[0]
    a12_auc = u_val_auc / (n1 * n2)
    results.append({
        'Metric': 'Branch Coverage Growth (AUC)', 'p-value': p_val_auc, 'A12': a12_auc,
        'Interpretation': 'Lower is better (faster)'
    })

    # 3. Final Branch Coverage (Higher is better for Enhanced)
    mwu_final = pg.mwu(x=enhanced_data['branch_coverage_final'], y=baseline_data['branch_coverage_final'], alternative='greater')
    p_val_final = mwu_final['p-val'].iloc[0]
    u_val_final = mwu_final['U-val'].iloc[0]
    a12_final = u_val_final / (n1 * n2)
    results.append({
        'Metric': 'Final Branch Coverage', 'p-value': p_val_final, 'A12': a12_final,
        'Interpretation': 'Higher is better'
    })
    
    # Format the table
    report = "## 🔬 Statistical Significance Analysis\n\n"
    report += "| Metric | p-value | A₁₂ (Enhanced vs. Baseline) | Conclusion |\n"
    report += "|:---|:---:|:---:|:---|\n"
    
    for res in results:
        p_str = f"**{res['p-value']:.3f}**" if res['p-value'] < 0.05 else f"{res['p-value']:.3f}"
        
        a12 = res['A12']
        effect_size = ""
        # Effect size thresholds for A12
        if a12 > 0.71 or a12 < 0.29: effect_size = "large"
        elif a12 > 0.64 or a12 < 0.36: effect_size = "medium"
        elif a12 > 0.56 or a12 < 0.44: effect_size = "small"
        else: effect_size = "negligible"
        
        conclusion = "Not Statistically Significant"
        if res['p-value'] < 0.05:
            advantage = "Enhanced" if a12 > 0.5 else "Baseline"
            conclusion = f"**Significant**, with a **{effect_size}** effect size in favor of **{advantage}**."
        elif effect_size != "negligible":
             conclusion = f"Not significant, but a **{effect_size} effect size** trend was observed."


        report += f"| **{res['Metric']}** | {p_str} | {a12:.3f} | {conclusion} |\n"
        
    report += "\n*The **p-value** indicates statistical significance (p < 0.05 is significant).*\n"
    report += "*The **A₁₂ effect size** measures the probability that a random run from 'Enhanced' will outperform a random run from 'Baseline'. 0.5 is no difference, >0.5 favors Enhanced.*\n"

    return report


def analyze_coverage_comparison(base_dir="."):
    """
    Main analysis function comparing baseline vs enhanced coverage AND AUC metrics.
    """
    print("🔍 Loading coverage files...")
    print("="*80)
    
    # Load all coverage files
    baseline_files = load_all_coverage_files(base_dir, "baseline")
    enhanced_files = load_all_coverage_files(base_dir, "enhanced")
    
    if not baseline_files or not enhanced_files:
        print("❌ Could not load coverage files. Please check directory structure.")
        return
    
    print(f"\n📊 Loaded {len(baseline_files)} baseline runs and {len(enhanced_files)} enhanced runs")
    
    # Load AUC data
    print("\n🔍 Loading AUC data...")
    baseline_auc = load_auc_data(base_dir, "baseline")
    enhanced_auc = load_auc_data(base_dir, "enhanced")

    # NEW: Load unique fault data
    print("\n🔍 Loading unique fault data...")
    baseline_faults = load_all_unique_faults(base_dir, "baseline")
    enhanced_faults = load_all_unique_faults(base_dir, "enhanced")
    
    print("="*80)
    
    # Aggregate coverage for each tool
    print("\n🔄 Aggregating coverage data...")
    baseline_union, baseline_freq, baseline_hit_freq = aggregate_tool_coverage(baseline_files)
    enhanced_union, enhanced_freq, enhanced_hit_freq = aggregate_tool_coverage(enhanced_files)
    
    # Analysis results
    only_in_enhanced = enhanced_union - baseline_union
    only_in_baseline = baseline_union - enhanced_union
    shared_branches = baseline_union & enhanced_union

    # NEW: Unique Fault analysis
    faults_only_in_enhanced = enhanced_faults - baseline_faults
    faults_only_in_baseline = baseline_faults - enhanced_faults
    shared_faults = baseline_faults & enhanced_faults
    
    # Consistency analysis for shared branches
    enhanced_more_consistent = []
    baseline_more_consistent = []
    
    for branch in shared_branches:
        baseline_hits = baseline_hit_freq.get(branch, 0)
        enhanced_hits = enhanced_hit_freq.get(branch, 0)
        
        # Consider "more consistent" if hit in at least 10+ runs vs <5 runs
        if enhanced_hits >= 10 and baseline_hits < 5:
            enhanced_more_consistent.append((branch, enhanced_hits, baseline_hits))
        elif baseline_hits >= 10 and enhanced_hits < 5:
            baseline_more_consistent.append((branch, baseline_hits, enhanced_hits))
    
    # Calculate AUC statistics
    baseline_fault_stats = calculate_auc_statistics(baseline_auc['fault_scores'])
    enhanced_fault_stats = calculate_auc_statistics(enhanced_auc['fault_scores'])
    baseline_cov_auc_stats = calculate_auc_statistics(baseline_auc['branch_coverage_auc'])
    enhanced_cov_auc_stats = calculate_auc_statistics(enhanced_auc['branch_coverage_auc'])
    baseline_final_cov_stats = calculate_auc_statistics(baseline_auc['branch_coverage_final'])
    enhanced_final_cov_stats = calculate_auc_statistics(enhanced_auc['branch_coverage_final'])

    test_files_dir = copy_relevant_test_files(only_in_enhanced, enhanced_files, enhanced_hit_freq)

    # Generate report
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"dimeshift_coverage_comparison_report_{timestamp}.md"
    
    print(f"\n📝 Generating detailed report: {report_file}")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Dimeshift Coverage Comparison Report\n\n")
        f.write(f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Baseline runs:** {len(baseline_files)}\n")
        f.write(f"**Enhanced runs:** {len(enhanced_files)}\n\n")
        
        # AUC Analysis Section
        f.write("## 🚀 AUC Performance Analysis\n\n")
        
        # --- MODIFIED TABLE SECTION 1 ---
        # Fault Discovery AUC
        f.write("### 🎯 Fault Discovery Performance\n\n")
        f.write("| Metric | Baseline | Enhanced | Difference |\n")
        f.write("|--------|----------|----------|------------|\n")
        f.write(f"| Average Score | {baseline_fault_stats['mean']:.4f} | {enhanced_fault_stats['mean']:.4f} | {enhanced_fault_stats['mean'] - baseline_fault_stats['mean']:+.4f} |\n")
        f.write(f"| Median Score | {baseline_fault_stats['median']:.4f} | {enhanced_fault_stats['median']:.4f} | {enhanced_fault_stats['median'] - baseline_fault_stats['median']:+.4f} |\n")
        f.write(f"| Std Deviation | {baseline_fault_stats['std']:.4f} | {enhanced_fault_stats['std']:.4f} | {enhanced_fault_stats['std'] - baseline_fault_stats['std']:+.4f} |\n")
        f.write(f"| IQR | {baseline_fault_stats['iqr']:.4f} | {enhanced_fault_stats['iqr']:.4f} | {enhanced_fault_stats['iqr'] - baseline_fault_stats['iqr']:+.4f} |\n")
        f.write(f"| Min Score | {baseline_fault_stats['min']:.4f} | {enhanced_fault_stats['min']:.4f} | {enhanced_fault_stats['min'] - baseline_fault_stats['min']:+.4f} |\n")
        f.write(f"| Max Score | {baseline_fault_stats['max']:.4f} | {enhanced_fault_stats['max']:.4f} | {enhanced_fault_stats['max'] - baseline_fault_stats['max']:+.4f} |\n")
        f.write(f"| Data Points | {baseline_fault_stats['count']} | {enhanced_fault_stats['count']} | - |\n\n")
        
        # --- MODIFIED TABLE SECTION 2 ---
        # Branch Coverage AUC
        f.write("### 📈 Branch Coverage Growth (AUC)\n\n")
        f.write("| Metric | Baseline | Enhanced | Difference |\n")
        f.write("|--------|----------|----------|------------|\n")
        f.write(f"| Average AUC | {baseline_cov_auc_stats['mean']:.2f} | {enhanced_cov_auc_stats['mean']:.2f} | {enhanced_cov_auc_stats['mean'] - baseline_cov_auc_stats['mean']:+.2f} |\n")
        f.write(f"| Median AUC | {baseline_cov_auc_stats['median']:.2f} | {enhanced_cov_auc_stats['median']:.2f} | {enhanced_cov_auc_stats['median'] - baseline_cov_auc_stats['median']:+.2f} |\n")
        f.write(f"| Std Deviation | {baseline_cov_auc_stats['std']:.2f} | {enhanced_cov_auc_stats['std']:.2f} | {enhanced_cov_auc_stats['std'] - baseline_cov_auc_stats['std']:+.2f} |\n")
        f.write(f"| IQR | {baseline_cov_auc_stats['iqr']:.2f} | {enhanced_cov_auc_stats['iqr']:.2f} | {enhanced_cov_auc_stats['iqr'] - baseline_cov_auc_stats['iqr']:+.2f} |\n")
        f.write(f"| Min AUC | {baseline_cov_auc_stats['min']:.2f} | {enhanced_cov_auc_stats['min']:.2f} | {enhanced_cov_auc_stats['min'] - baseline_cov_auc_stats['min']:+.2f} |\n")
        f.write(f"| Max AUC | {baseline_cov_auc_stats['max']:.2f} | {enhanced_cov_auc_stats['max']:.2f} | {enhanced_cov_auc_stats['max'] - baseline_cov_auc_stats['max']:+.2f} |\n")
        f.write(f"| Data Points | {baseline_cov_auc_stats['count']} | {enhanced_cov_auc_stats['count']} | - |\n\n")
        
        # --- MODIFIED TABLE SECTION 3 ---
        # Final Coverage
        f.write("### 🎯 Final Branch Coverage\n\n")
        f.write("| Metric | Baseline | Enhanced | Difference |\n")
        f.write("|--------|----------|----------|------------|\n")
        f.write(f"| Average Coverage | {baseline_final_cov_stats['mean']:.2f}% | {enhanced_final_cov_stats['mean']:.2f}% | {enhanced_final_cov_stats['mean'] - baseline_final_cov_stats['mean']:+.2f}% |\n")
        f.write(f"| Median Coverage | {baseline_final_cov_stats['median']:.2f}% | {enhanced_final_cov_stats['median']:.2f}% | {enhanced_final_cov_stats['median'] - baseline_final_cov_stats['median']:+.2f}% |\n")
        f.write(f"| Std Deviation | {baseline_final_cov_stats['std']:.2f}% | {enhanced_final_cov_stats['std']:.2f}% | {enhanced_final_cov_stats['std'] - baseline_final_cov_stats['std']:+.2f}% |\n")
        f.write(f"| IQR | {baseline_final_cov_stats['iqr']:.2f}% | {enhanced_final_cov_stats['iqr']:.2f}% | {enhanced_final_cov_stats['iqr'] - baseline_final_cov_stats['iqr']:+.2f}% |\n")
        f.write(f"| Min Coverage | {baseline_final_cov_stats['min']:.2f}% | {enhanced_final_cov_stats['min']:.2f}% | {enhanced_final_cov_stats['min'] - baseline_final_cov_stats['min']:+.2f}% |\n")
        f.write(f"| Max Coverage | {baseline_final_cov_stats['max']:.2f}% | {enhanced_final_cov_stats['max']:.2f}% | {enhanced_final_cov_stats['max'] - baseline_final_cov_stats['max']:+.2f}% |\n")
        f.write(f"| Data Points | {baseline_final_cov_stats['count']} | {enhanced_final_cov_stats['count']} | - |\n\n")
        
        # --- ADD THE NEW STATISTICAL ANALYSIS SECTION TO THE REPORT ---
        f.write(run_and_format_stat_tests(baseline_auc, enhanced_auc))
        f.write("\n")

        # --- NEW FAULT ANALYSIS SECTION ---
        f.write("## 🐞 Unique Fault Discovery Analysis\n\n")
        f.write(f"- **Total unique fault types (Baseline):** {len(baseline_faults)}\n")
        f.write(f"- **Total unique fault types (Enhanced):** {len(enhanced_faults)}\n")
        f.write(f"- **Shared fault types found by both:** {len(shared_faults)}\n")
        f.write(f"- **Fault types found ONLY by Enhanced:** {len(faults_only_in_enhanced)}\n")
        f.write(f"- **Fault types found ONLY by Baseline:** {len(faults_only_in_baseline)}\n\n")

        f.write("### Fault Types Found ONLY by Enhanced Tool\n\n")
        if faults_only_in_enhanced:
            for fault in sorted(list(faults_only_in_enhanced)):
                f.write(f"- `{fault}`\n")
        else:
            f.write("*None found.*\n")
        f.write("\n")

        f.write("### Fault Types Found ONLY by Baseline Tool\n\n")
        if faults_only_in_baseline:
            for fault in sorted(list(faults_only_in_baseline)):
                f.write(f"- `{fault}`\n")
        else:
            f.write("*None found.*\n")
        f.write("\n")
        
        # Summary statistics
        f.write("## 📊 Branch Discovery Summary\n\n")
        f.write(f"- **Total unique branches (Baseline):** {len(baseline_union)}\n")
        f.write(f"- **Total unique branches (Enhanced):** {len(enhanced_union)}\n")
        f.write(f"- **Shared branches:** {len(shared_branches)}\n")
        f.write(f"- **Only in Enhanced:** {len(only_in_enhanced)}\n")
        f.write(f"- **Only in Baseline:** {len(only_in_baseline)}\n\n")
        
        # Discovery advantage
        f.write("## 🎯 Discovery Advantage\n\n")
        f.write("### Branches found ONLY by Enhanced tool\n")
        f.write(f"**Count:** {len(only_in_enhanced)}\n\n")
        
        if only_in_enhanced:
            for branch in sorted(only_in_enhanced):
                hits = enhanced_hit_freq[branch]
                f.write(f"- {format_branch_info(branch, baseline_files, enhanced_files)} (hit in {hits}/20 runs)\n")
            # Add run-specific analysis for unique enhanced branches
            f.write("\n#### Detailed Run Analysis for Enhanced-Only Branches\n\n")
            for branch in sorted(only_in_enhanced):
                # Find which specific runs hit this branch
                hitting_runs = []
                for run_num, coverage_data in enhanced_files:
                    run_branches = extract_branches_from_run(coverage_data)
                    if branch in run_branches and run_branches[branch] > 0:
                        hitting_runs.append(run_num)

                f.write(f"**{format_branch_info(branch, baseline_files, enhanced_files)}**\n")
                f.write(f"- Hit in runs: {hitting_runs}\n")
                f.write(f"- Test suites to examine: `dimeshift-enhanced-20-run-cc/{'/testdimeshiftLLM_0/, '.join(map(str, hitting_runs))}/testdimeshiftLLM_0/`\n\n")

                # Add pattern analysis
                if hitting_runs:
                    patterns = analyze_test_patterns(hitting_runs, "enhanced")
                    f.write(f"**Pattern Analysis for this branch:**\n")
                    f.write(f"- Average test length: {statistics.mean(patterns['test_lengths']):.1f} method calls\n")
                    f.write(f"- Most frequent methods: {', '.join([f'{method}({count})' for method, count in sorted(patterns['method_calls'].items(), key=lambda x: x[1], reverse=True)[:3]])}\n")
                    f.write(f"- Common parameters: {', '.join([f'{param}({count})' for param, count in sorted(patterns['parameters'].items(), key=lambda x: x[1], reverse=True)[:3]])}\n\n")
                else:
                    f.write("*None found*\n")
        
        f.write("\n### Branches found ONLY by Baseline tool\n")
        f.write(f"**Count:** {len(only_in_baseline)}\n\n")
        
        if only_in_baseline:
            for branch in sorted(only_in_baseline):
                hits = baseline_hit_freq[branch]
                f.write(f"- {format_branch_info(branch, baseline_files, enhanced_files)} (hit in {hits}/20 runs)\n")
        else:
            f.write("*None found*\n")
        
        # Consistency advantage
        f.write("\n## 📊 Consistency Advantage\n\n")
        f.write("### Branches Enhanced hits more consistently (≥10 runs vs <5 runs)\n")
        f.write(f"**Count:** {len(enhanced_more_consistent)}\n\n")
        
        if enhanced_more_consistent:
            for branch, enhanced_hits, baseline_hits in sorted(enhanced_more_consistent):
                f.write(f"- {format_branch_info(branch, baseline_files, enhanced_files)}\n")
                f.write(f"  - Enhanced: {enhanced_hits}/20 runs, Baseline: {baseline_hits}/20 runs\n")
        else:
            f.write("*None found*\n")
        
        f.write("\n### Branches Baseline hits more consistently (≥10 runs vs <5 runs)\n")
        f.write(f"**Count:** {len(baseline_more_consistent)}\n\n")
        
        if baseline_more_consistent:
            for branch, baseline_hits, enhanced_hits in sorted(baseline_more_consistent):
                f.write(f"- {format_branch_info(branch, baseline_files, enhanced_files)}\n")
                f.write(f"  - Baseline: {baseline_hits}/20 runs, Enhanced: {enhanced_hits}/20 runs\n")
        else:
            f.write("*None found*\n")
        
        f.write(f"\n📁 **Test files copied to:** `{test_files_dir}/` for manual inspection\n\n")

    
    # Console summary
    print("\n" + "="*80)
    print("📈 COMPREHENSIVE COMPARISON SUMMARY")
    print("="*80)
    
    # AUC Results
    print(f"🚀 AUC Performance:")
    print(f"   Fault Discovery (avg): Baseline {baseline_fault_stats['mean']:.4f} vs Enhanced {enhanced_fault_stats['mean']:.4f}")
    print(f"   Coverage Growth (avg): Baseline {baseline_cov_auc_stats['mean']:.2f} vs Enhanced {enhanced_cov_auc_stats['mean']:.2f}")
    print(f"   Final Coverage (avg): Baseline {baseline_final_cov_stats['mean']:.2f}% vs Enhanced {enhanced_final_cov_stats['mean']:.2f}%")

    # NEW: Unique Fault Summary
    print(f"\n🐞 Unique Fault Discovery:")
    print(f"   Baseline: {len(baseline_faults)} unique fault types")
    print(f"   Enhanced: {len(enhanced_faults)} unique fault types")
    print(f"   Shared: {len(shared_faults)} fault types")
    print(f"   Fault types ONLY Enhanced finds: {len(faults_only_in_enhanced)}")
    print(f"   Fault types ONLY Baseline finds: {len(faults_only_in_baseline)}")
    
    print(f"\n🔢 Branch Discovery:")
    print(f"   Baseline: {len(baseline_union)} unique branches")
    print(f"   Enhanced: {len(enhanced_union)} unique branches")
    print(f"   Shared: {len(shared_branches)} branches")
    
    print(f"\n🎯 Discovery results:")
    print(f"   Branches ONLY Enhanced finds: {len(only_in_enhanced)}")
    print(f"   Branches ONLY Baseline finds: {len(only_in_baseline)}")
    
    print(f"\n📊 Consistency results:")
    print(f"   Enhanced more consistent: {len(enhanced_more_consistent)}")
    print(f"   Baseline more consistent: {len(baseline_more_consistent)}")

    print(f"\n📝 Detailed report saved to: {report_file}")
    
    # Key insights
    print(f"\n💡 Key insights:")
    
    # AUC insights
    fault_diff = enhanced_fault_stats['mean'] - baseline_fault_stats['mean']
    cov_auc_diff = enhanced_cov_auc_stats['mean'] - baseline_cov_auc_stats['mean']
    final_cov_diff = enhanced_final_cov_stats['mean'] - baseline_final_cov_stats['mean']
    
    if fault_diff > 0.01:
        print(f"   ✅ Enhanced has {fault_diff:.3f} better fault discovery score on average")
    elif fault_diff < -0.01:
        print(f"   ⚠️  Baseline has {abs(fault_diff):.3f} better fault discovery score on average")
    
    if cov_auc_diff > 5:
        print(f"   ✅ Enhanced has {cov_auc_diff:.1f} higher coverage growth AUC on average")
    elif cov_auc_diff < -5:
        print(f"   ⚠️  Baseline has {abs(cov_auc_diff):.1f} higher coverage growth AUC on average")
    
    if final_cov_diff > 1:
        print(f"   ✅ Enhanced achieves {final_cov_diff:.1f}% higher final coverage on average")
    elif final_cov_diff < -1:
        print(f"   ⚠️  Baseline achieves {abs(final_cov_diff):.1f}% higher final coverage on average")
    
    # Branch discovery insights
    if len(only_in_enhanced) > 0:
        print(f"   ✅ Enhanced discovers {len(only_in_enhanced)} unique branches never found by baseline")
    if len(enhanced_more_consistent) > 0:
        print(f"   ✅ Enhanced shows better consistency on {len(enhanced_more_consistent)} branches")

    # NEW: Fault discovery insights
    if len(faults_only_in_enhanced) > 0:
        print(f"   ✅ Enhanced discovers {len(faults_only_in_enhanced)} unique fault types never found by baseline")
    
    if (len(only_in_enhanced) == 0 and len(enhanced_more_consistent) == 0 and 
        fault_diff <= 0.01 and cov_auc_diff <= 5 and final_cov_diff <= 1 and len(faults_only_in_enhanced) == 0):
        print(f"   ⚠️  Enhanced shows limited advantages in this analysis")
        print(f"   💭 Consider: Are there other metrics to explore? Different thresholds?")
    else:
        print(f"   🎉 Enhanced tool shows measurable improvements in multiple metrics!")


if __name__ == "__main__":
    analyze_coverage_comparison()