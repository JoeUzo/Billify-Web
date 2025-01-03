$(function () {
    // Target only the form with ID `#date-form`
    $('#date-form').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        // Add a loading state to the link container
        const linkContainer = $('#link-container');
        linkContainer.html('<span class="loading-text">Loading Please Wait...</span>');

        // Serialize form data and make AJAX requests
        const formData = $(this).serialize();
        $.ajax({
            url: '/', // Replace with your server endpoint
            type: 'POST',
            data: formData,
            success: function (response) {
                // Update the link container with a "Click Me" button
                if (response.link) {
                    linkContainer.html(
                        `<a href="${response.link}" class="btn btn-primary">Click Me</a>`
                    );
                } else {
                    linkContainer.html('<span class="text-danger">No link provided. Please try again.</span>');
                }
            },
            error: function () {
                // Display an error message in the link container
                linkContainer.html('<span class="text-danger">An error occurred. Please try again.</span>');
            }
        });
    });
});
