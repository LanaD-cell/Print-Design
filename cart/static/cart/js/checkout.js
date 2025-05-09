/* jshint esversion: 8 */
/* global Stripe */
document.addEventListener("DOMContentLoaded", function() {
    const stripe = Stripe('pk_test_51REARw07B3iAgZ7iWDLVkGICKIihYRy4Qwkgp2xmVPq8wulwd3E2mszbQkvII5BLzpDrhiEr2e24vr9vyjwNYVpx00moQgnZMh');
    const paymentForm = document.getElementById('payment-form');

    if (paymentForm) {
            // Event listener for the payment form submit
            paymentForm.addEventListener('submit', async (e) => {
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
                const name = document.getElementById('id_name').value;
                const email = document.getElementById('email').value;
                const phone = document.getElementById('phone_number').value;
                const address_line_1 = document.getElementById('address_line_1').value;
                const town_or_city = document.getElementById('town_or_city').value;
                const postcode = document.getElementById('postcode').value;
                const country = document.getElementById('country').value;
                const grandTotal = parseFloat(document.getElementById('grand-total').value);
                const deliveryOption = document.querySelector('input[name="delivery_option"]:checked')?.value || '';

                // Send a request to your server to create a checkout session
                const response = await fetch('/cart/create-checkout-session/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify({
                        name,
                        email,
                        phone,
                        address_line_1,
                        town_or_city,
                        postcode,
                        country,
                        delivery_option: deliveryOption,
                        grand_total: grandTotal
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
    } else {
        console.error("Payment form not found.");
    }
});