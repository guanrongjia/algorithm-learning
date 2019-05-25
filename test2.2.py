def fill_table_score(ni, nj, s1, s2):
    ''' fill out the table'''
    table = [[0] * nj for i in range(ni)]
    for i in range(ni):
        for j in range(nj):
            if i == 0 or j == 0:
                table[i][j] = 0
            elif s1[i - 1] == s2[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table


def longest_common_substring(s1, s2):
    """ get longest substring """
    i = ni = len(s1)
    j = nj = len(s2)
    table = fill_table_score(ni + 1, nj + 1, s1, s2)
    result = []
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            result.append(s1[i - 1])
            i -= 1
            j -= 1
        else:
            if table[i - 1][j] > table[i][j - 1]:
                i -= 1
            else:
                j -= 1
    result.reverse()
    return ''.join(result)


if __name__ == '__main__':
    # auto test
    test_data = [{'s1' : "Look at me, I can fly!",
                  's2' : "Look at that, it's a fly",
                  'result': ['Look at ,  a fly']},

                 {'s1': "abcdefghijklmnopqrstuvwxyz",
                  's2': "ABCDEFGHIJKLMNOPQRSTUVWXYS",
                  'result': ['']},

                 {'s1': "balderdash!",
                  's2': "balderdash!",
                  'result': ['balderdash!']},

                 {'s1': 1500 * "x",
                  's2': 1500 * "y",
                  'result': ['']},

                 {'s1': "xyxxzx",
                  's2': "zxzyyzxx",
                  'result': ['xyxx', 'xyzx']},
                 ]

    for index, item in enumerate(test_data):
        print('*' * 5, index, '*' * 5)
        s1 = item.get('s1', '')
        s2 = item.get('s2', '')
        result = item.get('result', '')
        calc_result = longest_common_substring(s1, s2)
        is_correct = True if calc_result in result else False
        if not is_correct:
            print('result         ', result)
            print('calc_result    ', calc_result)
        print('is_correct    ', is_correct)


