from datetime import datetime
import json
from creator import create_resume_dict
from generate_keywords import getKeywords, handle_prompt
from latex_generator import createLatexDocument

def outResume(resumeOrdered, inputData):
    
    with open('template.tex', 'r') as f:
        outString = f.read()

    outString = createLatexDocument(outString, resumeOrdered, inputData['locationState'])
    
    with open('./exports/Alexander Eckardt.tex', 'w') as f:
        f.write(outString)
        
    c = inputData['companyName']
    p = inputData['positionName']
    with open(f'./exports/Backlog/{datetime.today().year}-{c}-{p}.tex', 'w') as f:
        f.write(outString)
    
    

def runResumeScript(inputData):

    # Get
    # inputData = getKeywords()
    print('f')
    criteria = handle_prompt(inputData)

    # Transform Json into scoring json
    resumeDict = create_resume_dict(criteria)
    
    # bestBullets = generateBestBullets(rankedBullets)
    
    # resumeOrdered = orderBestBullets(bestBullets)
    
    # #
    # #
    outResume(resumeDict, inputData)
    
if __name__ == '__main__':
    runResumeScript()
    pass