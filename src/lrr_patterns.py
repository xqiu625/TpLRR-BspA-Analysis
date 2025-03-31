#!/usr/bin/env python3
"""
LRR Patterns Module

This module defines regular expression patterns for different classes of
Leucine-Rich Repeat (LRR) proteins.
"""

import json
import os
import re
from pathlib import Path

# Define LRR patterns
LRR_PATTERNS = {
    "TpLRR": {
        "pattern": r"(?:C|N).{2}L.{2}I.{1}L.{3}L.{2}I.{3}AF",
        "length": 21,
        "description": "TpLRR pattern (21 AA)"
    },
    "RI-like": {
        "pattern": r".{3}L.{2}L.{1}L.{2}[NC].{1}L.{3}G[GAIVLMFPWC].{2}L.{2}[GAIVLMFPWC]L.{2}",
        "length": 28,
        "description": "RI-like pattern (28 AA)"
    },
    "SDS22-like": {
        "pattern": r"L.{2}L.{2}L.{1}L.{2}N.{1}I.{2}I.{2}L.{2}",
        "length": 22,
        "description": "SDS22-like pattern (22 AA)"
    },
    "Cysteine-containing": {
        "pattern": r"C.{2}L.{2}L.{1}L.{2}C.{2}ITD.{2}[GAIVLMFPWC].{2}LA.{2}",
        "length": 22,
        "description": "Cysteine-containing pattern (22 AA)"
    },
    "Bacterial": {
        "pattern": r"P.{2}L.{2}L.{1}V.{2}N.{1}L.{2}LP.{1}L",
        "length": 20,
        "description": "Bacterial pattern (20 AA)"
    },
    "Typical": {
        "pattern": r"L.{2}L.{2}L.{1}L.{2}N.{1}L.{2}LP.{2}[GAIVLMFPWC]F.{2}",
        "length": 24,
        "description": "Typical LRR pattern"
    },
    "Plant-specific": {
        "pattern": r"L.{2}L.{2}L.{1}L.{2}N.{1}L.{3}IP.{2}LG.{1}",
        "length": 22,
        "description": "Plant-specific pattern (22 AA)"
    }
}

def get_compiled_pattern(pattern_name):
    """
    Get a compiled regex pattern for the specified LRR class
    
    Args:
        pattern_name (str): Name of the LRR pattern
        
    Returns:
        tuple: (compiled_pattern, pattern_length)
    """
    if pattern_name not in LRR_PATTERNS:
        raise ValueError(f"Unknown pattern: {pattern_name}")
    
    pattern_info = LRR_PATTERNS[pattern_name]
    return (re.compile(pattern_info["pattern"]), pattern_info["length"])

def save_patterns_to_file(file_path=None):
    """
    Save the LRR patterns to a JSON file
    
    Args:
        file_path (str, optional): Path to save the patterns. 
                                   Defaults to data/patterns.json
    """
    if file_path is None:
        # Get the directory of the current script
        current_dir = Path(__file__).parent.absolute()
        # Go up one level to the project root
        project_root = current_dir.parent
        # Create data directory if it doesn't exist
        data_dir = project_root / "data"
        data_dir.mkdir(exist_ok=True)
        file_path = data_dir / "patterns.json"
    
    with open(file_path, 'w') as f:
        json.dump(LRR_PATTERNS, f, indent=2)
    
    print(f"Patterns saved to {file_path}")

def load_patterns_from_file(file_path=None):
    """
    Load LRR patterns from a JSON file
    
    Args:
        file_path (str, optional): Path to load the patterns from.
                                   Defaults to data/patterns.json
    
    Returns:
        dict: Dictionary of LRR patterns
    """
    if file_path is None:
        # Get the directory of the current script
        current_dir = Path(__file__).parent.absolute()
        # Go up one level to the project root
        project_root = current_dir.parent
        file_path = project_root / "data" / "patterns.json"
    
    with open(file_path, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    # If run directly, save patterns to file
    save_patterns_to_file()
