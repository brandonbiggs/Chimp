# Chimp - Constrained Hidden Markov Process
CCIL Lab Research Project. Hopefully everything is commented well enough that it makes sense.
Let Brandon know if things aren't commented very well.

### Dependencies

I created a requirements.txt that have the packages that are used. Not all of them
are used though. I'll try cleaning up the ones that aren't used. 

You may need to use the following two lines for the NLTK package.
`nltk.download('tagsets')`
`nltk.download('averaged_perceptron_tagger')`
    
### Folder Structure
- constraints
    - each file is a class that represents a different type of constraint.
They are supposed to all inherit from `Constraint.py` however I don't believe that's working
exactly as intended.
    - Currently only 5 kinds of constraints. Constraint contains a string, is a specific part of speech
    matches a string, or rhymes with.
- data
    - These are just a handful of test documents that I've used for a few different things.
    None of these are particularly important. ccil.txt just represents the data we came up
    with in our meetings while the other books are just random collections from The Gutenberg Project.
- examples
    - Instead of having one large file of examples, I tried parsing them out to just one file per example.
    I tried naming them in a way that is helpful. Most of these aren't important at all. The 
    ones that might be important are "RedRhyme.py" and "FirstDog.py". The others were things
    I was testing. Any of the ones named "dynamic" will provide examples of how I was pulling
    from the text documents in the data folder.
- markovs
    - this is where models and any model helping tools are. 
    - `HiddenMarkovModel.py` is purely
    a hmm. Just an object for holding information. 
    - `NonHomogeneousHMM.py` is where the meat and potatoes are. This is where all of the calculations 
    happen. All of the example files use this in some capacity.
    - `NonHomogeneousHMMSentences.py` is where the sentences are generated based on the 
    Nhhmm that is passed to it. 
- markovs_matrix
    - This is the matrix implementations of everything. Still have a lot to do with this.
    Hopefully using this will increase the speed of the model.
- markovs_parallel
    - This is some testing I've been doing. Trying to parallelize the nhhmm process. Not yet working.
- nltk_data
    - This was supposed to be used for the data nltk needed to do it's parsing. I'm not sure if it's used.
    I had some problems with telling ntlk which folder to use. Regardless, it's not anything we
    need to edit.
- notes
    - basically just some notes/scratch work. A picture of the first time we hand wrote the 
    nhhmm.
- pickle_files
    - to save time, we can pickle the hidden markov model. It really worked well and saved a ton
    of time since the longest part I've ran into so far was the data processing part. If you
    process the data, pickle it, you can then use it whenever you want with the nhhmm. Examples
    of this can be found in one or two of the dynamic examples. The current pickle files
    are not important and the names aren't helpful. Sorry.
- utility
    - Some useful utility functions
    - `interactive.py` - this is where I've been working on making an interactive CLI. It works
    a little bit, but still needs some work.
    - `ProcessData.py` - This is where the document gets read in and the probabilities are created.
    This is where I have some concern and would like to work on verifying at some point. Seems to work
    with the redrhyme example however.
    - `Utility.py` - right now it only contains a random number generator. I wanted that to
    be it's own function in case we wanted to chance how we wanted to create random numbers
    in the future.
- venv
    - Just the virtual environment that I use. Should have all of the packages that we could need.
- `__init__.py`
    - Just some general pieces of information about the program like version and a dictionary
    of all the ntlk parts of speech. Nothing fancy.
- `index.py`
    - This file is what I've been using to call all the examples or whatever else I may want to run.
    There are a lot of comments in here, but it's all just stuff that can be called. Should just be
    calling example functions or the CLI.
 - `testing.py`
    - Exactly what it sounds like. Test code I wanted to run without deleting things in index.
    I was mostly using this for multiproccessing and multithreading.

# TODO
- Update the CLI with the new chimp name
- Update this documentation that reflects the new features, programs, and name changes
- At some point implement the matrix model

### Matrix Implementation
1. This is nowhere near ready. Please do not even try to use it yet.
2. There are many bugs that I'm working through. These are listed below.
    
    - When calculating the e_tilde probabilities of the observed nodes, I 
    do a constraint check. This constraint check either leaves the value alone,
    or it removes it if it doesn't meet the constraint. The problem I'm having
    however is that with the matrix implementation we just have a bunch of numbers
    in the array. This is an issue because the constraint check may check something
    like "Does this word have the letter 'T' in it?". We can't do that with just numbers.
    Dictionaries worked just fine, but numbers don't. I created a class for lookups 
    based on the matrix but when doing it dynamically, this could get kind of messy. 
    So we'll need to figure out some kind of approach to make sure everything lines 
    up as it should..
