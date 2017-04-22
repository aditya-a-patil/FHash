#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
``FHash`` is a GUI enabled python script to compute hash files in a directory
and verify the hashes generated to check if files were changed/altered.
List of hashes created is stored in a text file with **current timestamp**
as filename.
\nFormat of hash stored is as follows:

.. centered:: ABSOLUTE_PATH_TO_FILE|DIGEST_ALGORITHM|HASH

.. note::
    * '|' is used as a delimitter.
    * Hash algorithm used must be supported by Hashlib.

"""

import os
import datetime
import hashlib

from lib.appJar import gui

# String constants
HASH_FILENAME = "Hash%s.txt"
CNFM_INSECURE_DGST = "Algorithm has known hash collision weakness.\nProceed?"
HASH_SUCCESS = "Hashed %d files."
VERIFY_SUCCESS = "Successfully verified %d files."
INFO = "Info"
ERR = "Error"
ERR_DESTINATION = "Please choose a valid file with hash list to verify."
ERR_SOURCE = "No source directory selected."
ERR_NOFILE = "No file found to verify"
ERR_HASH = "Found %d Errors.\nHashed %d/%d files"
ERR_VERIFY = "Verified %d/%d files.\nFailed to verify following files:\n%s"
ERR_WRITING = "Error while writing to file."
ERR_UNEXPECTED = "Unexpected Error"
MISSING_DIGEST = "Please select a digest to use."
HASH_LIST_DIRECTORY = "Choose a directory where you want to save hash list."

# Supported digests
SUPPORTED_DIGESTS = ["- DIGEST ALGORITHM -", "MD5", "SHA1", "SHA224",
                     "SHA256", "SHA384", "SHA512"]

# List of insecure digests.
# Prompt user of inherent security risk of using these algorithms.
INSECURE_DIGESTS = ['md5', 'sha1']


def sanity_check_source(s):
    """Sanity check if directory or file exists.

    :param s: source directory/file to to check for existance
    :return: 0 if error else 1 if no error
    :rtype: int
    """
    if not os.path.isdir(s):
        app.errorBox(ERR, ERR_SOURCE)
        return 0
    return 1


def sanity_check_destination(d):
    """Sanity check if hash file exists.

    :param d: hash file to to check for existance
    :return: 0 if error else 1 if no error
    :rtype: int
    """
    if not os.path.isfile(d):
        app.errorBox(ERR, ERR_DESTINATION)
        return 0
    return 1


def write_file(result):
    """Write result to file that user will choose.

    :param result: result to be written
    """
    now = datetime.datetime.now()
    destination_dir = app.directoryBox(HASH_LIST_DIRECTORY)
    filename = str(now.strftime("%Y%m%d%H%M%S"))
    destination_file = os.path.join(destination_dir, HASH_FILENAME % filename)
    try:
        with open(destination_file, 'w') as f:
            f.write(result)
        f.close()
    except Exception, e:
        app.errorBox(ERR, ERR_WRITING)
        return 0


def hash_file(filename, digest):
    """Hash file

    :param source: source directory in which all files are to be hashed
    :param digest: digest algorithm to use
    """
    if digest == 'md5':
        h = hashlib.md5()
    elif digest == 'sha1':
        h = hashlib.sha1()
    elif digest == 'sha224':
        h = hashlib.sha224()
    elif digest == 'sha256':
        h = hashlib.sha256()
    elif digest == 'sha384':
        h = hashlib.sha384()
    elif digest == 'sha512':
        h = hashlib.sha512()
    else:
        return ERR
    with open(filename) as f:
        h.update(f.read())
    f.close()
    return h.hexdigest()


def iter_verify(destination):
    """Iterate through all files in hash list and verify.

    :param destination: file with target filenames, digest algorithm and hash
    """
    ctr = 0
    err = 0
    atleast_one_file = False
    err_list = []
    with open(destination, 'r') as f:
        for line in f:
            try:
                filename = line.split("|")[0]
                digest_algorithm = line.split("|")[1]
                old_digest = line.split("|")[2].rstrip()

                if os.path.isfile(filename):
                    atleast_one_file = True
                else:
                    err += 1
                    ctr += 1
                    err_list.append(filename)
                    continue

                new_digest = hash_file(filename, digest_algorithm)
                if new_digest != old_digest:
                    err += 1
                    err_list.append(filename)
                ctr += 1
            except Exception, e:
                continue
    f.close()

    if not atleast_one_file:
        app.errorBox(ERR, ERR_NOFILE)
    elif err > 0:
        app.errorBox(ERR, ERR_VERIFY % ((ctr-err), ctr,
                                        ', '.join(map(str, err_list))))
    else:
        app.infoBox(INFO, VERIFY_SUCCESS % (ctr))


def iter_hash(source, digest_algorithm):
    """Iterate through all files in source list and hash.

    :param source: source directory in which all files are to be hashed
    :param digest_algorithm: digest algorithm to use
    """
    ctr = 0
    err = 0
    result_str = ''
    for root, dirs, files in os.walk(source, topdown=True):
        total_files = len(files)
        for name in files:
            digest = hash_file(os.path.join(root, name), digest_algorithm)
            result_str = result_str + '%s|%s|%s\n' % (os.path.join(root, name),
                                                      digest_algorithm,
                                                      digest)
            if digest == ERR:
                err += 1
            ctr += 1

    try:
        write_file(result_str)
    except Exception, e:
        app.errorBox(ERR, ERR_UNEXPECTED)
        return 0

    if err > 0:
        app.errorBox(ERR, ERR_HASH % (err, (ctr-err), ctr))
    else:
        app.infoBox(INFO, HASH_SUCCESS % (ctr))


def choose_file(btn):
    """Action function for file interaction buttons.

    :param btn: identifier of button being pressed
    """
    if 'Source' in btn:
        src = app.directoryBox()
        app.setEntry('src', src)
    else:
        dest = app.openBox(title="Destination directory",
                           dirName=None,
                           fileTypes=None,
                           asFile=False)
        if dest is not None:
            app.setEntry('dest', dest)


def press(btn):
    """Function called by pressing the action buttons in GUI.

    :param btn: identifier of button being pressed
    """
    if btn == "Close":
        app.stop()
    elif btn == "Hash":

        source = app.getEntry('src')
        if not sanity_check_source(source):
            return 0

        try:
            digest_algorithm = app.getOptionBox("Digest").lower()
        except Exception, e:
            app.warningBox(ERR, MISSING_DIGEST)
            return 0

        if digest_algorithm in INSECURE_DIGESTS:
            if not app.yesNoBox("Confirm Digest",
                                CNFM_INSECURE_DGST):
                return 0
        iter_hash(source, digest_algorithm)
    elif btn == 'Verify':
        destination = app.getEntry('dest')
        if not sanity_check_destination(destination):
            return 0
        iter_verify(destination)


def main():
    """Main function for FCopy."""

    global app

    # initialize app gui
    app = gui("FHash", "600x400")
    app.setFont(16, "Helvetica")
    # app.setBg("lightblue")

    # Counter to maintain current row of widget
    widget_row = 0

    # Row 0, Column 0, Span 2
    app.addLabel("FHash", "Welcome to File Hash", widget_row, 0, 3)
    widget_row += 1

    # Hash Group - Begin
    app.startLabelFrame("Hash")

    # Row 1, Column 0+1
    app.addLabel("src", "Directory to hash:", widget_row, 0)
    app.addEntry("src", widget_row, 1)
    app.addButtons(["Source\ndirectory"], choose_file, widget_row, 2)
    widget_row += 1

    # Row 2, Option Box
    app.addOptionBox("Digest", SUPPORTED_DIGESTS, widget_row, 1)
    widget_row += 1

    app.stopLabelFrame()
    # Hash Group - End

    # Verify group - Begin
    app.startLabelFrame("Verify")

    # Row 3, Column 0+1
    app.addLabel("dest", "Hash list to verify:", widget_row, 0)
    app.addEntry("dest", widget_row, 1)
    app.addButtons(["Hash\nList"], choose_file, widget_row, 2)
    widget_row += 1

    app.stopLabelFrame()
    # Verify group - End

    # Row 5,Column 0,Span 2
    app.addButtons(["Hash", "Verify", "Close"], press, widget_row, 0, 3)

    # Launch gui
    app.go()


if __name__ == "__main__":
    main()
