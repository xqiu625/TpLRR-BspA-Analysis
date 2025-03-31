#!/usr/bin/env python3
"""
Revised TpLRR Finder

This script finds TpLRR patterns in a FASTA file using a more specific regex pattern
that accounts for amino acid substitutions in the conserved positions.
"""

import os
import sys
import re
import argparse
import logging
from datetime import datetime
from Bio import SeqIO

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("revised_tplrr_finder.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def find_lrr_patterns(file_name, log_interval=1000):
    """
    Find TpLRR patterns in the specified file using a more specific pattern
    that accounts for amino acid substitutions
    
    Args:
        file_name (str): Path to the input FASTA file
        log_interval (int): Interval for logging progress
        
    Returns:
        dict: Dictionary of TpLRR data by sequence ID
    """
    # More specific pattern allowing for amino acid substitutions in conserved positions
    lrr_pattern = re.compile("[CN].{2}[LVI].{2}[LVI].{1}[LVI].{3}[LVI].{2}[LVI].{3}AF")
    lrr_data = {}
    processed_count = 0
    
    logger.info(f"Searching for revised TpLRR patterns in {file_name}...")
    
    try:
        with open(file_name, 'rt') as f:
            for record in SeqIO.parse(f, 'fasta'):
                sequence = str(record.seq)
                pattern_matches = lrr_pattern.findall(sequence)
                
                lrr_data[record.id] = {
                    'count': len(pattern_matches),
                    'total_lrr_length': len(pattern_matches) * 21,  # 21 AA length for TpLRR
                    'total_length': len(sequence),
                    'patterns': " ".join(pattern_matches)
                }
                
                processed_count += 1
                if processed_count % log_interval == 0:
                    logger.info(f"Processed {processed_count} sequences")
    
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise
    
    logger.info(f"Completed search. Processed {processed_count} sequences.")
    
    # Count sequences with at least one pattern match
    matching_sequences = sum(1 for data in lrr_data.values() if data['count'] > 0)
    logger.info(f"Found {matching_sequences} sequences with TpLRR patterns.")
    
    return lrr_data

def save_results(lrr_data, output_file=None):
    """
    Save TpLRR pattern results to a file
    
    Args:
        lrr_data (dict): Dictionary of TpLRR data by sequence ID
        output_file (str, optional): Path to the output file.
                                    Defaults to "TpLRR_data_{timestamp}.txt".
    """
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"TpLRR_data_{timestamp}.txt"
    
    logger.info(f"Saving results to {output_file}...")
    
    try:
        with open(output_file, 'w') as f:
            f.write("Name\tCount\tTotal TpLRR Length\tTotal Sequence Length\tPatterns\n")
            for name, data in lrr_data.items():
                if data['patterns']:  # Only include sequences with patterns
                    f.write(f"{name}\t{data['count']}\t{data['total_lrr_length']}\t{data['total_length']}\t{data['patterns']}\n")
        
        logger.info(f"Results saved to {output_file}")
        return output_file
    
    except Exception as e:
        logger.error(f"Error saving results: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Find revised TpLRR patterns in a FASTA file")
    parser.add_argument("input_file", help="Path to the input FASTA file")
    parser.add_argument("--output", help="Name of the output file")
    parser.add_argument("--log-interval", type=int, default=1000, 
                        help="Interval for logging progress")
    
    args = parser.parse_args()
    
    try:
        # Find TpLRR patterns
        lrr_data = find_lrr_patterns(args.input_file, args.log_interval)
        
        # Save results
        save_results(lrr_data, args.output)
        
        logger.info("Process completed successfully.")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
