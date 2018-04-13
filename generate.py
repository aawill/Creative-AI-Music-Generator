#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True # Suppress .pyc files
import socket
import random
from pysynth import pysynth
from pysynth import mixfiles
from data.dataLoader import *
from models.musicInfo import *
from models.unigramModel import *
from models.bigramModel import *
from models.trigramModel import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

TEAM = '~G L Y T C H~'
LYRICSDIRS = ['funkadelic']
MUSICDIRS = ['gamecube']
WAVDIR = 'wav/'

###############################################################################
# Helper Functions
###############################################################################

def sentenceTooLong(desiredLength, currentLength):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  returns a bool indicating whether or not this sentence should
              be ended based on its length. This function has been done for
              you.
    """
    STDEV = 1
    val = random.gauss(currentLength, STDEV)
    return val > desiredLength

def printSongLyrics(verseOne, verseTwo, chorus):
    """
    Requires: verseOne, verseTwo, and chorus are lists of lists of strings
    Modifies: nothing
    Effects:  prints the song. This function is done for you.
    """
    verses = [verseOne, chorus, verseTwo, chorus]
    print
    for verse in verses:
        for line in verse:
            print (' '.join(line)).capitalize()
        print

def trainLyricModels(lyricDirs):
    """
    Requires: lyricDirs is a list of directories in data/lyrics/
    Modifies: nothing
    Effects:  loads data from the folders in the lyricDirs list,
              using the pre-written DataLoader class, then creates an
              instance of each of the NGramModel child classes and trains
              them using the text loaded from the data loader. The list
              should be in tri-, then bi-, then unigramModel order.

              Returns the list of trained models.
    """
    models = [TrigramModel(), BigramModel(), UnigramModel()]
    for ldir in lyricDirs:
        lyrics = loadLyrics(ldir)
        for model in models:
            model.trainModel(lyrics)
    return models

###############################################################################
# Core
###############################################################################

def trainMusicModels(musicDirs):
    """
    Requires: lyricDirs is a list of directories in data/midi/
    Modifies: nothing

    Effects:  works exactly as trainLyricsModels, except that
              now the dataLoader calls the DataLoader's loadMusic() function
              and takes a music directory name instead of an artist name.
              Returns a list of trained models in order of tri-, then bi-, then
              unigramModel objects.
    """
    models = [TrigramModel(), BigramModel(), UnigramModel()]
    # call loadMusic for each directory in musicDirs
    for mdir in musicDirs:
        music = loadMusic(mdir)
        for model in models:
            model.trainModel(music)
    return models

def selectNGramModel(models, sentence):
    """
    Requires: models is a list of NGramModel objects sorted by descending
              priority: tri-, then bi-, then unigrams.
    Modifies: nothing
    Effects:  returns the best possible model that can be used for the
              current sentence based on the n-grams that the models know.
              (Remember that you wrote a function that checks if a model can
              be used to pick a word for a sentence!)
    """
    if models[0].trainingDataHasNGram(sentence) == True:
        return models[0]
    elif models[1].trainingDataHasNGram(sentence) == True:
        return models[1]
    else:
        return models[2]

def generateLyricalSentence(models, desiredLength):
    """
    Requires: models is a list of trained NGramModel objects sorted by
              descending priority: tri-, then bi-, then unigrams.
              desiredLength is the desired length of the sentence.
    Modifies: nothing
    Effects:  returns a list of strings where each string is a word in the
              generated sentence. The returned list should NOT include
              any of the special starting or ending symbols.

              For more details about generating a sentence using the
              NGramModels, see the spec.
    """
    sentence = ['^::^', '^:::^']
    #while sentence isn't too long
    while sentenceTooLong(desiredLength, len(sentence)) == False:
        #gets next suggested note
        next_word = selectNGramModel(models, sentence).getNextToken(sentence)
        #if note is ending character, returns sentence
        if next_word == '$:::$':  
            return sentence[2:]
        else:
            #append the next suggested character to the sentence
            sentence.append(next_word)            
    return sentence[2:]
def generateMusicalSentence(models, desiredLength, possiblePitches):
    """
    Requires: possiblePitches is a list of pitches for a musical key
    Modifies: nothing
    Effects:  works exactly like generateLyricalSentence from the core, except
              now we call the NGramModel child class' getNextNote()
              function instead of getNextToken(). Everything else
              should be exactly the same as the core.
    """
    sentence = ['^::^', '^:::^']
    #basically same as previous function
    while sentenceTooLong(desiredLength, len(sentence)) == False:
        next_note = selectNGramModel(models, sentence).getNextNote(sentence, possiblePitches)
        if next_note == '$:::$':
            return sentence[2:]
        else:
            sentence.append(next_note)
    return sentence[2:]

def runLyricsGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """
    verseOne = []
    verseTwo = []
    chorus = []

    verseOne.append(generateLyricalSentence(models, 6))
    verseOne.append(generateLyricalSentence(models, 6))
    verseOne.append(generateLyricalSentence(models, 8))
    verseOne.append(generateLyricalSentence(models, 6))

    verseTwo.append(generateLyricalSentence(models, 6))
    verseTwo.append(generateLyricalSentence(models, 6))
    verseTwo.append(generateLyricalSentence(models, 9))
    verseTwo.append(generateLyricalSentence(models, 5))

    chorus.append(generateLyricalSentence(models, 7))
    chorus.append(generateLyricalSentence(models, 10))
    chorus.append(generateLyricalSentence(models, 6))
    chorus.append(generateLyricalSentence(models, 6))

    printSongLyrics(verseOne, verseTwo, chorus)
    return

def runMusicGenerator(models, songName):
    """                                          
    Requires: models is a list of trained models
    Modifies: nothing
    Effects:  runs the music generator. this now involves choosing key signature,
              creating melody and bassline, adjusting durations, sending all relevant 
              info to max/msp, and plotting the trajectories of melody and bassline. 
    """
    key = random.choice(KEY_SIGNATURES.keys())
    print 'Key:', key
    note_list = KEY_SIGNATURES[key]
    determineMajMin(note_list, key, 4500)
    melody = createMelody(models, songName, note_list)
    bassline = createBassLine(models, songName, note_list)
    pysynth.mix_files(songName + "_melody.wav", songName + "_bassLine.wav", songName)
    fixed_melody = fixStupidDurations(melody)
    fixed_bassline = fixStupidDurations(bassline)
    sendToMax(fixed_melody, 7000)
    sendToMax(fixed_bassline, 7001)
    melody_graph = createPointList(fixed_melody, songName, 'melody')
    bassline_graph = createPointList(fixed_bassline, songName, 'bassline')
    plottwoListGraphs(melody_graph, bassline_graph, songName)

    


###############################################################################
# Reach
###############################################################################

def plottwoListGraphs(melody_list, bass_list, songName):
    """
    Requires: melody_list and bass_list are lists of ints
              songName is a str
              part is a str
    Modifies: nothing
    Effects:  plots the trajectory of two lists on one figure
    """
    plt.title(songName[4:] + " ")
    melody, = plt.plot(melody_list, label='melody')
    bassline, = plt.plot(bass_list, 'o-', label='bassline')
    axes = plt.gca()
    axes.set_xlim([0, (len(melody_list) - 1)])
    plt.legend(handles=[melody, bassline], loc=0)
    plt.show()


def determineMajMin(list, key, port):
    """
    Requires: list is a key signature from KEY_SIGNATURES
              key is a str such as c major, g# minor, etc
              port is a valid UDP port
    Modifies: midi_list, the coll object in max
    Effects:  sends a dictionary of sorts to the coll object in max, with
              scale degree midi values as keys and either 0 or 1 as value,
              depending if the chord built should be minor or major. This is
              determined by the scale degree, as follows:
              Major key: 1, 4, and 5 are major chords
                         2, 3, 6, and 7 are minor chords
                         (7 should actually be diminished)
              Minor key: 3, 6, and 7 are major chords
                         1, 2, 4, and 5 are minor chords
                         (2 should be diminished)
              This is because of some music theory stuff. 
            
    """
    #opens UDP communication with max/msp
    UDP_IP = "127.0.0.1"
    sock = socket.socket(socket.AF_INET, 
                         socket.SOCK_DGRAM) 
    #builds a list of notes in the key as midi values in octave 2, to match bass notes
    midi_list = []
    for note in list:
        midi_list.append(MidiNoteToInt(note + '2'))
    #clears the destination text object in max
    sock.sendto('clear', (UDP_IP, port))
    #checks if key is major, then sends 0s or 1s along with each scale degree based on chord quality
    if key[-3] == 'j':
        for i in range(len(list)):
            if i == 1 or i == 2 or i == 5 or i == 6:
                sock.sendto(('%s %s' % (str(midi_list[i]), '0')), (UDP_IP, port))
            elif i == 0 or i == 3 or i == 4:
                sock.sendto(('%s %s' % (str(midi_list[i]), '1')), (UDP_IP, port))
    else:
        for i in range(len(list)):
            if i == 0 or i == 1 or i == 3 or i == 4:
                sock.sendto(('%s %s' % (str(midi_list[i]), '0')), (UDP_IP, port))
            elif i == 2 or i == 5 or i == 6:
                sock.sendto(('%s %s' % (str(midi_list[i]), '1')), (UDP_IP, port))
    

def sendToMax(song, port):
    """
    Requires: song is a list of tuples in form (pitch, duration)
              port is a valid integer UDP port number
              port must also be the same port on max's udpreceive object
    Modifies: the udprecieve object in max/msp
    Effects:  sends song as a list of midi notes with durations to external 
              program Max/MSP for additional processing and playback
    """
    UDP_IP = "127.0.0.1"
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM) 
    sock.sendto('clear', (UDP_IP, port))
    for note in song:
        sock.sendto(('%s %s \n') % (MidiNoteToInt(note[0]), note[1]), (UDP_IP, port))

def createPointList(song, songName, part):
    """
    Requires: song is a list of tuples in form (pitch, duration)
              songName and part are strings
    Modifies: nothing
    Effects:  creates a list of pitches, with each pitch
              in song listed as many times as its new duration
    """
    point_list = []
    for note in song:
        for i in range(note[-1]):
            point_list.append(MidiNoteToInt(note[0]))
    return point_list

def fixStupidDurations(song):
    """
    Requires: song is a list of tuples in form (pitch, duration)
    Modifies: nothing
    Effects:  returns a copy of song, where durations are changed 
              to reflect actual duration in 32nd notes.
    """
    #we are aware how dumb this is
    #just go with it
    fixed_song = []
    for note in song:
        if note[-1] == 16:
            fixed_song.append((note[0], 2))
        elif note[-1] == -16:
            fixed_song.append((note[0], 3))
        elif note[-1] == 8:
            fixed_song.append((note[0], 4))
        elif note[-1] == -8:
            fixed_song.append((note[0], 6))
        elif note[-1] == 4:
            fixed_song.append((note[0], 8))
        elif note[-1] == -4:
            fixed_song.append((note[0], 12))
        elif note[-1] == 2:
            fixed_song.append((note[0], 16))
        elif note[-1] == -2:
            fixed_song.append((note[0], 24))
        elif note[-1] == 1:
            fixed_song.append((note[0], 32))
        else:
            fixed_song.append((note[0], 48))
    return fixed_song

def createMelody(models, songName, note_list):
    """
    Requires: models is a list of trained unigram, bigram, etc models
              songName is a string
    Modifies: nothing
    Effects:  creates a .wav file containing a randomly generated melody.
              Returns the melody as a list of tuples.
    """
    melody = []
    for i in range(1, 16):
        melody.extend(generateMusicalSentence(models, 8, note_list))

    pysynth.make_wav(melody, fn=songName + "_melody.wav")
    return melody

def createBassLine(models, songName, note_list):
    """
    Requires: models is a list of trained unigram, bigram, etc models
              songName is a string
    Modifies: nothing
    Effects:  creates a .wav file containing a randomly generated bassline,
              which is constrained to chord tones 1, 3, 5, and 7 in octave 2.
              Returns the bassline as a list of tuples.
    """
    bass_line = []
    lowered_bass = []
    chord_note_list = note_list[::2]
    #creates a bassline out of chord tones
    for i in range(1, 16):
        bass_line.extend(generateMusicalSentence(models, 8, chord_note_list))
    #puts all notes in octave 2
    for i in range(len(bass_line)):
        lowered_bass.append((bass_line[i][0][:-1] + '2', 2))
    pysynth.make_wav(lowered_bass, fn=(songName + "_bassLine.wav"))
    return lowered_bass

def MidiNoteToInt(note):
    """
    Requires: note is a string of form 'c4', 'd#6', 'b0', etc
    Modifies: nothing
    Effects:  returns the corresponding midi value 0-127
    """
    notes = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
    int_note = 0
    if (0 <= int(note[-1]) <= 10) and ('a' <= note[0] <= 'g'):
        #adds 12 for each octave
        int_note += int(note[-1]) * 12
        for i in range(len(notes)):
            #adds 2 for each whole step from c
            if note[0] == notes[i]:
                int_note += i * 2
                #subtracts one due to no note existing between e and f
                if note[0] == 'f' or note[0] == 'g' or note[0] == 'a' or note[0] == 'b':
                    int_note -= 1
        #adjusts for sharps/flats
        if note[1] == '#':
            int_note += 1
        elif note[1] == 'b':
            int_note -= 1
    else:
        return 'Invalid note'
    return int_note

PROMPT = """
(1) Generate song lyrics by Funkadelic
(2) Generate a song using data from Nintendo Gamecube
(3) Quit the music generator
> """

def main():
    """
    Requires: Nothing
    Modifies: Nothing
    Effects:  This is your main function, which is done for you. It runs the
              entire generator program for both the reach and the core.

              It prompts the user to choose to generate either lyrics or music.
    """
    print('Starting program and loading data...')
    lyricModels = trainLyricModels(LYRICSDIRS)
    musicModels = trainMusicModels(MUSICDIRS)
    print('Data successfully loaded')

    print('Welcome to the ' + TEAM + ' music generator!')
    while True:
        try:
            userInput = int(raw_input(PROMPT))
            if userInput == 1:
                runLyricsGenerator(lyricModels)
            elif userInput == 2:
                songName = raw_input('What would you like to name your song? ')

                runMusicGenerator(musicModels, WAVDIR + songName + '.wav')
            
            elif userInput == 3:
                print('Thank you for using the ' + TEAM + ' music generator!')
                sys.exit()
            else:
                print("Invalid option!")
        except ValueError:
            print("Please enter a number")

if __name__ == '__main__':
    main()
