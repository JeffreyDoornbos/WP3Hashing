$(document).ready(function() {
    // Listen for submit events on the inschrijven/uitschrijven forms
    $("form").on("submit", function(event) {
        // Prevent the default form submission
        event.preventDefault();

        // Get form data and action URL
        const form = $(this);
        const url = form.attr("action");
        const method = form.find("input[name='_method']").val() || "POST";
        const formData = form.serialize();

        // Show loading indicator
        const button = form.find("button");
        const originalText = button.text();
        button.prop("disabled", true);
        button.text("Bezig...");

        // Send AJAX request
        $.ajax({
            url: url,
            method: "POST",
            data: formData,
            success: function(response) {
                // Refresh the page to show updated state
                location.reload();
            },
            error: function(xhr) {
                // Show error message
                alert("Er is een fout opgetreden: " + xhr.responseText);
                button.text(originalText);
                button.prop("disabled", false);
            }
        });
    });
});