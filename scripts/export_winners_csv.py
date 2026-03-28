#!/usr/bin/env python3
"""Export complete match data to CSV with winner's character."""

import argparse
import csv
from pathlib import Path

try:
    import ijson
    HAS_IJSON = True
except ImportError:
    HAS_IJSON = False


def export_winners_csv_streaming(input_file: str, output_file: str) -> dict:
    """
    Parse complete games and export to CSV with id, stage, and winning character.
    
    Args:
        input_file: Path to input JSON file
        output_file: Path to output CSV file
    
    Returns:
        dict with statistics
    """
    if not HAS_IJSON:
        raise ImportError("ijson is required for streaming. Install with: pip install ijson")
    
    total = 0
    exported = 0
    
    with open(input_file, 'rb') as infile, open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['id', 'stage', 'winning_character'])
        
        for match in ijson.items(infile, 'item'):
            total += 1
            
            if not match.get('gameComplete'):
                continue
            
            winner_code = match.get('winner')
            stage = match.get('stage')
            
            winning_character = None
            for player in match.get('players', []):
                if player.get('code') == winner_code:
                    winning_character = player.get('character')
                    break
            
            if winning_character:
                exported += 1
                writer.writerow([exported, stage, winning_character])
    
    return {
        'total_matches': total,
        'complete_matches': exported,
        'output_file': output_file
    }


def main():
    parser = argparse.ArgumentParser(description='Export complete match winners to CSV (streaming)')
    parser.add_argument('input', help='Input JSON file')
    parser.add_argument('-o', '--output', help='Output CSV file (default: <input>_winners.csv)')
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = args.output or f"{input_path.stem}_winners.csv"
    
    stats = export_winners_csv_streaming(args.input, output_path)
    
    print(f"Total matches: {stats['total_matches']}")
    print(f"Complete matches exported: {stats['complete_matches']}")
    print(f"Saved to: {stats['output_file']}")


if __name__ == '__main__':
    main()
