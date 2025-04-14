#!/bin/bash

# Get the directory of the current script
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Get the parent directory of the script directory
BASE_DIR="$(dirname "$TEST_DIR")"

# Initialize counters
total=0
valid=0

SCHEMA="$TEST_DIR/tei_all.rng"

# Find all XML files and count total for the progress bar
file_list=($(find "$BASE_DIR" -path "$BASE_DIR/include" -prune -o -name 'S155.xml' -print))
total_files=${#file_list[@]}
current=0

# Function to print the progress bar
print_progress() {
    progress=$(( 100 * current / total_files ))
    bar_length=50
    filled=$(( progress * bar_length / 100 ))
    empty=$(( bar_length - filled ))

    # Ensure filled and empty are non-negative
    [ $filled -lt 0 ] && filled=0
    [ $empty -lt 0 ] && empty=0

    # Print the progress bar
    printf "\r["
    for ((i = 0; i < filled; i++)); do printf "#"; done
    for ((i = 0; i < empty; i++)); do printf "-"; done
    printf "] %d%% (%d/%d)" "$progress" "$current" "$total_files"
}

# Loop over XML files
for file in "${file_list[@]}"; do
    if [ -f "$file" ]; then
        ((total++))
        ((current++))

        # Print progress bar
        print_progress

        # Use the TEI schema to validate the XML file
        error_message=$(xmllint --xinclude "$file" 2>&1 | xmllint --noout --relaxng "$SCHEMA" - 2>&1)
        if [ $? -eq 0 ]; then
            ((valid++))
        else
            # Move to a new line for errors without disrupting the progress bar
            echo -e "\n$file: invalid"
            echo "$error_message"
            echo "----------------------------------------"
        fi
    fi
done

# Print final progress bar and move to a new line
print_progress
echo

# Calculate and print the percentage of valid files
if [ $total -eq 0 ]; then
    echo "No XML files found."
else
    percentage=$((100 * valid / total))
    echo "Valid XML files: $valid/$total ($percentage%)"
fi

# Set badge color based on percentage
if [ $percentage -ge 99 ]; then
    color="#4c1"  # green
elif [ $percentage -ge 90 ]; then
    color="#dfb317"  # yellow
else
    color="#e05d44"  # red
fi

# Define label and message
label="TEI Valid"
message="${percentage}%"

# Calculate dynamic widths
label_width=70
message_width=$(( ${#message} * 7 + 20 )) # dynamic width based on text length
total_width=$((label_width + message_width))

# Generate the badge SVG
cat <<EOF > "$TEST_DIR/xml_validation_badge.svg"
<svg xmlns="http://www.w3.org/2000/svg" width="$total_width" height="20" role="img" aria-label="$label: $message">
  <title>$label: $message</title>
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r">
    <rect width="$total_width" height="20" rx="3" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#r)">
    <rect width="$label_width" height="20" fill="#555"/>
    <rect x="$label_width" width="$message_width" height="20" fill="$color"/>
    <rect width="$total_width" height="20" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" text-rendering="geometricPrecision" font-size="11">
    <text x="$((label_width / 2))" y="14">$label</text>
    <text x="$((label_width + message_width / 2))" y="14">$message</text>
  </g>
</svg>
EOF
