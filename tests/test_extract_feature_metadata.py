import os
import json
import tempfile
import unittest
from scripts.extract_feature_metadata import extract_feature_metadata


class TestExtractFeatureMetadata(unittest.TestCase):
    
    def write_temp_metadata(self, data):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp:
            json.dump(data, tmp)
            tmp_path = tmp.name
        return tmp_path

    def test_all_fields_present(self):
        # All fields provided
        metadata = {
            "feature_id": "feat_001",
            "feature_name": "Test Feature",
            "description": "This is a test feature",
            "data_type": "float",
            "units": "meters",
            "source": "sensor",
            "creation_timestamp": "2025-04-07T20:00:00Z",
            "is_deleted": False
        }
        tmp_path = self.write_temp_metadata(metadata)
        result = extract_feature_metadata(tmp_path)
        os.remove(tmp_path)
        self.assertEqual(result["feature_id"], "feat_001")
        self.assertEqual(result["feature_name"], "Test Feature")
        self.assertEqual(result["description"], "This is a test feature")
        self.assertEqual(result["data_type"], "float")
        self.assertEqual(result["units"], "meters")
        self.assertEqual(result["source"], "sensor")
        self.assertEqual(result["creation_timestamp"], "2025-04-07T20:00:00Z")
        self.assertFalse(result["is_deleted"])
    
    def test_missing_fields(self):
        # Some fields are missing; expect missing keys to be None
        metadata = {
            "feature_id": "feat_002",
            "feature_name": "Incomplete Feature"
            # missing description, data_type, units, source, creation_timestamp, is_deleted
        }
        tmp_path = self.write_temp_metadata(metadata)
        result = extract_feature_metadata(tmp_path)
        os.remove(tmp_path)
        self.assertEqual(result["feature_id"], "feat_002")
        self.assertEqual(result["feature_name"], "Incomplete Feature")
        self.assertIsNone(result.get("description"))
        self.assertIsNone(result.get("data_type"))
        self.assertIsNone(result.get("units"))
        self.assertIsNone(result.get("source"))
        self.assertIsNone(result.get("creation_timestamp"))
        self.assertIsNone(result.get("is_deleted"))
    
    def test_extra_fields(self):
        # Include extra fields not used by the parser; should be ignored
        metadata = {
            "feature_id": "feat_003",
            "feature_name": "Extra Feature",
            "description": "Feature with extra data",
            "data_type": "integer",
            "units": "cm",
            "source": "calculation",
            "creation_timestamp": "2025-04-07T21:00:00Z",
            "is_deleted": True,
            "extra_field": "extra_value"
        }
        tmp_path = self.write_temp_metadata(metadata)
        result = extract_feature_metadata(tmp_path)
        os.remove(tmp_path)
        self.assertEqual(result["feature_id"], "feat_003")
        self.assertEqual(result["feature_name"], "Extra Feature")
        self.assertEqual(result["description"], "Feature with extra data")
        self.assertEqual(result["data_type"], "integer")
        self.assertEqual(result["units"], "cm")
        self.assertEqual(result["source"], "calculation")
        self.assertEqual(result["creation_timestamp"], "2025-04-07T21:00:00Z")
        self.assertTrue(result["is_deleted"])
        
    def test_invalid_json(self):
        # Test behavior with invalid JSON; expect a JSONDecodeError
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp:
            tmp.write("Not a JSON content")
            tmp_path = tmp.name
        with self.assertRaises(json.JSONDecodeError):
            extract_feature_metadata(tmp_path)
        os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
