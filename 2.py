def add_style_to_html_file(file_name):
    style_code = """/* Style for the floating button */
        .floating-button {
            position: fixed;
            bottom: 20px;
            /* Adjust this value for the desired vertical position */
            right: 20px;
            /* Adjust this value for the desired horizontal position */
            background-color: #ddb98b;
            /* Background color for the button */
            color: #ffc0cb;
            /* Text color */
            border: none;
            border-radius: 50%;
            /* Make it round */
            width: 60px;
            /* Adjust the size as needed */
            height: 60px;
            /* Adjust the size as needed */
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: center;
            align-items: center;
        }
    """

    try:
        with open(file_name, 'r') as file:
            html_content = file.read()

        # Check if the style is already present in the HTML
        if '/* Style for the floating button */' not in html_content:
            # Insert the style code into the head section
            head_start = html_content.find('<head>')
            if head_start != -1:
                head_end = html_content.find('</head>', head_start)
                if head_end != -1:
                    modified_html = (
                        html_content[:head_end] + '\n<style>\n' + style_code + '\n</style>\n' + html_content[head_end:]
                    )
                    with open(file_name, 'w') as file:
                        file.write(modified_html)
                    print(f'Style added to {file_name}')
                else:
                    print('Could not find </head> tag in the HTML file.')
            else:
                print('Could not find <head> tag in the HTML file.')
        else:
            print('Style is already present in the HTML.')

    except FileNotFoundError:
        print(f'File not found: {file_name}')

# Example usage:
file_name = 'your_file.html'
add_style_to_html_file(file_name)
