/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here:
    https://stripe.com/docs/stripe-js
*/

document.addEventListener("DOMContentLoaded", function () {
    var stripePublicKey = document.getElementById('id_stripe_public_key').textContent.trim();
    var clientSecret = document.getElementById('id_client_secret').textContent.trim();

    var stripe = Stripe(stripePublicKey);
    var elements = stripe.elements();

    var style = {
        base: {
            color: '#212f45',
            fontFamily: '"Figtree", sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#065a60'
            }
        },
        invalid: {
            color: 'red',
            iconColor: '#272640'
        }
    };

    var card = elements.create('card', { style: style });
    var cardElement = document.getElementById('card-element');
    if (cardElement) {
        card.mount('#card-element');
    } else {
        console.error('The card element is not found in the DOM!');
    };

    card.addEventListener('change', function (event) {
        var errorDiv = document.getElementById('card-errors');
        if (event.error) {
            var html = `
                <span class="icon" role="alert">
                    <i class="fa-solid fa-circle-xmark"></i>
                </span>
                <span>${event.error.message}</span>
            `;
            errorDiv.innerHTML = html;
        } else {
            errorDiv.textContent = '';
        }
    });

    // Handle form submition
    var form = document.getElementById('payment-form');

    form.addEventListener('submit', function(ev) {
        ev.preventDefault();
        card.update({ 'disabled': true});
        $('#submit-button').attr('disabled', true);
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
            }
        }).then(function(result) {
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fa-solid fa-circle-xmark"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);
                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    });
});
