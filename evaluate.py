from __future__ import division
#!/usr/bin/env python
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators
 
def word_matches(h, ref):
    return sum(1 for w in h if w in ref)

def calculateF(h,ref):
    commonTerms=sum(1 for w in h if w in ref )
    nChunks=0
    prevTrans = False
    if(commonTerms!=0):
        for i in range(0,len(ref)):
            if ref[i] not in h and prevTrans==False:
                prevTrans=True
                nChunks+=1
            if ref[i] in h:
                prevTrans=False
            if i==len(ref)-1 and ref[i] in h:
                nChunks+=1
        alpha=0.77
        #print "nChunks-->"+str(nChunks)
        precision=commonTerms/len(h)
        recall=commonTerms/len(ref)
        F=(precision*recall)/((alpha*precision)+((1-alpha)*recall))
        Penalty=(0.5*nChunks)/(commonTerms)
        MeteorScore=(1-Penalty)*F
        return MeteorScore
    else:
        return 0
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
                yield [sentence.strip().split() for sentence in pair.split(' ||| ')]
 
    # note: the -n option does not work in the original code
    for h1, h2, ref in islice(sentences(), opts.num_sentences):
        """
        rset = set(ref)
        h1_match = word_matches(h1, rset)
        h2_match = word_matches(h2, rset)
        """
        h1_Fscore = calculateF(h1, ref)
        h2_Fscore= calculateF(h2, ref)
        F_weight=1
        rset = set(ref)
        h1_match = word_matches(h1, rset)
        h2_match = word_matches(h2, rset)
        len_weight=0.5
        h1_Total=F_weight*h1_Fscore+len_weight*h1_match
        h2_Total=F_weight*h2_Fscore+len_weight*h2_match
        print "hello"
        print(1 if h1_Total > h2_Total else # \begin{cases}
                (0 if h1_Total == h2_Total
                    else -1)) # \end{cases}
 
# convention to allow import of this file as a module
if __name__ == '__main__':
    main()
