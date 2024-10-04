import hashlib
import os
import tempfile
import unittest

from ecutils.utils import calculate_file_hash


class TestFileHashing(unittest.TestCase):

    def generate_expected_hash(self, file_path, block_size=16384):
        """Computes the expected SHA-256 hash using hashlib."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(block_size), b""):
                hash_sha256.update(block)
        return int(hash_sha256.hexdigest(), 16)

    def test_calculate_file_hash(self):
        """Test the file hashing function with a temporary file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_path = temp_file.name
            # Write some data to the file
            temp_file.write(b"Sample data for hashing")

        try:
            # Calculate the hash using the function being tested
            calculated_hash = calculate_file_hash(file_path)

            # Calculate the expected hash manually
            expected_hash = self.generate_expected_hash(file_path)

            # Compare the hashes
            self.assertEqual(
                calculated_hash, expected_hash, "The file hashes do not match!"
            )
        finally:
            # Clean up the temporary file
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_file_not_found_error(self):
        """Test the handling of FileNotFoundError in calculate_file_hash."""
        non_existent_file = "non_existent_file.txt"

        # Ensure the file does not exist
        if os.path.exists(non_existent_file):
            os.remove(non_existent_file)

        # Expecting a FileNotFoundError when trying to hash a non-existent file
        with self.assertRaises(FileNotFoundError) as context:
            calculate_file_hash(non_existent_file)

        # Check if the raised error message contains the correct file information
        self.assertIn(f"File not found: {non_existent_file}", str(context.exception))
