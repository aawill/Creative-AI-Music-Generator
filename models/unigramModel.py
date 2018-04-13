import random
from nGramModel import *

class UnigramModel(NGramModel):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the UnigramModel object)
        Effects:  this is the UnigramModel constructor, which is done
                  for you. It allows UnigramModel to access the data
                  in the NGramModel class by calling the NGramModel
                  constructor.
        """
        super(UnigramModel, self).__init__()

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts
        Effects:  this function populates the self.nGramCounts dictionary,
                  which is a dictionary of {string: integer} pairs.
                  For further explanation of UnigramModel's version of
                  self.nGramCounts, see the spec.

                  Note: make sure to use the return value of prepData to
                  populate the dictionary, which will allow the special
                  symbols to be included as their own tokens in
                  self.nGramCounts. For more details, see the spec.
        """
        #adds beginning and ending characters to text
        text = self.prepData(text)
        #looks through each word of each line
        for line in text:
            for word in range(len(line)):
                #doesn't count beginning characters as words
                if line[word] != '^::^' and line[word] != '^:::^':
                    #if current word is not a key in nGramcounts, adds it with value of 1
                    if line[word] not in self.nGramCounts:
                        self.nGramCounts[line[word]] = 1
                    else:
                        #increments value associated with word
                        self.nGramCounts[line[word]] += 1

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the UnigramModel, see the spec.
        """
        #returns true if nGramCounts is not empty
        if bool(self.nGramCounts):
            return True
        else:
            return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNgGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  UnigramModel sees as candidates, see the spec.
        """
        return self.nGramCounts

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    textA = ['this', 'is', 'a', 'sentence']
    textB = []
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    text2 = [ ['boy', 'you\'re', 'gonna', 'carry', 'that', 'weight'], 
            ['carry', 'that', 'weight', 'a', 'long', 'time'], 
            ['boy', 'you\'re', 'gonna', 'carry', 'that', 'weight'], 
            ['carry', 'that', 'weight', 'a', 'long', 'time']]
    sentence = [ 'brown' ]
    cScale = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
    music = [ [('c4', 3), ('db3', 4), ('e5', 5), ('f4', 2)], 
              [('g#3', 3), ('a5', 4), ('b2', 2)] ]
    uni = UnigramModel()
    print(uni)
    uni.trainModel(music)
    print uni.trainingDataHasNGram(textA)
    print uni.getNextToken(textA)
    print uni.getNextNote(music, cScale)
