def calc_score_table(section1, section2):
    ''' return score of position in table  '''
    m = len(section1) + 1
    n = len(section2) + 1
    table = [[0 for i in range(n)] for j in range(m)]
    for t in range(n):
        table[0][t] = t
    for t in range(m):
        table[t][0] = t
    for i in range(1, m):
        for j in range(1, n):
            table[i][j] = min(table[i - 1][j] + 1, table[i][j - 1] + 1,
                              table[i - 1][j - 1] + (0 if section1[i - 1] == section2[j - 1] else 1))
    return table


def line_edits(str1, str2):
    ''' main function  '''
    section1 = str1.splitlines()
    section2 = str2.splitlines()
    table = calc_score_table(section1, section2)
    i = len(section1)
    j = len(section2)
    result = []
    while i > 0 or j > 0:
        _d = table[i - 1][j] if i > 0 else 9
        _i = table[i][j - 1] if j > 0 else 9
        _s = table[i - 1][j - 1] if j > 0 and i > 0 else 9
        min_change = min(_d, _i, _s)
        if min_change == table[i][j]:
            line_data = ['T', section1[i - 1], section2[j - 1]]
            i -= 1
            j -= 1
        elif min_change == _d:
            line_data = ['D', section1[i - 1], '']
            i -= 1
        elif min_change == _i:
            line_data = ['I', '', section2[j - 1]]
            j -= 1
        else:
            str1, str2 = longest_common_substring(section1[i - 1], section2[j - 1])
            line_data = ['S', str1, str2]
            i -= 1
            j -= 1

        result.append(tuple(line_data))
    result.reverse()
    return result


def longest_common_substring(s1, s2):
    """ calculate the longest common substring """
    row_num = len(s1) + 1
    col_num = len(s2) + 1
    table = [[None] * col_num for i in range(row_num)]
    for row_index in range(row_num):
        for col_index in range(col_num):
            if row_index == 0 or col_index == 0:
                table[row_index][col_index] = 0
            elif s1[row_index - 1] == s2[col_index - 1]:
                table[row_index][col_index] = table[row_index - 1][col_index - 1] + 1
            else:
                table[row_index][col_index] = max(table[row_index - 1][col_index], table[row_index][col_index - 1])
    # find longest common substring
    r1 = []
    r2 = []
    row_index = len(s1)
    col_index = len(s2)
    while row_index > 0 and col_index > 0:
        if s1[row_index - 1] == s2[col_index - 1]:
            r1.append(s1[row_index - 1])
            r2.append(s2[col_index - 1])
            row_index -= 1
            col_index -= 1
        else:
            if table[row_index - 1][col_index] > table[row_index][col_index - 1]:
                r1.append('[['+s1[row_index - 1]+']]')
                row_index -= 1
            else:
                r2.append('[['+s2[col_index - 1]+']]')
                col_index -= 1
    if row_index > 0:
        r1.append(''.join(['[['+char+']]' for char in s1[:row_index]]))
    if col_index > 0:
        r2.append(''.join(['[[{'+char+'}]]' for char in s2[:col_index]]))

    r1.reverse()
    r2.reverse()
    return ''.join(r1), ''.join(r2)


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
