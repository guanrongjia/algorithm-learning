def fill_table_score(section1, section2):
    ''' fill table '''
    m = len(section1) + 1
    n = len(section2) + 1
    table = [[0 for j in range(n)] for i in range(m)]
    for i in range(0, m):
        for j in range(0, n):
            if i == 0 or j == 0:
                table[i][j] = i or j
            elif section1[i-1] == section2[j-1]:
                table[i][j] = table[i - 1][j - 1]
            else:
                table[i][j] = 1 + min(table[i - 1][j], table[i][j - 1],table[i - 1][j - 1])
    return table


def get_result(i, j, table, list1, list2):
    result = []
    while i > 0 or j > 0:
        min_cost = min(table[i - 1][j], table[i][j - 1], table[i - 1][j - 1])
        if min_cost == table[i][j]:
            result.insert(0, ('T', list1[i - 1], list2[j - 1]))
            i -= 1
            j -= 1
        elif min_cost == table[i - 1][j]:
            result.insert(0, ('D', list1[i - 1], ''))
            i -= 1
        elif min_cost == table[i][j - 1]:
            result.insert(0, ('I', '', list2[j - 1]))
            j -= 1
        else:
            result.insert(0, ('S', list1[i - 1], list2[j - 1]))
            i -= 1
            j -= 1
    return result


def line_edits(str1, str2):
    ''' get longest substring '''
    str_list1 = str1.splitlines()
    str_list2 = str2.splitlines()
    i = len(str_list1)
    j = len(str_list2)
    table = fill_table_score(str_list1, str_list2)
    return get_result(i, j, table, str_list1, str_list2)


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
