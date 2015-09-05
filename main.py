#main.py

from markov import *
from pysynth_b import *
from subprocess import check_output, call
from ast import literal_eval
from math import fabs


def float_cmp(a, b):
    eps = .001
    return fabs(a - b) < eps

def replace_notes(l):
    for elem in l:
        c = elem[1]
        if (float_cmp(c, 5.3333)): elem[1] = -8
        if (float_cmp(c, 2.6666)): elem[1] = -4
        if (float_cmp(c, 1.3333)): elem[1] = -2
    return l

def run():

    #Read input trainer file
    s = check_output("python read_abc.py learn3.abc")
    a = literal_eval(s)
    #s = check_output("python read_abc.py learn2.abc")
    #b = literal_eval(s)

    #Parse input
    a = replace_notes(a)
    #b = replace_notes(b)

    #Remove duplicates
    l_step = list(set(x[0] for x in a))
    l_beat = list(set(x[1] for x in a))
    #r_step = list(set(x[0] for x in b))
    #r_beat = list(set(x[1] for x in b))

    #Instantiate Song class
    l_song = Song(l_step, l_beat)
    r_song = Song(r_step, r_beat)

    #Train model
    for elem in a:
        l_song.add_note(elem)
    #for elem in b:
    #    r_song.add_note(elem)

    #Generating new song
    #2 channels: left and right
    l_result = [tuple(a[0])]
    for i in xrange(150):
        l_result.append(l_song.next_note(l_result[i]))

    #r_result = [tuple(b[0])]
    #for j in xrange(150):
    #    r_result.append(r_song.next_note(r_result[j]))

    make_wav(l_result, fn = "l.wav")
    #make_wav(r_result, fn = "r.wav")

    #Mix the two channels
    #call("python mixfiles.py l.wav r.wav result.wav")

run()
