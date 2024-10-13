import re
from bs4 import BeautifulSoup

def add_table_to_html(input_file_name):
    # Read the input HTML file
    with open(input_file_name, 'r') as file:
        html_content = file.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the table in the HTML
    table = soup.find('table')

    if table:


        #fix
        # coding=utf8
        # the above tag defines encoding for this document and is for Python 2.x compatibility


        regex = r"<table>"

        test_str = html_content
        subst = "<table data-toggle=\"table\">            <thead>                <tr>                    <th data-field=\"name\" data-sortable=\"true\">name</th>                    <th data-field=\"create_date\" data-sortable=\"true\">create_date</th>                    <th data-field=\"update_date\" data-sortable=\"true\">update_date</th>                    <th data-field=\"JSU\" data-sortable=\"true\">JSU</th>                    <th data-field=\"grade\" data-sortable=\"true\">grade</th>                    <th data-field=\"subject\" data-sortable=\"true\">subject</th>                    <th data-field=\"url\" data-sortable=\"true\">url</th>                    <th data-field=\"download\" data-sortable=\"false\">download</th>                </tr>            </thead>            <tbody>"

        # You can manually specify the number of replacements by changing the 4th argument
        result = re.sub(regex, subst, test_str, 0, re.MULTILINE)

        #if result:
            #print (result)

        # Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
        # coding=utf8
        # the above tag defines encoding for this document and is for Python 2.x compatibility

        regex = r"</table>"

        test_str = result
        subst = "</tbody>        </table>"

        # You can manually specify the number of replacements by changing the 4th argument
        result = re.sub(regex, subst, test_str, 0, re.MULTILINE)

        #if result:
            #print (result)

        # Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.

        # Save the modified HTML to a new file or overwrite the original file
        with open(input_file_name, 'w') as output_file:
            output_file.write(result)
        print("Table added successfully.")

    else:
        print("No table found in the HTML file.")


