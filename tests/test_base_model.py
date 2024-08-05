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

    def tearDown(self) -> None:
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
        file_path = FileStorage._FileStorage__file_path  # Accessing the mangled name
        if os.path.isfile(file_path):
            os.remove(file_path)

    def test_str(self):
        """
        Test the __str__ method
        """
        self.assertIsInstance(str(self.base_model), str)

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
        self.assertIsInstance(self.base_model.to_dict(), dict)


if __name__ == '__main__':
    unittest.main()
