document.addEventListener("DOMContentLoaded", function () {
    const categoryButtons = document.querySelectorAll(".category-btn");
    const productLists = document.querySelectorAll(".product-list");

    function showCategory(categoryId) {
        // Hide all product lists
        productLists.forEach(list => list.style.display = "none");

        // Show the selected category
        const selectedCategory = document.querySelector(`.category-${categoryId}`);
        if (selectedCategory) {
            selectedCategory.style.display = "block";
        }
    }

    // Set the first category as default
    const defaultCategoryButton = document.querySelector(".category-btn");
    if (defaultCategoryButton) {
        defaultCategoryButton.classList.add("active");
        const defaultCategoryId = defaultCategoryButton.getAttribute("data-category-id");
        showCategory(defaultCategoryId);
    }

    // Handle category button clicks
    categoryButtons.forEach(button => {
        button.addEventListener("click", function () {
            categoryButtons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");

            const categoryId = this.getAttribute("data-category-id");
            showCategory(categoryId);
        });
    });
});

$(document).ready(function () {
    $(".add-to-cart-btn").click(function () {
        let productId = $(this).data("product-id");
        let button = $(this);

        $.ajax({
            type: "POST",
            url: "/add-to-cart/",
            data: {
                product_id: productId,
                quantity: 1,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                button.text(`✓ Added ${response.product_name}`).addClass("added-success");
                updateCartCount(response.total_items);
                setTimeout(() => button.text("Add to Cart").removeClass("added-success"), 2000);
            },
            error: function () {
                alert("Error adding to cart!");
            }
        });
    });

    function updateCartCount(count) {
        $("#cart-count").text(count);
    }
});