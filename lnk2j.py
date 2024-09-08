#!/usr/bin/env python3
import os
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from LnkParse3.lnk_file import LnkFile


def parse_lnk_file(file_path):
    with open(file_path, 'rb') as f:
        lnk = LnkFile(f)
        lnk_data = lnk.get_json()

        # Read file timestamps to the desired format with microseconds and UTC offset
        source_created = datetime.fromtimestamp(os.path.getctime(file_path), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z')
        source_modified = datetime.fromtimestamp(os.path.getmtime(file_path), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z')
        source_accessed = datetime.fromtimestamp(os.path.getatime(file_path), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z')

        # Insert a colon in the timezone offset to match LnkParse3 timestamps
        source_created = source_created[:-2] + ':' + source_created[-2:]
        source_modified = source_modified[:-2] + ':' + source_modified[-2:]
        source_accessed = source_accessed[:-2] + ':' + source_accessed[-2:]

        # Add a dictionary to the beginning and merge with LNK data
        output_data = {
            'SourceFile': str(file_path),
            'SourceCreated': source_created,
            'SourceModified': source_modified,
            'SourceAccessed': source_accessed,
            **lnk_data
        }
        return output_data

def traverse_directory(directory):
    results = []
    path = Path(directory)
    for file_path in path.rglob('*.lnk'):
        try:
            lnk_data = parse_lnk_file(file_path)
            results.append(lnk_data)
        except Exception:
            print(f"Error parsing {file_path}: {e}")
    return results

def process_input_path(input_path):
    results = []
    path = Path(input_path)
    if path.is_dir():
        results = traverse_directory(input_path)
    elif path.is_file() and path.suffix == '.lnk':
        try:
            lnk_data = parse_lnk_file(input_path)
            results.append(lnk_data)
        except Exception:
            print(f"Error parsing {input_path}: {e}")
    else:
        print(f"Invalid input path: {input_path}. Must be a directory or a .lnk file.")
    return results

def write_to_jsonl(results, output_file=None):
    if output_file:
        with open(output_file, 'w') as f:
            for result in results:
                f.write(json.dumps(result, default=str) + '\n')
    else:
        for result in results:
            print(json.dumps(result, default=str))

def write_to_json(results, output_file=None):
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, default=str, indent=4)
    else:
        print(json.dumps(results, default=str, indent=4))

def main():
    parser = argparse.ArgumentParser(description="Parse LNK files from a directory or a single file and output as json or jsonl.")
    parser.add_argument("-i", "--input", required=True, help="Path to directory or LNK file.")
    parser.add_argument("-f", "--format", choices=['json', 'jsonl'], help="Output format.")
    parser.add_argument("-o", "--output", help="Output file name.")
    args = parser.parse_args()

    input_path = args.input
    output_format = args.format
    output_file = args.output

    results = process_input_path(input_path)

    if output_format == 'jsonl':
        write_to_jsonl(results, output_file)
    else:
        write_to_json(results, output_file)

if __name__ == "__main__":
    main()
