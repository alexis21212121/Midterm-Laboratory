$(document).ready(function () {
    function getCSRFToken() {
        return $('input[name="csrfmiddlewaretoken"]').val();
    }

    // ✅ Update Cart Quantity
    $(document).on("change", ".cart-quantity", function () {
        let itemId = $(this).data("item-id");
        let newQuantity = $(this).val();
        let row = $(this).closest("tr");

        $.ajax({
            type: "POST",
            url: "/update-cart/",
            data: {
                item_id: itemId,
                quantity: newQuantity,
                csrfmiddlewaretoken: getCSRFToken()
            },
            success: function (response) {
                if (response.success) {
                    row.find(".cart-item-total").text("₱" + response.item_total);
                    $("#cart-total").text(response.new_total);
                } else {
                    alert("❌ Error: " + response.error);
                }
            },
            error: function () {
                alert("❌ Error updating cart.");
            }
        });
    });

    // ✅ Remove Item from Cart
    $(document).on("click", ".remove-from-cart-btn", function () {
        let itemId = $(this).data("item-id");
        let row = $(this).closest("tr");

        $.ajax({
            type: "POST",
            url: "/remove-from-cart/",
            data: {
                item_id: itemId,
                csrfmiddlewaretoken: getCSRFToken()
            },
            success: function (response) {
                if (response.success) {
                    row.fadeOut(300, function () { $(this).remove(); });
                    $("#cart-total").text(response.new_total);
                } else {
                    alert("❌ Error: " + response.error);
                }
            },
            error: function () {
                alert("❌ Error removing item.");
            }
        });
    });

    // ✅ Prevent accidental form submission (in case of Enter key press)
    $("#cart-form").on("submit", function (event) {
        event.preventDefault();
    });
});

$(document).ready(function () {
    $(".order-btn").click(function () {
        $.ajax({
            url: "/place_order/",
            type: "POST",
            data: {
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (response) {
                if (response.success) {
                    alert("✅ Order placed successfully!");
                    window.location.href = "/orders/";  // Redirect to order tracking page
                } else {
                    alert("❌ Error: " + response.error);
                }
            },
            error: function () {
                alert("❌ An error occurred while placing the order.");
            }
        });
    });
});