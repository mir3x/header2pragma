from argparse import ArgumentParser
import os
import sys
import traceback
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove, path

def remove_lines(filename, numlines):
    empty_lines = 0;
    line_number = 0;
    old_line = None
    try:
        #Create temp file
        fh, abs_path = mkstemp()
        with fdopen(fh,'w') as new_file:
            with open(filename) as old_file:
                for line in old_file:
                    line_number += 1;
                    if line.strip() == '':
                        empty_lines += 1;
                    else:
                        empty_lines = 0;
                    if empty_lines < numlines and old_line:
                        new_file.write(old_line)
                    else:
                        if (line_number > 1):
                            print("removed line {} in {}".format(line_number - 1, filename))
                    old_line = line
                if old_line != '':
                    new_file.write(old_line)
        copymode(filename, abs_path)
        remove(filename)
        move(abs_path, filename)

    except:
        err = sys.exc_info()[0]
        print(f"\033[91mError ***{err}*** when reading file {self.filename}. Exiting\033[0m")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        exit(1)


def main(input, numlines, ext):
    if input == '':
        exit(0)
    if os.path.isdir(input):
        for dirpath, dirnames, filenames in os.walk(input):
            for filename in [f for f in filenames if f.endswith(ext)]:
                x = os.path.join(dirpath, filename)
                remove_lines(x , numlines)

    else:
        remove_lines(input, numlines)

if __name__ == '__main__':
    parser = ArgumentParser(description='Empty Line Remover')
    parser.add_argument('input', nargs='?', default='',
                        help='file/dir to check')
    parser.add_argument('-ext', type=str, metavar='string', nargs='?', default="cpp",
                        help='file extension')
    parser.add_argument('-lines', type=int, metavar='lines', nargs='?', default="3",
                        help='Remove lines if there is *lines* in a row ')
    args = parser.parse_args()
    main(args.input, args.lines, args.ext)