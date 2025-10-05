## to run the script:
## cmod -x analyze_sequences.sh 
## ./analyze_sequences.sh ./resources
#!/bin/bash

# Configuration
SYSTEM=$(uname -s)
INPUT_DIR="${1:-.}"
OUTPUT_DIR="fasta_analysis_results_$(date +%Y%m%d_%H%M%S)"

log_message() {
    echo "[$(date '+%H:%M:%S')] $1"
}

file="${1?Error: No file specified}"

get_percent() {
    local part=$1
    local total=$2
    if [ $total -eq 0 ]; then
        percent=0
    else
        # System-specific calculation
        if [[ "$SYSTEM" == "Darwin" ]]; then
            percent=$(echo "scale=2; $part * 100 / $total" | bc)
       else
            percent=$((part * 100 / total))
        fi
    fi
    echo "$percent"
}

analyze_fasta() {
    local file="$1"
    # extract the filename or the last component of a path
    local basename=$(basename "$file" .fasta)
    
    # Create reformatted FASTA file (one line per sequence)
    awk '/^>/ {printf("\n%s\n",$0);next;} {printf("%s",$0);} END {printf("\n");}' "$file" | sed '/^$/d' > formatted.fasta

    # Now use this file for all operations
    seq_count=$(grep -c "^>" formatted.fasta)
    sequences=$(grep -v "^>" formatted.fasta)
    local formattedFile="formatted.fasta"

    # get sequences count
    seq_count=$(grep -c "^>" "$formattedFile")
    
    # get bases count
    total_bases_count=$(grep -v "^>" "$formattedFile" | tr -d '\n' | wc -c)

    # get G bases percentage
    g_count=$(grep -v "^>" "$formattedFile" | grep -o 'G' | wc -l)
    g_percent=$(get_percent "$g_count" "$total_bases_count")
    
    # get G bases percentage
    c_count=$(grep -v "^>" "$formattedFile" | grep -o 'C' | wc -l)
    c_percent=$(get_percent "$c_count" "$total_bases_count")

    # get GC combinations percentage
    gc_count=$(grep -v "^>" "$formattedFile" | tr -d '\n' | grep -o '[GC]' | wc -l)
    gc_percent=$(get_percent "$gc_count" "$total_bases_count")

    # get longest sequence length
    max_len=$(grep -v "^>" "$formattedFile" | awk '{print length}' | sort -n | tail -1)

    # get shortest sequence length
    min_len=$(grep -v "^>" "$formattedFile" | awk '{print length}' | sort -n | head -1)

    # Output results
    echo "$basename,$seq_count,$total_bases_count,$gc_percent,$c_percent,$g_percent,$min_len,$max_len"
}

# Main pipeline
log_message "Starting Genomic Data Analysis Pipeline"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Header for CSV
echo "Sample,SequencesCount,TotalBases,GCPercentage,CPercentage,GPercentage,MinLength,MaxLength" > "$OUTPUT_DIR/summary.csv"

# Process all FASTA files
for fasta in "$INPUT_DIR"/*.fasta; do
    if [ -f "$fasta" ]; then
        analyze_fasta "$fasta" >> "$OUTPUT_DIR/summary.csv"
    fi
done

log_message "Pipeline complete! Results location: $OUTPUT_DIR/"