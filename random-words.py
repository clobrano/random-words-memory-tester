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

import datetime
import docopt
import logging
import os
import pickle
import random
import sys
import time

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

home = os.path.expanduser('~/')
testfile = '/tmp/random-words.' + flags['--lang']
starttime = os.path.join('/', 'tmp','random-words.start')
report = os.path.join(home, 'Dropbox', 'random-word-report.txt')

def start():
    ''' Generate a list of random words in the given language'''
    words_files = { 'it' : './words-it.txt'}
    words_file = words_files[flags['--lang']]
    dbg(words_file)

    it_words = open(words_file).read().splitlines()
    it_words_len = len(it_words)

    selection_len = int(flags['--num'])
    selection = random.sample(it_words, selection_len)
    with open(testfile, 'w') as f:
        for id, word in enumerate(selection):
            f.write(word.lower() + '\n')
            print('{id} | {word}'.format(id=id, word=word.lower()))
    with open(starttime, 'w') as f:
        pickle.dump(datetime.datetime.now(), f)

def test():
    '''Test memory and recall on a list of words'''
    now = datetime.datetime.now()
    info('Wait 60 seconds before begin test')
    time.sleep(60)
    try:
        with open(starttime, 'r') as f:
            start_time = pickle.load(f)
    except IOError:
        fatal('Test is not started yet. Run --start first')


    try:
        with open(testfile) as f:
            selection = f.read().splitlines()
        os.remove(testfile)
    except IOError:
        fatal('Could not find any generated random words. Run the script with --generate flag first')

    correct = 0
    for id, word in enumerate(selection):
        guess = raw_input('word #{num}: '.format(num=id + 1))
        if guess != word:
            info('{word} != {guess}'.format(word=word, guess=guess))
        else:
            correct += 1

    delta = str(now - start_time).split('.')[0]
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    info('Correctly guessed {num}/{full} words in {sec}'.format(num=correct, full=len(selection), sec=delta))
    with open(report, 'a') as f:
        f.write('{date} {num}/{full} words in {sec}\n'.format(date=today, num=correct, full=len(selection), sec=delta))



if __name__ == '__main__':
    if flags['--start']:
        start()
    elif flags['--test']:
        test()
    else:
        pass

