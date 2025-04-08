document.addEventListener("DOMContentLoaded", function () {
    const sizeSelect = document.getElementById('size_select');
    const quantitySelect = document.getElementById('quantity_select');
    const additionalServicesCheckboxes = document.querySelectorAll('input[type="checkbox"]');
    const deliveryOptionsRadioButtons = document.querySelectorAll('input[name="deliveryOption"]');
    const totalPriceElem = document.getElementById('total_price');
    const selectedSizeElem = document.getElementById('selected_size');
    const selectedQuantityElem = document.getElementById('selected_quantity');
    const additionalServicesElem = document.getElementById('additional_services');
    const deliveryServiceElem = document.getElementById('delivery_service');
    const addToCartButton = document.getElementById('add_to_cart');
    const orderForm = document.getElementById('orderform');

    // Access product data from the embedded 'product-data' div
    const productDataElem = document.getElementById('product-data');
    const productSizes = JSON.parse(productDataElem.getAttribute('data-sizes'));
    const productQuantities = JSON.parse(productDataElem.getAttribute('data-quantities'));
    const productServices = JSON.parse(productDataElem.getAttribute('data-services'));

    let selectedSizePrice = 0;
    let selectedQuantityPrice = 0;
    let selectedDeliveryPrice = 0;
    let additionalServicesPrice = 0;
    let selectedServices = [];

    // Function to update the total price and the selection summary
    function updateTotalPrice() {
        // Reset prices and services
        selectedSizePrice = 0;
        selectedQuantityPrice = 0;
        additionalServicesPrice = 0;
        selectedServices = [];

        // Get selected size
        const selectedSize = sizeSelect.value;
        selectedSizePrice = productSizes.find(size => size.size === selectedSize)?.price || 0;

        // Get selected quantity
        const selectedQuantity = quantitySelect.value;
        selectedQuantityPrice = productQuantities.find(quantity => quantity.quantity == selectedQuantity)?.price || 0;

        // Get selected services
        additionalServicesCheckboxes.forEach(checkbox => {
            if (checkbox.checked) {
                const serviceId = checkbox.id;
                const service = productServices.find(service => service.service === serviceId);
                if (service) {
                    selectedServices.push(service.service);
                    additionalServicesPrice += service.price;
                }
            }
        });

        // Get selected delivery option
        const selectedDeliveryOption = document.querySelector('input[name="deliveryOption"]:checked');
        selectedDeliveryPrice = selectedDeliveryOption ? parseFloat(selectedDeliveryOption.dataset.price) : 0;

        // Calculate the total price
        const totalPrice = selectedSizePrice + selectedQuantityPrice + additionalServicesPrice + selectedDeliveryPrice;

        // Update the selection summary
        selectedSizeElem.textContent = selectedSize || "None";
        selectedQuantityElem.textContent = selectedQuantity ? `Quantity: ${selectedQuantity}` : "None";
        additionalServicesElem.textContent = selectedServices.length ? selectedServices.join(", ") : "None";
        deliveryServiceElem.textContent = selectedDeliveryOption ? selectedDeliveryOption.value : "None";

        // Update total price display
        totalPriceElem.textContent = `€${totalPrice.toFixed(2)}`;
    }

    // Handle size change
    sizeSelect.addEventListener('change', function () {
        updateTotalPrice();
    });

    // Handle quantity change
    quantitySelect.addEventListener('change', function () {
        updateTotalPrice();
    });

    // Handle additional services selection
    additionalServicesCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            updateTotalPrice();
        });
    });

    // Handle delivery option change
    deliveryOptionsRadioButtons.forEach(function (radio) {
        radio.addEventListener('change', function () {
            updateTotalPrice();
        });
    });

    // Initial call to update total price on page load
    updateTotalPrice();
});
