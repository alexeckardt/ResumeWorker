from copy import copy, deepcopy
from datetime import datetime
import heapq
import re
import spacy
import pyperclip

LINELENGTH = 100

sectionData = {}

def prompt():
    
    #     
    # job_description = input('Paste Job Description in:\n').strip()
    job_description = '''
Google's software engineers develop the next-generation technologies that change how billions of users connect, explore, and interact with information and one another. Our products need to handle information at massive scale, and extend well beyond web search. We're looking for engineers who bring fresh ideas from all areas, including information retrieval, distributed computing, large-scale system design, networking and data storage, security, artificial intelligence, natural language processing, UI design and mobile; the list goes on and is growing every day. As a software engineer, you will work on a specific project critical to Google’s needs with opportunities to switch teams and projects as you and our fast-paced business grow and evolve. We need our engineers to be versatile, display leadership qualities and be enthusiastic to take on new problems across the full-stack as we continue to push technology forward.
Behind everything our users see online is the architecture built by the Technical Infrastructure team to keep it running. From developing and maintaining our data centers to building the next generation of Google platforms, we make Google's product portfolio possible. We're proud to be our engineers' engineers and love voiding warranties by taking things apart so we can rebuild them. We keep our networks up and running, ensuring our users have the best and fastest experience possible.
With your technical expertise you will manage project priorities, deadlines, and deliverables. You will design, develop, test, deploy, maintain, and enhance software solutions.
Google Cloud accelerates every organization's ability to digitally transform its business and industry. We deliver enterprise-grade solutions that leverage Google’s cutting-edge technology, and tools that help developers build more sustainably. Customers in more than 200 countries and territories turn to Google Cloud as their trusted partner to enable growth and solve their most critical business problems.
The US base salary range for this full-time position is $161,000-$239,000 + bonus + equity + benefits. Our salary ranges are determined by role, level, and location. The range displayed on each job posting reflects the minimum and maximum target salaries for the position across all US locations. Within the range, individual pay is determined by work location and additional factors, including job-related skills, experience, and relevant education or training. Your recruiter can share more about the specific salary range for your preferred location during the hiring process.
    '''
    
    return f'''Pretend you are a HR manager incharge of hiring new computer science and software engineering candidates for a Software developer
    positions at your technology firm. 
To rank the viability of a candidate, you are going to go line by line of each resume's bullet point, using Python's Spacy
    library. What follows will be a job description of the position. Based on these requirements, 
    state approximately 10 key words that you would expect to score a high match, using Spacy, with an interviewable
    candidate's resume. Return results in one line, sepeated by commas. The following is the job descritpion. "{job_description}" '''


def generate_key_words_from_job(positionName, companyName):
    
    pyperclip.copy(prompt())
    
    
    print('Copied Prompt to Clipboard.')
    x = input('Paste Chat GPT Response here:')
    
    splits = x.split(',')
    bestkeywords = [x.strip() for x in splits]
    
    return bestkeywords


#
#
#
class Ranker:
    
    def __init__(self):
        
        print('Loading SpaCy model')
        self.nlp = spacy.load('en_core_web_md')
        self.keywords = None
    
    def load_keywords(self, keywords):
        keywordString = " ".join(keywords);
        self.keywords = self.nlp(keywordString)

    def rank_sentence(self, sentence):

        # Compute similarity between the sentence and keywords
        sentence_doc = self.nlp(sentence)
        similarity = sentence_doc.similarity(self.keywords)
        
        return similarity

def remove_latex_from_string(latex_string):
    # Remove LaTeX commands with content (e.g., \emph{content}, \textbf{content})
    result = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', latex_string)
    # Remove other LaTeX commands and symbols like \%, which could be escaped as \%
    result = re.sub(r'\\[a-zA-Z%]', '', result)
    return result


def rank_bullet(bullet, ranker):
    return ranker.rank_sentence(bullet)


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, score):
        # Using a negative score to turn heapq into a max-heap
        heapq.heappush(self._queue, (-score, self._index, item))
        self._index += 1

    def pop(self):
        if self._queue:
            return heapq.heappop(self._queue)[-1]
        raise IndexError("pop from an empty priority queue")

    def to_list(self):
        # Convert the priority queue to a sorted list
        return [item for score, index, item in sorted(self._queue)]

    def merge(self, other):
        # Combine two priority queues
        for score, index, item in other._queue:
            heapq.heappush(self._queue, (score, self._index, item))
            self._index += 1

    def __len__(self):
        return len(self._queue)

def create_bullets_pq(data, keywords):
    
    # Split
    ranker = Ranker()
    ranker.load_keywords(keywords)
    
    globalPQ = PriorityQueue()
    globalPQ.merge(__create_bullet_pq(data, ranker, 'work_experience'))
    globalPQ.merge(__create_bullet_pq(data, ranker, 'projects'))
    
    return globalPQ;
    
    
def __create_bullet_pq(data, ranker, sectionName):
    
    # Unpack
    section = data.get(sectionName)
    subsections = section.get('subsections')
    minimum = section.get('minimum_to_show')
    
    #Store
    sectionData[sectionName] = deepcopy(section)
    
    # Create
    pq = PriorityQueue()
    
    # Rank
    for subsection in subsections:
        bullets = subsection.get('bullets')
        subsection_bias = subsection.get('score_bias')
        
        i = 0
        for bullet in bullets:
            
            # Define Bias
            bullet_bias = bullet.get('score_bias', 0) #no bias if not defined
            bias = subsection_bias + bullet_bias
            
            # Choose Best TEXT Variant in this scendario
            bestScore = -1000
            bestVariant = ''
            variants = bullet.get('variants')
            
            for variant in variants:
                bulletCleanedString = remove_latex_from_string(variant)
                score = rank_bullet(bulletCleanedString, ranker)
                
                if score >= bestScore:
                    bestScore = score
                    bestVariant = variant
            #
            # Found Best. Save to PQ
            
            print(f'{bestVariant} ranked with score={score} + {bias}')
            score += bias
            
            pq.push({
                "score": score,
                "section": sectionName,
                "subsection": subsection.get('title'),
                "lines": (len(bestVariant) // LINELENGTH) + 1,
                "text": bestVariant, 
                "local_index": i,
                'total_bias': bias
                }, 
                score),
            
    return pq
            
            
        
    
    
SUBSECTIONLINEHEIGHT = 2
LINESALLOWED = 38 # remeber to include space for the section headers -- knapsack is easier without it.

def generateBestBullets(pq):
    
    #
    # Convert to a list
    #
    
    pqList = pq.to_list()
    sectionOccurances = {}
    subsectionOccurances = {}
    
    #
    # Give the best n bullets a really high score
    # so they are gurenteed to show up on the resume --
    # where n is the number of subsections that need to appear
    #
    
    i = 0;
    for item in pqList:
        
        item['final_global_index'] = i
        i += 1
        
        sec = item["section"] 
        subsec = sec + item['subsection']
        
        # Add 2 unique
        occurances = sectionOccurances.get(sec, 0)
        minimum = sectionData.get(sec).get('minimum_to_show', 0)
        
        if occurances < minimum:
        
            # Added -- will show
            if subsec not in subsectionOccurances:
                item['score'] = 10 
                subsectionOccurances[subsec] = 1
                sectionOccurances[sec] = occurances + 1 # tally that we marked one
    
    
    
    bestConfig, max_score = knapsack_with_sections(pqList, LINESALLOWED, SUBSECTIONLINEHEIGHT);
    print(bestConfig, '\nwith best score', max_score)
    
    return bestConfig
    


def totalScore(groupOfBullets):
    score = 0
    for bulletScoring in groupOfBullets:
        score += bulletScoring['score']
        
    return score

def knapsack_with_sections(objects, max_height, section_cost):
    # objects is a list of dictionaries with keys: "score", "height", and "section"
    # max_height is the maximum height capacity
    # section_cost is the additional height cost per section
    
    n = len(objects)
    
    # Initialize a table to store the maximum score for each height up to max_height
    dp = [{} for _ in range(max_height + 1)]
    dp[0][frozenset()] = 0  # Initialize the base case

    # Fill the table
    for obj in objects:
        score, height, section = obj["score"], obj["lines"], obj["subsection"]
        
        for h in range(max_height, -1, -1):
            for sections_used in list(dp[h].keys()):
                current_score = dp[h][sections_used]
                new_height = h + height + (section_cost if section not in sections_used else 0)
                if new_height <= max_height:
                    new_sections_used = sections_used | frozenset([section])
                    if new_height not in dp or new_sections_used not in dp[new_height]:
                        dp[new_height][new_sections_used] = current_score + score
                    else:
                        dp[new_height][new_sections_used] = max(dp[new_height][new_sections_used], current_score + score)
    
    # Find the maximum score achievable
    max_score = 0
    best_combination = []
    for h in range(max_height + 1):
        for sections_used in dp[h]:
            if dp[h][sections_used] > max_score:
                max_score = dp[h][sections_used]
                best_combination = [obj for obj in objects if frozenset([obj["subsection"]]) & sections_used]

    return best_combination, max_score

# def generateBestBullets_aux(currentListbulletList, listOfBullets, indexOn, memo = {}):

#     if (currentListbulletList == None): 
#         return None

#     lineCount = calculateLineCount(currentListbulletList)
#     if (lineCount == LINESALLOWED):
#         return currentListbulletList
    
#     if (lineCount > LINESALLOWED):
#         return [] # won't be able to fit this configuration

#     # Not parseable anymore
#     if (indexOn >= len(listOfBullets)):
#         return currentListbulletList

#     # Get Current Item
#     bulletItem = listOfBullets[indexOn]
    
#     # Create Bullet Lists
#     withBullet = [x for x in currentListbulletList]
#     withBullet.append(bulletItem)
#     withoutBullet = [x for x in currentListbulletList]
    
#     #
#     hashingWith = tuple([x.get('final_global_index') for x in withBullet])
#     hashingWithout = tuple([x.get('final_global_index') for x in withoutBullet])
    
#     # Check Best
#     if hashingWith not in memo:
#         optimalWith = generateBestBullets_aux(withBullet, listOfBullets, indexOn+1, memo)
#         memo[hashingWith] = deepcopy(optimalWith)
#     else:
#         optimalWith = memo[hashingWith]
#         print('hit')
        
#     if hashingWithout not in memo:
#         optimalWithout = generateBestBullets_aux(withoutBullet, listOfBullets, indexOn+1, memo)
#         memo[hashingWith] = deepcopy(optimalWithout)
#     else:
#         optimalWithout = memo[hashingWithout]
#         print('hit')
        
#     withScore = totalScore(optimalWith)
#     withoutScore = totalScore(optimalWithout)
    
#     # Passback
    
#     if optimalWith is None:
#         return optimalWithout
#     if optimalWithout is None:
#         return optimalWith
    

#     return optimalWith if withScore > withoutScore else optimalWithout
    
    
#
#
#
#
#

def orderBestBullets(bestBullets):
    
    #
    # Place into correct bucket
    #
    
    data = {}
    for bullet in bestBullets:
        
        sec = bullet['section']
        subsec = bullet['subsection']
        
        if sec not in data:
            data[sec] = {}
        
        if subsec not in data[sec]:
            data[sec][subsec] = []
            
        data[sec][subsec].append(bullet)
        
    #
    # Order each subsection in the JSON order
    for sec in data:
        
        print(sec)
        for subsec in data[sec]:
            
            print(f'\t{subsec}')
            data[sec][subsec] = sorted(data[sec][subsec], key=lambda obj: obj['local_index'], reverse=True)
            
            for bullet in data[sec][subsec]:
                item = bullet['text']
                print(f'\t\t{item}')
                
            
    # Sort & Passback
    return sort_keys(sectionData, data)

#
#
#

def month_key(month):
    
    if month == 1:
        return 'Jan.'
    if month == 2:
        return 'Feb.'
    if month == 3:
        return 'Mar.'
    if month == 4:
        return 'Apr.'
    if month == 5:
        return 'May'
    if month == 6:
        return 'June'
    if month == 7:
        return 'July'
    if month == 8:
        return 'Aug.'
    if month == 9:
        return 'Sep.'
    if month == 10:
        return 'Oct.'
    if month == 11:
        return 'Nov.'
    if month == 12:
        return 'Dec.'

def writeLocation(subSecData, locationState):
    
    state = subSecData['state']
    city = subSecData['city']
    country = subSecData['country']
    
    if locationState == 'out-country':
        return f'{state}, {country}'
    return f'{city}, {state}'


def generateListSection(resumeContent, section, locationState):
    
    # Get
    try:
        sec = sectionData[section]
        check = resumeContent[section]
    except:
        return ''
    
    template = sec.get('latexCode')
    
    string = ''
    # Go Over
    for subsection in check:
        
        # Get the Data from the correct subsection
        subSecData = {}
        for subsectionData in sec['subsections']:
            if subsectionData['title'] == subsection:
                subSecData = subsectionData
                break
            
        # Generate the subsection header
            
        templateHeader = copy(template)
        for key, value in subSecData.items():
            
            # Date Handle
            if key in {'from', 'until', 'date'}:
                try:
                    date = datetime.strptime(value, '%Y/%m/%d')
                    month = month_key(date.month)
                    value = f'{month} {date.year}'
                except:
                    pass
            
            templateHeader = templateHeader.replace(f'%{key.upper()}', str(value))
            
        # Replace LOCATION
        if '%LOCATION' in templateHeader:
            templateHeader = templateHeader.replace('%LOCATION', writeLocation(subSecData, locationState))
            
        #
        # GENERATE POINTS
        #
        bulletString = '\\resumeItemListStart\n'
        
        # Go OVer
        bulletPoints = resumeContent[section][subsection]
        for bulletPonit in bulletPoints:
            
            #Add 
            score = bulletPonit['score'] 
            text = f'({score:.2f}) ' + bulletPonit['text']
            bulletString += '\\resumeItem{' + text + '}\n'
            
        bulletString += '\\resumeItemListEnd'
        
        # Store
        string += templateHeader + '\n\n' + bulletString + '\n\n\n'
    
    #Out
    return string

def sort_keys(original, new):
    sorted_new_json = {}
    
    for section, subsection_dict in original.items():
        if section in new:
            original_subsections = [x.get('title') for x in subsection_dict["subsections"]]
            new_section = new[section]
            sorted_section = {}
            for key in original_subsections:
                if key in new_section:
                    sorted_section[key] = new_section[key]
            sorted_new_json[section] = sorted_section
    
    return sorted_new_json


def createLatexDocument(string, resumeContent, locationState):
  
        string = string.replace('$$$WORK EXPERIENCE$$$',generateListSection(resumeContent, 'work_experience', locationState))
        string = string.replace('$$$PROJECTS$$$', generateListSection(resumeContent, 'projects', locationState))
        
        # Others
        # string = string.replace('$$$PROJECTS$$$', generateListSection(resumeContent, 'projects', locationState))
        return string