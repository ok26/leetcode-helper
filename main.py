import sys
import json

from query import get_problem_data, get_daily_problem
from link import run_tests

def main():
    args = sys.argv
    if len(args) == 1:
        print("Missing arguments") # Add help later

    args = args[1:]

    if args[0] == "test":
        test_active()

    elif args[0] == "clear":
        if len(args) == 1:
            print("Expected problem-name or \"all\"")
        clear_problem(args[1])
    
    elif args[0] == "set":
        if len(args) == 1:
            print("Expected problem-name")
        set_problem(args[1])
        

    else:
        print("Unknown arguments")
    

def load_cache():
    with open("problem_list.json", "r") as file:
        data = json.load(file)
        return data


def overwrite_cpp(problem_data):
    with open("leetcode.cpp", "w") as file:
        file.write(f"#include <bits/stdc++.h>\n\n{problem_data["code"]}")
    
    binding_code = ""
    with open("binding.cpp", "r") as file:
        binding_code = file.read()
    
    idx = binding_code.index("Solution solution;") + 18
    idx2 = binding_code.index("return 0;")
    binding_code = binding_code[:idx] + binding_code[idx2:]
    example_calls = ""
    for example in problem_data["examples"]:
        example_calls += f"\tprint(solution.{example[0]});std::cout<<std::endl;\n"
    binding_code = binding_code[:idx] +  "\n" + example_calls + binding_code[idx:]

    with open("binding.cpp", "w") as file:
        file.write(binding_code)


def test_active():
    problem_list = load_cache()
    if problem_list["active"] == "":
        print("No problem currently active")
        return
    
    test_output = run_tests()
    if not test_output:
        return

    test_output = test_output.split("\n")
    examples = []
    for problem in problem_list["problem_list"]:
        if problem["name"] == problem_list["active"]:
            for example in problem["examples"]:
                examples.append(example)
    
    for i in range(len(examples)):
        print(f"Test {i + 1}:\nInput: {examples[i][0]}\nsExpected output: {examples[i][1]}\nTest output: {test_output[i]}\n")
    

def set_problem(problem_name):
    if problem_name == "daily":
        problem_name = get_daily_problem()
        
    problem_list = load_cache()
    if problem_list["active"] == problem_name:
        print(f"Already set to {problem_name}")
        return
    
    for problem in problem_list["problem_list"]:
        if problem["name"] == problem_name:
            problem_list["active"] = problem_name
            problem_list["active_examples"] = problem["examples"]
            overwrite_cpp(problem)
            with open("problem_list.json", "w") as file:
                json.dump(problem_list, file, indent=4)
            return

    data = get_problem_data(problem_name)
    if not data:
        return
    
    return_type, code, examples = data
    
    problem_list["problem_list"].append({"name": problem_name, "code": code.replace("&", ""), "return_type": return_type, "examples": examples})
    problem_list["active"] = problem_name
    problem_list["active_examples"] = examples
    overwrite_cpp(problem_list["problem_list"][-1])

    with open("problem_list.json", "w") as file:
        json.dump(problem_list, file, indent=4)


def clear_problem(problem_name):
    problem_list = load_cache()
    if problem_name == "all":
        problem_list["problem_list"].clear()
        problem_list["active"] = ""
        problem_list["active_examples"] = ""
    
    else:
        found = False
        for i, problem in enumerate(problem_list["problem_list"]):
            if problem["name"] == problem_name:
                problem_list["problem_list"].pop(i)
                if problem_list["active"] == problem_name:
                    problem_list["active"] = ""
                    problem_list["active_examples"] = ""
                found = True
        
        if not found:
            print("Problem does not exist in save")
    
    with open("problem_list.json", "w") as file:
        json.dump(problem_list, file, indent=4)
        


if __name__ == "__main__":
    main()