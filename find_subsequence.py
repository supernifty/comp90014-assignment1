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

def reverse_complement(sequence):
  '''
    return the reverse complement of the input sequence
    TODO: YOU NEED TO IMPLEMENT THIS
  '''
  return sequence

def find_target(target):
  '''
    given a target sequence, read the fasta sequence from stdin and report
    any exact matches
  '''

  # this section reads the entire fasta file from stdin
  # and stores the sequence in the fasta variable
  logging.info('reading fasta file...\n')
  fasta = ''
  for line in sys.stdin:
    if line.startswith('>'):
      continue

    # append the line to fasta, 
    # ignoring any whitespace
    # we also want our string to be upper case.
    fasta += line.strip().upper()

  logging.info('searching %i bases...', len(fasta))

  # this is the part you need to implement
  # one method of finding 'target' is to slide across
  # the fasta sequence with a loop and check for an exact match at
  # each position.

  # some potentially useful things to use
  count = 0
  rctarget = reverse_complement(target)
  k = len(target)

  # TODO: YOUR CODE HERE

  logging.info("done: found %i", count)

if __name__ == '__main__':
  # accept and parse command line arguments
  parser = argparse.ArgumentParser(description='Find sequence')
  parser.add_argument('--target', required=True, help='sequence to find')
  args = parser.parse_args()

  # configure program logging
  logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  
  # find target in fasta (read from stdin)
  find_target(args.target)

