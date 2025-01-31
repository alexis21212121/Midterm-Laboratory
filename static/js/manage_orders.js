document.querySelectorAll('.remove-order-form').forEach(function(form) {
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        var orderId = this.getAttribute('action').split('/').pop(); // Extract order ID from URL

        var formData = new FormData(this); // Create FormData object with CSRF token

        // Disable the button to prevent multiple clicks
        var removeButton = this.querySelector('button');
        removeButton.disabled = true;
        removeButton.innerText = 'Removing...';

        fetch(this.action, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);  // Debug log to inspect the response

            if (data.success) {
                // Hide the order item from the page immediately
                var orderElement = document.getElementById('order-' + orderId);
                if (orderElement) {
                    orderElement.style.display = 'none'; // Hide the order element
                }

                // Check if the user has any remaining orders, if not, hide their section
                var userOrdersSection = orderElement.closest('.user-orders');
                if (userOrdersSection.querySelectorAll('li:visible').length === 0) {
                    userOrdersSection.style.display = 'none';
                }
            } else {
                alert('Failed to remove order');
            }
        })
        .catch(error => {
            console.log('Error:', error);
            alert('An error occurred while removing the order');
        })
        .finally(() => {
            // Re-enable the button after the AJAX call (optional)
            removeButton.disabled = false;
            removeButton.innerText = 'Remove Order';
        });
    });
});