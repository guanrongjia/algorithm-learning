def get_table_score(s1, s2, cache, i=None, j=None):
    ''' using Recursion to calculate value of table cell '''
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
    """ longest substring """
    table = [[None for j in range(len(s2) + 1)] for i in range(len(s1) + 1)]
    result = [0] * (get_table_score(s1, s2, table, len(s1), len(s2)))

    def longest_substring(i, j):
        ''' get longest substring '''
        if i > 0 and j > 0:
            if s1[i-1] == s2[j-1]:
                result[get_table_score(s1, s2, table, i, j) - 1] = s1[i - 1]
                longest_substring(i - 1, j - 1)
            else:
                if get_table_score(s1, s2, table, i-1, j) <= get_table_score(s1, s2, table, i, j-1):
                    longest_substring(i, j - 1)
                else:
                    longest_substring(i - 1, j)
    longest_substring(len(s1), len(s2))
    return ''.join(result)


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