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
        # Create the new table structure
        new_table = BeautifulSoup('''
        <table data-toggle="table">
            <thead>
                <tr>
                    <th data-field="name" data-sortable="true">name</th>
                    <th data-field="create_date" data-sortable="true">create_date</th>
                    <th data-field="update_date" data-sortable="true">update_date</th>
                    <th data-field="JSU" data-sortable="true">JSU</th>
                    <th data-field="grade" data-sortable="true">grade</th>
                    <th data-field="subject" data-sortable="true">subject</th>
                    <th data-field="url" data-sortable="true">url</th>
                    <th data-field="download" data-sortable="false">download</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
        ''', 'html.parser')

        # Replace the original table with the new table
        table.replace_with(new_table)

        # Save the modified HTML to a new file or overwrite the original file
        with open(input_file_name, 'w') as output_file:
            output_file.write(str(soup))
        print("Table added successfully.")
    else:
        print("No table found in the HTML file.")

# Usage example
#input_file_name = 'your_input_file.html'
#add_table_to_html(input_file_name)
