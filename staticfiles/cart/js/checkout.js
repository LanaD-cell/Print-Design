/* jshint esversion: 8 */
/* global Stripe */
const stripe = Stripe('pk_test_51REARw07B3iAgZ7iWDLVkGICKIihYRy4Qwkgp2xmVPq8wulwd3E2mszbQkvII5BLzpDrhiEr2e24vr9vyjwNYVpx00moQgnZMh');

// Event listener for the payment form submit
document.getElementById('payment-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    try {
        // Gather the data needed to send to the backend
        const grandTotal = parseFloat(document.getElementById('grand-total').value);
        const deliveryOption = document.querySelector('input[name="delivery_option"]:checked').value;  // Assuming you have a delivery option field

        // Send a request to your server to create a checkout session
        const response = await fetch('/cart/create-checkout-session/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                grand_total: grandTotal,
                delivery_option: deliveryOption
            })
        });

        // Parse the JSON response
        const data = await response.json();

        if (data.error) {
            document.getElementById('error-message').textContent = data.error;
            return;
        }

        // Get the session ID from the response
        const checkoutSessionId = data.sessionId;

        // Redirect to Checkout
        stripe.redirectToCheckout({ sessionId: checkoutSessionId }).then(function (result) {
            if (result.error) {
                console.error(result.error.message);
            }
        });

    } catch (err) {
        document.getElementById('error-message').textContent = 'An unexpected error occurred.';
        console.error(err);
    }
});
