import util
import wordsegUtil

_X_ = None

class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def start_state(self):
        # position before which text is reconstructed & previous word
        return 0, wordsegUtil.SENTENCE_BEGIN


    def is_end(self, state):
        return state[0] == len(self.query)

    def succ_and_cost(self, state):
        pos, prev_word = state
        for step in range(1, len(self.query) - pos + 1):
            next_state = pos + step
            word = self.query[pos: next_state]  # constructed word
            fills = self.possibleFills(word)

            for fill in fills:
                next_state = pos + step, fill
                cost = self.bigramCost(word,  fill)
                yield fill, next_state, cost  # return action, state, cost



    # use "self.possibleFills(vowel_removed_word)" instead of
    # "self.possibleFills(vowel_removed_word) | {vowel_removed_word}"
    #
    # user two overlapped 'for' loops

unigramCost, bigramCost = wordsegUtil.makeLanguageModels('leo-will.txt')
smoothCost = wordsegUtil.smoothUnigramAndBigram(unigramCost, bigramCost, 0.2)
possibleFills = wordsegUtil.makeInverseRemovalDictionary('leo-will.txt', 'aeiou')
problem = JointSegmentationInsertionProblem('mgnllthppl', smoothCost, possibleFills)

import dynamic_programming_search
dps = dynamic_programming_search.DynamicProgrammingSearch(verbose=1)
# dps = dynamic_programming_search.DynamicProgrammingSearch(memory_use=False, verbose=1)
print(dps.solve(problem))

import uniform_cost_search
ucs = uniform_cost_search.UniformCostSearch(verbose=0)
print(ucs.solve(problem))
