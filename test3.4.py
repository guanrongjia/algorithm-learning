def longest_common_substring(s1, s2):
    '''ppap'''
    m = len(s1)
    n = len(s2)
    table = [[0 for _ in range(n + 1)] for __ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                table[i][j] = 0
            elif s1[i - 1] == s2[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    # print(table)
    ans1 = []
    ans2 = []
    s1_index = len(s1)
    s2_index = len(s2)
    while s1_index > 0 and s2_index > 0:
        if s1[s1_index - 1] == s2[s2_index - 1]:
            ans1.append(s1[s1_index - 1])
            ans2.append(s2[s2_index - 1])
            s1_index -= 1
            s2_index -= 1
        else:
            if table[s1_index - 1][s2_index] > table[s1_index][s2_index - 1]:
                ans1.append('[[%s]]' % s1[s1_index - 1])
                s1_index -= 1
            else:
                ans2.append('[[%s]]' % s2[s2_index - 1])
                s2_index -= 1
    if s1_index > 0:
        ans1.append(''.join(['[[%s]]' % char for char in s1[:s1_index]]))
    if s2_index > 0:
        ans2.append(''.join(['[[%s]]' % char for char in s2[:s2_index]]))
    ans1.reverse()
    ans2.reverse()
    return ''.join(ans1), ''.join(ans2)



def make_table(sec_1, sec_2):
    '''nmsl'''
    m = len(sec_1) + 1
    n = len(sec_2) + 1
    table = [[0 for _ in range(n)] for __ in range(m)]
    for i in range(n):
        table[0][i] = i
    for i in range(m):
        table[i][0] = i
    for i in range(1, m):
        for j in range(1, n):
            if sec_1[i - 1] == sec_2[j - 1]:
                table[i][j] = min(table[i - 1][j] + 1, table[i][j - 1] + 1, table[i - 1][j - 1] + 0)
            else:
                table[i][j] = min(table[i - 1][j] + 1, table[i][j - 1] + 1, table[i - 1][j - 1] + 1)
    return table


def mmp(sec_1, sec_2, table, i, j):
    '''zltzhdh'''
    lst = []
    while i > 0 or j > 0:
        if i > 0:
            num_1 = table[i - 1][j]
        else:
            num_1 = 9
        if j > 0:
            num_2 = table[i][j - 1]
        else:
            num_2 = 9
        if j > 0 and i > 0:
            num_3 = table[i - 1][j - 1]
        else:
            num_3 = 9
        num_min = min(num_1, num_2, num_3)

        if num_min == table[i][j]:
            line_data = ['T', sec_1[i - 1], sec_2[j - 1]]
            i -= 1
            j -= 1
        elif num_min == num_1:
            line_data = ['D', sec_1[i - 1], '']
            i -= 1
        elif num_min == num_2:
            line_data = ['I', '', sec_2[j - 1]]
            j -= 1
        else:
            string1, string2 = longest_common_substring(sec_1[i - 1], sec_2[j - 1])
            line_data = ['S', string1, string2]
            i -= 1
            j -= 1
        lst.append(tuple(line_data))
    return lst


def line_edits(s1, s2):
    '''ppap'''
    sec_1 = s1.splitlines()
    sec_2 = s2.splitlines()
    table = make_table(sec_1, sec_2)
    i = len(sec_1)
    j = len(sec_2)
    lst = mmp(sec_1, sec_2, table, i, j)
    lst.reverse()
    return lst



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

