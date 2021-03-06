from __future__ import division
# !/usr/bin/env python
import argparse  # optparse is deprecated
from itertools import islice  # slicing for iterators
from difflib import SequenceMatcher
import nltk
from nltk import word_tokenize
from nltk.util import ngrams

def word_matches(h, ref):
    return sum(1 for w in h if w in ref)


def calculateF(h, ref):
    commonTerms = sum(1 for w in h if w in ref)
    nChunks = 0
    prevTrans = False
    if (commonTerms != 0):
        for i in range(0, len(ref)):
            if ref[i] not in h and prevTrans == False:
                prevTrans = True
                nChunks += 1
            if ref[i] in h:
                prevTrans = False
            if i == len(ref) - 1 and ref[i] in h:
                nChunks += 1
        alpha = 0.77
        # print "nChunks-->"+str(nChunks)
        precision = commonTerms / len(h)
        recall = commonTerms / len(ref)
        F = (precision * recall) / ((alpha * precision) + ((1 - alpha) * recall))
        Penalty = (0.5 * nChunks) / (commonTerms)
        MeteorScore = (1 - Penalty) * F
        return MeteorScore
    else:
        return 0

def compluteBleu(ref,h,i):
    #compute i grams
    #print nltk.word_tokenize(ref)
    ngrams_ref=ngrams(ref.split(),i)
    print ngrams_ref
    print "******************************************************"
    ref_lst=[]
    for grams in ngrams_ref:
       ref_lst.append(grams)
    print ref_lst
    ngrams_h=ngrams(h.split(),i)
    h_lst=[]
    #print "h--->" + str(ngrams_h)
    print "#####################################################"
    for grams in ngrams_h:
        h_lst.append(grams)
    #print h_lst
    print len(h_lst)
    #print set.intersection(set(h_lst),set(ref_lst))
    return sum(1 for w in h_lst if w in ref_lst)+1,len(h_lst)+1

def main():
    parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
    parser.add_argument('-i', '--input', default='data/hyp1-hyp2-ref',
                        help='input file (default data/hyp1-hyp2-ref)')
    parser.add_argument('-n', '--num_sentences', default=None, type=int,
                        help='Number of hypothesis pairs to evaluate')
    # note that if x == [1, 2, 3], then x[:None] == x[:] == x (copy); no need for sys.maxint
    opts = parser.parse_args()

    # we create a generator and avoid loading all sentences into a list
    def sentences():
        with open(opts.input) as f:
            for pair in f:
                #yield [sentence.strip().split() for sentence in pair.split(' ||| ')]
                 yield [sentence.strip() for sentence in pair.split(' ||| ')]


    # note: the -n option does not work in the original code
    for h1, h2, ref in islice(sentences(), opts.num_sentences):
        """
        rset = set(ref)
        h1_match = word_matches(h1, rset)
        h2_match = word_matches(h2, rset)
        """
        h1_Fscore = calculateF(h1, ref)
        h2_Fscore = calculateF(h2, ref)
        F_weight = 1
        rset = set(ref)
        h1_match = word_matches(h1, rset)
        h2_match = word_matches(h2, rset)
        len_weight = 0.5
        #h1_Total = F_weight * h1_Fscore + len_weight * h1_match
        #h2_Total = F_weight * h2_Fscore + len_weight * h2_match
        #h1_Total=0.5*SequenceMatcher(None, h1, ref).ratio()+1*h1_Fscore
        #h2_Total = 0.5*SequenceMatcher(None, h2, ref).ratio()+1*h2_Fscore
        print "h1-->"+str(h1)
        print "h2-->"+str(h2)
        print "ref-->"+str(ref)
        common, hyp_len=compluteBleu(ref, h1, 2)
        print common,hyp_len
        #compluteBleu(ref, h1, 2)
        common, hyp_len =compluteBleu(ref, h2, 2)
        print common, hyp_len


        break
        h1_Total=SequenceMatcher(None, h1, ref).ratio()
        h2_Total = SequenceMatcher(None, h2, ref).ratio()

        print(1 if h1_Total > h2_Total else  # \begin{cases}
              (0 if h1_Total == h2_Total
               else -1))  # \end{cases}


# convention to allow import of this file as a module
if __name__ == '__main__':
    main()
