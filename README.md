# TpLRR/BspA-like LRR Proteins Analysis

This repository contains the code and data associated with the paper:

> Takkouche A, Qiu X, Sedova M, Jaroszewski L, Godzik A. (2023). Unusual structural and functional features of TpLRR/BspA-like LRR proteins. *Journal of Structural Biology*, 215, 108011. https://doi.org/10.1016/j.jsb.2023.108011

## Overview

This code repository provides tools and analysis scripts for studying the structural and functional features of proteins from the TpLRR/BspA-like class of leucine-rich repeat (LRR) proteins. These proteins exhibit unusual structural features compared to other LRR classes, including a flipped curvature with the beta sheet on the convex side and irregular secondary structure on the concave side.

## Contents

- `structural_analysis/` - Scripts for analyzing PDB structures of TpLRR proteins
- `sequence_analysis/` - Scripts for sequence pattern analysis and identification of TpLRR proteins
- `domain_analysis/` - Code for domain distribution statistics
- `data/` - Supporting data files
- `results/` - Output files and results
- `supplementary/` - Supplementary materials referenced in the paper

## Dependencies

- Python 3.7+
- BioPython
- PyMOL (for visualization)
- FATCAT and POSA (for structural alignments)
- Regular expression libraries

## Installation

```bash
# Clone the repository
git clone https://github.com/godziklab/tplrr-analysis.git
cd tplrr-analysis

# Create and activate a conda environment (recommended)
conda create -n tplrr python=3.9
conda activate tplrr

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Structural Analysis

To perform structural analysis on the TpLRR class LRR proteins:

```bash
python structural_analysis/analyze_structures.py --pdb_list pdb_files.txt
```

### Sequence Pattern Analysis

To identify proteins using the TpLRR class signature pattern:

```bash
python sequence_analysis/pattern_search.py --database uniref50.fasta --pattern "C/NxxLxxIxLxxxLxxIgxxAFxx"
```

### Domain Distribution Statistics

To calculate domain distribution statistics for TpLRR proteins:

```bash
python domain_analysis/domain_stats.py --input tplrr_hits.txt --num 1000
```

## Key Features Studied

1. Novel structural features of TpLRR/BspA-like LRRs
2. The flipped curvature of the beta sheet to the convex side
3. Lack of helices on the opposite side of the beta sheet
4. Conservation patterns specific to TpLRR proteins
5. Domain architecture of TpLRR proteins (LRR domains, Ig-like domains, dockerin domains)
6. Distribution and prevalence in bacterial and protozoan pathogens

## Data Sources

- PDB structures: 4FS7, 4FDW, 4FD0, 4OJU, 4GT6, 4CP6, and 6MLX
- UniRef50 database for sequence analysis
- InterPro database for domain structure information
- NCBI RefSeq and UniProtKB for homolog identification

## Citation

If you use this code or data in your research, please cite:

```
Takkouche, A., Qiu, X., Sedova, M., Jaroszewski, L., & Godzik, A. (2023). 
Unusual structural and functional features of TpLRR/BspA-like LRR proteins. 
Journal of Structural Biology, 215, 108011. 
https://doi.org/10.1016/j.jsb.2023.108011
```

## License

This code is provided under the [MIT License](LICENSE).

## Contact

For questions or issues, please contact:
- Adam Godzik (adam.godzik@medsch.ucr.edu)
- Lukasz Jaroszewski (lukasz.jaroszewski@medsch.ucr.edu)

## Acknowledgments

This work was funded by the NIAID contract NIH NIAID contract #75N93022C00035 to the Center for Structural Biology of Infectious Diseases (CSBID) and by the Bruce D. and Nancy B. Varner Endowment Fund.
