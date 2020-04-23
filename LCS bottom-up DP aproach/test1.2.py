def longest_common_substring(s1, s2):
    """ find the longest common substring """
    row_num = len(s1) + 1
    col_num = len(s2) + 1
    table = [[None] * col_num for i in range(row_num)]
    for row_index in range(row_num):
        for col_index in range(col_num):
            if row_index == 0 or col_index == 0:
                table[row_index][col_index] = 0
            elif s1[row_index - 1] == s2[col_index - 1]:
                table[row_index][col_index] = table[row_index -
                                                    1][col_index - 1] + 1
            else:
                table[row_index][col_index] = max(
                    table[row_index - 1][col_index], table[row_index][col_index - 1])
    result = []
    row_index = len(s1)
    col_index = len(s2)
    while row_index > 0 and col_index > 0:
        if s1[row_index - 1] == s2[col_index - 1]:
            result.append(s1[row_index - 1])
            row_index -= 1
            col_index -= 1
        else:
            if table[row_index - 1][col_index] > table[row_index][col_index - 1]:
                row_index -= 1
            else:
                col_index -= 1
    result.reverse()
    return ''.join(result)


if __name__ == '__main__':
    # auto test
    test_data = [{'s1': "Look at me, I can fly!",
                  's2': "Look at that, it's a fly",
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
