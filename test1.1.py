def init_table(s1, s2):
    """ init_table """
    return [[None for c in range(len(s2) + 1)] for r in range(len(s1) + 1)]


def longest_common_substring(s1, s2):
    '''  longest_common_substring'''

    def calc_longest_string(s1, s2, i, j):
        ''' calc_longest_string '''
        if table[i][j] != None:
            return table[i][j]
        else:
            if j == 0 or i == 0:
                table[i][j] = ''
                return ''
            elif s1[i - 1] == s2[j - 1]:
                table[i][j] = calc_longest_string(s1, s2, i - 1, j - 1) + s1[i - 1]
                return table[i][j]
            else:
                str1 = calc_longest_string(s1, s2, i, j - 1)
                str2 = calc_longest_string(s1, s2, i - 1, j)
                if len(str1) > len(str2):
                    table[i][j] = str1
                else:
                    table[i][j] = str2
                return table[i][j]

    table = init_table(s1, s2)
    return calc_longest_string(s1, s2, len(s1), len(s2))


if __name__ == '__main__':
    # auto test
    test_data = [
        {'s1': "them",
         's2': "tim",
         'result': ['tm']},

        {'s1': "",
         's2': "",
         'result': [""]},

        {'s1': "Solidandkeen",
         's2': "Whoisn'tsick",
         'result': ["""oink"""]},

        {'s1': "Solidandkeen\nSolidandkeen\nSolidandkeen\n",
         's2': "Whoisn'tsick\nWhoisn'tsick\nWhoisn'tsick",
         'result': ["""oink\noink\noink"""]},

        {'s1': "Look at me, I can fly!",
         's2': "Look at that, it's a fly",
         'result': ['Look at ,  a fly']},

        {'s1': "abcdefghijklmnopqrstuvwxyz",
         's2': "ABCDEFGHIJKLMNOPQRSTUVWXYS",
         'result': ['']},

        {'s1': "balderdash!",
         's2': "balderdash!",
         'result': ['balderdash!']},

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
        print('is_correct    ', is_correct)
        if not is_correct:
            print('result    ', result)
            print('calc_result    ', calc_result)
        print('*' * 5)