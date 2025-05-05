const stripe = Stripe('pk_test_51REARw07B3iAgZ7iWDLVkGICKIihYRy4Qwkgp2xmVPq8wulwd3E2mszbQkvII5BLzpDrhiEr2e24vr9vyjwNYVpx00moQgnZMh');

document.getElementById('payment-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    try {
        // ✅ Make the fetch request first and define `res`
        const response = await fetch('/checkout/create_checkout_session/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                grand_total: parseFloat(document.getElementById('grand-total').value) // Make sure you have this in your form
            })
        });

        const res = await response.json();  // ✅ Now res is defined

        if (res.error) {
            document.getElementById('error-message').textContent = res.error;
            return;
        }

        const clientSecret = res.clientSecret;

        const result = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card, // Make sure `card` is defined via Stripe Elements
            }
        });

        if (result.error) {
            document.getElementById('error-message').textContent = result.error.message;
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                alert('Payment successful!');
                // Optionally redirect
            }
        }

    } catch (err) {
        document.getElementById('error-message').textContent = 'An unexpected error occurred.';
        console.error(err);
    }
});
