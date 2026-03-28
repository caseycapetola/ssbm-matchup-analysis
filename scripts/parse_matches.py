#!/usr/bin/env python3
"""
Parse large JSON match data file using streaming to handle very large files.
Extracts: match info, stage, winner, player details, and action counts.
"""

import os
import sys

try:
    import ijson
except ImportError:
    print("Error: ijson library is required for streaming JSON parsing")
    sys.exit(1)


def extract_match_data(match):
    """Extract relevant fields from a single match."""
    extracted = {
        'matchid': match.get('matchid'),
        'stage': match.get('settings', {}).get('stageString'),
        'winner': match.get('metadata', {}).get('winner'),
        'startAt': match.get('metadata', {}).get('startAt', {}).get('$date'),
        'gameComplete': match.get('metadata', {}).get('gameComplete'),
        'players': []
    }

    # Extract player information
    for player in match.get('players', []):
        player_data = {
            'code': player.get('code'),
            'character': player.get('characterString'),
            'characterColor': player.get('characterColor'),
            'actionCounts': player.get('actionCounts', {})
        }
        extracted['players'].append(player_data)

    return extracted


def stream_parse_json_array(input_file, output_file):
    """
    Stream parse a JSON array without loading entire file into memory.
    Processes one match at a time using ijson.
    """
    print(f"Reading from: {input_file}")

    match_count = 0

    with open(input_file, 'rb') as infile, open(output_file, 'w') as outfile:
        # Write opening bracket for output array
        outfile.write('[\n')

        first_match = True

        # Use ijson to iterate through array items
        matches = ijson.items(infile, 'item')

        for match in matches:
            try:
                extracted = extract_match_data(match)

                # Write comma before all but first match
                if not first_match:
                    outfile.write(',\n')
                first_match = False

                # Write extracted match
                import json
                json.dump(extracted, outfile, indent=2)

                match_count += 1

                # Progress meter
                if match_count % 1000 == 0:
                    print(f"Processed {match_count} matches...")

            except Exception as e:
                print(f"Warning: Error processing match {match_count}: {e}")
                continue

        # Write closing bracket for output array
        outfile.write('\n]\n')

    print(f"\nTotal matches processed: {match_count}")
    return match_count


def parse_json_file(input_file, output_file):
    """Parse large JSON file and write extracted data to output file."""

    try:
        matches = stream_parse_json_array(input_file, output_file)

        print(f"\nTotal Matches: {matches}")

        # Show size comparison
        original_size = os.path.getsize(input_file) / (1024 * 1024 * 1024)  # GB
        new_size = os.path.getsize(output_file) / (1024 * 1024)  # MB

        if original_size >= 1:
            print(f"\nOriginal size: {original_size:.2f} GB")
        else:
            print(f"\nOriginal size: {original_size * 1024:.2f} MB")

        print(f"New size: {new_size:.2f} MB")

        if original_size > 0:
            reduction = ((original_size * 1024 - new_size) / (original_size * 1024)) * 100
            print(f"Reduction: {reduction:.1f}%")

        print(f"\nExtracted data written to: {output_file}")

    except Exception as e:
        print(f"Error during processing: {e}")
        raise


if __name__ == '__main__':
    input_file = 'test.json'
    output_file = 'extracted_matches.json'

    # Allow custom filenames via command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    try:
        parse_json_file(input_file, output_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nProcessing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
