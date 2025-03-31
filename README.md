# TpLRR-BspA-Analysis

A computational toolkit for identifying and analyzing different classes of leucine-rich repeat (LRR) proteins in the UniRef50 database, with a focus on the TpLRR/BspA-like class.  https://www.sciencedirect.com/science/article/pii/S1047847723000746 

## Overview

This repository contains tools for analyzing LRR protein patterns using regular expression matching across the UniRef50 database. The analysis focuses on identifying eight different classes of LRR proteins:

1. TpLRR (21 AA)
2. RI-like (28 AA)
3. SDS22-like (22 AA)
4. Cysteine-containing (22 AA)
5. Bacterial (20 AA)
6. Typical LRR
7. Plant-specific (22 AA)
8. BspA-like

## Features

- Regular expression pattern matching for different LRR classes
- Processing of large protein databases (UniRef50)
- Cloud storage integration for input/output management
- Parallel processing capabilities with session management

## Installation

```bash
# Clone the repository
git clone https://github.com/xqiu625/TpLRR-Pattern-Finder.git
cd TpLRR-BspA-Analysis

# Create a conda environment (recommended)
conda create -n lrr_finder python=3.9
conda activate lrr_finder

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Download UniRef50 Database

```bash
# Run the download script
./scripts/download_uniref50.sh
```

### 2. Run Analysis for Specific LRR Patterns

```bash
# Analyze TpLRR patterns
python src/tplrr_finder.py uniref50_lrr uniref50.fasta.gz

# Or use the run_analysis script to run multiple patterns
./scripts/run_analysis.sh
```

### 3. Managing Sessions

```bash
# Create a new session
./scripts/tmux_management.sh create lrr_analysis

# List active sessions
./scripts/tmux_management.sh list

# Attach to a session
./scripts/tmux_management.sh attach lrr_analysis

# Kill a session
./scripts/tmux_management.sh kill lrr_analysis
```

## LRR Patterns

The repository includes regular expression patterns for various LRR classes:

- TpLRR: `(?:C|N).{2}L.{2}I.{1}L.{3}L.{2}I.{3}AF`
- RI-like: `.{3}L.{2}L.{1}L.{2}[NC].{1}L.{3}G[GAIVLMFPWC].{2}L.{2}[GAIVLMFPWC]L.{2}`
- SDS22-like: `L.{2}L.{2}L.{1}L.{2}N.{1}I.{2}I.{2}L.{2}`
- And more (see `data/patterns.json`)

## Citation

If you use this code in your research, please cite:

```
Takkouche, A., Qiu, X., Sedova, M., Jaroszewski, L., & Godzik, A. (2023). 
Unusual structural and functional features of TpLRR/BspA-like LRR proteins. 
Journal of Structural Biology, 215, 108011.
https://doi.org/10.1016/j.jsb.2023.108011
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
