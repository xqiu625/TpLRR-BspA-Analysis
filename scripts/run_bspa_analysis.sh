#!/bin/bash
#
# Script to run BspA LRR pattern analysis
#

set -e

# Activate conda environment
if command -v conda &> /dev/null; then
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate llr_ml  # Update this to your environment name
    echo "Activated conda environment: llr_ml"
else
    echo "Warning: conda not found. Make sure required packages are available."
fi

# Set default values
BUCKET_NAME="bspa_lrr"
FILE_NAME="bspaLRR.fasta"
OUTPUT_FILE="TpLRR_data.txt"
USE_LOCAL=""
NO_UPLOAD=""
CUSTOM_PATTERN=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --bucket)
      BUCKET_NAME="$2"
      shift
      shift
      ;;
    --file)
      FILE_NAME="$2"
      shift
      shift
      ;;
    --output)
      OUTPUT_FILE="$2"
      shift
      shift
      ;;
    --pattern)
      CUSTOM_PATTERN="--pattern $2"
      shift
      shift
      ;;
    --local)
      USE_LOCAL="--local"
      shift
      ;;
    --no-upload)
      NO_UPLOAD="--no-upload"
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--bucket BUCKET_NAME] [--file FILE_NAME] [--output OUTPUT_FILE] [--pattern PATTERN] [--local] [--no-upload]"
      exit 1
      ;;
  esac
done

echo "Running BspA LRR pattern analysis..."
echo "Bucket: $BUCKET_NAME"
echo "File: $FILE_NAME"
echo "Output: $OUTPUT_FILE"
if [[ -n "$CUSTOM_PATTERN" ]]; then
  echo "Using custom pattern"
fi
if [[ -n "$USE_LOCAL" ]]; then
  echo "Using local file"
fi
if [[ -n "$NO_UPLOAD" ]]; then
  echo "Not uploading results"
fi

# Run the analysis
python ../src/bspa_lrr_analyzer.py "$BUCKET_NAME" "$FILE_NAME" \
  --output "$OUTPUT_FILE" $CUSTOM_PATTERN $USE_LOCAL $NO_UPLOAD

echo "Analysis complete."
