#!/usr/bin/env python3
"""
TpLRR Finder

Find TpLRR patterns in the UniRef50 database and analyze their distribution.
"""

import os
import sys
import re
import gzip
import argparse
import logging
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

from Bio import SeqIO
from google.cloud import storage

# Import from parent directory
current_dir = Path(__file__).parent.absolute()
sys.path.append(str(current_dir))
from lrr_patterns import get_compiled_pattern

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tplrr_finder.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def download_file(bucket_name, file_name, local_path=None):
    """
    Download a file from Google Cloud Storage
    
    Args:
        bucket_name (str): Name of the bucket
        file_name (str): Name of the file to download
        local_path (str, optional): Local path to save the file. 
                                   Defaults to file_name.
                                   
    Returns:
        str: Path to the downloaded file
    """
    if local_path is None:
        local_path = file_name
    
    logger.info(f"Downloading {file_name} from {bucket_name}...")
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.download_to_filename(local_path)
        logger.info(f"Downloaded {file_name} to {local_path}")
        return local_path
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise

def find_lrr_patterns(file_name, pattern_name="TpLRR", max_sequences=None):
    """
    Find LRR patterns in the specified file
    
    Args:
        file_name (str): Path to the input file (gzipped FASTA)
        pattern_name (str): Name of the pattern to search for
        max_sequences (int, optional): Maximum number of sequences to process
        
    Returns:
        dict: Dictionary of LRR data by sequence ID
    """
    pattern, pattern_length = get_compiled_pattern(pattern_name)
    lrr_data = {}
    processed_count = 0
    
    logger.info(f"Searching for {pattern_name} patterns in {file_name}...")
    
    # Check if file exists and is readable
    if not os.path.isfile(file_name):
        raise FileNotFoundError(f"File not found: {file_name}")
    
    try:
        with gzip.open(file_name, 'rt') as f:
            for record in tqdm(SeqIO.parse(f, 'fasta'), desc="Processing sequences", unit="seq"):
                sequence = str(record.seq)
                pattern_matches = pattern.findall(sequence)
                
                if pattern_matches:
                    lrr_data[record.id] = {
                        'count': len(pattern_matches),
                        'total_lrr_length': len(pattern_matches) * pattern_length,
                        'total_length': len(sequence),
                        'patterns': " ".join(pattern_matches)
                    }
                
                processed_count += 1
                if processed_count % 10000 == 0:
                    logger.info(f"Processed {processed_count} sequences, found {len(lrr_data)} with patterns")
                
                if max_sequences and processed_count >= max_sequences:
                    logger.info(f"Reached maximum sequence count ({max_sequences})")
                    break
    
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise
    
    logger.info(f"Completed search. Processed {processed_count} sequences.")
    logger.info(f"Found {len(lrr_data)} sequences with {pattern_name} patterns.")
    
    return lrr_data

def save_results(lrr_data, pattern_name, output_file=None):
    """
    Save LRR pattern results to a file
    
    Args:
        lrr_data (dict): Dictionary of LRR data by sequence ID
        pattern_name (str): Name of the pattern that was searched
        output_file (str, optional): Path to the output file.
                                     Defaults to "{pattern_name}_data.txt".
    """
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{pattern_name}_data_{timestamp}.txt"
    
    logger.info(f"Saving results to {output_file}...")
    
    try:
        with open(output_file, 'w') as f:
            f.write(f"Name\tCount\tTotal {pattern_name} Length\tTotal Sequence Length\tPatterns\n")
            for name, data in lrr_data.items():
                f.write(f"{name}\t{data['count']}\t{data['total_lrr_length']}\t{data['total_length']}\t{data['patterns']}\n")
        
        logger.info(f"Results saved to {output_file}")
        return output_file
    
    except Exception as e:
        logger.error(f"Error saving results: {e}")
        raise

def upload_to_bucket(bucket_name, file_name):
    """
    Upload a file to Google Cloud Storage
    
    Args:
        bucket_name (str): Name of the bucket
        file_name (str): Name of the file to upload
    """
    logger.info(f"Uploading {file_name} to {bucket_name}...")
    
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_name)
        logger.info(f"Uploaded {file_name} to {bucket_name}")
    
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Find TpLRR patterns in UniRef50 database")
    parser.add_argument("bucket_name", help="Name of the Google Cloud Storage bucket")
    parser.add_argument("file_name", help="Name of the file in the bucket")
    parser.add_argument("--pattern", default="TpLRR", help="Pattern to search for")
    parser.add_argument("--max-sequences", type=int, help="Maximum number of sequences to process")
    parser.add_argument("--local", action="store_true", help="Use local file instead of downloading from bucket")
    parser.add_argument("--output", help="Name of the output file")
    parser.add_argument("--no-upload", action="store_true", help="Do not upload result to bucket")
    
    args = parser.parse_args()
    
    try:
        # Get input file
        if not args.local:
            fasta_file = download_file(args.bucket_name, args.file_name)
        else:
            fasta_file = args.file_name
            if not os.path.isfile(fasta_file):
                raise FileNotFoundError(f"Local file not found: {fasta_file}")
        
        # Find LRR patterns
        lrr_data = find_lrr_patterns(fasta_file, args.pattern, args.max_sequences)
        
        # Save results
        output_file = save_results(lrr_data, args.pattern, args.output)
        
        # Upload results to bucket
        if not args.no_upload:
            upload_to_bucket(args.bucket_name, output_file)
        
        logger.info("Process completed successfully.")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
