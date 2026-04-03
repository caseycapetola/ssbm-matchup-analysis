#!/usr/bin/env python3
"""Filter matches by competitive stages."""

import argparse
from pathlib import Path

import pandas as pd

COMPETITIVE_STAGES = {
    'YOSHIS_STORY',
    'FOUNTAIN_OF_DREAMS',
    'FINAL_DESTINATION',
    'POKEMON_STADIUM',
    'BATTLEFIELD',
    'DREAMLAND'
}

def filter_by_competitive_stages(input_file: str, output_file: str) -> dict:
    """
    Filter matches to keep only those on competitive stages.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
    
    Returns:
        dict with statistics about the filtering
    """
    df = pd.read_csv(input_file)
    total = len(df)
    
    filtered_df = df[df['stage'].isin(COMPETITIVE_STAGES)]
    matched = len(filtered_df)
    
    filtered_df.to_csv(output_file, index=False)
    
    return {
        'total': total,
        'matched': matched,
        'filtered_out': total - matched,
        'output_file': output_file
    }


def main():
    parser = argparse.ArgumentParser(description='Filter matches by competitive stages')
    parser.add_argument('input', help='Input CSV file')
    parser.add_argument('-o', '--output', help='Output CSV file (default: <input>_competitive.csv)')
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = args.output or f"{input_path.stem}_competitive.csv"
    
    stats = filter_by_competitive_stages(args.input, output_path)
    
    print(f"Total matches: {stats['total']}")
    print(f"Competitive stage matches: {stats['matched']}")
    print(f"Filtered out: {stats['filtered_out']}")
    print(f"Saved to: {stats['output_file']}")


if __name__ == '__main__':
    main()
