#!/usr/bin/env python3

"""
createMemFs.py - Mirrors the functionality of epicsMakeMemFs, but with more control
Designed to be used with simulated RTEMS IOCs for testing purposes
Yes, this is ugly and horrible :)
"""

import argparse
import subprocess
import re
import shutil
import os
import glob
import string
import json

fs_file = None
files = []
varname = 'epicsRtemsFSImage'
ignores: list[str] = []

template = """
static const epicsMemFile file_${SFILE} = {
    file_${SFILE}_dir,
    "${BASENAME}",
    file_${SFILE}_data,
    sizeof(file_${SFILE}_data)
};
"""

def _sanitize_name(name: str):
    return name.replace('/', '_').replace('.', '_').replace('-', '_').replace('+', '_')


# This is all so ugly
def _is_ignored(file: str) -> bool:
    if os.path.isdir(file): return True
    s = file.split('/')
    for ig in ignores:
        if any([re.match(ig, x) for x in s]):
            return True
    return False


def _add_bytes(array: bytes):
    for x in array:
        fs_file.write(f'{hex(x)},')


def _add_file(disk_path: str, basename: str, dir: str, root: str) -> bool:
    san = _sanitize_name(disk_path.lstrip(root))
    c = ", ".join([f"\"{x}\"" for x in dir.strip('/').split("/")]) + ', NULL'
    fs_file.write(f'static const char* const file_{san}_dir[] = {{ {c} }};\n')
    fs_file.write(f'static const char file_{san}_data[] = {{\n')
    with open(disk_path, 'rb') as fp:
        data = fp.read(16384) # Read in 16k blocks
        while len(data) > 0:
            _add_bytes(data)
            data = fp.read(16384)
    fs_file.write('\n};\n\n')
    fs_file.write(
        string.Template(template).substitute({
            'SFILE': san,
            'BASENAME': basename
        })
    )
    files.append(f'file_{san}')


def _add_from_dir(dir: str, root: str):
    l = glob.iglob(f'{dir}/**', recursive=True)
    for file in l:
        if not _is_ignored(file):
            dn = os.path.dirname(file)
            print(f'Adding {file}')
            _add_file(file, os.path.basename(file), f'{root}/{os.path.dirname(file)[len(dir)+1:]}', dir)


def _create_dir():
    fs_file.write('static const epicsMemFile* files[] = {\n')
    for f in files:
        fs_file.write(f' &{f},\n')
    fs_file.write(' NULL\n};')
    fs_file.write(f"""
static const epicsMemFS {varname}_image = {{&files[0]}};
const epicsMemFS* {varname} = &{varname}_image;
""")


def main():
    global varname
    parser = argparse.ArgumentParser()
    parser.add_argument('DIRS', nargs='+', help='List of directories to add to the memory fs')
    parser.add_argument('--root', default='/app', type=str, help='Root directory to place all matched files under')
    parser.add_argument('-o', '--output', dest='OUT', required=True, help='File to generate')
    parser.add_argument('--var', type=str, default=varname, help='Variable name for the FS')
    args = parser.parse_args()

    cfg = {}
    with open(f'{os.path.dirname(__file__)}/.memfs.json', 'r') as fp:
        cfg = json.load(fp)
    global ignores
    ignores = cfg['ignore']
    ignores.append(args.OUT)

    varname = args.var

    global fs_file
    fs_file = open(args.OUT, 'w')
    fs_file.write('// WARNING: Generated file! Do not modify if you want to live!\n\n\n#include <epicsMemFs.h>\n\n')

    for d in args.DIRS:
        _add_from_dir(d, args.root)
    _create_dir()


if __name__ == '__main__':
    main()
