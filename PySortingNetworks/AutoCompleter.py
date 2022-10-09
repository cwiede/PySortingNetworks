import random

def _base(sn, geninputs, select, doprint=False):
    sn = sn.copy()

    def callback(d_in, d_out):
        #print("failed", d_in, d_out)
        nonlocal suggest
        zero = True
        for idx in range(len(d_out)):
            if zero and d_out[idx]:
                firstNonZero = idx
                zero = False
            elif not zero and not d_out[idx]:
                lastZero = idx
        test = d_out[:]
        assert test[firstNonZero] > test[lastZero] and firstNonZero < lastZero
        test[firstNonZero], test[lastZero] = test[lastZero], test[firstNonZero]
        if all(test[i] <= test[i+1] for i in range(len(test)-1)):
            if not (firstNonZero, lastZero) in suggest:
                suggest[(firstNonZero, lastZero)] = 0
            suggest[(firstNonZero, lastZero)] += 1
    
    suggest = None
    while True:
        if suggest is None:
            suggest = dict()
            passed, failed = sn.test( geninputs(), callback)
            if doprint: 
                print("nops", sn.nops(), "passed", passed, "failed", failed, "suggest", len(suggest))
        if failed == 0:
            break
        def applySuggestion(sgst):
            nonlocal suggest
            test = sn.copy()
            test.P(*sgst)
            suggest = dict()
            passed, failed = test.test(geninputs(), callback)
            return passed, failed, suggest
        passed, failed, suggest, (i,j) = select(suggest, applySuggestion)
        sn.P(i,j)
        if doprint:
            print("nops", sn.nops(), "passed", passed, "failed", failed, "suggest", len(suggest))
            #print(sn)
    return sn

def greedy(sn, geninputs, doprint=False, maxNumSuggestsToTry=None):
    def select(suggest, applySuggestion):
        best = None
        if maxNumSuggestsToTry is not None:
            last_suggest = sorted(suggest.keys(), key=lambda x: -suggest[x])[:maxNumSuggestsToTry]
        else:
            last_suggest = list(suggest.keys())
        random.shuffle(last_suggest)
        for i,j in last_suggest:
            passed, failed, suggest = applySuggestion( (i,j) )
            if best is None or (passed > best[0]) or (passed == best[0] and len(suggest) > len(best[2])):
                best = passed, failed, suggest, (i,j)
        return best
    return _base(sn, geninputs, select, doprint)
                
def randbest5(sn, geninputs, doprint=False):
    def select(suggest, applySuggestion):
        best = []
        last_suggest = list(suggest)
        random.shuffle(last_suggest)
        for i,j in last_suggest:
            passed, failed, suggest = applySuggestion( (i,j) )
            best.append( (passed, failed, suggest, (i,j)) )
        best.sort(key = lambda x: (x[1], -len(x[2])))
        best = best[:5]
        random.shuffle(best)
        return best[0]
    return _base(sn, geninputs, select, doprint)
        
