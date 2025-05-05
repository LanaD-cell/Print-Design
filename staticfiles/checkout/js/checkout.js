const stripe = Stripe('your_publishable_key');

let elements = stripe.elements();
let card = elements.create('card');
card.mount('#card-element');

document.getElementById('payment-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Step 1: Get the clientSecret from the server
    const res = await fetch('/checkout/create-payment-intent/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ amount: 1099 }) // or dynamically set this
    });

    const { clientSecret, error } = await res.json();
    if (error) {
        document.getElementById('error-message').textContent = error;
        return;
    }

    // Step 2: Confirm the card payment
    const result = await stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    });

    if (result.error) {
        document.getElementById('error-message').textContent = result.error.message;
    } else {
        if (result.paymentIntent.status === 'succeeded') {
            alert('Payment successful!');
            // Redirect or update UI
        }
    }
});
