def add_footer_to_html_file(file_name):
    # Define the footer HTML
    footer_html = """
    <footer>
        <!-- Floating button with a Font Awesome hamburger icon -->
        <button class="floating-button" onclick="hamb();" data-state1="1" data-stat2="1">
            <i class="fas fa-bars"></i>
        </button>

        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"
            integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
            crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"
            integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
            crossorigin="anonymous"></script>
        <script src="https://unpkg.com/bootstrap-table@1.16.0/dist/bootstrap-table.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11.9.0/dist/sweetalert2.all.min.js"
            integrity="sha256-kuoM7/Z00lbaqHRO9Vpa95aaMzlSTZiJIIvK46igrug=" crossorigin="anonymous"></script>
    </footer>
    <script>function hamb() {
        Swal.fire({
            title: "~date~",
            showDenyButton: true,
            showCancelButton: true,
            confirmButtonText: "create toggle",
            denyButtonText: `update toggle`,
        }).then((result) => {
            const button = document.querySelector('.floating-button');
            const currentState1 = button.getAttribute('data-state1');
            const currentState2 = button.getAttribute('data-state2');
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
                if (currentState1 === '1') {
                    button.setAttribute('data-state1', '2');
                    $('table').bootstrapTable('hideColumn', 'create_date');
                } else {
                    button.setAttribute('data-state1', '1');
                    $('table').bootstrapTable('showColumn', 'create_date');
                }
            } else if (result.isDenied) {
                if (currentState2 === '1') {
                    button.setAttribute('data-state2', '2');
                    $('table').bootstrapTable('hideColumn', 'update_date');
                } else {
                    button.setAttribute('data-state2', '1');
                    $('table').bootstrapTable('showColumn', 'update_date');
                }
            }
        });
    }</script>
    """

    # Read the existing HTML content from the file
    with open(file_name, 'r') as file:
        html_content = file.read()

    # Append the footer HTML to the existing content
    updated_html_content = html_content + footer_html

    # Write the updated HTML content back to the file
    with open(file_name, 'w') as file:
        file.write(updated_html_content)

# Usage example:
file_name = "your_html_file.html"
add_footer_to_html_file(file_name)
