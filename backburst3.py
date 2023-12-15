def add_css_and_js_to_html(file_name):
    # Read the HTML file using utf8 encoding
    with open(file_name, 'r', encoding='cp950') as file:
        html_content = file.read()

    # Define the CSS and JavaScript links to add to the head section
    css_and_js_links = '''
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
        integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <script src="https://kit.fontawesome.com/ab5a8dbf3c.js" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="https://unpkg.com/bootstrap-table@1.16.0/dist/bootstrap-table.min.css">
    '''

    # Find the </head> tag in the HTML and insert the CSS and JavaScript links before it
    head_index = html_content.find('</head>')
    if head_index != -1:
        updated_html = html_content[:head_index] + css_and_js_links + html_content[head_index:]
    else:
        # If </head> is not found, just append the links to the end of the HTML
        updated_html = html_content + css_and_js_links

    # Write the updated HTML back to the file
    with open(file_name, 'w') as file:
        file.write(updated_html)

