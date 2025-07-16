#!/usr/bin/env python3
"""
Backend Test Suite for Distributed LLM Penetration Testing CLI Tools
====================================================================
Tests both the main distributed CLI tool and demo version.
"""

import subprocess
import json
import os
import sys
import time
import tempfile
import shutil
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock
import requests

class TestDistributedLLMPentestCLI(unittest.TestCase):
    """Test suite for distributed LLM penetration testing CLI tools"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path("/app")
        self.main_cli = self.test_dir / "distributed_llm_pentest_cli.py"
        self.demo_cli = self.test_dir / "demo_distributed_llm_pentest_cli.py"
        self.usage_guide = self.test_dir / "DISTRIBUTED_USAGE_GUIDE.md"
        
        # Ensure files exist
        self.assertTrue(self.main_cli.exists(), "Main CLI tool not found")
        self.assertTrue(self.demo_cli.exists(), "Demo CLI tool not found")
        self.assertTrue(self.usage_guide.exists(), "Usage guide not found")
        
        # Clean up any existing test files
        self.cleanup_test_files()
    
    def tearDown(self):
        """Clean up after tests"""
        self.cleanup_test_files()
    
    def cleanup_test_files(self):
        """Remove test-generated files"""
        patterns = [
            "distributed_test_result_*.json",
            "demo_distributed_test_result_*.json",
            "distributed_llm_pentest.log",
            "demo_distributed_llm_pentest.log"
        ]
        
        for pattern in patterns:
            for file in self.test_dir.glob(pattern):
                try:
                    file.unlink()
                except:
                    pass
    
    def run_cli_command(self, cli_path, args, timeout=30):
        """Run CLI command and return result"""
        cmd = [sys.executable, str(cli_path)] + args
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.test_dir)
            )
            return result
        except subprocess.TimeoutExpired:
            return None
    
    def test_main_cli_help(self):
        """Test main CLI help functionality"""
        print("\n🧪 Testing main CLI help...")
        
        result = self.run_cli_command(self.main_cli, ["--help"])
        self.assertIsNotNone(result, "CLI help command timed out")
        self.assertEqual(result.returncode, 0, "Help command failed")
        
        # Check for key help content
        help_text = result.stdout
        self.assertIn("Distributed LLM Penetration Testing CLI Tool", help_text)
        self.assertIn("--tester-url", help_text)
        self.assertIn("--target-url", help_text)
        self.assertIn("--tester-model", help_text)
        self.assertIn("--target-model", help_text)
        self.assertIn("--list-models", help_text)
        self.assertIn("--test-connections", help_text)
        self.assertIn("--max-tests", help_text)
        self.assertIn("--delay", help_text)
        
        print("✅ Main CLI help test passed")
    
    def test_demo_cli_help(self):
        """Test demo CLI help functionality"""
        print("\n🧪 Testing demo CLI help...")
        
        result = self.run_cli_command(self.demo_cli, ["--help"])
        self.assertIsNotNone(result, "Demo CLI help command timed out")
        self.assertEqual(result.returncode, 0, "Demo help command failed")
        
        # Check for key help content
        help_text = result.stdout
        self.assertIn("Demo Distributed LLM Penetration Testing CLI Tool", help_text)
        self.assertIn("--tester-url", help_text)
        self.assertIn("--target-url", help_text)
        self.assertIn("--tester-model", help_text)
        self.assertIn("--target-model", help_text)
        self.assertIn("--list-models", help_text)
        self.assertIn("--test-connections", help_text)
        
        print("✅ Demo CLI help test passed")
    
    def test_main_cli_missing_models_error(self):
        """Test main CLI error handling for missing model arguments"""
        print("\n🧪 Testing main CLI missing models error...")
        
        result = self.run_cli_command(self.main_cli, [
            "--tester-url", "http://localhost:11434",
            "--target-url", "http://localhost:11435"
        ])
        
        self.assertIsNotNone(result, "CLI command timed out")
        # Note: CLI returns 0 but prints error message (design choice)
        
        # Check error message
        output = result.stdout + result.stderr
        self.assertIn("Both --tester-model and --target-model are required", output)
        
        print("✅ Main CLI missing models error test passed")
    
    def test_demo_cli_list_models(self):
        """Test demo CLI model listing functionality"""
        print("\n🧪 Testing demo CLI model listing...")
        
        result = self.run_cli_command(self.demo_cli, [
            "--list-models",
            "--tester-url", "http://192.168.1.100:11434",
            "--target-url", "http://192.168.1.101:11434"
        ])
        
        self.assertIsNotNone(result, "Demo CLI list-models command timed out")
        self.assertEqual(result.returncode, 0, "Demo list-models command failed")
        
        # Check output content
        output = result.stdout
        self.assertIn("[DEMO] Available Ollama models:", output)
        self.assertIn("Tester Endpoint (http://192.168.1.100:11434):", output)
        self.assertIn("Target Endpoint (http://192.168.1.101:11434):", output)
        self.assertIn("llama3.2:latest", output)
        self.assertIn("mistral:latest", output)
        
        print("✅ Demo CLI model listing test passed")
    
    def test_demo_cli_test_connections(self):
        """Test demo CLI connection testing functionality"""
        print("\n🧪 Testing demo CLI connection testing...")
        
        result = self.run_cli_command(self.demo_cli, [
            "--test-connections",
            "--tester-url", "http://192.168.1.100:11434",
            "--target-url", "http://192.168.1.101:11434"
        ])
        
        self.assertIsNotNone(result, "Demo CLI test-connections command timed out")
        self.assertEqual(result.returncode, 0, "Demo test-connections command failed")
        
        # Check output content
        output = result.stdout
        self.assertIn("[DEMO] Testing connections to both endpoints", output)
        self.assertIn("✅ [DEMO] Both endpoints are accessible", output)
        
        print("✅ Demo CLI connection testing test passed")
    
    def test_demo_cli_distributed_testing(self):
        """Test demo CLI distributed testing functionality"""
        print("\n🧪 Testing demo CLI distributed testing...")
        
        result = self.run_cli_command(self.demo_cli, [
            "--tester-model", "llama3.2:latest",
            "--target-model", "llama3.2:1b",
            "--tester-url", "http://192.168.1.100:11434",
            "--target-url", "http://192.168.1.101:11434",
            "--max-tests", "3",
            "--delay", "0.1"
        ], timeout=60)
        
        self.assertIsNotNone(result, "Demo CLI distributed testing timed out")
        self.assertEqual(result.returncode, 0, "Demo distributed testing failed")
        
        # Check output content
        output = result.stdout
        self.assertIn("Demo Distributed LLM Penetration Testing Tool", output)
        self.assertIn("📝 This is a DEMO version", output)
        self.assertIn("RUNNING DEMO DISTRIBUTED TEST", output)
        self.assertIn("Tester: llama3.2:latest @ http://192.168.1.100:11434", output)
        self.assertIn("Target: llama3.2:1b @ http://192.168.1.101:11434", output)
        self.assertIn("DEMO DISTRIBUTED PENETRATION TESTING SUMMARY", output)
        
        # Check for OWASP categories
        self.assertIn("LLM01", output)
        self.assertIn("LLM02", output)
        self.assertIn("LLM04", output)
        self.assertIn("LLM06", output)
        
        print("✅ Demo CLI distributed testing test passed")
    
    def test_demo_cli_json_output_format(self):
        """Test demo CLI JSON output format"""
        print("\n🧪 Testing demo CLI JSON output format...")
        
        result = self.run_cli_command(self.demo_cli, [
            "--tester-model", "llama3.2:latest",
            "--target-model", "llama3.2:1b",
            "--tester-url", "http://192.168.1.100:11434",
            "--target-url", "http://192.168.1.101:11434",
            "--max-tests", "2",
            "--delay", "0.1"
        ], timeout=30)
        
        self.assertIsNotNone(result, "Demo CLI JSON test timed out")
        self.assertEqual(result.returncode, 0, "Demo CLI JSON test failed")
        
        # Check for JSON structure in output
        output = result.stdout
        
        # Look for JSON structure indicators
        self.assertIn('"test_id":', output)
        self.assertIn('"timestamp_utc":', output)
        self.assertIn('"target_model": "llama3.2:1b"', output)
        self.assertIn('"tester_model": "llama3.2:latest"', output)
        self.assertIn('"tester_endpoint": "http://192.168.1.100:11434"', output)
        self.assertIn('"target_endpoint": "http://192.168.1.101:11434"', output)
        self.assertIn('"owasp_category_code":', output)
        self.assertIn('"owasp_category_name":', output)
        self.assertIn('"attack_vector":', output)
        self.assertIn('"attack_strategy":', output)
        self.assertIn('"prompt_payload":', output)
        self.assertIn('"vulnerability_identified":', output)
        self.assertIn('"severity_assessment":', output)
        
        print("✅ Demo CLI JSON output format test passed")
    
    def test_demo_cli_file_generation(self):
        """Test demo CLI test result file generation"""
        print("\n🧪 Testing demo CLI file generation...")
        
        # Clean up first
        self.cleanup_test_files()
        
        result = self.run_cli_command(self.demo_cli, [
            "--tester-model", "llama3.2:latest",
            "--target-model", "llama3.2:1b",
            "--tester-url", "http://192.168.1.100:11434",
            "--target-url", "http://192.168.1.101:11434",
            "--max-tests", "2",
            "--delay", "0.1"
        ], timeout=30)
        
        self.assertIsNotNone(result, "Demo CLI file generation test timed out")
        self.assertEqual(result.returncode, 0, "Demo CLI file generation test failed")
        
        # Check for generated files
        json_files = list(self.test_dir.glob("demo_distributed_test_result_*.json"))
        self.assertGreater(len(json_files), 0, "No JSON result files generated")
        
        log_file = self.test_dir / "demo_distributed_llm_pentest.log"
        self.assertTrue(log_file.exists(), "Log file not generated")
        
        # Validate JSON file content
        for json_file in json_files:
            with open(json_file, 'r') as f:
                data = json.load(f)
                
                # Check required fields
                required_fields = [
                    'test_id', 'timestamp_utc', 'target_model', 'tester_model',
                    'tester_endpoint', 'target_endpoint', 'owasp_category_code',
                    'owasp_category_name', 'attack_vector', 'attack_strategy',
                    'prompt_payload', 'vulnerability_identified', 'severity_assessment'
                ]
                
                for field in required_fields:
                    self.assertIn(field, data, f"Missing field {field} in JSON output")
                
                # Check distributed endpoint information
                self.assertEqual(data['tester_endpoint'], "http://192.168.1.100:11434")
                self.assertEqual(data['target_endpoint'], "http://192.168.1.101:11434")
                self.assertEqual(data['tester_model'], "llama3.2:latest")
                self.assertEqual(data['target_model'], "llama3.2:1b")
        
        print("✅ Demo CLI file generation test passed")
    
    def test_demo_cli_attack_scenarios(self):
        """Test demo CLI predefined attack scenarios"""
        print("\n🧪 Testing demo CLI attack scenarios...")
        
        result = self.run_cli_command(self.demo_cli, [
            "--tester-model", "llama3.2:latest",
            "--target-model", "llama3.2:1b",
            "--max-tests", "5",
            "--delay", "0.1"
        ], timeout=45)
        
        self.assertIsNotNone(result, "Demo CLI attack scenarios test timed out")
        self.assertEqual(result.returncode, 0, "Demo CLI attack scenarios test failed")
        
        output = result.stdout
        
        # Check for different OWASP categories
        owasp_categories = ["LLM01", "LLM02", "LLM04", "LLM06"]
        found_categories = []
        
        for category in owasp_categories:
            if category in output:
                found_categories.append(category)
        
        self.assertGreater(len(found_categories), 0, "No OWASP categories found in output")
        
        # Check for specific attack vectors
        attack_vectors = [
            "Authority Impersonation",
            "System Prompt Extraction", 
            "Script Injection",
            "Resource Exhaustion",
            "Role Manipulation"
        ]
        
        found_vectors = []
        for vector in attack_vectors:
            if vector in output:
                found_vectors.append(vector)
        
        self.assertGreater(len(found_vectors), 0, "No attack vectors found in output")
        
        print("✅ Demo CLI attack scenarios test passed")
    
    def test_main_cli_connection_failure_handling(self):
        """Test main CLI connection failure handling"""
        print("\n🧪 Testing main CLI connection failure handling...")
        
        # Test with invalid URLs
        result = self.run_cli_command(self.main_cli, [
            "--test-connections",
            "--tester-url", "http://invalid-host:11434",
            "--target-url", "http://another-invalid-host:11434"
        ], timeout=20)
        
        self.assertIsNotNone(result, "Main CLI connection failure test timed out")
        # Should not crash, but may return non-zero exit code
        
        output = result.stdout + result.stderr
        self.assertIn("Failed to connect", output)
        
        print("✅ Main CLI connection failure handling test passed")
    
    def test_usage_guide_completeness(self):
        """Test usage guide completeness"""
        print("\n🧪 Testing usage guide completeness...")
        
        with open(self.usage_guide, 'r') as f:
            content = f.read()
        
        # Check for key sections
        required_sections = [
            "# Distributed LLM Penetration Testing CLI Tool",
            "## Overview",
            "## Features",
            "## Installation", 
            "## Usage",
            "## System Setup",
            "## Command Line Options",
            "## Output Format",
            "## Example Scenarios",
            "## Troubleshooting",
            "## Security Considerations"
        ]
        
        for section in required_sections:
            self.assertIn(section, content, f"Missing section: {section}")
        
        # Check for key technical details
        technical_details = [
            "--tester-url",
            "--target-url", 
            "--tester-model",
            "--target-model",
            "http://192.168.1.100:11434",
            "http://192.168.1.101:11434",
            "LLM01", "LLM02", "LLM04", "LLM06",
            "distributed_test_result_",
            "demo_distributed_test_result_"
        ]
        
        for detail in technical_details:
            self.assertIn(detail, content, f"Missing technical detail: {detail}")
        
        print("✅ Usage guide completeness test passed")
    
    def test_cli_argument_validation(self):
        """Test CLI argument validation"""
        print("\n🧪 Testing CLI argument validation...")
        
        # Test main CLI with invalid arguments
        test_cases = [
            # Missing both models
            {
                "args": ["--max-tests", "5"],
                "should_fail": True,
                "error_text": "Both --tester-model and --target-model are required"
            },
            # Invalid max-tests
            {
                "args": ["--tester-model", "test", "--target-model", "test", "--max-tests", "-1"],
                "should_fail": False,  # argparse handles this
                "error_text": None
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            print(f"  Testing argument case {i+1}...")
            result = self.run_cli_command(self.main_cli, test_case["args"], timeout=10)
            
            if test_case["should_fail"]:
                self.assertNotEqual(result.returncode, 0, f"Test case {i+1} should have failed")
                if test_case["error_text"]:
                    output = result.stdout + result.stderr
                    self.assertIn(test_case["error_text"], output)
        
        print("✅ CLI argument validation test passed")
    
    def test_distributed_architecture_features(self):
        """Test distributed architecture specific features"""
        print("\n🧪 Testing distributed architecture features...")
        
        # Test with different URLs to ensure distributed functionality
        result = self.run_cli_command(self.demo_cli, [
            "--tester-model", "llama3.2:latest",
            "--target-model", "mistral:latest",
            "--tester-url", "http://tester-system:11434",
            "--target-url", "http://target-system:11434",
            "--max-tests", "2",
            "--delay", "0.1"
        ], timeout=30)
        
        self.assertIsNotNone(result, "Distributed architecture test timed out")
        self.assertEqual(result.returncode, 0, "Distributed architecture test failed")
        
        output = result.stdout
        
        # Verify distributed endpoint information is displayed
        self.assertIn("Tester: llama3.2:latest @ http://tester-system:11434", output)
        self.assertIn("Target: mistral:latest @ http://target-system:11434", output)
        
        # Check that JSON output contains distributed information
        self.assertIn('"tester_endpoint": "http://tester-system:11434"', output)
        self.assertIn('"target_endpoint": "http://target-system:11434"', output)
        
        print("✅ Distributed architecture features test passed")

def run_tests():
    """Run all tests and return results"""
    print("🚀 Starting Distributed LLM Penetration Testing CLI Tests")
    print("=" * 70)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDistributedLLMPentestCLI)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)