def parse_code(code):
    words = code.replace("&", "").split()
    args = []
    types = []
    return_type = ""
    function_name = ""
    for i in range(len(words)):
        if words[i] == "public:":
            return_type = words[i + 1]
            function_name, arg_type = words[i + 2].split("(")
            types.append(arg_type)
            args.append(words[i + 3][:-1])

            if words[i + 3][-1] == ")":
                break

            for j in range(i + 4, len(words), 2):
                arg_type = words[j]
                types.append(words[j])
                args.append(words[j + 1][:-1])
                if words[j + 1][-1] == ")":
                    break
            
            break
    
    return function_name, args, types, return_type


def parse_examples(function_name, problem_desc, args, types, return_type):
    words = problem_desc.split()
    examples = []
    
    for i in range(len(words)):
        if words[i] == "Example" and len(words[i + 1]) == 2 and words[i + 1][0].isdigit() and words[i + 1][1] == ":":

            return_string = f"{function_name}("
            expected_output = ""
            for j in range(i + 2, len(words)):
                if words[j] == "Input:":
                    for p in range(j + 1, len(words), 3):
                        if words[p] == "Output:":
                            break

                        value = parse_value(types[args.index(words[p])], words[p + 2])
                        return_string += f"{value},"
                
                elif words[j] == "Output:":
                    expected_output = parse_value(return_type, words[j + 1])
                    break

            if len(return_string) != 1:
                return_string = return_string[:-1]
            examples.append([return_string + ")", expected_output])

    return examples


def parse_value(ty, value):
    if ty == "int" or ty == "string" or ty == "double" or ty == "float":
        return value
    elif "<" in ty:
        ret = "{"
        parts = ty.split("<", 1)
        if parts[1].split("<")[0] == "vector":
            for i in range(len(value)):
                if i > 0 and i < len(value) - 1 and value[i - 1:i + 2] == "],[":
                    value = value[:i] + "#" + value[i + 1:]
            value = value[1:-1].split("#")
        else:
            value = value[1:-1].split(",")

        for v in value:
            ret += f"{parse_value(parts[1][:-1], v)},"
        ret = ret[:-1]
        if ret[-1] == "]":
            ret = ret[:-1]
        return ret + "}"
    else:
        print(ty, value)
