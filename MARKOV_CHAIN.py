import ai_tools

l = ['String 1', 'String 2']

chain = ai_tools.markov_chain('word',l,3)

print(chain.generate())