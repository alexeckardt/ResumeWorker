import re
from components.PriorityQueue import PriorityQueue
from components.Ranker import Ranker

class Point:
    
    def __init__(self, text, score, section, subsection, i):
        self.text = text
        self.score = score
        self.section = section
        self.subsection = subsection
        self.localIndex = i
        self.finalGlobalIndex = i
        self.lines = (len(text) // 110) + 1

    def __str__(self) -> str:
        return f'({self.score}) {self.text}'
    
    def __repr__(self) -> str:
        return str(self)


class PointList:
    
    def __init__(self, keywords) -> None:
        self.points = {}
        self.hRankings = {}
        self.vRankings = PriorityQueue()
        
        self.ranker = Ranker()
        self.ranker.load_keywords(keywords)
        
    def compile(self, data):
        
        #
        # Go Over
        #
        def remove_latex_from_string(latex_string):
            # Remove LaTeX commands with content (e.g., \emph{content}, \textbf{content})
            result = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', latex_string)
            # Remove other LaTeX commands and symbols like \%, which could be escaped as \%
            result = re.sub(r'\\[a-zA-Z%]', '', result)
            return result

        for section in data:
            subsections = data.get(section).get('subsections')
            for subsection in subsections:
                
                # Get the Correct PQ
                i = 0
                pq = self.vRankings
                title = subsection.get('title')
                if data.get(section).get('one_liner', True):
                    
                    #Generate a key for each individual line
                    key = f'{section}.{title}'
                    
                    if key not in self.hRankings:
                        self.hRankings[key] = PriorityQueue()
                    pq = self.hRankings[key]
                
                # Go Over Points
                for point in subsection.get('points'):
                    
                    # Find best variant
                    bestVariant = ''
                    bestScore = -1
                    variants = point.get('variants')
                    
                    for variant in variants:
                        
                        # Get Variant Score 
                        varientText = remove_latex_from_string(variant)
                        score = self.ranker.rank_sentence(varientText)

                        if score > bestScore:
                            bestScore = score
                            bestVariant = variant
   
                    # Add Scores of Point & Subsection for global check
                    adjustedScore = bestScore + subsection.get('score_bias', 0) + point.get('score_bias', 0)
                    
                    # Store
                    variantData = Point(bestVariant, adjustedScore, section, title, i)

                    # Push Variant
                    pq.push(variantData, adjustedScore)
                    i += 1
                    
        # Convert
        self.hRankings = {x: y.to_list() for x, y in self.hRankings.items()}
        self.vRankings = self.vRankings.to_list()