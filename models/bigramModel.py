import random
from nGramModel import *


class BigramModel(NGramModel):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the BigramModel object)
        Effects:  this is the BigramModel constructor, which is done
                  for you. It allows BigramModel to access the data
                  from the NGramModel class by calling the NGramModel
                  constructor.
        """
        super(BigramModel, self).__init__()

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a two-dimensional dictionary. For examples
                  and pictures of the BigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries of
                  {string: integer} pairs as values.

                  Note: make sure to use the return value of prepData to
                  populate the dictionary, which will allow the special
                  symbols to be included as their own tokens in
                  self.nGramCounts. For more details, see the spec.
        """
        text = self.prepData(text)
        for line in text:
            for word in range(len(line) - 1):
                # If first word is not already a key in nGramCounts, makes new dict
                # (Key = first word, value = {second word: 1})
                if line[word] not in self.nGramCounts.keys():
                    self.nGramCounts[line[word]] = {line[word + 1] : 1}
            
                else:
                    # Second word is already a key in first word's dict, increments value
                    if line[word + 1] in self.nGramCounts[line[word]].keys():
                        self.nGramCounts[line[word]][line[word + 1]] += 1
                    # For adding new key:value pair of second-word to first-word outer dict
                    else:
                        self.nGramCounts[line[word]].update({line[word + 1] : 1})

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 1
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the BigramModel, see the spec.
        """
        # Checks if last word in sentence is a key in nGramCounts
        if sentence[-1] in self.nGramCounts.keys():
            return True
        else:
            return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  BigramModel sees as candidates, see the spec.
        """
        # Returns dictionary of candidate words to be added to sentence
        return self.nGramCounts[sentence[-1]]

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    text.append([ 'quick', 'brown' ])
    text2 = [ ['happy', 'birthday', 'to', 'you'], ['happy', 'birthday', 'to', 'you'], ['happy', 'birthday', 'dear', 'python'], ['happy', 'birthday', 'to', 'you'] ]
    sentence = [ 'lazy', 'quick' ]
    sentence2 = [ 'boy', 'birthday']
    cScale = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
    music = [ [('c4', 3), ('db3', 4), ('e5', 5), ('f4', 2)],
             [('g#3', 3), ('a5', 4), ('b2', 2)] ]
    musicSentence = [('c4', 3), ('db3', 4), ('e5', 5)]
    musicSentence2 = [('c4', 3), ('db3', 4)]
    steve = BigramModel()
    print(steve)
    steve.trainModel(text2)
    print steve.trainingDataHasNGram(sentence2)
    print steve.getCandidateDictionary(sentence2)
    steve.getNextToken(sentence2)

    brian = BigramModel()
    brian.trainModel(music)
    brian.getNextNote(musicSentence2, cScale)

