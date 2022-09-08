import os
import ast
import json
from django.http import JsonResponse
from django.core.cache import cache


def getCacheFromFile1(file_path):
    if os.path.isfile(file_path) is False:
        return False
    else:
        file_ = open(file_path, 'r')
        data = file_.read()
        file_.close()
        # x = u'{}'.format(data)
        data = ast.literal_eval(data)



        # all_data_list.append(data[0])
        # try:
        #     data = ast.literal_eval(data)
        # except Exception as e:
        #     print(e)
        # data = JsonResponse(data, safe=False)
        # print("data={}".format(data.data))
        # data = list(map(str.strip, data.strip('][').replace('"', '').split(',')))


        return data

def getCacheFromFile(file_path):
    response = cache.get(file_path)
    if response is None:
        return None
    else:
        return response

def createFileCache(file_path, queryset):
    # if os.path.isfile(file_path) is False:
    #     file1 = open(file_path, "w+")
    #     # file1.write(data)
    #     # file1.write(str(data))
    #
    #
    #     # data = list(queryset.values())
    #     # data = list(queryset.values())
    #     # file1.write(str(data))
    #
    #     file1.close()

    try:
        response = cache.get(file_path)
        if response is None:
            cache.set(file_path, queryset, 86400000)
        return response
    except Exception as e:
        cache.set(file_path, queryset, 86400000)

