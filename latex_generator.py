from copy import copy, deepcopy
from datetime import datetime
import json

LINELENGTH = 100
DISPLAYSCORE = True

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
    
    # Get Data
    sectionData = {}
    with open('fields.json', 'r') as f:
        sectionData = json.load(f)
    
    # Get
    try:
        sec = sectionData[section]
        check = resumeContent[section]
    except:
        return ''
    
    template = sec.get('latex_code')
    
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
        for bulletPoint in bulletPoints:
            
            #Add 
            if DISPLAYSCORE:
                score = bulletPoint.score
                text = f'({score:.2f}) ' + bulletPoint.text
            else:
                text = bulletPoint.text
                
                
            bulletString += '\\resumeItem{' + text + '}\n'
            
        bulletString += '\\resumeItemListEnd'
        
        # Store
        string += templateHeader + '\n\n' + bulletString + '\n\n\n'
    
    #Out
    return string

def generate_hline(resumeContent, sectionName):
    
    # Get Data
    sectionData = {}
    with open('fields.json', 'r') as f:
        sectionData = json.load(f)
    
    # Get
    try:
        sec = sectionData[sectionName]
        check = resumeContent[sectionName]
    except:
        return ''
    
    template = sec.get('latex_code')
    
    string = ''
    
    # Go Over
    for subsection in check:
        
        listt = ''
        for item in check.get(subsection):
            listt += item + ', '
        string += template.replace('%SECTION', subsection).replace('%LIST', listt[:-2])
        
    return string


def createLatexDocument(string, resumeContent, locationState):
  
        string = string.replace('$$$WORK EXPERIENCE$$$',generateListSection(resumeContent, 'work_experience', locationState))
        string = string.replace('$$$PROJECTS$$$', generateListSection(resumeContent, 'projects', locationState))
        
        string = string.replace('$$$TECHSKILLS$$$', generate_hline(resumeContent, 'technical_skills'))
        
        # Others
        # string = string.replace('$$$PROJECTS$$$', generateListSection(resumeContent, 'projects', locationState))
        return string