#!/bin/bash
# Quality Control Pipeline for Sequencing Data
# to run the script:
# ./qc_pipeline.sh sample.fasta 

SYSTEM=$(uname -s)
echo "=== Quality Control Pipeline ==="
echo "Starting at: $(date)"
echo "System: $SYSTEM"
echo ""

# Function to check sequence quality
check_quality() {
    local file="$1"
    echo "Checking $file..."
    
    # Check for N bases (unknown nucleotides)
    n_count=$(grep -v "^>" "$file" | grep -o 'N' | wc -l)
    total_bases=$(grep -v "^>" "$file" | tr -d '\n' | wc -c)
    
    # Avoid division by zero
    if [ $total_bases -eq 0 ]; then
        n_percent=0
    else
        # System-specific calculation
        if [[ "$SYSTEM" == "Darwin" ]]; then
            n_percent=$(echo "scale=2; $n_count * 100 / $total_bases" | bc)
       else
            n_percent=$((n_count * 100 / total_bases))
        fi
    fi
    
    # Check sequence lengths
    min_len=$(grep -v "^>" "$file" | awk '{print length}' | sort -n | head -1)
    max_len=$(grep -v "^>" "$file" | awk '{print length}' | sort -n | tail -1)
    
    # Report
    echo "  N bases: $n_count ($n_percent%)"
    echo "  Length range: $min_len-$max_len bp"
    
    # Flag if quality issues
    if (( $(echo "$n_percent > 5" | bc -l 2>/dev/null || echo 0) )); then
        echo "  ⚠️  WARNING: High N content!"
    fi
    
    if [ $min_len -lt 50 ]; then
        echo "  ⚠️  WARNING: Short sequences found!"
    fi
    
    echo ""
}

# Process all FASTA files
for fasta in *.fasta; do
    if [ -f "$fasta" ]; then
        check_quality "$fasta"
    fi
done

echo "QC Pipeline completed at: $(date)"