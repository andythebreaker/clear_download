from bs4 import BeautifulSoup

def change_html_title(input_file_name):
    # Read the HTML file
    with open(input_file_name, 'r') as file:
        html_content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the title tag and change its content
    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = "my note"
    else:
        # If the title tag doesn't exist, create one
        new_title_tag = soup.new_tag('title')
        new_title_tag.string = "my note"
        soup.head.append(new_title_tag)

    # Write the modified HTML back to the file
    with open(input_file_name, 'w') as file:
        file.write(str(soup))

# Example usage:
input_file_name = 'index.html'
change_html_title(input_file_name)