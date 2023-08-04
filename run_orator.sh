#!/bin/bash

echo 'Hello!'
# Check if an argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <input_id_list>"
    exit 1
fi

# Loop through the provided input IDs
for input_id in "$@"; do
    echo "Running for input ID: $input_id"
    python orator.py "$input_id" > "outputs/${input_id}.oration.md"
    echo "Done"
done
