def calc_score_table(section1, section2):
    ''' calc_score_table '''
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
    ''' line_edits '''
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
            line_data = ['C', section1[i - 1], section2[j - 1]]
            i -= 1
            j -= 1
        elif min_change == _d:
            line_data = ['D', section1[i - 1], '']
            i -= 1
        elif min_change == _i:
            line_data = ['I', '', section2[j - 1]]
            j -= 1
        else:
            line_data = ['S', section1[i - 1], section2[j - 1]]
            i -= 1
            j -= 1

        result.append(tuple(line_data))
    result.reverse()
    return result


if __name__ == '__main__':
    # auto test
    test_data = [
        {'s1': "Line1\n",
         's2': "",
         'result': [('D', 'Line1', '')]},

        {'s1': "Line1\nLine3\nLine5\n",
         's2': "Twaddle\nLine5\n",
         'result': [('D', 'Line1', ''), ('S', 'Line3', 'Twaddle'),  ('C', 'Line5', 'Line5')]},

        {'s1': "Line1\nLine2\nLine3\nLine4\n",
         's2': "Line1\nLine3\nLine4\nLine5\n",
         'result': [('C', 'Line1', 'Line1'), ('D', 'Line2', ''), ('C', 'Line3', 'Line3'),
                    ('C', 'Line4', 'Line4'), ('I', '', 'Line5')]},

        {'s1': "Line1\nLine2\nLine3\nLine4\n",
         's2': "Line5\nLine4\nLine3\n",
         'result': [('S', 'Line1', 'Line5'), ('S', 'Line2', 'Line4'), ('C', 'Line3', 'Line3'),
                    ('D', 'Line4', '')]},

        {'s1': r'''# ============== DELETEs =====================
# TODO: add docstrings
@app.route('/queue/<hostname>', methods=['DELETE'])
def delete(hostname):
    try:
        data = json.loads(request.get_data())
        mac_address = data['macAddress']
    except:
        abort(400, 'Missing or invalid user data')
    status = queue.dequeue(hostname, macAddress)
    return ('', status)


@app.route('/queue', methods=['DELETE'])
def empty_queue():
    if request.remote_addr.upper() != TUTOR_MACHINE.upper():
        abort(403, "Not authorised")
    else:
        queue.clear_queue()
        response = jsonify({"message": "Queue emptied"})
        response.status_code = 204
        return response
''',

         's2': r'''# ============== DELETEs =====================
@app.route('/queue/<hostname>', methods=['DELETE'])
def delete(hostname):
    """Handle delete request from the given host"""
    try:
        data = json.loads(request.get_data())
        mac_address = data['mac_address']
    except:
        abort(400, 'Missing or invalid user data')
    status = queue.dequeue(hostname, mac_address)
    return ('', status)


@app.route('/queue', methods=['DELETE'])
def clear_queue():
    """Clear the queue. Valid only if coming from tutor machine"""
    if request.remote_addr.upper() != TUTOR_MACHINE.upper():
        abort(403, "Only the tutor machine can clear the queue")
    else:
        queue.clear_queue()
        response = jsonify({"message": "Queue cleared"})
        response.status_code = 204
        return response
''',
         'result': [
             ('C', '# ============== DELETEs =====================',
              '# ============== DELETEs ====================='),
             ('D', '# TODO: add docstrings', ''), ('C', "@app.route('/queue/<hostname>', methods=['DELETE'])",
                                                   "@app.route('/queue/<hostname>', methods=['DELETE'])"),
             ('C', 'def delete(hostname):', 'def delete(hostname):'),
             ('I', '', '    """Handle delete request from the given host"""'), ('C',
                                                                                '    try:', '    try:'),
             ('C', '        data = json.loads(request.get_data())',
              '        data = json.loads(request.get_data())'),
             ('S', "        mac_address = data['macAddress']",
              "        mac_address = data['mac_address']"),
             ('C', '    except:', '    except:'), ('C', "        abort(400, 'Missing or invalid user data')",
                                                   "        abort(400, 'Missing or invalid user data')"), (
                 'S', '    status = queue.dequeue(hostname, macAddress)',
                 '    status = queue.dequeue(hostname, mac_address)'),
             ('C', "    return ('', status)",
              "    return ('', status)"), ('C', '', ''), ('C', '', ''),
             ('C', "@app.route('/queue', methods=['DELETE'])",
              "@app.route('/queue', methods=['DELETE'])"),
             ('S', 'def empty_queue():', 'def clear_queue():'),
             ('I', '', '    """Clear the queue. Valid only if coming from tutor machine"""'), (
                 'C', '    if request.remote_addr.upper() != TUTOR_MACHINE.upper():',
                 '    if request.remote_addr.upper() != TUTOR_MACHINE.upper():'), (
                 'S', '        abort(403, "Not authorised")',
                 '        abort(403, "Only the tutor machine can clear the queue")'), ('C', '    else:', '    else:'),
             ('C', '        queue.clear_queue()', '        queue.clear_queue()'), (
                 'S', '        response = jsonify({"message": "Queue emptied"})',
                 '        response = jsonify({"message": "Queue cleared"})'),
             ('C', '        response.status_code = 204',
              '        response.status_code = 204'),
             ('C', '        return response', '        return response')]},

    ]
    for index, item in enumerate(test_data):
        print('*' * 5, index, '*' * 5)
        s1 = item.get('s1', '')
        s2 = item.get('s2', '')
        result = item.get('result', '')
        calc_result = line_edits(s1, s2)
        is_correct = True if calc_result == result else False
        print('is_correct    ', is_correct)
        if not is_correct:
            print('result    ', result)
            print('calc_result    ', calc_result)
        print('*' * 5)
