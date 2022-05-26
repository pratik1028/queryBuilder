def check_if_input_is_valid(
        input_query: str,
):
    """

    :param input_query:
    :return:
    """
    stack = []
    open_list = ['(']
    quotes_list = ['"', "'"]
    close_list = [')']
    for i in input_query:
        if i in quotes_list and stack[len(stack) - 1] != i:
            stack.append(i)
        elif i in quotes_list and stack[len(stack) - 1] == i:
            stack.pop()
        if i in open_list:
            stack.append(i)
        elif i in close_list:
            pos = close_list.index(i)
            if ((len(stack) > 0) and
                    (open_list[pos] == stack[len(stack) - 1])):
                stack.pop()
            else:
                return False
    if len(stack) == 0:
        return True
    else:
        return False


def remove_space_from_multi_word(
        input_query: str
):
    """

    :param input_query:
    :return:
    """
    temp_input_query = list(input_query)
    i = 0
    while i < len(temp_input_query):
        if temp_input_query[i] not in ['"', "'"]:
            i += 1
            continue
        temp_input_query.pop(i)
        while temp_input_query[i] not in ['"', "'"]:
            if temp_input_query[i] == ' ':
                temp_input_query[i] = '_'
            i += 1
        temp_input_query.pop(i)
    # Add ( ) if does not exists
    if temp_input_query[0] != '(':
       return '({})'.format("".join(temp_input_query))
    return "".join(temp_input_query)