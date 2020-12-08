# XORcrypt

Run a bytewise XOR operation on a file for a given range of bytes.
For a given directory, it will modify all files matching the given extension, including sub-directories.
The script edits files in place, make backups before running.

## Dependencies

pathlib2

## USAGE

*-file* By default the current working directory is used. If this argument is set, only the given file will be modified.

*-sbyte* Start index for the operation. Default: 0

*-nbyte* Number of bytes to modify. Set to 0 to edit all following bytes.

*-mask* Bytemask used with XOR.

*-ext* Specify the extension. Use .* to modify all files.

Example:
```
python xorCrypt.py -nbyte=1024 -mask=255 -ext=".pack"
```
