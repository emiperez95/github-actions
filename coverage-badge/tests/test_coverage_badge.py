#!/usr/bin/env python3
"""
Unit tests for coverage_badge.py
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path to import coverage_badge
sys.path.insert(0, str(Path(__file__).parent.parent))
import coverage_badge


class TestBadgeColor(unittest.TestCase):
    """Test badge color determination."""
    
    def test_color_thresholds(self):
        """Test color selection for different coverage percentages."""
        test_cases = [
            (95.0, "brightgreen"),
            (90.0, "brightgreen"),
            (89.9, "green"),
            (80.0, "green"),
            (79.9, "yellowgreen"),
            (70.0, "yellowgreen"),
            (69.9, "yellow"),
            (60.0, "yellow"),
            (59.9, "orange"),
            (50.0, "orange"),
            (49.9, "red"),
            (0.0, "red"),
        ]
        
        for coverage, expected_color in test_cases:
            with self.subTest(coverage=coverage):
                color = coverage_badge.get_badge_color(coverage)
                self.assertEqual(color, expected_color)


class TestCoverageExtraction(unittest.TestCase):
    """Test coverage extraction from JSON files."""
    
    def setUp(self):
        """Set up test fixtures path."""
        self.fixtures_dir = Path(__file__).parent / "fixtures"
    
    def test_valid_coverage_file(self):
        """Test extraction from valid coverage file."""
        coverage_file = self.fixtures_dir / "coverage_90.json"
        coverage, color = coverage_badge.extract_coverage(str(coverage_file))
        
        self.assertEqual(coverage, 92.5)
        self.assertEqual(color, "brightgreen")
    
    def test_low_coverage_file(self):
        """Test extraction from low coverage file."""
        coverage_file = self.fixtures_dir / "coverage_50.json"
        coverage, color = coverage_badge.extract_coverage(str(coverage_file))
        
        self.assertEqual(coverage, 52.3)
        self.assertEqual(color, "orange")
    
    def test_missing_file(self):
        """Test handling of missing coverage file."""
        with self.assertRaises(FileNotFoundError):
            coverage_badge.extract_coverage("nonexistent.json")
    
    def test_invalid_json_structure(self):
        """Test handling of invalid JSON structure."""
        coverage_file = self.fixtures_dir / "invalid_coverage.json"
        
        with self.assertRaises(KeyError):
            coverage_badge.extract_coverage(str(coverage_file))
    
    def test_malformed_json(self):
        """Test handling of malformed JSON."""
        coverage_file = self.fixtures_dir / "malformed.json"
        
        with self.assertRaises(json.JSONDecodeError):
            coverage_badge.extract_coverage(str(coverage_file))


class TestGitHubOutputs(unittest.TestCase):
    """Test GitHub Actions output writing."""
    
    def test_write_outputs(self):
        """Test writing outputs to GITHUB_OUTPUT file."""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            output_file = f.name
        
        try:
            # Set GITHUB_OUTPUT environment variable
            os.environ['GITHUB_OUTPUT'] = output_file
            
            # Write outputs
            outputs = {
                "coverage": 85.5,
                "color": "green",
                "badge-url": "https://example.com/badge"
            }
            coverage_badge.write_github_outputs(outputs)
            
            # Read and verify outputs
            with open(output_file) as f:
                content = f.read()
            
            self.assertIn("coverage=85.5\n", content)
            self.assertIn("color=green\n", content)
            self.assertIn("badge-url=https://example.com/badge\n", content)
            
        finally:
            # Clean up
            if 'GITHUB_OUTPUT' in os.environ:
                del os.environ['GITHUB_OUTPUT']
            if os.path.exists(output_file):
                os.unlink(output_file)
    
    def test_no_github_output_env(self):
        """Test behavior when GITHUB_OUTPUT is not set."""
        # Ensure GITHUB_OUTPUT is not set
        if 'GITHUB_OUTPUT' in os.environ:
            del os.environ['GITHUB_OUTPUT']
        
        # Should not raise an error
        coverage_badge.write_github_outputs({"test": "value"})


class TestMainFunction(unittest.TestCase):
    """Test main function behavior."""
    
    def setUp(self):
        """Set up test fixtures path."""
        self.fixtures_dir = Path(__file__).parent / "fixtures"
        self.original_argv = sys.argv.copy()
    
    def tearDown(self):
        """Restore original argv."""
        sys.argv = self.original_argv
    
    def test_main_with_valid_file(self):
        """Test main function with valid coverage file."""
        coverage_file = str(self.fixtures_dir / "coverage_90.json")
        sys.argv = ["coverage_badge.py", coverage_file]
        
        # Capture stdout
        from io import StringIO
        import contextlib
        
        output = StringIO()
        with contextlib.redirect_stdout(output):
            try:
                coverage_badge.main()
            except SystemExit as e:
                self.assertEqual(e.code, None)
        
        result = output.getvalue()
        self.assertIn("Coverage: 92.5%", result)
        self.assertIn("Color: brightgreen", result)
    
    def test_main_missing_arguments(self):
        """Test main function with missing arguments."""
        sys.argv = ["coverage_badge.py"]
        
        with self.assertRaises(SystemExit) as cm:
            coverage_badge.main()
        
        self.assertEqual(cm.exception.code, 1)
    
    def test_main_with_badge_url(self):
        """Test main function with gist parameters."""
        coverage_file = str(self.fixtures_dir / "coverage_90.json")
        sys.argv = ["coverage_badge.py", coverage_file, "gist123", "badge.json"]
        
        # Set required environment variable
        os.environ['GITHUB_REPOSITORY_OWNER'] = 'testowner'
        
        try:
            from io import StringIO
            import contextlib
            
            output = StringIO()
            with contextlib.redirect_stdout(output):
                with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
                    os.environ['GITHUB_OUTPUT'] = f.name
                    try:
                        coverage_badge.main()
                    except SystemExit:
                        pass
                    
                    # Check if badge URL was written to outputs
                    with open(f.name) as output_file:
                        content = output_file.read()
                        self.assertIn("badge-url=https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/testowner/gist123/raw/badge.json", content)
                    
                    os.unlink(f.name)
        finally:
            if 'GITHUB_REPOSITORY_OWNER' in os.environ:
                del os.environ['GITHUB_REPOSITORY_OWNER']
            if 'GITHUB_OUTPUT' in os.environ:
                del os.environ['GITHUB_OUTPUT']


if __name__ == '__main__':
    unittest.main()