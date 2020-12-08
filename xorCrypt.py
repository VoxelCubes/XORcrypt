# -*- coding: utf-8 -*-
"""
Created on 8.12.2020

@author: Voxel
"""

import os
import sys
import time
import argparse
import pathlib2

class FileTooShort(Exception):
    pass



def file_decrypt(path, start_byte, number, mask):
    """Performs an XOR operation on the designated range of bytes."""
    data = bytearray()

    with open(path, "rb") as binfile:
        data = bytearray(binfile.read())

        if number > 0:
            try:
                for i in range(start_byte, start_byte + number):
                    data[i] = data[i] ^ mask
            except:
                raise FileTooShort()
        else:
            #modify all bytes
            for i in range(start_byte, len(data)):
                    data[i] = data[i] ^ mask


    with open(path, "wb") as binfile:
        binfile.write(data)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Edits files or directories with the XOR operation.")
    parser.add_argument("-file", default="", help="Use a file in the current directory. Default: Use the current directory.")
    parser.add_argument("-sbyte", type=int, default=0, help="The byte to start modifying.")
    parser.add_argument("-nbyte", type=int, default=1024, help="Number of bytes to modify. 0 to modify all.")
    parser.add_argument("-mask", type=int, default=0xFF, help="Byte mask used with XOR.")
    parser.add_argument("-ext", default="", help="The file extension to match.")
    args = parser.parse_args()

    #flags
    file = args.file
    start_byte = args.sbyte
    number_bytes = args.nbyte
    mask_byte = args.mask
    file_ext = args.ext

    #handle args
    directory = pathlib2.Path(os.getcwd() + file)

    if not file_ext.startswith('.'):
        file_ext = '.' + file_ext

    #walk directory
    file_paths = []

    if os.path.isdir(directory):
        file_paths = list(directory.rglob(f"*{file_ext}"))
    elif os.path.isfile(directory):
        file_paths.append(directory)
    else:
        sys.exit("ERROR: Directory not found!")

    if not file_paths:
        sys.exit("ERROR: No files found!")
    #consent
    print(f"\nFound {len(file_paths)} file{'s' if len(file_paths) > 1 else ''}:")

    for i,file in enumerate(file_paths):
        print(file.name)
        if i >= 9:
            print("...")
            break

    print(f"\nBytes {start_byte} through {start_byte + number_bytes - 1 if number_bytes > 0 else 'to the end'} will recieve the XOR operation with {mask_byte}")
    if not input("\nProceed to edit files? CANNOT BE UNDONE! [y/n]: ").upper()[0] == 'Y':
        print("...Process aborted.")
        sys.exit()

    #modify all files
    print("Starting modifications...")
    tic = time.perf_counter()

    for path in file_paths:
        try:
            file_decrypt(path, start_byte, number_bytes, mask_byte)
        except FileTooShort:
            print(f"WARNING: file {path.name} too short, skipping...")
            continue

    toc = time.perf_counter()
    print(f"Finished in {toc - tic:0.4f} seconds")
