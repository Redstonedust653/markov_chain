import random

Probs = dict[tuple,dict[tuple,float]]

def tokenize(data:list[str],mode:str,n:int=1) -> tuple[list[list[str]], list[list[list[str]]]]:
    output_list:list[list[str]] = []
    output_ngrams:list[list[list[str]]] = []
    for i in data:
        tmp_list = ["START"]
        if mode == 'char':
            output_list.append(tmp_list)
        else:
            tmp_list += i.rstrip().lower().split(' ')
            output_list.append(tmp_list)
        tmp_list.append('END')
        sample_occurrences = [(tmp_list[j:(j+n)]) for j in range(len(tmp_list)-(n-1))]
        output_ngrams.append(sample_occurrences)
    return (output_list,output_ngrams)


def ngram_counts(ngrams:list[list[list[str]]]) -> dict[tuple,int]:
    numNGrams = {}
    for j in ngrams:
        for n in j:
            i = tuple(n)
            numNGrams[i] = numNGrams.get(i,0)+1
    return numNGrams

def ngram_occurrences(ngrams:list[list[list[str]]]) -> dict[tuple,dict[tuple,int]]:
    after_counts:dict[tuple,dict[tuple,int]] = {}
    for sample in ngrams:
        for gram_idx in range(len(sample)-1):
            a = tuple(sample[gram_idx])
            b = tuple(sample[gram_idx+1])
            # TODO: count "b happened after a"
            if a not in after_counts:
                after_counts[a] = {b:1}
            else:
                after_counts[a][b] = after_counts[a].get(b,0) + 1
    return after_counts

def ngram_probs(ngrams:list[list[list[str]]]) -> dict[tuple,dict[tuple,float]]:
    prob_out = {}
    counts:dict[tuple,int] = ngram_counts(ngrams)
    occurrences = ngram_occurrences(ngrams)
    for item_list in occurrences:
        item = tuple(item_list)
        for item_two in occurrences[item]:
            active_item_prob = occurrences[item][item_two]/counts[item]
            if item not in prob_out:
                prob_out[item] = {item_two:active_item_prob}
            else:
                prob_out[item][item_two] = active_item_prob
    return prob_out

def ngram_next_gram(probs:dict[tuple,dict[tuple,float]], gram:list[str]) -> list[str]:
    options = probs[tuple(gram)]
    return list(random.choices(list(options.keys()), list(options.values()))[0])

def possible_starts(counts:dict[tuple,int]) -> dict[tuple,float]:
    start_prob_dict = {}
    begin_with_start = 0
    for key in counts:
        if key[0] == 'START':
            count = counts[key]
            begin_with_start += count
            start_prob_dict[key] = count
    for key in start_prob_dict:
        start_prob_dict[key] /= begin_with_start
    return start_prob_dict
        

def ngram_train(samples:list[str],mode:str,n:int) -> tuple[Probs, dict[tuple,int]]:
    token_seq = tokenize(samples,mode,n)[1]
    return (ngram_probs(token_seq),ngram_counts(token_seq))



def ngram_generate(probs:Probs,counts:dict[tuple,int]) -> list[list[str]]:
    output_seq:list[list[str]] = []
    # get a start from possible starts
    starts = possible_starts(counts)
    output_seq.append(list(random.choices(list(starts.keys()), list(starts.values()))[0]))
    # use a while loop to generate until END
    current_token = output_seq[-1]
    while not current_token[-1] == 'END':
        next_gram = ngram_next_gram(probs,current_token)
        output_seq.append(next_gram)
        current_token = output_seq[-1]
    # return all the tokens we met along the way
    return output_seq

def cleanup(toks:list[list[str]], mode:str) -> str:
    output = ""
    for toki in range(1,len(toks)-1):
        output += toks[toki][0]
        if mode != "char":
            output += " "
    output += ("" if mode == "char" else " ").join(toks[-1][0:-1])
    return output


class markov_chain():
    def __init__(self,mode,train_list,n):
        self.mode = mode
        self.train = train_list
        self.n = n

    def generate(self) -> str:
        token_seq = tokenize(self.train,self.mode,self.n)[1]
        return cleanup(ngram_generate(ngram_probs(token_seq),ngram_counts(token_seq)), self.mode)