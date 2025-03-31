#!/bin/bash
#
# Script to download UniRef50 database and upload to cloud storage
#

set -e

# Default bucket name
BUCKET_NAME="uniref50_lrr"
UNIPROT_URL="ftp://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref50/uniref50.fasta.gz"
OUTPUT_FILE="uniref50.fasta.gz"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --bucket)
      BUCKET_NAME="$2"
      shift
      shift
      ;;
    --output)
      OUTPUT_FILE="$2"
      shift
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

echo "Downloading UniRef50 database..."
echo "This may take several hours. The file is approximately 12GB."

# Download with progress tracking
wget "$UNIPROT_URL" -O "$OUTPUT_FILE" --progress=dot:giga

echo "Download complete."

# Upload to Google Cloud Storage if gsutil is available
if command -v gsutil &> /dev/null; then
  echo "Uploading to Google Cloud Storage bucket: $BUCKET_NAME"
  gsutil cp "$OUTPUT_FILE" "gs://$BUCKET_NAME/$OUTPUT_FILE"
  echo "Upload complete."
  
  # Optionally remove local file
  read -p "Remove local file? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm "$OUTPUT_FILE"
    echo "Local file removed."
  fi
else
  echo "gsutil not found. Skipping upload to Google Cloud Storage."
  echo "File saved locally as: $OUTPUT_FILE"
fi

echo "Process completed successfully."
