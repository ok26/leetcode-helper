from time import sleep

import requests
from bs4 import BeautifulSoup

from parse_example import parse_code, parse_examples


def get_problem_data(problem_name):
    
    code = get_editor_code(problem_name)
    if not code:
        print("Question does not exist")
        return
        
    problem_desc = get_problem_desc(problem_name)
    if not problem_desc:
        print("Question does not exist")
        return

    function_name, args, types, return_type = parse_code(code)
    return return_type, code, parse_examples(function_name, problem_desc, args, types, return_type)


def get_daily_problem():
    query = """
        query questionOfToday {
        activeDailyCodingChallengeQuestion {
            date
            userStatus
            link
            question {
            acRate
            difficulty
            freqBar
            frontendQuestionId: questionFrontendId
            isFavor
            paidOnly: isPaidOnly
            status
            title
            titleSlug
            hasVideoSolution
            hasSolution
            topicTags {
                name
                id
                slug
            }
            }
        }
        }
    """

    response = requests.post(
        'https://leetcode.com/graphql', 
        json={'query': query}
    ).json()

    problem_name = response["data"]["activeDailyCodingChallengeQuestion"]["question"]["titleSlug"]
    
    sleep(0.1)
    return problem_name


def get_editor_code(problem_name):
    query = """
        query questionEditorData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            codeSnippets {
            lang
            langSlug
            code
            }
            envInfo
            enableRunCode
        }
        }
    """

    variables = {
        "titleSlug": problem_name
    }

    response = requests.post(
        'https://leetcode.com/graphql', 
        json={'query': query, 'variables': variables}
    ).json()

    
    if response["data"]["question"] == None:
        return None

    sleep(0.1)
    return response["data"]["question"]["codeSnippets"][0]["code"]


def get_problem_desc(problem_name):
    query = """
        query questionContent($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            content
            mysqlSchemas
        }
        }
    """

    variables = {
        "titleSlug": problem_name 
    }

    response = requests.post(
        'https://leetcode.com/graphql',  
        json={'query': query, 'variables': variables}
    ).json()

    if response["data"]["question"] == None:
        return None

    soup = BeautifulSoup(response['data']['question']['content'], "html.parser")
    sleep(0.1)
    return soup.get_text()