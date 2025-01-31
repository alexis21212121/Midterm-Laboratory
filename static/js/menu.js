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

document.addEventListener("DOMContentLoaded", function () {
    const categoryButtons = document.querySelectorAll(".category-btn");
    const productLists = document.querySelectorAll(".product-list");
    const searchBox = document.getElementById("search-box");
    const searchBtn = document.getElementById("search-btn");
    const sortOptions = document.getElementById("sort-options");

    function showCategory(categoryId) {
        productLists.forEach(list => list.style.display = "none");
        const selectedCategory = document.querySelector(`.category-${categoryId}`);
        if (selectedCategory) selectedCategory.style.display = "block";
    }

    const defaultCategoryButton = document.querySelector(".category-btn");
    if (defaultCategoryButton) {
        defaultCategoryButton.classList.add("active");
        showCategory(defaultCategoryButton.getAttribute("data-category-id"));
    }

    categoryButtons.forEach(button => {
        button.addEventListener("click", function () {
            categoryButtons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");
            showCategory(this.getAttribute("data-category-id"));
        });
    });

    // Search functionality
    searchBtn.addEventListener("click", function () {
        const searchQuery = searchBox.value.toLowerCase();
        document.querySelectorAll(".product-item").forEach(item => {
            const productName = item.querySelector(".product-name").textContent.toLowerCase();
            item.style.display = productName.includes(searchQuery) ? "block" : "none";
        });
    });

    // Sorting functionality
    sortOptions.addEventListener("change", function () {
        const selectedOption = this.value;
        const visibleCategory = document.querySelector(".product-list[style='display: block;']");
        if (!visibleCategory) return;

        let products = Array.from(visibleCategory.querySelectorAll(".product-item"));

        if (selectedOption === "name") {
            products.sort((a, b) => a.querySelector(".product-name").textContent.localeCompare(b.querySelector(".product-name").textContent));
        } else if (selectedOption === "price_low_high") {
            products.sort((a, b) => parseFloat(a.querySelector(".product-price").textContent.replace("₱", "")) - parseFloat(b.querySelector(".product-price").textContent.replace("₱", "")));
        } else if (selectedOption === "price_high_low") {
            products.sort((a, b) => parseFloat(b.querySelector(".product-price").textContent.replace("₱", "")) - parseFloat(a.querySelector(".product-price").textContent.replace("₱", "")));
        }

        // Append sorted products back to the container
        products.forEach(product => visibleCategory.querySelector(".products-container").appendChild(product));
    });
});