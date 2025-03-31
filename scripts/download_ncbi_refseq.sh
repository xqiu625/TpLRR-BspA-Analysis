#!/bin/bash
#
# Script to download NCBI RefSeq protein data files
#

set -e

# Default values
REFSEQ_CATEGORY="viral"  # Options: viral, bacteria, fungi, plant, vertebrate_mammalian, etc.
OUTPUT_DIR="data/ncbi_refseq"
EXTENSION="protein.faa.gz"  # Only download protein FASTA files

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --category)
      REFSEQ_CATEGORY="$2"
      shift
      shift
      ;;
    --output)
      OUTPUT_DIR="$2"
      shift
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--category CATEGORY] [--output OUTPUT_DIR]"
      echo "  CATEGORY: RefSeq category (e.g., viral, bacteria, fungi)"
      echo "  OUTPUT_DIR: Directory to save downloaded files"
      exit 1
      ;;
  esac
done

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Map of available RefSeq categories
declare -A REFSEQ_CATEGORIES=(
  ["viral"]="viral"
  ["bacteria"]="bacteria"
  ["fungi"]="fungi"
  ["invertebrate"]="invertebrate"
  ["plant"]="plant"
  ["protozoa"]="protozoa"
  ["vertebrate_mammalian"]="vertebrate_mammalian"
  ["vertebrate_other"]="vertebrate_other"
)

# Check if the specified category is valid
if [[ ! ${REFSEQ_CATEGORIES[$REFSEQ_CATEGORY]} ]]; then
  echo "Error: Invalid RefSeq category: $REFSEQ_CATEGORY"
  echo "Available categories:"
  for category in "${!REFSEQ_CATEGORIES[@]}"; do
    echo "  $category"
  done
  exit 1
fi

REFSEQ_URL="ftp://ftp.ncbi.nih.gov/refseq/release/${REFSEQ_CATEGORIES[$REFSEQ_CATEGORY]}/"

echo "Downloading NCBI RefSeq $REFSEQ_CATEGORY protein FASTA files..."
echo "Output directory: $OUTPUT_DIR"
echo "URL: $REFSEQ_URL"

cd "$OUTPUT_DIR"

# Use wget to download files recursively
# -r: recursive download
# -nH: don't create host directory
# --cut-dirs=5: remove 5 levels of directories from the path
# -A: only download files matching the pattern
# -np: don't ascend to parent directory
wget -r -nH --cut-dirs=5 -np -A "*.$EXTENSION" "$REFSEQ_URL"

echo "Download complete. Files saved to $OUTPUT_DIR"
