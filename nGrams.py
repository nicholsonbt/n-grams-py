import nltk, random

# Creates an n-gram given a sequence of words.
# The n-gram will stop after 'length' words or until it reaches the
# end of the text if 'length' is None.
def createNGram(words, n, length=None):
    # n-gram           = [freq, {word_0: <(n-1)-gram>, word_1: <(n-1)-gram>, ...}]
    # bigram (2-gram)  = [freq, {word_0:  <unigram>,   word_1:  <unigram>,   ...}]
    # unigram (1-gram) = [freq, {word_0:     freq,     word_1:     freq,     ...}]

    # Adds a sequence of n words to the n-gram.
    def add(nGram, words):
        
        # Get the first word in the sequence.
        word = words[0]

        # If there is only one word, add a unigram.
        if len(words) == 1:
            # Increment the word frequency by 1.
            if word not in nGram:
                nGram[word] = 1
            else:
                nGram[word] += 1

        # Add an n-gram where n > 1.
        else:
            # Increment the word frequency by 1.
            if word not in nGram:
                nGram[word] = [1, dict()]
            else:
                nGram[word][0] += 1

            # Add the next word to an (n-1)-gram.
            add(nGram[word][1], words[1:])


    # If the length is None, read all the text.
    if length == None:
        length = len(words)

    # Initialise the n-gram.
    nGram = [0, dict()]

    # Add sequences of n words to the n-gram (upto the desired length).
    for i in range(0, length - n):
        nGram[0] += 1
        add(nGram[1], words[i : i + n])

    return nGram


# Generates an array of words using the given n-gram.
def generate(nGram, n, size, seed_word=None, seed=None):

    # Gets a random word from the n-gram.
    def getWord(nGram):
        words = nGram[1]

        # Generate a random number k, where 0 <= k < nGram[0].
        # This will allow us to select a random word, using weightings
        # to ensure it has the same frequency of occurring as in the
        # original text used.
        k = random.randrange(nGram[0])
        i = -1

        wordList = list(words)

        # Iterate over word frequencies to select a random next word.
        while k >= 0:
            i += 1
            word = wordList[i]

            # If the current word maps to an integer only, it must be
            # a unigram, so take its frequency as is.
            if type(words[word]) == int:
                k -= words[word]

            # If not a unigram, get the frequency of the current word
            # via the first argument of the n-gram.
            else:
                k -= words[word][0]

        # Returns the randomly chosen word.
        return wordList[i]

    # If no seed word, randomly select one.
    if seed_word == None:
        seed_word = getWord(nGram)

    # If no seed, don't use one.
    if seed != None:
        random.seed(seed)

    # Get the (n-1)-gram.
    newNGram = nGram[1][seed_word]

    # Add the seed word to the array of words.
    ws = [seed_word]

    # Get the (n-2)-gram up to the bigram, adding the chosen word
    # to the array of words each time.
    for i in range(n - 2):
        w = getWord(newNGram)
        newNGram = newNGram[1][w]
        ws.append(w)

    # Choose and add the remaining words by updating the n-gram before
    # each new word is selected.
    for i in range(n - 1, size):
        newNGram = nGram
        
        for j in range(n - 1, 0, -1):
            newNGram = newNGram[1][ws[i - j]]

        ws.append(getWord(newNGram))

    # Return the array of words.
    return ws


# Tokenize the abc corpus into words (punctuation is counted as
# seperate words).
words = nltk.corpus.abc.words()

# Use a 4-gram.
n = 4

# Calculate the n-gram.
nGram = createNGram(words, n)

# Generate an array of text given the n-gram.
generated = generate(nGram, n, 1000, seed_word="Australia", seed=0)

# Print out a string representation of the generated array of text.
print(" ".join(generated))
