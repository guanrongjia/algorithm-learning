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
            line_data = ['S', sec_1[i - 1], sec_2[j - 1]]
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
        {'s1': "Line1\n",
         's2': "",
         'result': [('D', 'Line1', '')]},

        {'s1': "Line1\nLine3\nLine5\n",
         's2': "Twaddle\nLine5\n",
         'result': [('S', 'Line1', 'Twaddle'), ('D', 'Line3', ''), ('T', 'Line5', 'Line5')]},

        {'s1': "Line1\nLine2\nLine3\nLine4\n",
          's2': "Line1\nLine3\nLine4\nLine5\n",
          'result': [('T', 'Line1', 'Line1'), ('D', 'Line2', ''), ('T', 'Line3', 'Line3'),
                     ('T', 'Line4', 'Line4'), ('I', '', 'Line5')]},

        {'s1': "Line1\nLine2\nLine3\nLine4\n",
          's2': "Line5\nLine4\nLine3\n",
          'result': [('S', 'Line1', 'Line5'), ('S', 'Line2', 'Line4'), ('T', 'Line3', 'Line3'),
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
         'result':[('T', '# ============== DELETEs =====================', '# ============== DELETEs ====================='), ('D', '# TODO: add docstrings', ''), ('T', "@app.route('/queue/<hostname>', methods=['DELETE'])", "@app.route('/queue/<hostname>', methods=['DELETE'])"), ('T', 'def delete(hostname):', 'def delete(hostname):'), ('I', '', '    """Handle delete request from the given host"""'), ('T', '    try:', '    try:'), ('T', '        data = json.loads(request.get_data())', '        data = json.loads(request.get_data())'), ('S', "        mac_address = data['macAddress']", "        mac_address = data['mac_address']"), ('T', '    except:', '    except:'), ('T', "        abort(400, 'Missing or invalid user data')", "        abort(400, 'Missing or invalid user data')"), ('S', '    status = queue.dequeue(hostname, macAddress)', '    status = queue.dequeue(hostname, mac_address)'), ('T', "    return ('', status)", "    return ('', status)"), ('T', '', ''), ('T', '', ''), ('T', "@app.route('/queue', methods=['DELETE'])", "@app.route('/queue', methods=['DELETE'])"), ('S', 'def empty_queue():', 'def clear_queue():'), ('I', '', '    """Clear the queue. Valid only if coming from tutor machine"""'), ('T', '    if request.remote_addr.upper() != TUTOR_MACHINE.upper():', '    if request.remote_addr.upper() != TUTOR_MACHINE.upper():'), ('S', '        abort(403, "Not authorised")', '        abort(403, "Only the tutor machine can clear the queue")'), ('T', '    else:', '    else:'), ('T', '        queue.clear_queue()', '        queue.clear_queue()'), ('S', '        response = jsonify({"message": "Queue emptied"})', '        response = jsonify({"message": "Queue cleared"})'), ('T', '        response.status_code = 204', '        response.status_code = 204'), ('T', '        return response', '        return response')]},

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
            print('result    ', _result)
            print('calc_result    ', calc_result)
