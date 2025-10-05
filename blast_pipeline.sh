#!/bin/bash
# BLAST Pipeline for Multiple Queries

# Configuration
QUERY_FILE="$1"
DATABASE="$2"
OUTPUT_DIR="blast_results_$(date +%Y%m%d)"
SYSTEM=$(uname -s)

echo "Running on $SYSTEM system"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Split multi-sequence FASTA into individual files
awk '/^>/ {if (seq) print seq; printf "%s\n", $0; seq=""; next} {seq=seq$0} END {if (seq) print seq}' "$QUERY_FILE" | \
while read -r header; do
    read -r sequence
    seq_id=$(echo "$header" | cut -d' ' -f1 | sed 's/>//')
    echo "$header" > "$OUTPUT_DIR/${seq_id}.fasta"
    echo "$sequence" >> "$OUTPUT_DIR/${seq_id}.fasta"
    
    echo "Processing $seq_id..."
    if [[ "$SYSTEM" == "Darwin" ]]; then
        blastn -query "$OUTPUT_DIR/${seq_id}.fasta" -db "$DATABASE" -out "$OUTPUT_DIR/${seq_id}_blast.txt" -outfmt 6
    else
        blastn -query "$OUTPUT_DIR/${seq_id}.fasta" -db "$DATABASE" -out "$OUTPUT_DIR/${seq_id}_blast.txt" -outfmt 6
    fi
done

# Combine all results
cat "$OUTPUT_DIR"/*_blast.txt > "$OUTPUT_DIR/all_results.txt" 2>/dev/null || echo "No BLAST results found (BLAST not installed)"

echo "Pipeline complete! Results in $OUTPUT_DIR/"
echo "To install BLAST:"
echo "  Mac: brew install blast"
echo "  Linux: sudo apt-get install ncbi-blast+"