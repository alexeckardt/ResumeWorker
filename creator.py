import json
from components.PointsList import PointList
from helpers import knapsack_with_sections, sort_keys

    
SUBSECTIONLINEHEIGHT = 2
LINESALLOWED = 38 # remeber to include space for the section headers -- knapsack is easier without it.
ORDER_POINTS_BY_SCORE = True


def sort_vertical_points(bestVPoints, secData):
    
    # Place into correct vBucket
    data = {}
    for point in bestVPoints:
        
        sec = point.section
        subsec = point.subsection
        
        if sec not in data:
            data[sec] = {}
        
        if subsec not in data[sec]:
            data[sec][subsec] = []
            
        data[sec][subsec].append(point)
        
    # Order each subsection in the JSON order
    for sec in data:
        
        print(sec)
        for subsec in data[sec]:
            
            print(f'\t{subsec}')
            if not ORDER_POINTS_BY_SCORE:
                data[sec][subsec] = sorted(data[sec][subsec], key=lambda obj: obj.localIndex, reverse=False)
            
            for point in data[sec][subsec]:
                item = point.text
                print(f'\t\t{item}')
    
    # Generate RThOrder
    order = {}
    for sec in secData:
        order[sec] = {}
        for subsec in secData[sec].get('subsections'):
            order[sec][subsec['title']] = 0
    
    # Sort & Passback
    return sort_keys(order, data)


def generate_best_vertical_points(pqList, secData):
    
    sectionOccurances = {}
    subsectionOccurances = {}
    
    #
    # Give the best n bullets a really high score
    # so they are gurenteed to show up on the resume --
    # where n is the number of subsections that need to appear
    #
    
    i = 0;
    for item in pqList:
        
        item.finalGlobalIndex = i
        i += 1
        
        sec = item.section
        subsec = sec + item.subsection
        
        # Add 2 unique
        occurances = sectionOccurances.get(sec, 0)
        minimum = secData.get(sec).get('minimum_to_show', 0)
        
        if occurances < minimum:
        
            # Added -- will show
            if subsec not in subsectionOccurances:
                item.score = 10 
                subsectionOccurances[subsec] = 1
                sectionOccurances[sec] = occurances + 1 # tally that we marked one
    
    #
    #
    #
    bestConfig, max_score = knapsack_with_sections(pqList, LINESALLOWED, SUBSECTIONLINEHEIGHT);
    print(bestConfig, '\nwith best score', max_score)
    
    return sort_vertical_points(bestConfig, secData)

def generate_best_horizontal_points(hRankings):
    
    out = {}
    
    for key in hRankings:
        points = hRankings[key]
        
        # Construct
        section, subsection = tuple(key.split('.'))
        if (section not in out):
            out[section] = {}
        if (subsection not in out[section]):
            out[section][subsection] = []
        
        # Insert upto certian length
        length = len(subsection) + 3
        for point in points:
            
            pLen = len(point.text) + 2
            if (length + pLen > 110):
                break
            
            out[section][subsection].append(point.text)
            length += pLen
            
    return out

def create_resume_dict(keywords):
    
    # Get Data
    with open('fields.json', 'r') as f:
        secData = json.load(f)
        
    # Generate
    resume = PointList(keywords)
    resume.compile(secData)
    
    # Get the Best VBullets
    orderedVerticals = generate_best_vertical_points(resume.vRankings, secData);
    
    # Generate the HDirections
    orderedHorizontals = generate_best_horizontal_points(resume.hRankings)
    
    # Combine
    out = {}
    for key in orderedVerticals:
        out[key] = orderedVerticals[key]
        
    for key in orderedHorizontals:
        out[key] = orderedHorizontals[key]
        
    return out