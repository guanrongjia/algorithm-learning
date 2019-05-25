def longest_common_substring(s1, s2, cache=None, i=None, j=None):
    '''longest_common_substring'''
    lst_1 = list(s1)
    lst_2 = list(s2)

    if cache == None:
        i = len(s1)
        j = len(s2)
        cache = [[None for _ in range(j+1)] for __ in range(i+1)]

    if cache[i][j] == None:
        if j == 0 or i == 0:
            cache[i][j] = ''
            return ''
        elif lst_1[i-1] == lst_2[j-1]:
            table = longest_common_substring(s1, s2, cache, i - 1, j - 1) + s1[i - 1]
            cache[i][j] = table
            return table
        else:
            num_1 = len(longest_common_substring(s1, s2, cache, i, j - 1))
            num_2 = len(longest_common_substring(s1, s2, cache, i - 1, j))
            if num_1 > num_2:
                table = longest_common_substring(s1, s2, cache, i, j - 1)
            else:
                table = longest_common_substring(s1, s2, cache, i - 1, j)
            cache[i][j] = table
            return table
    return cache[i][j]


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