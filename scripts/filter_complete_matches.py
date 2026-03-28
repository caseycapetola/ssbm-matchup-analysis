#!/usr/bin/env python3
"""Filter out incomplete matches from extracted match data."""
import argparse
import json
from pathlib import Path

try:
    import ijson
    HAS_IJSON = True
except ImportError:
    HAS_IJSON = False


def filter_complete_matches_streaming(input_file: str, output_file: str) -> dict:
    """
    Filter matches to keep only those with gameComplete=True.
    
    Args:
        input_file: Path to input JSON file
        output_file: Path to output JSON file
    
    Returns:
        dict with statistics about the filtering
    """
    if not HAS_IJSON:
        raise ImportError("ijson is required for streaming. Install with: pip install ijson")
    
    total = 0
    complete = 0
    
    with open(input_file, 'rb') as infile, open(output_file, 'w') as outfile:
        outfile.write('[\n')
        first = True
        
        for match in ijson.items(infile, 'item'):
            total += 1
            if match.get('gameComplete') is True:
                if not first:
                    outfile.write(',\n')
                json.dump(match, outfile, indent=2)
                first = False
                complete += 1
        
        outfile.write('\n]')
    
    return {
        'total': total,
        'complete': complete,
        'incomplete': total - complete,
        'output_file': output_file
    }


def main():
    parser = argparse.ArgumentParser(description='Filter incomplete matches (streaming)')
    parser.add_argument('input', help='Input JSON file')
    parser.add_argument('-o', '--output', help='Output JSON file (default: <input>_complete.json)')
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = args.output or input_path.stem + '_complete.json'
    
    stats = filter_complete_matches_streaming(args.input, output_path)
    
    print(f"Total matches: {stats['total']}")
    print(f"Complete matches: {stats['complete']}")
    print(f"Incomplete (excluded): {stats['incomplete']}")
    print(f"Saved to: {stats['output_file']}")


if __name__ == '__main__':
    main()
