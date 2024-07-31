
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
        score, height, section = obj.score, obj.lines, obj.subsection
        
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
                best_combination = [obj for obj in objects if frozenset([obj.subsection]) & sections_used]

    return best_combination, max_score

def sort_keys(original, new):
    sorted_new_json = {}
    
    for section, subsection_dict in original.items():
        if section in new:
            original_subsections = [x for x in subsection_dict]
            new_section = new[section]
            sorted_section = {}
            for key in original_subsections:
                if key in new_section:
                    sorted_section[key] = new_section[key]
            sorted_new_json[section] = sorted_section
    
    return sorted_new_json