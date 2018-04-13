import random
import sys
import json
from musicInfo import *

class NGramModel(object):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  This is the NGramModel constructor. It sets up an empty
                  dictionary as a member variable. It is called from the
                  constructors of the NGramModel child classes. This
                  function is done for you.
        """
        self.nGramCounts = {}

    def __str__(self):
        """
        Requires: nothing
        Modifies: nothing
        Effects:  Returns the string to print when you call print on an
                  NGramModel object. This string will be formatted in JSON
                  and display the currently trained dataset.
                  This function is done for you.
        """
        return self.__class__.__name__ + ':\n' +\
            json.dumps(
                       self.nGramCounts,
                       sort_keys=True,
                       indent=4,
                       separators=(',', ': ')
            )

    def prepData(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: nothing
        Effects:  returns a copy of text where each inner list starts with
                  the symbols '^::^' and '^:::^', and ends with the symbol
                  '$:::$'. For example, if an inner list in text were
                  ['hello', 'goodbye'], that list would become
                  ['^::^', '^:::^', 'hello', 'goodbye', '$:::$'] in the
                  returned copy.
        """
        textCopy = []
        for line in text:
            textCopy.append(['^::^', '^:::^'] + line + ['$:::$'])
        return textCopy

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts
        Effects:  this function populates the self.nGramCounts dictionary.
                  It does not need to be modified here because you will
                  override it in the NGramModel child classes according
                  to the spec.
        """
        pass

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns a bool indicating whether or not this n-gram model
                  can be used to choose the next token for the current
                  sentence. This function does not need to be modified because
                  you will override it in NGramModel child classes according
                  to the spec.
        """
        pass

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. This function does not need to be
                  modified because you will override it in the NGramModel child
                  classes according to the spec.
        """
        pass

    def weightedChoice(self, candidates):
        """
        Requires: candidates is a dictionary; the keys of candidates are items
                  you want to choose from and the values are integers
        Modifies: nothing
        Effects:  returns a candidate item (a key in the candidates dictionary)
                  based on the algorithm described in the spec.
        """
        #create a list of the keys in candidates
        words = []
        for key in candidates:
            words.append(key)
        #create a list of the values in candidates
        values = []
        for key in candidates:
            values.append(candidates[key])
        #create the list of cumulative values
        cumulative = []
        count = 0
        for number in values:
            count += number
            cumulative.append(count)
        #get a random number between [1, last number in cumulative]
        x = random.randrange(0, cumulative[-1])
        #as soon as the cumulative value is higher than random number, return key
        for i in range(len(words)):
            if cumulative[i] > x:
                return words[i]

    def getNextToken(self, sentence):
        """
        Requires: sentence is a list of strings, and this model can be used to
                  choose the next token for the current sentence
        Modifies: nothing
        Effects:  returns the next token to be added to sentence by calling
                  the getCandidateDictionary and weightedChoice functions.
                  For more information on how to put all these functions
                  together, see the spec.
        """
        return self.weightedChoice(self.getCandidateDictionary(sentence))

    def getNextNote(self, musicalSentence, possiblePitches):
        """
        Requires: musicalSentence is a list of PySynth tuples,
                  possiblePitches is a list of possible pitches for this
                  line of music (in other words, a key signature), and this
                  model can be used to choose the next note for the current
                  musical sentence
        Modifies: nothing
        Effects:  returns the next note to be added to the "musical sentence".
                  For details on how to do this and how this will differ
                  from getNextToken, see the spec.
        """
        #makes dict consisting of possible notes
        allCandidates = self.getCandidateDictionary(musicalSentence)
        #makes new dict consisting of possible notes that are also in the key signature
        constrainedCandidates = {}
        for note in allCandidates:
            if note[0][: -1] in possiblePitches or note == '$:::$':
                constrainedCandidates[note] = allCandidates[note]
        if constrainedCandidates != {}:
            return self.weightedChoice(constrainedCandidates)
        else:
            return (random.choice(possiblePitches) + '4', random.choice(NOTE_DURATIONS))

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    # Add your tests here
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    choices = { 'the': 2, 'quick': 1, 'brown': 1 }
    mod = NGramModel()
    print(mod)
    dict = {'the' : 2, 'birthday' : 5, 'python' : 1, 'jessica' : 10, 'aaron' : 9, 'brad' : 48, 'seven' : 6}
    sentence = ['happy', 'birthday']
    mod.weightedChoice(dict)
