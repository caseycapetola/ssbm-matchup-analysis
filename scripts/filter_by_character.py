#!/usr/bin/env python3
"""Filter matches by character matchup."""

import argparse
import json
from pathlib import Path

try:
    import ijson
    HAS_IJSON = True
except ImportError:
    HAS_IJSON = False


def filter_by_characters_streaming(input_file: str, char1: str, char2: str, output_file: str) -> dict:
    """
    Filter matches to keep only those with specified character matchup.
    Order of characters doesn't matter.
    
    Args:
        input_file: Path to input JSON file
        char1: First character name (e.g., FOX)
        char2: Second character name (e.g., MARTH)
        output_file: Path to output JSON file
    
    Returns:
        dict with statistics about the filtering
    """
    if not HAS_IJSON:
        raise ImportError("ijson is required for streaming. Install with: pip install ijson")
    
    char1 = char1.upper()
    char2 = char2.upper()
    target_matchup = {char1, char2}
    
    total = 0
    matched = 0
    
    with open(input_file, 'rb') as infile, open(output_file, 'w') as outfile:
        outfile.write('[\n')
        first = True
        
        for match in ijson.items(infile, 'item'):
            total += 1
            players = match.get('players', [])
            
            if len(players) == 2:
                match_chars = {
                    (players[0].get('character') or '').upper(),
                    (players[1].get('character') or '').upper()
                }
                if match_chars == target_matchup:
                    if not first:
                        outfile.write(',\n')
                    json.dump(match, outfile, indent=2)
                    first = False
                    matched += 1
        
        outfile.write('\n]')
    
    return {
        'total': total,
        'matched': matched,
        'filtered_out': total - matched,
        'matchup': f'{char1} vs {char2}',
        'output_file': output_file
    }


def main():
    parser = argparse.ArgumentParser(description='Filter matches by character matchup (streaming)')
    parser.add_argument('input', help='Input JSON file')
    parser.add_argument('char1', help='First character (e.g., FOX)')
    parser.add_argument('char2', help='Second character (e.g., MARTH)')
    parser.add_argument('-o', '--output', help='Output JSON file (default: <input>_<char1>_vs_<char2>.json)')
    args = parser.parse_args()
    
    input_path = Path(args.input)
    char1 = args.char1.upper()
    char2 = args.char2.upper()
    output_path = args.output or f"{input_path.stem}_{char1}_vs_{char2}.json"
    
    stats = filter_by_characters_streaming(args.input, char1, char2, output_path)
    
    print(f"Matchup: {stats['matchup']}")
    print(f"Total matches: {stats['total']}")
    print(f"Matching matchup: {stats['matched']}")
    print(f"Filtered out: {stats['filtered_out']}")
    print(f"Saved to: {stats['output_file']}")


if __name__ == '__main__':
    main()
