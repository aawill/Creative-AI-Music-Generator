import random
from nGramModel import *

class TrigramModel(NGramModel):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  this is the TrigramModel constructor, which is done
                  for you. It allows TrigramModel to access the data
                  from the NGramModel class.
        """
        super(TrigramModel, self).__init__()

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a three-dimensional dictionary. For
                  examples and pictures of the TrigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries as values,
                  where those inner dictionaries have strings as keys
                  and dictionaries of {string: integer} pairs as values.

                  Note: make sure to use the return value of prepData to
                  populate the dictionary, which will allow the special
                  symbols to be included as their own tokens in
                  self.nGramCounts. For more details, see the spec.
        """
        text = self.prepData(text)
        for line in text:
            for word in range(len(line) - 2):      
                #if first word is not a key in nGramCounts
                if line[word] not in self.nGramCounts.keys():
                    #add the full 3d dict to nGramCounts with inner value 1: {word1 : {word2 : {word3 : 1}}}
                    self.nGramCounts[line[word]] = {line[word + 1] : {line[word + 2] : 1}} 
                #if first and second words are already there
                elif line[word + 1] in self.nGramCounts[line[word]].keys(): 
                    #if all three are there
                    if line[word + 2] in self.nGramCounts[line[word]][line[word + 1]].keys(): 
                        #increment trigram count
                        self.nGramCounts[line[word]][line[word + 1]][line[word + 2]] += 1 
                    #if only first and second are there, not third
                    else: 
                        #update second word's dict with a new 1d dict with key = word3, value = 1
                        self.nGramCounts[line[word]][line[word + 1]].update({line[word + 2] : 1}) 
                #if only first is there       
                else:   
                    #update first word's dict with new 2d dict with key = word2, value = {word3 : 1}
                    self.nGramCounts[line[word]].update({line[word + 1] : {line[word + 2] : 1}}) 

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 2
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the TrigramModel, see the spec.
        """
        #if last two words in sentence have appeared at start of a trigram
        if sentence[-2] in self.nGramCounts and sentence[-1] in self.nGramCounts[sentence[-2]]:
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
                  TrigramModel sees as candidates, see the spec.
        """
        return self.nGramCounts[sentence[-2]][sentence[-1]]


###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    text2 = [ ['happy', 'birthday', 'to', 'you'], 
              ['happy', 'birthday', 'to', 'you'], 
              ['happy', 'birthday', 'dear', 'python'], 
              ['happy', 'birthday', 'to', 'you'] ]
    text3 = [ ['boy', 'you\'re', 'gonna', 'carry', 'that', 'weight'], 
              ['carry', 'that', 'weight', 'a', 'long', 'time'], 
              ['boy', 'you\'re', 'gonna', 'carry', 'that', 'weight'], 
              ['carry', 'that', 'weight', 'a', 'long', 'time']]
    sentence = [ 'the', 'quick', 'brown' ]
    sentence2 = [ 'the', 'happy', 'birthday']
    sentence3 = ['^::^', '^:::^']
    sentence4 = ['carry', 'that', 'weight']
    cScale = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
    music = [ [('c4', 3), ('db3', 4), ('e5', 5), ('f4', 2)], 
              [('g#3', 3), ('a5', 4), ('b2', 2)] ]
    musicSentence = [ ('c4', 3), ('db3', 4), ('e5', 5) ]
    phil = TrigramModel()
    bill = TrigramModel()
    bill.trainModel(text2)
    print(phil)
    phil.trainModel(text3)
    phil.trainModel(music)
    print bill.trainingDataHasNGram(sentence2)
    print bill.getCandidateDictionary(sentence2)
    phil.getNextToken(sentence4)
    phil.getNextNote(musicSentence, cScale)
