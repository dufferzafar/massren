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


class FileDelete():

    def __init__(self, old):
        self.old = old

    def __repr__(self):
        return "Delete: '%s'" % self.old

    def perform(self):
        # TODO: Handle conflicts that can occur.
        os.remove(self.old)


class FileRename():

    def __init__(self, old, new):
        self.old = old
        self.new = new

    def __repr__(self):
        return "Rename: '%s' -> '%s'" % (self.old, self.new)

    def perform(self):
        # TODO: Handle conflicts that can occur.
        os.makedirs(self.new)
        os.rename(self.old, self.new)


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


def get_actions_diff(old_files, new_files):
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
                yield FileRename(old, new)
        elif tag == 'delete':
            for old in old_files[alo:ahi]:
                yield FileDelete(old)


def get_actions_line(old_files, new_files):
    """
    Perform line by line comparisons to generate a list of file actions.

    * Requires both the lists to be of the same length.
    * Deletes are represented by commenting out the files (prepending '//')
    """

    assert len(old_files) == len(new_files)

    for old, new in zip(old_files, new_files):
        if new.startswith("//"):
            yield FileDelete(old)
        elif old != new:
            yield FileRename(old, new)


if __name__ == '__main__':

    import sys
    pattern = sys.argv[1]

    old_files = list_matching_files(pattern)
    new_files = launch_text_editor(old_files)

    file_actions = get_actions_line(old_files, new_files)

    for act in file_actions:
        print(act)
