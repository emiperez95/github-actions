#!/usr/bin/env python3
"""
Coverage Badge Generator

Extracts coverage percentage from a JSON file and determines badge color.
"""

import json
import os
import sys
from typing import Tuple, Dict, Any


def get_badge_color(coverage: float) -> str:
    """
    Determine badge color based on coverage percentage.
    
    Args:
        coverage: Coverage percentage as a float
        
    Returns:
        Color string for the badge
    """
    if coverage >= 90:
        return "brightgreen"
    elif coverage >= 80:
        return "green"
    elif coverage >= 70:
        return "yellowgreen"
    elif coverage >= 60:
        return "yellow"
    elif coverage >= 50:
        return "orange"
    else:
        return "red"


def extract_coverage(coverage_file: str) -> Tuple[float, str]:
    """
    Extract coverage percentage from JSON file and determine badge color.
    
    Args:
        coverage_file: Path to the coverage JSON file
        
    Returns:
        Tuple of (coverage_percentage, badge_color)
        
    Raises:
        FileNotFoundError: If coverage file doesn't exist
        KeyError: If required keys are missing in JSON
        json.JSONDecodeError: If file is not valid JSON
    """
    with open(coverage_file) as f:
        data = json.load(f)
    
    coverage = float(data['totals']['percent_covered_display'])
    color = get_badge_color(coverage)
    
    return coverage, color


def write_github_outputs(outputs: Dict[str, Any]) -> None:
    """
    Write outputs to GitHub Actions output file.
    
    Args:
        outputs: Dictionary of output key-value pairs
    """
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            for key, value in outputs.items():
                f.write(f"{key}={value}\n")


def main():
    """Main function for command line usage."""
    if len(sys.argv) < 2:
        print("Usage: coverage_badge.py <coverage_file>")
        sys.exit(1)
    
    coverage_file = sys.argv[1]
    
    try:
        coverage, color = extract_coverage(coverage_file)
        
        print(f"Coverage: {coverage}%")
        print(f"Color: {color}")
        
        # Build outputs
        outputs = {
            "coverage": coverage,
            "color": color
        }
        
        
        # Write outputs for GitHub Actions
        write_github_outputs(outputs)
        
    except FileNotFoundError:
        print(f"Error: Coverage file '{coverage_file}' not found")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing key in coverage data: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in coverage file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing coverage data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()