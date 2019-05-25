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
