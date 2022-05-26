import json

from django.http import HttpResponse

from queryBuilder.constant import SQL, MONGO, ORM
from queryBuilder.query_builder import construct_sql_query, construct_mongo_query, construct_orm_query
from queryBuilder.utils import check_if_input_is_valid, remove_space_from_multi_word
from rest_framework.decorators import api_view

input_str = "(Java AND python) OR (Ruby AND ('ruby on rails' AND ('ruby on rails' OR ROR)))"
DICT_QUERY_BUILDER = {SQL: construct_sql_query,
                      MONGO: construct_mongo_query,
                      ORM: construct_orm_query}


def get_query_fnc(
        input_query: str,
        output_format: str
):
    """

    :param input_query:
    :param output_format:
    :return:
    """
    if not check_if_input_is_valid(input_query):
        return "Input Query is not valid"

    input_query = remove_space_from_multi_word(input_query)
    input_query = input_query.split()
    result_query = DICT_QUERY_BUILDER[output_format](input_query)
    return result_query


@api_view(['POST'])
def get_query(
        request
):
    """

    :param input_query:
    :param output_format:
    :return:
    """
    input = json.loads(request.body)
    input_query = input['input_query']
    output_format = input['output_format']
    if not check_if_input_is_valid(input_query):
        return HttpResponse(json.dumps({'error_msg': "Input Query is not valid"}))

    input_query = remove_space_from_multi_word(input_query)
    input_query = input_query.split()
    result_query = DICT_QUERY_BUILDER[output_format](input_query)
    return HttpResponse(json.dumps({f'{output_format}_Query': result_query}))


# print('SQL QUERY =', get_query_fnc(input_query=input_str, output_format='SQL'))
# print('MONGO QUERY =', get_query_fnc(input_query=input_str, output_format='MONGO'))
# print('MONGO QUERY =', get_query_fnc(input_query=input_str, output_format='ORM'))


