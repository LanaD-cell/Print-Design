require('dotenv').config();
console.log('Stripe Secret Key:', process.env.STRIPE_SECRET_KEY);

const Stripe = require('stripe');
require('dotenv').config();

const stripe = Stripe(process.env.STRIPE_SECRET_KEY);

async function getAccount() {
  try {
    const account = await stripe.accounts.retrieve('acct_1REARh02Dugwb6Pe');
    console.log(account);
  } catch (error) {
    console.error('Error retrieving account:', error);
  }
}

getAccount();