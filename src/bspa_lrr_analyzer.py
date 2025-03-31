#!/usr/bin/env python3
"""
BspA LRR Pattern Analyzer

This script analyzes FASTA sequences for TpLRR patterns specifically in BspA proteins.
It can download files from Google Cloud Storage, analyze patterns, and upload results.
"""

import os
import sys
import re
import argparse
import logging
from Bio import SeqIO
from google.cloud import storage

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bspa_lrr_analyzer.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def download_file(bucket_name, file_name, local_path=None):
    """
    Download a file from Google Cloud Storage
    
    Args:
        bucket_name (str): Name of the GCS bucket
        file_name (str): Name of the file to download
        local_path (str, optional): Local path to save the file
        
    Returns:
        str: Path to the downloaded file
    """
    if local_path is None:
        local_path = file_name
    
    logger.info(f"Downloading {file_name} from bucket {bucket_name}")
    
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

def find_lrr_patterns(file_name, pattern_str=None):
    """
    Find LRR patterns in the specified FASTA file
    
    Args:
        file_name (str): Path to the input FASTA file
        pattern_str (str, optional): Custom regex pattern to use
        
    Returns:
        dict: Dictionary of LRR data by sequence ID
    """
    # Default TpLRR pattern
    if pattern_str is None:
        pattern_str = r"C.{2}L.{2}I.{1}L.{3}L.{2}I.{3}AF"
    
    lrr_pattern = re.compile(pattern_str)
    lrr_data = {}
    pattern_length = 21  # Length of TpLRR pattern
    
    logger.info(f"Analyzing file {file_name} for pattern: {pattern_str}")
    
    try:
        with open(file_name, 'r') as f:
            for record in SeqIO.parse(f, 'fasta'):
                sequence = str(record.seq)
                pattern_matches = lrr_pattern.findall(sequence)
                
                lrr_data[record.id] = {
                    'count': len(pattern_matches),
                    'total_lrr_length': len(pattern_matches) * pattern_length,
                    'total_length': len(sequence),
                    'patterns': " ".join(pattern_matches)
                }
        
        # Count sequences with at least one pattern match
        matches = sum(1 for data in lrr_data.values() if data['count'] > 0)
        logger.info(f"Analysis complete. Found {matches} sequences with matching patterns")
        return lrr_data
    
    except Exception as e:
        logger.error(f"Error analyzing file: {e}")
        raise

def save_results(lrr_data, output_file="TpLRR_data.txt"):
    """
    Save LRR pattern analysis results to a file
    
    Args:
        lrr_data (dict): Dictionary of LRR data by sequence ID
        output_file (str): Path to the output file
        
    Returns:
        str: Path to the output file
    """
    logger.info(f"Saving results to {output_file}")
    
    try:
        with open(output_file, 'w') as f:
            f.write("Name\tCount\tTotal TpLRR Length\tTotal Sequence Length\tPatterns\n")
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
        bucket_name (str): Name of the GCS bucket
        file_name (str): Name of the file to upload
    """
    logger.info(f"Uploading {file_name} to bucket {bucket_name}")
    
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_name)
        logger.info(f"Uploaded {file_name} to bucket {bucket_name}")
    
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Analyze BspA proteins for TpLRR patterns")
    parser.add_argument("bucket_name", help="Name of the Google Cloud Storage bucket")
    parser.add_argument("file_name", help="Name of the FASTA file to analyze")
    parser.add_argument("--output", default="TpLRR_data.txt", help="Name of the output file")
    parser.add_argument("--pattern", help="Custom regex pattern to search for")
    parser.add_argument("--local", action="store_true", help="Use local file instead of downloading from bucket")
    parser.add_argument("--no-upload", action="store_true", help="Don't upload results to bucket")
    
    args = parser.parse_args()
    
    try:
        # Get the FASTA file
        if not args.local:
            fasta_file = download_file(args.bucket_name, args.file_name)
        else:
            fasta_file = args.file_name
            logger.info(f"Using local file: {fasta_file}")
        
        # Find LRR patterns
        lrr_data = find_lrr_patterns(fasta_file, args.pattern)
        
        # Save results
        output_file = save_results(lrr_data, args.output)
        
        # Upload results if requested
        if not args.no_upload:
            upload_to_bucket(args.bucket_name, output_file)
            logger.info(f"TpLRR protein pattern data has been saved to {output_file} in the {args.bucket_name} bucket")
        else:
            logger.info(f"TpLRR protein pattern data has been saved to {output_file}")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
