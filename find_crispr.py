#!/usr/bin/env python
'''
  locates potential CRISPR sites by finding nearby repeats that are 
  longer than some specified minimum and have a gap (spacer) within
  some specified range.

  Usage:
    python find_crispr.py < bacteria.fa
'''

import argparse
import collections
import logging
import sys

def find_crispr(min_repeat=23, min_spacer=20, max_spacer=50):
  # read the fasta file
  logging.info("reading file...")
  fasta = ''
  for line in sys.stdin:
    if line.startswith('>'):
      continue
    fasta += line.strip()

  # build the position of all kmers within the fasta sequence
  logging.info("building kmers...")
  kmers = collections.defaultdict(list)
  for idx in range(0, len(fasta) - min_repeat + 1):
    kmer = fasta[idx:idx+min_repeat]
    kmers[kmer].append(idx)

  # find repeated kmers that are within some range
  logging.info("analysing...")
  sys.stdout.write('potential crispr sites:\n')
  sys.stdout.write('#pos,pre,spacer,post\n')
  for kmer in kmers: # every kmer
    for idx in range(len(kmers[kmer])-1): # every position for each kmer
      next_repeat_dist = kmers[kmer][idx+1] - kmers[kmer][idx]
      if min_spacer + min_repeat < next_repeat_dist < max_spacer + min_repeat:
        start_first_repeat = kmers[kmer][idx]
        start_second_repeat = kmers[kmer][idx + 1]
        # potential crispr site
        sys.stdout.write('{},{},{},{}\n'.format(start_first_repeat, kmer, fasta[start_first_repeat + min_repeat:start_second_repeat], fasta[start_second_repeat:start_second_repeat + min_repeat]))

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Find sequence')
  parser.add_argument('--min_repeat', type=int, default=32, help='min repeat length')
  parser.add_argument('--min_spacer', type=int, default=20, help='min spacer length')
  parser.add_argument('--max_spacer', type=int, default=50, help='max spacer length')
  args = parser.parse_args()
  logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  find_crispr(args.min_repeat, args.min_spacer, args.max_spacer)
