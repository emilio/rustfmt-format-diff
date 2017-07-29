#!/usr/bin/env python
#
# rustfmt-format-diff.py

import argparse
import re
import json
import subprocess
import sys


def main():
  parser = argparse.ArgumentParser(description=
                                   'Reformat changed lines in diff. Without -i '
                                   'option just output the diff that would be '
                                   'introduced.')
  parser.add_argument('-i', action='store_true', default=False,
                      help='apply edits to files instead of displaying a diff')
  parser.add_argument('-p', metavar='NUM', default=0,
                      help='strip the smallest prefix containing P slashes')
  parser.add_argument('-iregex', metavar='PATTERN', default=r'.*\.rs',
                      help='custom pattern selecting file paths to reformat '
                      '(case insensitive, overridden by -regex)')
  parser.add_argument('-v', '--verbose', action='store_true',
                      help='be more verbose')
  parser.add_argument('-binary', default='rustfmt',
                      help='location of binary to use for rustfmt')
  args = parser.parse_args()

  # Extract changed lines for each file.
  filename = None
  ranges = []
  files = set()
  for line in sys.stdin:
    match = re.search('^\+\+\+\ (.*?/){%s}(\S*)' % args.p, line)
    if match:
      filename = match.group(2)
    if filename == None:
      continue

    if not re.match('^%s$' % args.iregex, filename, re.IGNORECASE):
      continue

    match = re.search('^@@.*\+(\d+)(,(\d+))?', line)
    if match:
      start_line = int(match.group(1))
      line_count = 1
      if match.group(3):
        line_count = int(match.group(3))
      if line_count == 0:
        continue
      end_line = start_line + line_count - 1;
      filename = filename.strip()
      files.add(filename)
      ranges.append({
        "file": filename,
        "range": [start_line, end_line],
      })

  if len(ranges) == 0:
    if args.verbose:
      print("No ranges found")
    return

  ranges_json = json.dumps(ranges)
  command = [args.binary, '--file-lines', ranges_json]
  command.extend(files)
  if args.verbose:
    print(command)
  p = subprocess.Popen(command, stdout=subprocess.PIPE,
                       stderr=None, stdin=subprocess.PIPE)
  stdout, stderr = p.communicate()
  if args.verbose:
    print(stdout)
    print(stderr)
  if p.returncode != 0:
    sys.exit(p.returncode);

if __name__ == '__main__':
  main()
