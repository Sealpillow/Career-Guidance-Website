import pandas as pd
from openpyxl import Workbook
import json
import os 


current_dir = os.path.dirname(os.path.abspath(__file__))
leetCodeMainPath = os.path.join(current_dir, 'LeetCodeQns.csv')
leetCodeQns = pd.read_csv(leetCodeMainPath)
# Path to the JSON file storing job skills
LEETCODE_EXCEL_PATH = os.path.join(current_dir, 'downloads/SelectedQns.xlsx')
LEETCODE_CSV_PATH = os.path.join(current_dir, 'downloads/SelectedQns.csv')
LEETCODE_JSON_PATH = os.path.join(current_dir, 'downloads/SelectedQns.json')

key_title_word = {
    'engineer','developer','analyst','achitect','administrator','specialist',
    'scientist','consultant','manager','technician','lead','director','support','operator','coordinator',
    'expert','tester','designer','consultant','intern'
}

jobMapTopics = {
    'engineer': {
        'array', 'string', 'hash table', 'dynamic programming', 'sorting',
        'greedy', 'graph', 'queue', 'stack', 'recursion', 'bit manipulation',
        'binary search', 'matrix', 'tree'
    },
    'developer': {
        'array', 'string', 'hash table', 'dynamic programming', 'sorting',
        'greedy', 'graph', 'binary search', 'queue', 'stack', 'recursion',
        'binary tree', 'tree'
    },
    'analyst': {
        'database', 'hash table', 'graph', 'sorting', 'counting',
        'probability and statistics', 'data stream'
    },
    'architect': {
        'design', 'system design', 'graph', 'tree', 'queue', 'stack', 'database'
    },
    'administrator': {
        'database', 'system design', 'concurrency', 'data stream', 'interactive'
    },
    'specialist': {
        'dynamic programming', 'number theory', 'algorithm design', 'hash table', 'binary search'
    },
    'scientist': {
        'dynamic programming', 'math', 'number theory', 'graph', 'probability and statistics', 'data stream'
    },
    'consultant': {
        'array', 'string', 'dynamic programming', 'design', 'graph',
        'database', 'sorting', 'recursion'
    },
    'manager': {
        'system design', 'project management', 'database', 'design'
    },
    'technician': {
        'system design', 'database', 'graph', 'queue', 'stack', 'tree'
    },
    'director': {
        'system design', 'project management', 'database', 'design'
    },
    'support': {
        'system design', 'database', 'graph', 'queue', 'stack', 'tree'
    },
    'operator': {
        'database', 'system design', 'queue', 'stack', 'graph'
    },
    'coordinator': {
        'project management', 'database', 'system design', 'design'
    },
    'expert': {
        'dynamic programming', 'number theory', 'algorithm design', 'graph', 'database'
    },
    'tester': {
        'array', 'string', 'dynamic programming', 'sorting', 'graph', 'tree'
    },
    'intern': {
        'array', 'string', 'hash table', 'dynamic programming', 'sorting',
        'greedy', 'graph', 'queue', 'stack'
    }
}

# to generate
def generateQuestionByJobTitle(inputJob):
    # job title-> split -> check if contain key title word -> get the array of topics -> check topics for relevant qns
    inputJob = inputJob.lower()
    jobSplit = set(inputJob.split(' '))
    selectedQns = pd.DataFrame(columns=['title','titleSlug','difficulty','url', 'topicTags'])
    keyword = jobSplit.intersection(key_title_word)
    jobLeetTopics = {topic for k in keyword for topic in jobMapTopics.get(k, [])}
    for index, qns in leetCodeQns.iterrows():
        topicList = {topic for topic in str(qns['topicTags']).split(",")}
        if jobLeetTopics.intersection(topicList):
            newRowDf = pd.DataFrame({'title': [qns['title']], 'titleSlug': [qns['titleSlug']], 'difficulty': [str(qns['difficulty'])], 'url':[f'https://leetcode.com/problems/'+ qns['titleSlug'] +'/description/'], 'topicTags': [', '.join(topicList)]})
            selectedQns = pd.concat([selectedQns,newRowDf], ignore_index=True)

        difficulty_order = ['Easy', 'Medium', 'Hard']
    selectedQns['difficulty'] = pd.Categorical(selectedQns['difficulty'], categories=difficulty_order, ordered=True)
    #exportExcel(selectedQns)
    #exportCSV(selectedQns)
    return selectedQns.to_json(), jobLeetTopics

def generateNRandomForEachDif(selectedQns, jobLeetTopics, num): # use this instead
    difficulty_order = ['Easy', 'Medium', 'Hard']
    selectedQns['difficulty'] = pd.Categorical(selectedQns['difficulty'], categories=difficulty_order, ordered=True)
    random_questions_list = []

    # Loop through each unique difficulty
    for difficulty in selectedQns['difficulty'].unique():
        subset = selectedQns[selectedQns['difficulty'] == difficulty]
        if not subset.empty:  # Check if the subset is not empty
            random_sample = subset.sample(n=min(num, len(subset)))  # No random_state
            random_questions_list.append(random_sample)

    # Concatenate all sampled DataFrames into one, check if list is not empty
    if random_questions_list:
        random_questions = pd.concat(random_questions_list).reset_index(drop=True)
    else:
        random_questions = pd.DataFrame()  # Create an empty DataFrame if no questions were sampled

    selectedQns = random_questions
    # Export functions
    exportExcel(selectedQns)
    exportCSV(selectedQns)
    exportJSON(selectedQns)
    return selectedQns.to_json(), jobLeetTopics


def generatefirstNForEachDif(selectedQns, num):
    difficulty_order = ['Easy', 'Medium', 'Hard']
    selectedQns['difficulty'] = pd.Categorical(selectedQns['difficulty'], categories=difficulty_order, ordered=True)
    selectedQns.groupby('difficulty', observed=True).head(num).reset_index(drop=True).to_json()
    return selectedQns, selectedQns['topicTags'].unique().tolist()

# to filter
def filterByTags(selectedQns, tags):
    # sort by tags
    #tags = {'design','queue','data-stream'}
    newQns = pd.DataFrame(columns=['title','titleSlug','difficulty','url', 'topicTags'])
    for index, qns in selectedQns.iterrows():
        topicList = {topic for topic in str(qns['topicTags']).split(",")}
        if set(topicList).intersection(tags):
            newRowDf = pd.DataFrame({'title': [qns['title']], 'titleSlug': [qns['titleSlug']], 'difficulty': [str(qns['difficulty'])], 'url':[f'https://leetcode.com/problems/'+ qns['titleSlug'] +'/description/'], 'topicTags': [', '.join(topicList)]})
            newQns = pd.concat([newQns,newRowDf], ignore_index=True)
    #print(newQns)
    #exportExcel(newQns)
    #exportCSV(newQns)
    return newQns.to_json(), tags

def filterByDifficulties(selectedQns, selectedDifficulties):
    # sort by difficulties
    # selectedDifficulties = {'Easy','Medium'}
    difficulty_order = ['Easy', 'Medium', 'Hard']
    selectedQns['difficulty'] = pd.Categorical(selectedQns['difficulty'], categories=difficulty_order, ordered=True)
    selectedQns = selectedQns[selectedQns['difficulty'].isin(selectedDifficulties)]
    exportExcel(selectedQns)
    exportCSV(selectedQns)
    return selectedQns, selectedQns['topicTags'].unique()

# to Export
def exportExcel(selectedQns):
    selectedQns.to_excel(LEETCODE_EXCEL_PATH, index=False)

def exportCSV(selectedQns):
    selectedQns.to_csv(LEETCODE_CSV_PATH, index=False)

def exportJSON(selectedQns):
    selectedQns.to_json(LEETCODE_JSON_PATH, index=False)

#   title	        titleSlug	difficulty	url
# 	Swap Salary	    swap-salary	Easy	    https://leetcode.com/problems/swap-salary/description/

# The selectedQns first generated by generateQuestionByJobTitle() will be saved in the flask
# If repeated filter/sort will be based on the first generated
if __name__ == "__main__":

    inputJob = 'Full Stack Engineer'
    baseQns, tags = generateQuestionByJobTitle(inputJob)
    baseQns, tags = generateNRandomForEachDif(pd.DataFrame(json.loads(baseQns)), tags, 5)
    print(type(tags))
    # 
    #sQns, tags = generateNRandomForEachDif(baseQns, 3)
    '''
    outpuQns = baseQns

    exportExcel(outpuQns)

    exportCSV(outpuQns)

    outpuQns = baseQns
    
    tags = {'design','queue','data-stream'}
    outpuQns, tags = filterByTags(outpuQns, tags)

    selectedDifficulties = {'Easy','Medium'}
    outpuQns, tags = filterByDifficulties(baseQns, selectedDifficulties)

    num = 5 
    outpuQns, tags = generateNRandomForEachDif(baseQns, num)

    num = 5 
    outpuQns, tags =  generatefirstNForEachDif(baseQns, num)
    '''