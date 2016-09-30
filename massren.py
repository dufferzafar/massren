#!/usr/bin/env python3

"""
rename multiple files using your text editor.

Usage:
    massren [path]

Examples:

    Process all the JPEGs in the specified directory:
    % massren /path/to/photos/*.jpg
"""

import codecs
import glob
import os
import subprocess
import tempfile


def list_matching_files(pattern):
    """ Take a pattern from the CLI and list all file that match. """

    # TODO: Decide whether we need to offload this to the shell
    return sorted(glob.glob(pattern))


def launch_text_editor(files):
    """ Create a text file, launch editor, get new file list. """

    tmp_fd, tmp_file_path = tempfile.mkstemp(prefix="massren_", text=True)

    # Write file list
    with codecs.open(tmp_file_path, "w", "utf-8") as tmp:
        tmp.write("\n".join(files))

    # Launch editor
    subprocess.call(["subl", "-w", tmp_file_path])

    # Get file list
    files = []
    with codecs.open(tmp_file_path, "r", "utf-8") as tmp:
        files = tmp.read().splitlines()

    # Delete the temp file
    os.close(tmp_fd)
    os.remove(tmp_file_path)

    return files


if __name__ == '__main__':

    import sys
    pattern = sys.argv[1]

    old_files = list_matching_files(pattern)
    new_files = launch_text_editor(old_files)
