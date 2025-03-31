#!/bin/bash
#
# Script to run LRR pattern analyses for multiple patterns
#

set -e

# Default values
BUCKET_NAME="uniref50_lrr"
FILE_NAME="uniref50.fasta.gz"
MAX_SEQUENCES=""
LOCAL_FLAG=""
UPLOAD_FLAG=""

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
    --max-sequences)
      MAX_SEQUENCES="--max-sequences $2"
      shift
      shift
      ;;
    --local)
      LOCAL_FLAG="--local"
      shift
      ;;
    --no-upload)
      UPLOAD_FLAG="--no-upload"
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Activate conda environment if available
if command -v conda &> /dev/null; then
    if conda env list | grep -q "lrr_finder"; then
        echo "Activating conda environment: lrr_finder"
        source "$(conda info --base)/etc/profile.d/conda.sh"
        conda activate lrr_finder
    fi
fi

# Define patterns to analyze
PATTERNS=("TpLRR" "RI-like" "SDS22-like" "Cysteine-containing" "Bacterial" "Typical" "Plant-specific")

# Function to run a single pattern analysis
run_pattern_analysis() {
    pattern=$1
    session_name="${pattern}_analysis"
    
    # Create tmux session
    echo "Creating session for $pattern pattern analysis..."
    ./scripts/tmux_management.sh create "$session_name"
    
    # Run analysis in the session
    tmux send-keys -t "$session_name" "python src/tplrr_finder.py $BUCKET_NAME $FILE_NAME --pattern \"$pattern\" $MAX_SEQUENCES $LOCAL_FLAG $UPLOAD_FLAG" C-m
    
    echo "Started analysis for $pattern pattern in session: $session_name"
    echo "Use './scripts/tmux_management.sh attach $session_name' to check progress"
    echo
}

# Run analyses for all patterns
for pattern in "${PATTERNS[@]}"; do
    run_pattern_analysis "$pattern"
    # Sleep briefly to avoid rate limiting
    sleep 2
done

echo "All analyses started. Use './scripts/tmux_management.sh list' to see all sessions."
