from argparse import ArgumentParser
import os
import sys
import traceback
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove, path

def rem_empty_lines(filename):
    changed = False;
    ignore_next = False;
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(filename) as old_file:
            remove_now = False
            for line in old_file:
                linestripped = line.strip()
                if not remove_now or line.strip() != '':
                    new_file.write(line)
                else:
                    changed = True
                if linestripped.endswith('{') and not ignore_next:
                    remove_now = True;
                else:
                    remove_now = False;
                #dont removed defines
                if linestripped.endswith('\\'):
                    ignore_next = True
                else:
                     ignore_next = False

    if (changed):
        copymode(filename, abs_path)
        remove(filename)
        move(abs_path, filename)
        print("File {} changed".format(filename))
    else:
        print("File {} NOT changed".format(filename))
        remove(abs_path)


def main(input, ext):
    if input == '':
        exit(0)
    if os.path.isdir(input):
        for dirpath, dirnames, filenames in os.walk(input):
            for filename in [f for f in filenames if f.endswith(ext)]:
                x = os.path.join(dirpath, filename)
                rem_empty_lines(x)

    else:
        rem_empty_lines(input)

if __name__ == '__main__':
    parser = ArgumentParser(description='Removes empty lines after block')
    parser.add_argument('input', nargs='?', default='',
                        help='file/dir to check')
    parser.add_argument('-ext', type=str, metavar='string', nargs='?', default=".cpp",
                        help='file extension ')
    args = parser.parse_args()
    main(args.input, args.ext)
