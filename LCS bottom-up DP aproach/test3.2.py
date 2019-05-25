def longest_common_substring(s1, s2):
    '''longest_common_substring'''
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
    ans = ''

    while len(ans) != table[-1][-1]:
        # print(table[m][n])
        # print([m, n])
        if s1[m - 1] == s2[n - 1]:
            # print(s1[m-1])
            ans += s1[m - 1]
            m -= 1
            n -= 1
        else:
            num_1 = table[m][n - 1]
            num_2 = table[m - 1][n]
            if num_1 == num_2:
                m = m
                n = n - 1
            elif num_1 > num_2:
                m = m
                n = n - 1
            elif num_1 < num_2:
                m = m - 1
                n = n
    return ans[::-1]


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
