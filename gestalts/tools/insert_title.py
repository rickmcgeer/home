'''
Add the title and timestamp of a conversation to the conversation and save it in /home/tmp/conversation.json
'''
import json
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print('Usage: python insert_title.py <filename>')
    exit(1)

filepath = Path(sys.argv[1])
full_title = filepath.stem  # e.g., AI_Programming_II_2025-07-10T20:21:09
parts = full_title.rsplit('_', 1)
if len(parts) != 2:
    print(f'Error: filename must be of the form <title>_yyyy-mm-ddTHH:MM:SS.json, not {filepath.name}')
    exit(6)

title = parts[0].replace('_', ' ')
timestamp = parts[1]

new_conversation = {
    "title": title,
    "timestamp": timestamp
}

output_file = '/workspaces/home/tmp/conversation.json'

try:
    with open(filepath, 'r') as f:
        conversation = json.load(f)
        new_conversation["messages"] = conversation
except FileNotFoundError:
    print(f'file {sys.argv[1]} not found')
    exit(2)
except json.JSONDecodeError as e:
    print(f'Error {e} in decoding {filepath}')
    exit(3)

try:
    with open(output_file, 'w') as f:
        json.dump(new_conversation, f, indent=2)
except Exception as e:
    print(f'Error {e} on writing {output_file}')
    exit(4)

print(f'Successfully wrote {output_file}')
