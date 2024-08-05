import unittest
from models.base_model import BaseModel
import os


class TestBaseModel(unittest.TestCase):
    """
    Test class for BaseModel
    """

    def setUp(self):
        """
        Set up method for the test class
        """
        self.base_model = BaseModel()

    def tearDown(self):
        """
        Tear down method for the test class
        """
        self.resetStorage()

    def resetStorage(self):
        """
        Reset the storage
        """
        from models.engine.file_storage import FileStorage
        FileStorage._FileStorage__objects = {}
        file_path = FileStorage._FileStorage__file_path
        if os.path.isfile(file_path):
            os.remove(file_path)

    def test_str(self):
        """
        Test the __str__ method
        """
        expected_str = f"[{self.base_model.__class__.__name__}] ({self.base_model.id}) {
            self.base_model.__dict__}"
        self.assertEqual(str(self.base_model), expected_str)

    def test_save(self):
        """
        Test the save method
        """
        initial_updated_at = self.base_model.updated_at
        self.base_model.save()
        self.assertGreater(self.base_model.updated_at, initial_updated_at)

    def test_to_dict(self):
        """
        Test the to_dict method
        """
        base_dict = self.base_model.to_dict()
        self.assertIsInstance(base_dict, dict)
        self.assertIn("id", base_dict)
        self.assertIn("created_at", base_dict)
        self.assertIn("updated_at", base_dict)
        self.assertIn("__class__", base_dict)
        self.assertEqual(base_dict["__class__"], "BaseModel")
        self.assertEqual(base_dict["id"], self.base_model.id)
        self.assertEqual(base_dict["created_at"],
                         self.base_model.created_at.isoformat())
        self.assertEqual(base_dict["updated_at"],
                         self.base_model.updated_at.isoformat())

    def test_update_attribute(self):
        """
        Test updating an attribute in BaseModel
        """
        self.base_model.test_name = "test_value"
        self.assertEqual(self.base_model.test_name, "test_value")

        # Verify that the attribute is included in the string representation
        expected_str = f"[{self.base_model.__class__.__name__}] ({self.base_model.id}) {
            self.base_model.__dict__}"
        self.assertEqual(str(self.base_model), expected_str)

        # Verify that the attribute is included in the dictionary representation
        base_dict = self.base_model.to_dict()
        self.assertIn("test_name", base_dict)
        self.assertEqual(base_dict["test_name"], "test_value")


if __name__ == '__main__':
    unittest.main()
