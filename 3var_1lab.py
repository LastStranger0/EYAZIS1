import spacy
import nltk
import tkinter.ttk as ttk
from nltk.collocations import *
from tkinter import *
from pymorphy2 import MorphAnalyzer

nltk.download('punkt')

morphy = MorphAnalyzer()
bigram_measures = nltk.collocations.BigramAssocMeasures()


def tokenize(sentences):
    list_word = []
    for sent in nltk.sent_tokenize(sentences.lower()):
        for word in nltk.word_tokenize(sent):
            list_word.append(word)
    return list_word


def parser(text):
    dictionary = {}
    doc = tokenize(text)
    for first, second in find_phrase(text).nbest(bigram_measures.likelihood_ratio,
                                                 len(tokenize(text))):
        for word in doc:
            if len(word) > 2:
                if first != ',' and first != '.' and second != ',' and second != '.':
                    if first == word:
                        dictionary.update({morphy.parse(word)[0].normal_form: first + ' ' + second})
                    if second == word:
                        dictionary.update({morphy.parse(word)[0].normal_form: first + ' ' + second})
    return sorted(dictionary.items(), key=lambda x: x[0])


def find_phrase(text):
    finder = BigramCollocationFinder.from_words(tokenize(text))
    return finder


root = Tk()
vocabulary = []

space0 = Label(root)
inputFrame = Frame(root, bd=2)
inputText = Text(inputFrame, height=8, width=80, wrap=WORD)
createVocabularyButton = Button(inputFrame, text='Create vocabulary from text', width=55, height=2, bg='grey')

space1 = Label(root)
vocabularyFrame = Frame(root, bd=2)
vocabularyTree = ttk.Treeview(vocabularyFrame, columns=("Lemma", "Phrase"), selectmode='browse',
                              height=11)
vocabularyTree.heading('Lemma', text="Lemma", anchor=W)
vocabularyTree.heading('Phrase', text="Phrase", anchor=W)
vocabularyTree.column('#0', stretch=NO, minwidth=0, width=0)
vocabularyTree.column('#1', stretch=NO, minwidth=347, width=347)
vocabularyTree.column('#2', stretch=NO, minwidth=347, width=347)


rows = 0


def showVocabulary():
    global rows, word_form
    rows = 0
    text = inputText.get(1.0, END).replace('\n', '')
    vocabularyTree.delete(*vocabularyTree.get_children())
    for lexeme in parser(text):
        vocabularyTree.insert('', 'end', values=(lexeme[0], lexeme[1]), iid=rows)
        rows += 1


def clearVocabulary():
    global rows
    rows = 0
    vocabularyTree.delete(*vocabularyTree.get_children())


def createVocabulary():
    clearVocabulary()
    showVocabulary()


createVocabularyButton.config(command=createVocabulary)

space0.pack()
inputFrame.pack()
inputText.pack()
createVocabularyButton.pack(side='left')
space1.pack()
vocabularyFrame.pack()
vocabularyTree.pack()
root.mainloop()
