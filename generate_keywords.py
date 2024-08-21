import pyperclip
from components.AICaller import AICaller

def create_prompt(inputData):
    with open('./prompt.txt', 'r') as f:
        text = f.read().replace('\n', '').strip()
        return text.replace('%POSITIONANME', inputData['positionName'])


def handle_prompt(inputData):
    
    # # Copy
    # pyperclip.copy(promptString)
    # print('Copied Prompt to Clipboard.')
    
    # Ask Gemini
    caller = AICaller(
        [
                {
                    "role": "user",
                    "parts": [
                        create_prompt(inputData)
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "Please provide the job description.\n",
                    ],
                },
        ]
    )
    result = caller.message(inputData['jobDesc'])
    return result;

#
# Get
def getKeywords():
     
    # Get Job Description
    positionName = 'Software Developer'
    companyName = 'Google'
    locationState = 'in-state' #in-state, out-state, out-country
    
    #  Prompt   
    job_description = '''
            Google's software engineers develop the next-generation technologies that change how billions of users connect, explore, and interact with information and one another. Our products need to handle information at massive scale, and extend well beyond web search. We're looking for engineers who bring fresh ideas from all areas, including information retrieval, distributed computing, large-scale system design, networking and data storage, security, artificial intelligence, natural language processing, UI design and mobile; the list goes on and is growing every day. As a software engineer, you will work on a specific project critical to Google’s needs with opportunities to switch teams and projects as you and our fast-paced business grow and evolve. We need our engineers to be versatile, display leadership qualities and be enthusiastic to take on new problems across the full-stack as we continue to push technology forward.
            Behind everything our users see online is the architecture built by the Technical Infrastructure team to keep it running. From developing and maintaining our data centers to building the next generation of Google platforms, we make Google's product portfolio possible. We're proud to be our engineers' engineers and love voiding warranties by taking things apart so we can rebuild them. We keep our networks up and running, ensuring our users have the best and fastest experience possible.
            With your technical expertise you will manage project priorities, deadlines, and deliverables. You will design, develop, test, deploy, maintain, and enhance software solutions.
            Google Cloud accelerates every organization's ability to digitally transform its business and industry. We deliver enterprise-grade solutions that leverage Google’s cutting-edge technology, and tools that help developers build more sustainably. Customers in more than 200 countries and territories turn to Google Cloud as their trusted partner to enable growth and solve their most critical business problems.
            The US base salary range for this full-time position is $161,000-$239,000 + bonus + equity + benefits. Our salary ranges are determined by role, level, and location. The range displayed on each job posting reflects the minimum and maximum target salaries for the position across all US locations. Within the range, individual pay is determined by work location and additional factors, including job-related skills, experience, and relevant education or training. Your recruiter can share more about the specific salary range for your preferred location during the hiring process.
                '''
    job_description = input('Paste Job Description in:\n').strip().replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')
    
    # Passback Result
    return {
        'positionName': positionName,
        'companyName': companyName,
        'locationState': locationState,
        'bestkeywords': handle_prompt(job_description)
    }