#!/usr/bin/env python3
"""
Test script for UMGFileTransformation API
Tests the conversion between UMG and JSON formats
"""

import json
import os
import sys

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from FileManage import UMGFileTransformation
from mcp_config import UNREAL_HOST, UNREAL_PORT

class TestUnrealConnection:
    """Mock connection for testing"""
    def __init__(self):
        self.commands = []
    
    def send_command(self, command, params):
        self.commands.append((command, params))
        # Mock response for testing
        if command == 'export_umg_to_json':
            return {
                "status": "success",
                "result": {
                    "data": {
                        "widget_name": "Root",
                        "widget_class": "/Script/UMG.UserWidget",
                        "properties": {},
                        "children": [
                            {
                                "widget_name": "TextBlock_0",
                                "widget_class": "/Script/UMG.TextBlock",
                                "properties": {
                                    "Text": "Hello World",
                                    "FontSize": 24
                                },
                                "children": []
                            }
                        ]
                    }
                }
            }
        elif command == 'apply_json_to_umg':
            return {
                "status": "success",
                "result": {
                    "message": "Successfully applied JSON to UMG asset"
                }
            }
        return {"status": "error", "error": "Unknown command"}

def test_export_umg_to_json():
    """Test exporting UMG to JSON"""
    print("Testing export_umg_to_json...")
    conn = TestUnrealConnection()
    transformer = UMGFileTransformation.UMGFileTransformation(conn)
    
    # Test with asset path
    result = transformer.export_umg_to_json("/Game/TestWidget.TestWidget")
    print(f"Export result: {json.dumps(result, indent=2)}")
    
    # Test with widget name
    result = transformer.export_umg_to_json("/Game/TestWidget.TestWidget", "TextBlock_0")
    print(f"Export with widget name result: {json.dumps(result, indent=2)}")
    
    print("OK export_umg_to_json test completed")

def test_apply_json_to_umg():
    """Test applying JSON to UMG"""
    print("\nTesting apply_json_to_umg...")
    conn = TestUnrealConnection()
    transformer = UMGFileTransformation.UMGFileTransformation(conn)
    
    # Test JSON data
    json_data = {
        "widget_name": "Root",
        "widget_class": "/Script/UMG.UserWidget",
        "properties": {},
        "children": [
            {
                "widget_name": "TextBlock_0",
                "widget_class": "/Script/UMG.TextBlock",
                "properties": {
                    "Text": "Hello World",
                    "FontSize": 24
                },
                "children": []
            }
        ]
    }
    
    # Test with asset path
    result = transformer.apply_json_to_umg("/Game/TestWidget.TestWidget", json_data)
    print(f"Apply result: {json.dumps(result, indent=2)}")
    
    # Test with widget name
    result = transformer.apply_json_to_umg("/Game/TestWidget.TestWidget", json_data, "TextBlock_0")
    print(f"Apply with widget name result: {json.dumps(result, indent=2)}")
    
    print("OK apply_json_to_umg test completed")

def test_round_trip():
    """Test round-trip conversion"""
    print("\nTesting round-trip conversion...")
    conn = TestUnrealConnection()
    transformer = UMGFileTransformation.UMGFileTransformation(conn)
    
    # Export
    export_result = transformer.export_umg_to_json("/Game/TestWidget.TestWidget")
    print("Exported JSON:")
    print(json.dumps(export_result, indent=2))
    
    # Apply the exported JSON back
    if export_result.get("status") == "success":
        json_data = export_result.get("result", {}).get("data", {})
        apply_result = transformer.apply_json_to_umg("/Game/TestWidget.TestWidget", json_data)
        print("\nApply result:")
        print(json.dumps(apply_result, indent=2))
    
    print("OK Round-trip test completed")

if __name__ == "__main__":
    print("=== UMGFileTransformation API Test ===")
    test_export_umg_to_json()
    test_apply_json_to_umg()
    test_round_trip()
    print("\n=== All tests completed ===")
