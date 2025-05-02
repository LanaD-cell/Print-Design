$(document).ready(function () {
    if (typeof $ === 'undefined') {
        console.error('jQuery not found. Aborting Stripe setup.');
        return;
    }

    const $form = $('#payment-form');
    const $submitBtn = $('#submit-button');
    const $loadingOverlay = $('#loading-overlay');
    const $errorDiv = $('#card-errors');

    if (!$form.length || !$submitBtn.length) {
        console.error('#payment-form or #submit-button not found. Aborting Stripe setup.');
        return;
    }

    const stripePublicKey = $('#id_stripe_public_key').text().trim().slice(1, -1);
    const clientSecret = $('#id_client_secret').text().trim().slice(1, -1);

    // Initialize Stripe
    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();

    const style = {
        base: {
            color: '#000',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#dc3545',
            iconColor: '#dc3545'
        }
    };

    const card = elements.create('card', { style: style });
    card.mount('#card-element');

    // Real-time validation
    card.on('change', function (event) {
        if (event.error) {
            const html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>`;
            $errorDiv.html(html);
        } else {
            $errorDiv.empty();
        }
    });

    // Form submission handler
    $form.on('submit', function (ev) {
        ev.preventDefault();

        card.update({ 'disabled': true });
        $submitBtn.prop('disabled', true);

        if (typeof $.fn.fadeToggle === 'function') {
            $form.fadeToggle(100);
            $loadingOverlay.fadeToggle(100);
        } else {
            $form.toggleClass('d-none');
            $loadingOverlay.toggleClass('d-none');
        }

        stripe.confirmCardPayment(clientSecret, {
            payment_method: { card: card }
        }).then(function (result) {
            if (result.error) {
                const html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $errorDiv.html(html);

                if (typeof $.fn.fadeToggle === 'function') {
                    $form.fadeToggle(100);
                    $loadingOverlay.fadeToggle(100);
                } else {
                    $form.toggleClass('d-none');
                    $loadingOverlay.toggleClass('d-none');
                }

                card.update({ 'disabled': false });
                $submitBtn.prop('disabled', false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    $form.get(0).submit();
                }
            }
        });
    });
});
