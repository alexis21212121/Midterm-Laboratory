document.querySelectorAll('.remove-order-form').forEach(function(form) {
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        var orderElement = this.closest('li'); // Get the order list item
        var orderId = orderElement.id.replace('order-', ''); // Extract order ID safely
        var userOrdersSection = orderElement.closest('.user-orders'); // Get user orders section

        // Hide the order element immediately
        orderElement.style.display = 'none'; 

        // Check if the user has any remaining visible orders
        var visibleOrders = userOrdersSection.querySelectorAll('li:not([style*="display: none"])');
        if (visibleOrders.length === 0) {
            userOrdersSection.style.display = 'none';
        }

        var formData = new FormData(this); // Create FormData object with CSRF token

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest' // Ensure it's recognized as an AJAX request
            }
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert('Failed to remove order');
                // If deletion fails, restore the order in UI
                orderElement.style.display = 'block'; 
                userOrdersSection.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while removing the order');
            // Restore the order in UI if an error occurs
            orderElement.style.display = 'block'; 
            userOrdersSection.style.display = 'block';
        });
    });
});