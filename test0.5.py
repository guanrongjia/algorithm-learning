def line_edits(s1, s2, cache=None):
    "D = 1, I = 1, S = 1, T = 0"

    s1_list = s1.splitlines()
    s2_list = s2.splitlines()

    if cache == None:
        cache = [[-1 for _ in range(len(s2_list) + 1)] for _ in range(len(s1_list) + 1)]

    for i in range(len(s1_list) + 1):
        for j in range(len(s2_list) + 1):
            if i == 0:
                cache[i][j] = j
            elif j == 0:
                cache[i][j] = i
            elif s1_list[i - 1] == s2_list[j - 1]:

                cache[i][j] = cache[i - 1][j - 1]
            else:
                delete = cache[i - 1][j] + 1
                insert = cache[i][j - 1] + 1
                substitute = cache[i - 1][j - 1] + 1
                cache[i][j] = min(delete, insert, substitute)

    result = []
    result = turn_to_result(s1_list, s2_list, cache, result)
    result.reverse()
    return result


def turn_to_result(s1_list, s2_list, cache, result):
    """back tracking and get result in [(ty_, s1, s2)]form"""
    i = len(cache) - 1
    j = len(cache[i]) - 1

    index_s1 = len(s1_list) - 1
    index_s2 = len(s2_list) - 1

    while i > 0 and j > 0:
        min_cost = min(cache[i - 1][j], cache[i][j - 1], cache[i - 1][j - 1])

        if cache[i - 1][j - 1] == cache[i][j] and min_cost == cache[i - 1][j - 1]:
            ty_cost = "T"
            result.append((ty_cost, s1_list[index_s1], s2_list[index_s2]))
            i, j, index_s1, index_s2 = adjust_data(ty_cost, i, j, index_s1, index_s2)
        elif min_cost == cache[i - 1][j]:
            ty_cost = "D"
            result.append((ty_cost, s1_list[index_s1], ''))
            i, j, index_s1, index_s2 = adjust_data(ty_cost, i, j, index_s1, index_s2)
        elif min_cost == cache[i][j - 1]:
            ty_cost = "I"
            result.append((ty_cost, '', s2_list[index_s2]))
            i, j, index_s1, index_s2 = adjust_data(ty_cost, i, j, index_s1, index_s2)
        else:
            ty_cost = "S"
            s1 = s1_list[index_s1]
            s2 = s2_list[index_s2]
            s1_modified, s2_modified = modify_S_element(s1, s2)
            result.append((ty_cost, s1_modified, s2_modified))
            i, j, index_s1, index_s2 = adjust_data(ty_cost, i, j, index_s1, index_s2)

    adjust_null_case(i, j, result, s1_list, s2_list)
    return result


def modify_S_element(s1, s2):
    """'S' ("Substitute") will have the changes tagged as follows"""
    lcm_string = longest_common_substring(s1, s2)
    s1_modified = ""
    s2_modified = ""
    for c in s1:
        if len(lcm_string) != 0 and lcm_string[0] == c:
            s1_modified += lcm_string[0]
            lcm_string = lcm_string[1:]
        else:
            s1_modified += "[[{}]]".format(c)
    lcm_string = longest_common_substring(s1, s2)
    for c in s2:
        if len(lcm_string) != 0 and lcm_string[0] == c:
            s2_modified += lcm_string[0]
            lcm_string = lcm_string[1:]
        else:
            s2_modified += "[[{}]]".format(c)
    return s1_modified, s2_modified


def adjust_data(ty_cost, i, j, index_s1, index_s2):
    """adjust_data i, j, index_s1, index_s2 """
    if ty_cost == "T" or ty_cost == "S":
        i = i - 1
        j = j - 1
        index_s1 -= 1
        index_s2 -= 1
    elif ty_cost == "D":
        i = i - 1
        j = j
        index_s1 -= 1
    else:
        i = i
        j = j - 1
        index_s2 -= 1
    return i, j, index_s1, index_s2


def adjust_null_case(i, j, result, s1_list, s2_list):
    """adjust case when i or j == 0"""
    if len(s1_list) == 0:
        i = 0
        j = len(s2_list) - 1
        while j >= 0:
            result.append(("I", '', s2_list[j]))
            j -= 1
    elif len(s2_list) == 0:
        i = len(s1_list) - 1
        j = 0
        while i >= 0:
            result.append(("D", s1_list[i], ''))
            i -= 1
    else:
        if i != 0 and j == 0:
            while i > 0:
                result.append(("D", s1_list[i - 1], ''))
                i -= 1
        elif i == 0 and j != 0:
            while j > 0:
                result.append(("I", '', s2_list[j - 1]))
                j -= 1


def longest_common_substring(s1, s2, cache=None, i=None, j=None):
    """return lcs but without recursion"""
    if cache == None:
        i = len(s1)
        j = len(s2)
        cache = [[None for _ in range(j + 1)] for _ in range(i + 1)]
    for index_i in range(i + 1):
        for index_j in range(j + 1):
            if index_i == 0 or index_j == 0:
                cache[index_i][index_j] = 0
            elif s1[index_i - 1] == s2[index_j - 1]:
                l_c = cache[index_i - 1][index_j - 1] + 1
                cache[index_i][index_j] = l_c
            else:
                first_s = cache[index_i][index_j - 1]
                second_s = cache[index_i - 1][index_j]
                if first_s > second_s:
                    l_c = first_s
                else:
                    l_c = second_s
                cache[index_i][index_j] = l_c

    lcs = cache[i][j]
    result = lcs_back_tracking(lcs, cache, s1, s2)
    return result[::-1]


def lcs_back_tracking(lcs, cache, s1, s2):
    """to get real sequence"""
    i = len(cache) - 1
    j = len(cache[-1]) - 1
    sub_sequence = ""
    while lcs > 0:
        if s1[i - 1] == s2[j - 1]:
            sub_sequence += s1[i - 1]
            i -= 1
            j -= 1
            lcs -= 1
        else:
            if cache[i - 1][j] >= cache[i][j - 1]:
                i = i - 1
            else:
                j = j - 1
    return sub_sequence


if __name__ == '__main__':
    # auto test
    test_data = [
        {'s1': "Line1\nLine 2a\nLine3\nLine4\n",
         's2': "Line5\nline2\nLine3\n",
         'result': [('S', 'Line[[1]]', 'Line[[5]]'),
                    ('S', '[[L]]ine[[ ]]2[[a]]', '[[l]]ine2'),
                    ('T', 'Line3', 'Line3'),
                    ('D', 'Line4', '')]},

        {'s1': "        mac_address = data['macAddress']",
         's2': "        mac_address = data['mac_address']",
         'result': [('S', "        mac_address = data['mac[[A]]ddress']", "        mac_address = data['mac[[_]][[a]]ddress']")]},

        {'s1': "def empty_queue():",
         's2': "def clear_queue():",
         'result': [('S', "def e[[m]][[p]][[t]][[y]]_queue():",
                     "def [[c]][[l]]e[[a]][[r]]_queue():")]},
    ]
    for index, item in enumerate(test_data):
        print('*' * 5, index, '*' * 5)
        s1 = item.get('s1', '')
        s2 = item.get('s2', '')
        _result = item.get('result', '')
        calc_result = line_edits(s1, s2)
        is_correct = True if calc_result == _result else False
        print('is_correct    ', is_correct)
        if not is_correct:
            for one in _result:
                print('result    ', one)
            print('*' * 15)
            for one in calc_result:
                print('result    ', one)

