$(document).ready(function () {
    // ✅ Toggle Order Items
    $(".view-order-btn").click(function () {
        var orderId = $(this).data("order-id");
        $("#order-" + orderId).toggle();
    });
    
    // Handle cancel order
    $(".cancel-order-btn").click(function() {
        let orderId = $(this).data("order-id");

        if (confirm("Are you sure you want to cancel this order?")) {
            $.ajax({
                url: "/cancel_order/",  // Ensure this matches your Django URL
                type: "POST",
                data: {
                    order_id: orderId,
                    csrfmiddlewaretoken: csrfToken  // Include CSRF token in the request
                },
                success: function(response) {
                    if (response.success) {
                        alert("Order canceled successfully.");
                        location.reload();  // Refresh the page to update the status
                    } else {
                        alert("Error: " + response.error);
                    }
                },
                error: function() {
                    alert("An error occurred while canceling the order.");
                }
            });
        }
    });
});