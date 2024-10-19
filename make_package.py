#!/usr/bin/python
import glob
import sys
import os
import shutil
import tempfile

if len(sys.argv) > 1:
    outzip = "./" + sys.argv[1]
else:
    outzip = "appsec-submission"


with open("allowed_files.txt", "rt") as f:
    file_patterns = [file.strip() for file in f.readlines()]

with tempfile.TemporaryDirectory() as tmp_dir:
    current_dir = os.getcwd()
    for pattern in file_patterns:
        print(pattern)
        base_dir = os.path.commonpath(glob.glob(pattern, recursive=True))  # Dynamic base for each pattern
        for file in glob.glob(pattern, recursive=True):
            if os.path.isfile(file):
                # Create the destination path inside the temporary directory
                dest_path = os.path.join(tmp_dir, os.path.relpath(file, current_dir))
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy(file, dest_path)

        # Create a zip archive from the temporary directory
        shutil.make_archive(outzip, 'zip', tmp_dir)
