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

from collections import namedtuple

# TODO: Move to class?
FileAction = namedtuple('FileAction', ['kind', 'old', 'new'])
FA_Rename = 1
FA_Delete = 2


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


def get_actions_from_diff(old_files, new_files):
    """
    Use difflib to generate a list of file actions.

    This method will NOT detect changes correctly in all cases,
    but it allows you to delete lines to mark files as deleted.
    """

    import difflib

    d = difflib.SequenceMatcher(None, old_files, new_files)

    for tag, alo, ahi, blo, bhi in d.get_opcodes():
        if tag == 'replace':
            for old, new in zip(old_files[alo:ahi], new_files[blo:bhi]):
                yield FileAction(FA_Rename, old, new)
        elif tag == 'delete':
            for old in old_files[alo:ahi]:
                yield FileAction(FA_Delete, old, '')


if __name__ == '__main__':

    import sys
    pattern = sys.argv[1]

    old_files = list_matching_files(pattern)
    new_files = launch_text_editor(old_files)
