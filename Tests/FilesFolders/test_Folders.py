# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
import unittest
import os

# Custom Library

# Custom Packages
from AthenaLib.FilesFolders.Folders import (
    FolderContent_All,FolderContent_Folders,FolderContent_Files, FolderExsist,FolderContent_Files_Extension
)


# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
class Test(unittest.TestCase):
    def test_FolderContentAll(self):
        self.assertEqual(FolderContent_All("Data"), {"Data\\test", "Data\\test.txt"})

    def test_FolderContentAll_Fullpaths(self):
        self.assertEqual(
            FolderContent_All("Data", fullpaths=True),
            {f'{os.getcwd()}\\Data\\test',
             f'{os.getcwd()}\\Data\\test.txt'}
        )

    def test_FolderContentFolders(self):
        self.assertEqual(FolderContent_Folders("Data"), {"Data\\test"})

    def test_FolderContentFolders_Fullpaths(self):
        self.assertEqual(FolderContent_Folders("Data", fullpaths=True), {f'{os.getcwd()}\\Data\\test'})

    def test_FolderContentFiles(self):
        self.assertEqual(FolderContent_Files("Data"), {"Data\\test.txt"})

    def test_FolderContentFiles_Fullpaths(self):
        self.assertEqual(FolderContent_Files("Data", fullpaths=True), {f'{os.getcwd()}\\Data\\test.txt'})

    def test_FolderExsists(self):
        self.assertFalse(FolderExsist("DoesNotExsist"))
        self.assertTrue(FolderExsist("Data"))
        with self.assertRaises(FileNotFoundError):
            self.assertFalse(FolderExsist("DoesNotExsist", fatal=True))

    def test_FolderContentFiles_Extensions(self):
        self.assertEqual(
            FolderContent_Files_Extension("Data", extension=['.txt']),
            {'Data\\test.txt'}
        )
        self.assertEqual(
            FolderContent_Files_Extension("Data", extension='.txt'),
            {'Data\\test.txt'}
        )
        self.assertEqual(
            FolderContent_Files_Extension("Data", fullpaths=True, extension=['.txt']),
            {f'{os.getcwd()}\\Data\\test.txt'}
        )
        self.assertEqual(
            FolderContent_Files_Extension("Data", fullpaths=True, extension='.txt'),
            {f'{os.getcwd()}\\Data\\test.txt'}
        )
