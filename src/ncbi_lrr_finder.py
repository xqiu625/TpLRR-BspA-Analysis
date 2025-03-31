#!/usr/bin/env python3
"""
NCBI LRR Pattern Finder

This script processes multiple compressed FASTA files from NCBI RefSeq,
finding different types of LRR patterns in each file.
"""

import os
import sys
import re
import gzip
import argparse
import logging
from datetime import datetime
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from Bio import SeqIO
from tqdm import tqdm

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ncbi_lrr_finder.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Define LRR patterns
LRR_PATTERNS = {
    "TpLRR": {
        "pattern": r"(?:C|N).{2}L.{2}I.{1}L.{3}L.{2}I.{3}AF",
        "length": 21,
        "description": "TpLRR pattern (21 AA)"
    },
    "RI-like": {
        "pattern": r".{3}L.{2}L.{1}L.{2}[NC].{1}L.{3}G[GAIVLMFPWC].{2}L.{2}[GAIVLMFPWC]L.{2}",
        "length": 28,
        "description": "RI-like pattern (28 AA)"
    },
    "SDS22-like": {
        "pattern": r"L.{2}L.{2}L.{1}L.{2}N.{1}I.{2}I.{2}L.{2}",
        "length": 22,
        "description": "SDS22-like pattern (22 AA)"
    },
    "Cysteine-containing": {
        "pattern": r"C.{2}L.{2}L.{1}L.{2}C.{2}ITD.{2}[GAIVLMFPWC].{2}LA.{2}",
        "length": 22,
        "description": "Cysteine-containing pattern (22 AA)"
    },
    "Bacterial": {
        "pattern": r"P.{2}L.{2}L.{1}V.{2}N.{1}L.{2}LP.{1}L",
        "length": 20,
        "description": "Bacterial pattern (20 AA)"
    },
    "Typical": {
        "pattern": r"L.{2}L.{2}L.{1}L.{2}N.{1}L.{2}LP.{2}[GAIVLMFPWC]F.{2}",
        "length": 24,
        "description": "Typical LRR pattern"
    },
    "Plant-specific": {
        "pattern": r"L.{2}L.{2}L.{1}L.{2}N.{1}L.{3}IP.{2}LG.{1}",
        "length": 22,
        "description": "Plant-specific pattern (22 AA)"
    }
}

def get_faa_gz_files(folder):
    """
    Get a list of all .faa.gz files in the specified folder
    
    Args:
        folder (str): Path to the folder containing .faa.gz files
        
    Returns:
        list: List of paths to .faa.gz files
    """
    folder_path = Path(folder)
    return [str(f) for f in folder_path.glob("**/*.protein.faa.gz") if f.is_file()]

def find_lrr_patterns(file_name, pattern_name="RI-like", log_interval=1000):
    """
    Find LRR patterns in the specified file
    
    Args:
        file_name (str): Path to the input file (gzipped FASTA)
        pattern_name (str): Name of the pattern to search for
        log_interval (int): Interval for logging progress
        
    Returns:
        dict: Dictionary of LRR data by sequence ID
    """
    if pattern_name not in LRR_PATTERNS:
        raise ValueError(f"Unknown pattern name: {pattern_name}")
    
    pattern_info = LRR_PATTERNS[pattern_name]
    lrr_pattern = re.compile(pattern_info["pattern"])
    pattern_length = pattern_info["length"]
    
    lrr_data = {}
    processed_count = 0
    match_count = 0
    
    logger.info(f"Searching for {pattern_name} patterns in {file_name}...")
    
    try:
        with gzip.open(file_name, 'rt') as f:
            for record in SeqIO.parse(f, 'fasta'):
                sequence = str(record.seq)
                pattern_matches = lrr_pattern.findall(sequence)
                
                if pattern_matches:
                    lrr_data[record.id] = {
                        'count': len(pattern_matches),
                        'total_lrr_length': len(pattern_matches) * pattern_length,
                        'total_length': len(sequence),
                        'patterns': " ".join(pattern_matches)
                    }
                    match_count += 1
                
                processed_count += 1
                if processed_count % log_interval == 0:
                    logger.info(f"Processed {processed_count} sequences, found {match_count} with patterns")
    
    except Exception as e:
        logger.error(f"Error processing file {file_name}: {e}")
        raise
    
    logger.info(f"Completed search in {file_name}. Processed {processed_count} sequences.")
    logger.info(f"Found {match_count} sequences with {pattern_name} patterns.")
    
    return lrr_data

def save_results(lrr_data, file_name, pattern_name, output_dir=None):
    """
    Save LRR pattern results to a file
    
    Args:
        lrr_data (dict): Dictionary of LRR data by sequence ID
        file_name (str): Name of the input file (used to generate output file name)
        pattern_name (str): Name of the pattern that was searched
        output_dir (str, optional): Directory to save the output file
                                   
    Returns:
        str: Path to the output file
    """
    base_name = os.path.basename(file_name).replace('.faa.gz', '')
    base_name = base_name.replace('.protein', '')
    
    if output_dir:
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_file = os.path.join(output_dir, f"{base_name}_{pattern_name}.txt")
    else:
        output_file = f"{base_name}_{pattern_name}.txt"
    
    logger.info(f"Saving results to {output_file}...")
    
    try:
        with open(output_file, 'w') as f:
            f.write(f"Name\tCount\tTotal {pattern_name} Length\tTotal Sequence Length\tPatterns\n")
            for name, data in lrr_data.items():
                if data['patterns']:
                    f.write(f"{name}\t{data['count']}\t{data['total_lrr_length']}\t{data['total_length']}\t{data['patterns']}\n")
        
        logger.info(f"Results saved to {output_file}")
        return output_file
    
    except Exception as e:
        logger.error(f"Error saving results to {output_file}: {e}")
        raise

def process_file(file_name, pattern_name, output_dir=None, log_interval=1000):
    """
    Process a single file for LRR patterns
    
    Args:
        file_name (str): Path to the input file
        pattern_name (str): Name of the pattern to search for
        output_dir (str, optional): Directory to save the output file
        log_interval (int): Interval for logging progress
        
    Returns:
        str: Path to the output file
    """
    try:
        lrr_data = find_lrr_patterns(file_name, pattern_name, log_interval)
        output_file = save_results(lrr_data, file_name, pattern_name, output_dir)
        return output_file
    except Exception as e:
        logger.error(f"Error processing file {file_name}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Find LRR patterns in NCBI RefSeq FASTA files")
    parser.add_argument("folder", help="Path to the folder containing NCBI RefSeq FASTA files")
    parser.add_argument("--pattern", default="RI-like", choices=LRR_PATTERNS.keys(),
                        help="Pattern to search for")
    parser.add_argument("--output-dir", help="Directory to save the output files")
    parser.add_argument("--log-interval", type=int, default=1000, 
                        help="Interval for logging progress")
    parser.add_argument("--parallel", action="store_true", 
                        help="Process files in parallel")
    parser.add_argument("--max-workers", type=int, default=os.cpu_count(), 
                        help="Maximum number of worker processes to use")
    
    args = parser.parse_args()
    
    try:
        # Get list of input files
        faa_gz_files = get_faa_gz_files(args.folder)
        
        if not faa_gz_files:
            logger.error(f"No .protein.faa.gz files found in {args.folder}")
            sys.exit(1)
        
        logger.info(f"Found {len(faa_gz_files)} .protein.faa.gz files")
        
        if args.parallel:
            logger.info(f"Processing files in parallel with {args.max_workers} workers")
            with ProcessPoolExecutor(max_workers=args.max_workers) as executor:
                futures = {
                    executor.submit(
                        process_file, 
                        file_name, 
                        args.pattern,
                        args.output_dir,
                        args.log_interval
                    ): file_name for file_name in faa_gz_files
                }
                
                for future in tqdm(futures, desc="Processing files"):
                    file_name = futures[future]
                    try:
                        output_file = future.result()
                        if output_file:
                            logger.info(f"Completed processing {file_name} -> {output_file}")
                    except Exception as e:
                        logger.error(f"Error processing {file_name}: {e}")
        else:
            logger.info("Processing files sequentially")
            for file_name in tqdm(faa_gz_files, desc="Processing files"):
                output_file = process_file(
                    file_name, 
                    args.pattern,
                    args.output_dir,
                    args.log_interval
                )
                if output_file:
                    logger.info(f"Completed processing {file_name} -> {output_file}")
        
        logger.info("All files processed successfully")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
