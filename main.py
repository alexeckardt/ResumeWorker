from datetime import datetime
import json
from prelim import create_bullets_pq, createLatexDocument, generate_key_words_from_job, generateBestBullets, orderBestBullets

def outResume(resumeOrdered, companyName, positionName, locationState):
    
    with open('template.tex', 'r') as f:
        outString = f.read()

    outString = createLatexDocument(outString, resumeOrdered, locationState)
    
    with open('./exports/Alexander Eckardt.tex', 'w') as f:
        f.write(outString)
        
    with open(f'./exports/Backlog/{datetime.today().year}-{companyName}-{positionName}.tex', 'w') as f:
        f.write(outString)
    
    




def main():
    
    with open('fields.json', 'r') as f:
        data = json.load(f)
    
    # Get Job Description
    positionName = 'Software Developer'
    companyName = 'Google'
    locationState = 'in-state' #in-state, out-state, out-country
    
    
    
    bestkeywords = generate_key_words_from_job(positionName, companyName)

    # Transform Json into scoring json
    rankedBullets = create_bullets_pq(data, bestkeywords)    
    
    bestBullets = generateBestBullets(rankedBullets)
    
    resumeOrdered = orderBestBullets(bestBullets)
    
    #
    #
    outResume(resumeOrdered, companyName, positionName, locationState)
    
if __name__ == '__main__':
    main()
    pass