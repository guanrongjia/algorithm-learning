def fill_table_score(section1, section2):
    ''' fill table '''
    m = len(section1) + 1
    n = len(section2) + 1
    table = [[0 for j in range(n)] for i in range(m)]
    for i in range(0, m):
        for j in range(0, n):
            if i == 0 or j == 0:
                table[i][j] = i or j
            elif section1[i-1] == section2[j-1]:
                table[i][j] = table[i - 1][j - 1]
            else:
                table[i][j] = 1 + min(table[i - 1][j], table[i][j - 1],table[i - 1][j - 1])
    return table


def get_result(i, j, table, list1, list2):
    ''' get result '''
    result = []
    while i > 0 or j > 0:
        min_cost = min(table[i - 1][j], table[i][j - 1], table[i - 1][j - 1])
        if min_cost == table[i][j]:
            result.insert(0, ('T', list1[i - 1], list2[j - 1]))
            i -= 1
            j -= 1
        elif min_cost == table[i - 1][j]:
            result.insert(0, ('D', list1[i - 1], ''))
            i -= 1
        elif min_cost == table[i][j - 1]:
            result.insert(0, ('I', '', list2[j - 1]))
            j -= 1
        else:
            s1, s2 = longest_common_substring(list1[i - 1], list2[j - 1])
            result.insert(0, ('S', s1, s2))
            i -= 1
            j -= 1
    return result


def get_table_score(s1, s2, cache, i=None, j=None):
    ''' get table score '''
    if cache[i][j] == None:
        if j == 0 or i == 0:
            cache[i][j] = 0
        elif s1[i - 1] == s2[j - 1]:
            cache[i][j] = get_table_score(s1, s2, cache, i - 1, j - 1) + 1
        else:
            num_1 = get_table_score(s1, s2, cache, i, j - 1)
            num_2 = get_table_score(s1, s2, cache, i - 1, j)
            cache[i][j] = max(num_1, num_2)
    return cache[i][j]


def longest_common_substring(s1, s2):
    """ longest substring, """
    table = [[None for j in range(len(s2) + 1)] for i in range(len(s1) + 1)]
    result1 = []
    result2 = []

    def longest_substring(i, j, result1, result2, table):
        ''' get longest substring '''
        if i > 0 and j > 0:
            if s1[i-1] == s2[j-1]:
                result1.insert(0, s1[i - 1])
                result2.insert(0, s2[j - 1])
                longest_substring(i - 1, j - 1, result1, result2, table)
            else:
                if get_table_score(s1, s2, table, i-1, j) <= get_table_score(s1, s2, table, i, j-1):
                    result2.insert(0, '[[{}]]'.format(s2[j - 1]))
                    longest_substring(i, j - 1, result1, result2, table)
                else:
                    result1.insert(0, '[[{}]]'.format(s1[i - 1]))
                    longest_substring(i - 1, j, result1, result2, table)
        else:
            if i > 0:
                result1.insert(0, ''.join(['[[{}]]'.format(char) for char in s1[:i]]))
            if j > 0:
                result2.insert(0, ''.join(['[[{}]]'.format(char) for char in s2[:i]]))

    longest_substring(len(s1), len(s2), result1, result2, table)
    return ''.join(result1), ''.join(result2)


def line_edits(str1, str2):
    ''' line edits '''
    str_list1 = str1.splitlines()
    str_list2 = str2.splitlines()
    i = len(str_list1)
    j = len(str_list2)
    table = fill_table_score(str_list1, str_list2)
    return get_result(i, j, table, str_list1, str_list2)


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

