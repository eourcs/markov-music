#markov.py
import random

class Markov:
    def __init__(self, vals):
        #Creates dictionary matching note to number (and vice-versa)
        #for easier lookup
        self.lookup = dict()
        self.rev_lookup = dict()
        for i in xrange(len(vals)):
            self.rev_lookup[i] = vals[i]
            self.lookup[vals[i]] = i
        #Creates the transition matrix
        self.matrix = [[0]*len(vals) for i in xrange(len(vals))]

    def add_val(self, prev, curr):
        #Adds values to the transition matrix
        self.matrix[self.lookup[prev]][self.lookup[curr]] += 1

    def next_val(self, prev):
        #Generates the next value and updates transition matrix
        result = self.generate_weighted_random(prev)
        self.add_val(prev, result)
        return result

    def generate_weighted_random(self, prev):
        #Generates a weighted random number
        n = self.lookup[prev]
        total = sum(self.matrix[n])
        arr_len = len(self.matrix[n])
        rand = random.randint(0, total)

        current = 0
        for i in xrange(arr_len):
            current += self.matrix[n][i]
            if rand <= current: return self.rev_lookup[i]


class Song:
    def __init__(self, step, notes):
        #Inputs notes into Markov model
        self.step = Markov(step)
        self.beat = Markov(notes)

        #Variable to keep track of previous note played
        self.prev_note = None

    def add_note(self, current):
        #When training the model, notes must be input manually
        if self.prev_note == None: self.prev_note = current
        self.step.add_val(self.prev_note[0], current[0])
        self.beat.add_val(self.prev_note[1], current[1])
        self.prev_note = current

    def next_note(self, prev):
        #Generates the next note using the Markov chain model
        return (self.step.next_val(prev[0]), self.beat.next_val(prev[1]))
