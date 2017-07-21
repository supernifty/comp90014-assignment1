#!/usr/bin/env python
'''
  search a fasta file for a specific sequence

  Usage:
    python find_sequence.py --target ATAAT < sequence.fa
'''

import argparse
import collections
import logging
import sys

COMPLEMENT = { 'A': 'T', 'C': 'G', 'T': 'A', 'G': 'C' }

def reverse_complement(s):
  return ''.join(reversed([COMPLEMENT[x] for x in s]))

def find_target(target='TGCTAGTCTGGAGTTGATCA'):
  logging.info('reading fasta file...\n')
  fasta = ''
  for line in sys.stdin:
    if line.startswith('>'):
      continue
    fasta += line.strip()

  logging.info('searching %i bases...', len(fasta))

  count = 0
  rctarget = reverse_complement(target)
  k = len(target)

  for idx in range(len(fasta) - k + 1):
    kmer = fasta[idx:idx+k].upper()
    if kmer == target or kmer == rctarget:
      sys.stdout.write('found {} at {}\n'.format(kmer, idx))
      count += 1

    if idx % 1000000 == 0:
      logging.info('processed %i', idx)

  logging.info("done: found %i", count)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Find sequence')
  parser.add_argument('--target', required=True, help='sequence to find')
  args = parser.parse_args()
  logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  find_target(args.target)

