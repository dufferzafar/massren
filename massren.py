#!/usr/bin/env python3

""" rename multiple files using your text editor. """

import glob
import os
import sys

import click

HEADER = """
Please change the filenames that need to be renamed and save the file.
Lines that are not changed will be ignored.

You may delete a file by putting "//" at the beginning of the line.
Note that this operation cannot be undone.

Do NOT swap the order of lines as this is what is used to match the original
filenames to the new ones.

Also, do NOT delete lines as the rename operation will be cancelled due to a
mismatch between the number of filenames before and after saving the file.

You may test the effect of the rename operation using the --dry-run parameter.

Caveats: massren expects filenames to be reasonably sane. Filenames that
include newlines or non-printable characters for example will probably not
work.
"""
HEADER = "\n".join(["// " + line for line in HEADER.splitlines()]) + "\n\n"


class FileDelete():

    def __init__(self, old):
        self.old = old

    def __repr__(self):
        return "Delete: '%s'" % self.old

    def perform(self):
        # TODO: Handle conflicts that can occur.
        # TODO: Use send2trash() instead of hard delete?
        os.remove(self.old)


class FileRename():

    def __init__(self, old, new):
        self.old = old
        self.new = new

    def __repr__(self):
        return "Rename: '%s' -> '%s'" % (self.old, self.new)

    def perform(self):
        new_dir = os.path.dirname(self.new)
        if new_dir:
            try:
                os.makedirs(new_dir)
            except FileExistsError:
                pass

        # TODO: Handle conflicts that can occur.
        os.rename(self.old, self.new)


def list_matching_files(pattern):
    """ Take a pattern from the CLI and list all file that match. """

    return sorted(glob.glob(pattern))


def get_files_from_editor(old_files, write_header=True):
    """ Launch editor and get new file list. """

    text = "\n".join(old_files)
    if write_header:
        text = HEADER + text

    print("Waiting for file list to be saved... (Press Ctrl + C to abort) \n")

    new_text = click.edit(
        text,
        editor="subl -w",
        # editor="suplemon",
        require_save=True
    )

    # No change
    if new_text is None:
        return old_files

    if write_header:
        new_text = new_text.splitlines()
        new_files = new_text[len(HEADER.splitlines()):]

    return new_files


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

    if len(old_files) != len(new_files):
        print("Number of files were changed.")
        sys.exit(1)

    for old, new in zip(old_files, new_files):
        if new.startswith("//"):
            yield FileDelete(old)
        elif old != new:
            yield FileRename(old, new)


@click.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
@click.option('--editor', '-e', is_flag=True,
              help="Editor to use to edit files.")
@click.option('--dry-run', '-n', is_flag=True,
              help="Only show operation that will be performed.")
@click.option('--recursive', '-R', is_flag=True,
              help="List files recursively.")
@click.option('--max-depth', '-d', is_flag=True,
              help="Maximum recursion depth.")
@click.option('--list-directories', '-D', is_flag=True,
              help="Include directories in the files buffer.")
@click.option('--show-header', '-H', is_flag=True,
              help="Add a header in the files buffer.")
@click.option('--verbose', '-v', is_flag=True,
              help="Enable verbose output.")
@click.version_option(version=0.7, prog_name="massren")
def cli(
        paths,
        recursive,
        max_depth,
        dry_run,
        editor,
        list_directories,
        show_header,
        verbose,
        ):

    # No path given, use current working directory
    if not paths:
        paths = list_matching_files("*")
    # paths is a single directory, assume we need its children
    elif len(paths) == 1:
        if os.path.isdir(paths[0]):
            paths = list_matching_files(os.path.join(paths[0], "*"))

    new_files = get_files_from_editor(paths)

    file_actions = get_actions_line(paths, new_files)

    # TODO: See what conflicts can occur

    # TODO: Perform all delete operations first.

    # Execute the actions now
    for action in file_actions:

        if verbose or dry_run:
            print(action)

        if not dry_run:
            action.perform()


if __name__ == '__main__':
    cli()
