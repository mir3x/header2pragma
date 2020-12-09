from argparse import ArgumentParser
import os
import sys
import traceback
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove, path

def replace_header(filename):
    empty_lines = 0;
    changed = 0;
    can_change = True;
    remove_next = False;
    remove_now = False;
    nested = 0
    line_number = 0
    line_changed = 0
    # try:
        #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(filename) as old_file:
            for line in old_file:
                if "#pragma once\n\n" in line:
                    break
                if remove_next and "#define" in line:
                    remove_now = True;
                remove_next = False;
                if "#ifdef" in line or "#ifndef" in line or "#if " in line.strip():
                    nested += 1
                if "#ifndef" in line.strip() and changed == 0:
                    remove_next = True;
                    line = "#pragma once"
                if "#endif" in line.strip() and not remove_now and nested == 1:
                    changed += 1
                    remove_now = True
                elif "#endif" in line.strip():
                    nested -= 1
                    remove_now = False
                if not remove_now:
                    new_file.write(line)
                else:
                    new_file.write('\n')
                    changed = True
                    line_changed = line_number
                remove_now = False
                line_number += 1

    if (changed == 1 and line_changed + 3 > line_number):
        copymode(filename, abs_path)
        remove(filename)
        move(abs_path, filename)
        print("File {} changed".format(filename))
    else:
        print("File {} NOT changed".format(filename))
        remove(abs_path)

    # except:
    #     err = sys.exc_info()[0]
    #     print(f"\033[91mError ***{err}*** when reading file {self.filename}. Exiting\033[0m")
    #     exc_type, exc_value, exc_traceback = sys.exc_info()
    #     traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    #     exit(1)


def main(input, ext):
    if input == '':
        exit(0)
    if os.path.isdir(input):
        for dirpath, dirnames, filenames in os.walk(input):
            for filename in [f for f in filenames if f.endswith(ext)]:
                x = os.path.join(dirpath, filename)
                replace_header(x)

    else:
        replace_header(input)

if __name__ == '__main__':
    parser = ArgumentParser(description='Replaced header guards with pragma')
    parser.add_argument('input', nargs='?', default='',
                        help='file/dir to check')
    parser.add_argument('-ext', type=str, metavar='string', nargs='?', default=".h",
                        help='file extension ')
    args = parser.parse_args()
    main(args.input, args.ext)
