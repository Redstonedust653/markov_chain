import ai_tools

l = ['String 1', 'String 2']

chain = ai_tools.markov_chain('word',l,3)

print(chain.generate())

# EXPLANATION TIME:
# Argument one is mode. it can be 'word' or 'char'. This is for the n-grams.
# Argument two is a list of str. It does not matter what order the strings are.
# Argument three is what n for the n-gram.

# and chain.generate() (or whatever you name your markov_chain) will return a str.
