"""A program to display the output of the line_edits function in an
   html table.
   Written for COSC261 Assignment 2, Questions 4, 2019.
   Richard Lobb 8 April 2019.
"""
import os
import re
from html import escape
import webbrowser
import sys

DEFAULT_CSS = """
table {font-size: 100%; border-collapse: collapse}
td, th  {border: 1px solid LightGrey; padding: 2px; }
td del {background-color: yellow; text-decoration: none;}
td del  {{background-color: yellow; text-decoration: none;}
"""

class HtmlTable:
    """A table to be rendered in HTML."""
    def __init__(self, column_headers):
        """The column headers is a list of strings. Its length determines the
           number of columns in the table"""
        self.headers = column_headers
        self.num_cols = len(column_headers)
        self._html = ""
        row = ''.join("<th>{}</th>".format(hdr) for hdr in column_headers)
        self._html += "<tr>" + row + "</tr>\n"

    def add_row(self, values, column_styles=None):
        """Given a list of strings ('values'), the length of which must match
           the length of the list of column headers when the table was created,
           add one row to the table. column_styles is an optional list of
           strings for setting the style attributes of the row's <td>
           elements. If given, its length must match the number of columns.

           For example
              add_row(["this", "that"], ["background-color:yellow", ""])

           would add a table row containing the values 'this' and 'that' with the
           first column having a background-color of yellow. An empty style
           string is ignored.
           String values are html-escaped (i.e. characters like '&' and '<' get
           converted to HTML-entities). Then, as a special feature for this
           assignment, any sequence of characters wrapped in double square
           brackets is instead wrapped in HTML <del> elements; these are by
           default rendered with a yellow background by the HTML renderer.
           Then any newline characters are converted to <br>.
           Finally the resulting string is wrapped in a <pre> element.
        """
        def td_element(value, style, i_column):
            value = escape(value)  # HTML escaping
            value = re.sub(r'\[\[(..*?)\]\]', r'<del>\1</del>', value,
                flags=re.DOTALL + re.MULTILINE)
            value = value.replace('\n', '<br>')
            style_string = ' style="{}"'.format(style) if style else ''
            td = "<td{}><pre>{}</pre></td>".format(style_string, value)
            return td

        if column_styles is None:
            column_styles = ["" for i in range(self.num_cols)]
        tds = [td_element(values[i], column_styles[i], i) for i in range(self.num_cols)]
        row = "<tr>{}</tr>\n".format(''.join(tds))
        self._html += row

    def html(self):
        return "<table>\n" + self._html + "</table>\n"


class HtmlRenderer:
    """A class to help with displaying HTML for COSC262 Assignment 2, 2019.
       Once constructed"""
    def __init__(self, css=DEFAULT_CSS):
        """Initialise self to contain the given html string"""
        self.html = ''
        self.css = css

    def add_html(self, html):
        """Concatenate the given html to the end of the current html string"""
        self.html += html

    def render(self):
        """Display the current html in a browser window"""
        html = """<html><head><style>{}</style></head><body>{}</body></html>""".format(
            self.css, self.html)
        path = os.path.abspath('temp.html')
        with open(path, 'w') as f:
            f.write(html)
        webbrowser.open('file://' + path)


def edit_table(operations):
    """Construct an HtmlTable to display the given sequence of operations, as
       returned by the line_edits function.
    """
    table = HtmlTable(["Previous", "Current"])
    grey = "background-color:LightGrey"
    for op, left, right in operations:
        if op == 'T':
            table.add_row([left, right])
        elif op == 'D':
            table.add_row([left, right], ["background-color:#F1C40F", grey])
        elif op == 'S':
            bg = "background-color:LightYellow"
            table.add_row([left, right], [bg, bg])
        else:
            table.add_row([left, right], [grey, "background-color:#ABEBC6"])
    return table


#************************************************************************
#
# Your line_edits function and any support functions goes here.
#
def line_edits(s1, s2, cache=None):
    "D = 1, I = 1, S = 1, T = 0"

    s1_list = s1.splitlines()
    s2_list = s2.splitlines()

    if cache == None:
        cache = [[-1 for _ in range(len(s2_list) + 1)] for _ in range(len(s1_list) + 1)]

    for i in range(len(s1_list) + 1):
        for j in range(len(s2_list) + 1):
            if i == 0:
                cache[i][j] = j
            elif j == 0:
                cache[i][j] = i
            elif s1_list[i - 1] == s2_list[j - 1]:

                cache[i][j] = cache[i - 1][j - 1]
            else:
                delete = cache[i - 1][j] + 1
                insert = cache[i][j - 1] + 1
                substitute = cache[i - 1][j - 1] + 1
                cache[i][j] = min(delete, insert, substitute)

    result = []
    result = turn_to_result(s1_list, s2_list, cache, result)
    result.reverse()
    return result


def turn_to_result(s1_list, s2_list, cache, result):
    """back tracking and get result in [(ty_, s1, s2)]form"""
    i = len(cache) - 1
    j = len(cache[i]) - 1

    index_s1 = len(s1_list) - 1
    index_s2 = len(s2_list) - 1

    while i > 0 and j > 0:
        min_cost = min(cache[i - 1][j], cache[i][j - 1], cache[i - 1][j - 1])

        if cache[i - 1][j - 1] == cache[i][j] and min_cost == cache[i - 1][j - 1]:
            ty_cost = "T"
            result.append((ty_cost, s1_list[index_s1], s2_list[index_s2]))
            i, j, index_s1, index_s2 = adjust_data(ty_cost, i, j, index_s1, index_s2)
        elif min_cost == cache[i - 1][j]:
            ty_cost = "D"
            result.append((ty_cost, s1_list[index_s1], ''))
            i, j, index_s1, index_s2 = adjust_data(ty_cost, i, j, index_s1, index_s2)
        elif min_cost == cache[i][j - 1]:
            ty_cost = "I"
            result.append((ty_cost, '', s2_list[index_s2]))
            i, j, index_s1, index_s2 = adjust_data(ty_cost, i, j, index_s1, index_s2)
        else:
            ty_cost = "S"
            s1 = s1_list[index_s1]
            s2 = s2_list[index_s2]
            s1_modified, s2_modified = modify_S_element(s1, s2)
            result.append((ty_cost, s1_modified, s2_modified))
            i, j, index_s1, index_s2 = adjust_data(ty_cost, i, j, index_s1, index_s2)

    adjust_null_case(i, j, result, s1_list, s2_list)
    return result


def modify_S_element(s1, s2):
    """'S' ("Substitute") will have the changes tagged as follows"""
    lcm_string = longest_common_substring(s1, s2)
    s1_modified = ""
    s2_modified = ""
    for c in s1:
        if len(lcm_string) != 0 and lcm_string[0] == c:
            s1_modified += lcm_string[0]
            lcm_string = lcm_string[1:]
        else:
            s1_modified += "[[{}]]".format(c)
    lcm_string = longest_common_substring(s1, s2)
    for c in s2:
        if len(lcm_string) != 0 and lcm_string[0] == c:
            s2_modified += lcm_string[0]
            lcm_string = lcm_string[1:]
        else:
            s2_modified += "[[{}]]".format(c)
    return s1_modified, s2_modified


def adjust_data(ty_cost, i, j, index_s1, index_s2):
    """adjust_data i, j, index_s1, index_s2 """
    if ty_cost == "T" or ty_cost == "S":
        i = i - 1
        j = j - 1
        index_s1 -= 1
        index_s2 -= 1
    elif ty_cost == "D":
        i = i - 1
        j = j
        index_s1 -= 1
    else:
        i = i
        j = j - 1
        index_s2 -= 1
    return i, j, index_s1, index_s2


def adjust_null_case(i, j, result, s1_list, s2_list):
    """adjust case when i or j == 0"""
    if len(s1_list) == 0:
        i = 0
        j = len(s2_list) - 1
        while j >= 0:
            result.append(("I", '', s2_list[j]))
            j -= 1
    elif len(s2_list) == 0:
        i = len(s1_list) - 1
        j = 0
        while i >= 0:
            result.append(("D", s1_list[i], ''))
            i -= 1
    else:
        if i != 0 and j == 0:
            while i > 0:
                result.append(("D", s1_list[i - 1], ''))
                i -= 1
        elif i == 0 and j != 0:
            while j > 0:
                result.append(("I", '', s2_list[j - 1]))
                j -= 1


def longest_common_substring(s1, s2, cache=None, i=None, j=None):
    """return lcs but without recursion"""
    if cache == None:
        i = len(s1)
        j = len(s2)
        cache = [[None for _ in range(j + 1)] for _ in range(i + 1)]
    for index_i in range(i + 1):
        for index_j in range(j + 1):
            if index_i == 0 or index_j == 0:
                cache[index_i][index_j] = 0
            elif s1[index_i - 1] == s2[index_j - 1]:
                l_c = cache[index_i - 1][index_j - 1] + 1
                cache[index_i][index_j] = l_c
            else:
                first_s = cache[index_i][index_j - 1]
                second_s = cache[index_i - 1][index_j]
                if first_s > second_s:
                    l_c = first_s
                else:
                    l_c = second_s
                cache[index_i][index_j] = l_c

    lcs = cache[i][j]
    result = lcs_back_tracking(lcs, cache, s1, s2)
    return result[::-1]


def lcs_back_tracking(lcs, cache, s1, s2):
    """to get real sequence"""
    i = len(cache) - 1
    j = len(cache[-1]) - 1
    sub_sequence = ""
    while lcs > 0:
        if s1[i - 1] == s2[j - 1]:
            sub_sequence += s1[i - 1]
            i -= 1
            j -= 1
            lcs -= 1
        else:
            if cache[i - 1][j] >= cache[i][j - 1]:
                i = i - 1
            else:
                j = j - 1
    return sub_sequence

#************************************************************************


def main(s1, s2):
    renderer = HtmlRenderer()
    renderer.add_html("<h1>Show Differences (COSC262 2019)</h1>")
    operations = line_edits(s1, s2)
    table = edit_table(operations)
    renderer.add_html(table.html())
    renderer.render()

# Two example strings s1 and s2, follow.
# These are the same ones used in the assignment spec.

s1 = r'''# ============== DELETEs =====================
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
'''

s2 = r'''# ============== DELETEs =====================
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
'''

main(s1, s2)
