document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('payment-form');
    const submitButton = document.getElementById('submit-button');

    // Ensure the form and submit button exist
    if (!form || !submitButton) {
        console.error('Form or submit button not found!');
        return;
    }

    // Get the Stripe public key and client secret from the DOM
    const stripePublicKey = document.getElementById('id_stripe_public_key').textContent.trim();
    const clientSecret = document.getElementById('id_client_secret').textContent.trim();

    // Initialize Stripe and Elements
    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();

    // Ensure #card-element is empty before mounting the card element
    const cardElementContainer = document.getElementById('card-element');
    if (cardElementContainer) {
        cardElementContainer.innerHTML = '';
    } else {
        console.error('Card element container not found in the DOM.');
        return;
    }

    // Create the card element and mount it to the DOM
    const card = elements.create('card');
    card.mount('#card-element');

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        // Disable the submit button to prevent multiple submissions
        submitButton.setAttribute('disabled', 'true');

        // Handle payment submission
        stripe.createPaymentMethod({
            type: 'card',
            card: card,
            billing_details: {
                name: document.getElementById('id_full_name').value,
                email: document.getElementById('id_email').value,
            },
        }).then(function (result) {
            if (result.error) {
                // If there's an error, display it in the 'card-errors' div
                const errorElement = document.getElementById('card-errors');
                errorElement.textContent = result.error.message;

                // Re-enable the submit button
                submitButton.removeAttribute('disabled');
            } else {
                const paymentMethodId = result.paymentMethod.id;

                // Send the payment method ID and client secret to the server to complete the payment
                fetch('/payment/confirm', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        payment_method: paymentMethodId,
                        client_secret: clientSecret,
                    }),
                }).then(function (response) {
                    return response.json();
                }).then(function (data) {
                    if (data.success) {
                        // If payment is successful, redirect to checkout success page
                        window.location.href = '/checkout_success';
                    } else {
                        // Display any errors from the server
                        const errorElement = document.getElementById('card-errors');
                        errorElement.textContent = data.error || 'Something went wrong!';
                    }

                    // Re-enable the submit button
                    submitButton.removeAttribute('disabled');
                }).catch(function (err) {
                    const errorElement = document.getElementById('card-errors');
                    errorElement.textContent = 'Network error: ' + err.message;

                    // Re-enable the submit button
                    submitButton.removeAttribute('disabled');
                });
            }
        });
    });
});
