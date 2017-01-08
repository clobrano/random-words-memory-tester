#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Random word training.
Generate a list of random words and test your memory and recall
usage:
    generator.py [--lang=<lang>] --start [--debug] [--num=<num>]
    generator.py [--lang=<lang>] --test [--debug]

options:
    -d, --debug                 enable debug logging
    -l <lang>, --lang=<lang>    language of the words [default: it]
    -n <num>, --num=<num>       Number of words in the list [default: 10]
    -s, --start                 generate a list of random words and start the timer
    -t, --test                  test your knowledge of the last random word list
'''
# Read file
# randomly select N words
# Show the the list of N words
# Count study time
# Clear list
# Check whether recalled words are correct (in order)

import sys
import random
import docopt
import logging
import datetime
import pickle

flags = docopt.docopt(__doc__)
if flags['--debug']:
    level = logging.DEBUG
else:
    level = logging.INFO

logging.basicConfig(level=level, format=' %(message)s')
logger = logging.getLogger(__name__)

dbg  = lambda x : logger.debug(x)
info = lambda x : logger.info(x)
def fatal(msg):
    logger.error(msg)
    sys.exit(1)

testfile = '/tmp/random-words.' + flags['--lang']
starttime = '/tmp/random-words.start'
report = '/home/carlo/Dropbox/random-word-report.txt'

def start():
    ''' Generate a list of random words in the given language'''
    words_files = { 'it' : './words.italian.txt'}
    words_file = words_files[flags['--lang']]
    dbg(words_file)

    it_words = open(words_file).read().splitlines()
    it_words_len = len(it_words)

    selection_len = int(flags['--num'])
    selection = random.sample(it_words, selection_len)
    with open(testfile, 'w') as f:
        for word in selection:
            f.write(word + '\n')
            print(word)
    with open(starttime, 'w') as f:
        pickle.dump(datetime.datetime.now(), f)

def test():
    '''Test memory and recall on a list of words'''
    now = datetime.datetime.now()
    try:
        with open(starttime, 'r') as f:
            start_time = pickle.load(f)
    except IOError:
        fatal('Test is not started yet. Run --start first')


    try:
        with open(testfile) as f:
            selection = f.read().splitlines()
    except IOError:
        fatal('Could not find any generated random words. Run the script with --generate flag first')

    for id, word in enumerate(selection):
        guess = raw_input('word #{num}: '.format(num=id + 1))
        if guess != word:
            info('{word} != {guess}'.format(word=word, guess=guess))
            break

    delta = str(now - start_time).split('.')[0]
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    info('Correctly guessed {num}/{full} words in {sec}'.format(num=id, full=len(word), sec=delta))
    with open(report, 'a') as f:
        f.write('{date} {num}/{full} words in {sec}\n'.format(date=today, num=id, full=len(word), sec=delta))



if __name__ == '__main__':
    if flags['--start']:
        start()
    elif flags['--test']:
        test()
    else:
        pass
