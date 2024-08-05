import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    """Tests the FileStorage class"""

    def setUp(self):
        """Set up the test environment"""
        self.file_storage = FileStorage()
        self.file_path = FileStorage._FileStorage__file_path
        self.file_storage._FileStorage__objects = {}

    def tearDown(self):
        """Tear down the test environment by deleting the JSON file"""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_file_path_initialization(self):
        """Test that __file_path is initialized correctly"""
        self.assertEqual(self.file_path, "file.json")

    def test_save_creates_file(self):
        """Test that save creates a file with the correct content"""
        base_model = BaseModel()
        self.file_storage.new(base_model)
        self.file_storage.save()

        self.assertTrue(os.path.exists(self.file_path))

        with open(self.file_path, "r", encoding="utf-8") as file:
            content = json.load(file)
            key = f"BaseModel.{base_model.id}"
            self.assertIn(key, content)
            self.assertEqual(content[key]['id'], base_model.id)

    def test_reload_loads_objects(self):
        """Test that reload loads objects from the file"""
        base_model = BaseModel()
        self.file_storage.new(base_model)
        self.file_storage.save()

        FileStorage.reload()
        objects = FileStorage._FileStorage__objects
        key = f"BaseModel.{base_model.id}"
        self.assertIn(key, objects)
        self.assertEqual(objects[key].id, base_model.id)


if __name__ == "__main__":
    unittest.main()
