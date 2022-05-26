from queryBuilder.constant import VALID_OPERATOR
import json
from django.db.models import Q
from queryBuilder.models import Resume


def construct_sql_query(
        input_query: list,
):
    """
    Contructs sql query.
    :param input_query:
    :return:
    """
    sql_query = "SELECT * FROM resume WHERE "
    open_count = 0
    column_name = "text"
    for i in input_query:
        if '_' in i:
            i = i.replace('_', ' ')
        if '(' in i:
            sql_query += f'({column_name} RLIKE "{i[1:]}"'
            open_count += 1
        elif i in VALID_OPERATOR:
            sql_query += f' {i} '
        elif ')' in i:
            sql_query += f'{column_name} RLIKE "{i[:-open_count]}"{")" * open_count}'
            open_count = 0
        else:
            sql_query += f'{column_name} RLIKE "{i}"'
    return sql_query


def construct_mongo_query(
        input_query: list,
):
    """
    Contructs mongo query.
    :param input_query:
    :return:
    """
    mongo_query = "db.resume.find({0})"
    result = {}
    stack = []
    operator = []
    curr_lvl = 0
    column_name = 'text'
    open_count = 0
    if len(input_query) == 1:
        return mongo_query.format({column_name: f'/.*{input_query[0][1:-1]}.*/'})
    for inp in input_query:
        if '_' in inp:
            inp = inp.replace('_', ' ')
        if '(' in inp:
            open_count += 1
            curr_lvl += 1
            dict = {column_name: f'/.*{inp[1:]}.*/'}
            stack.append((dict, curr_lvl))
        elif inp in VALID_OPERATOR:
            if not result:
                if (inp, curr_lvl) not in operator:
                    operator.append((inp, curr_lvl))
            else:
                curr_lvl += 1
                if (inp, curr_lvl) not in operator:
                    operator.append((inp, curr_lvl))
                stack.append((result, curr_lvl))
                result = {}
        elif ')' in inp:
            close_count = inp.count(')')
            dict = {column_name: f'/.*{inp[:-close_count]}.*/'}
            open_count = 0
            stack.append((dict, curr_lvl))
            while curr_lvl:
                optr, optr_lvl = operator[-1]
                if optr_lvl != curr_lvl:
                    curr_lvl -= 1
                    stack.append((result, curr_lvl))
                    result = {}
                    break
                optr, optr_lvl = operator.pop()
                while stack:
                    element, element_lvl = stack[-1]
                    if element_lvl != curr_lvl:
                        curr_lvl -= 1
                        stack.append((result, curr_lvl))
                        result = {}
                        break
                    element, element_lvl = stack.pop()
                    key = f'${optr}'
                    if key not in result:
                        result[key] = []
                    if key in result:
                        result[key].append(element)
                if optr_lvl == curr_lvl:
                    curr_lvl -= 1
        else:
            stack.append(({column_name: '/.*{i}.*/'}, curr_lvl))
    return mongo_query.format(json.dumps(result))


def construct_orm_query(
        input_query: list,
):
    """
    Contructs orm query.
    :param input_query:
    :return:
    """
    result = Q()
    stack = []
    operator = []
    curr_lvl = 0
    open_count = 0
    if len(input_query) == 1:
        f = Q(text__icontains=input_query[0][1:-1])
        return [obj.name for obj in Resume.objects.filter(f)]
    for inp in input_query:
        if '_' in inp:
            inp = inp.replace('_', ' ')
        if '(' in inp:
            open_count += 1
            curr_lvl += 1
            f = Q(text__icontains=inp[1:])
            stack.append((f, curr_lvl))
        elif inp in VALID_OPERATOR:
            if not result:
                if (inp, curr_lvl) not in operator:
                    operator.append((inp, curr_lvl))
            else:
                curr_lvl += 1
                if (inp, curr_lvl) not in operator:
                    operator.append((inp, curr_lvl))
                stack.append((result, curr_lvl))
                result = Q()
        elif ')' in inp:
            f = Q(text__icontains=inp[:-open_count])
            stack.append((f, curr_lvl))
            open_count = 0
            while curr_lvl:
                optr, optr_lvl = operator[-1]
                if optr_lvl != curr_lvl:
                    curr_lvl -= 1
                    stack.append((result, curr_lvl))
                    result = Q()
                    break
                optr, optr_lvl = operator.pop()
                while stack:
                    element, element_lvl = stack[-1]
                    if element_lvl != curr_lvl:
                        curr_lvl -= 1
                        stack.append((result, curr_lvl))
                        result = Q()
                        break
                    element, element_lvl = stack.pop()
                    if optr == 'AND':
                        result &= element
                    if optr == 'OR':
                        result |= element
                if optr_lvl == curr_lvl:
                    curr_lvl -= 1
        else:
            stack.append((Q(text__icontains=inp), curr_lvl))
    return [obj.name for obj in Resume.objects.filter(result)]