#!/usr/bin/env python
'''
  count prevalence of typical PAM seqences in an input fasta file

  Usage: 
    python find_pam.py < target.fa    
'''

import argparse
import collections
import logging
import sys

COMPLEMENT = { 'A': 'T', 'C': 'G', 'T': 'A', 'G': 'C', 'N': 'N' }
PAMS = set(['NGG', 'NNAGAA', 'NNNNGATT', 'NAAAAN'])

def reverse_complement(s):
  return ''.join(reversed([COMPLEMENT[x] for x in s]))

def test_current(fasta, idx, subsequence):
  '''
    tests the current location (idx) of the fasta sequence for the specified subsequence or the reverse complement of the subsequence
  '''
  if idx < len(fasta) - len(subsequence):
    for p in range(len(subsequence)):
      if subsequence[p].upper() != 'N' and subsequence[p].upper() != fasta[idx + p].upper():
        return False
    return True
  return False
  #return idx < len(fasta) - len(subsequence) and (fasta[idx:idx+len(subsequence)].upper() == subsequence or fasta[idx:idx+len(subsequence)].upper() == reverse_complement(subsequence))

def find_pams():
  logging.info('reading fasta file...')
  fasta = ''
  for line in sys.stdin:
    if line.startswith('>'):
      continue
    fasta += line.strip()

  logging.info('searching %i bases...', len(fasta))

  counts = collections.defaultdict(int)
  
  for idx in range(len(fasta)):
    # check for each pam
    for pam in PAMS:
      if test_current(fasta, idx, pam) or test_current(fasta, idx, reverse_complement(pam)):
        counts[pam] += 1

    if idx % 1000000 == 0:
      logging.info('processed %i', idx)

  # done counting
  sys.stdout.write('pam\tcount\t%\n')
  for pam in PAMS:
    sys.stdout.write('{}\t{}\t{:.1f}\n'.format(pam, counts[pam], 100. * counts[pam] / len(fasta)))

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  find_pams()

