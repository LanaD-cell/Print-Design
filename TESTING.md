# Print and Design Testing Information

This is the testing information for my project 5 eCommerce store Print & Design

[READ ME IS HERE](https://github.com/LanaD-cell/Print-Design) | DEVELOPER: Illana De Beer | [LinkedIn](https://linkedin.com/in/illana-de-beer-026332198)

<br>

## CONTENTS

[Features Testing](#features-testing)

[Admin Features](#admin-features)


[Store Features](#store-features)
- [Home Page Features](#home-page-features)
- [Navigation Bar Features](#navigation-bar-features)
- [Authentication Pages](#authentication-pages)
- [Products Page](#products-page)
- [Product Detail & Reviews](#product-detail-page)
- [Checkout Page](#checkout-page)
- [Profile Page](#profile-page)
- [Contact Us Page](#contact-us-page)
- [Wish List Page](#wish-list-page)
- [Newsletter Page](#newsletter-page)
- [Events Page](#events-page)
- [Compliance Pages](#compliance-pages)
- [Footer](#footer)

[UI Testing](#ui-testing)

[Browser Compatibility](#browser-compatibility)

[Responsiveness](#responsiveness)

[Code Validation](#code-validation)

- [CSS Validation](#css-validation)

- [JavaScript Validation](#javascript-validation)

- [HTML Validation](#html-validation)

<br>

[Lighthouse Validation](#lighthouse-validation)

- [index](#index-page)
- [registration](#registration-page )
- [login](#login-page)
- [forgotten password](#forgotten-password-page)
- [products page](#products-page-1)
- [checkout page](#checkout-page-1)
- [checkout success page](#checkout-success-page)
- [contact us page](#contact-us-page-1)
- [newsletter page](#newsletter-page-1)
- [event page](#event-page)

[Behaviour Driven Testing](#behaviour-driven-testing)

[Automated Testing](#automated-testing)

[Bugs](#bugs)

[Resources](#resources)

[Retrospective](#retrospective)

<br>

### Validator Testing

- HTML
  - No errors were returned when passing through the official [W3C validator](https://validator.w3.org/nu/?doc=https%3A%2F%2Fcode-institute-org.github.io%2Flove-running-2.0%2Findex.html)
- CSS
  - No errors were found when passing through the official [(Jigsaw) validator](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fvalidator.w3.org%2Fnu%2F%3Fdoc%3Dhttps%253A%252F%252Fcode-institute-org.github.io%252Flove-running-2.0%252Findex.html&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en#css)




## Features Testing

A thorough manual testing process was undertaken to ensure all parts of the store worked as it should. Both the admin area and the main store were tested.

<details>

### Admin Features:

Manual tests were conducted in the admin area to ensure everything is working. There was an error when deleting orders and the necessary refactoring of code took place to remove that error.

Admin Area - Role based access control successful - users are unable to log into the admin area

<img src="readme/testing/rm-testing-admin.png" width="80%"><br><br>

In the admin area products/categories/reviews can be added, edited and deleted. The following manual tests took place to ensure they all worked.

Reviews area:

<img src="readme/testing/rm-admin-reviews.png" width="80%"><br><br>

Review selected and ready to delete - PASSED

<img src="readme/testing/rm-admin-reviews-delete.png" width="80%"><br><br>

Confirm deletion of review - PASSED

<img src="readme/testing/rm-admin-reviews-delete-confirm.png" width="80%"><br><br>

Success message to show review has been deleted - PASSED

<img src="readme/testing/rm-admin-reviews-delete-success.png" width="80%"><br><br>

Highlight orders to be deleted - PASSED

<img src="readme/testing/rm-admin-delete-orders.png" width="80%"><br><br>

Confirmation of order deletion - PASSED

<img src="readme/testing/rm-admin-delete-orders-confirm.png" width="80%"><br><br>

Adding new categories - PASSED
<img src="readme/testing/rm-admin-category.png" width="80%"><br><br>

Adding new products - PASSED
<img src="readme/testing/rm-admin-add-product.png" width="80%"><br><br>

**Emails via gmail:**
Emails are received (to the gmail account being used to send emails to customers) when a new order is placed. If an email is incorrect admin is also told about that too. These emails are just test@test.com emails used when testing checkout.

<img src="readme/testing/rm-testing-email.png" width="90%"><br><br>

</details>

<p align="right">(<a href="#contents">back to top</a>)</p>

### Store Features

Tests have been undertaken to ensure the registration, email confirmation, confirming email, log-in, log out and password request all work.
Also tested has been the shopping journey from adding to wishlist, adding and removing products to shopping cart and checking out as an anonymous buyer as well as a registered buyer.
The process of adding a review has been tested for buyers and also for unregistered users.
This has all been documented on the [READ ME HERE](https://github.com/todiane/poster-palace)

<details>

Other manual tests have taken place.

I went through the customer journey procedure myself and three other people tested the site and the checkout process as well as adding a review and using the wishlist. Below are the results


## PEP8 Testing

I have been using linter in the Terminal, but tested the following pages in the CI Python Tool.

[Code Institute Python Tool](https://pep8ci.herokuapp.com/)

<img src="static/testing-docs/products-views-py.png" width="50%"><br><br>
Product - View.py

<img src="static/testing-docs/products-urls-py.png" width="50%"><br><br>
Product - Urls.py

<img src="static/testing-docs/products-models-py.png" width="50%"><br><br>
Product - Models.py

<img src="static/testing-docs/products-forms-py.png" width="50%"><br><br>
Product - Forms.py

<img src="static/testing-docs/products-app-py.png" width="50%"><br><br>
Product - App.py

<img src="static/testing-docs/products-admin-py.png" width="50%"><br><br>
Product - Admin.py

<img src="static/testing-docs/print_design-sitemaps-py.png" width="50%"><br><br>
Printe_design - Sitemaps.py

<img src="static/testing-docs/pring_design-urls-py.png" width="50%"><br><br>
Print_design - Urls.py

<img src="static/testing-docs/manage-py.png" width="50%"><br><br>
Manage.py

<img src="static/testing-docs/homepage-views-py.png" width="50%"><br><br>
Homepage - View.py

<img src="static/testing-docs/homepage-urls-py.png" width="50%"><br><br>
Homepage - Urls.py

<img src="static/testing-docs/homepage-signals-py.png" width="50%"><br><br>
Homepage - Signals.py

<img src="static/testing-docs/homepage-forms-py.png" width="50%"><br><br>
Homepage - Forms.py

<img src="static/testing-docs/homepage-model-py.png" width="50%"><br><br>
Homepage - Model.py

<img src="static/testing-docs/homepage-app-py.png" width="50%"><br><br>
Homepage - App.py

<img src="static/testing-docs/homepage-admin-py.png" width="50%"><br><br>
Homepage - Admin.py

<img src="static/testing-docs/checkout-webhook-py.png" width="50%"><br><br>
Checkout - Webhooks.py

<img src="static/testing-docs/checkout-webhook-handler-py.png" width="50%"><br><br>
Checkout - Webhook-handler.py

## CSS Validation

I used the CSS Validation service to test the site. (W3E Validator)[https://jigsaw.w3.org/css-validator/]

<img src="static/testing-docs/w3e-base-css.png" width="90%"><br><br>
<img src="static/testing-docs/w3e-checkout-css.png" width="90%"><br><br>

</details>

## JavaScript Validation

All javascript was put through the [JSHINT tool](https://jshint.com/)

<img src="static/testing-docs/carthtml-js-jshint.png" width="70%"><br><br>
cart.html.js

<img src="static/testing-docs/checkout-js-jshint.png" width="70%"><br><br>
checkout.js

<img src="static/testing-docs/homepagehtml-js-jshint.png" width="70%"><br><br>
homoepage.html.js

<img src="static/testing-docs/productdetailshtml-js-jshint.png" width="70%"><br><br>
product_detail.html.js

<img src="static/testing-docs/return-js-jshint.png" width="70%"><br><br>
return.js

<img src="static/testing-docs/subscribehtml-js-jshint.png" width="70%"><br><br>
subscribtion.html.js

<img src="static/testing-docs/successhtml-js-jshint.png" width="70%"><br><br>
success.html.js


## HTML Validation

<details>

| Page | Validation Image |
|:---|:---: |
| Base.html  |  <img src="readme/testing/rm-html-checker-success.png" width="90%">  |
| Index  |  <img src="readme/testing/rm-html-checker-success.png" width="90%">  |
| Main Navbar |  <img src="readme/testing/rm-html-checker-success.png" width="90%">  |
| Mobile Navbar |  <img src="readme/testing/rm-html-checker-success.png" width="90%">  |
| Register |  <img src="readme/testing/rm-html-checker-success.png" width="90%"> |
| Log In |  <img src="readme/testing/rm-html-checker-success.png" width="90%"> |
| Log Out | <img src="readme/testing/rm-html-checker-success.png" width="90%">  |
| Product | <img src="readme/testing/rm-html-checker-success.png" width="90%">    |
| Product Details | <img src="readme/testing/rm-html-checker-success.png" width="90%">    |
| Checkout |  <img src="readme/testing/rm-html-checker-success.png" width="90%">  |
| Checkout Success | <img src="readme/testing/rm-html-checker-success.png" width="90%">   |
| Profile |  <img src="readme/testing/rm-html-checker-success.png" width="90%"> |
| About Us |<img src="readme/testing/rm-html-checker-success.png" width="90%">   |
| Contact Us | <img src="readme/testing/rm-html-checker-success.png" width="90%">  |
| Contact Us Success | <img src="readme/testing/rm-html-checker-success.png" width="90%">  |
| Contact Us FAQ| <img src="readme/testing/rm-html-checker-success.png" width="90%">   |
| Events | <img src="readme/testing/rm-html-checker-success.png" width="90%">   |
| Newsletter | <img src="readme/testing/rm-html-checker-newsletter-page.png" width="90%">  |
| Wish List | <img src="readme/testing/rm-html-checker-success.png" width="90%">  |
| Choosing Poster Article | <img src="readme/testing/rm-html-checker-success.png" width="90%"> |
| All Compliance Pages | <img src="readme/testing/rm-html-checker-success.png" width="90%"> |
| Footer | <img src="readme/testing/rm-html-checker-success.png" width="90%">   |



</details>


<p align="right">(<a href="#contents">back to top</a>)</p>

## Lighthouse Validation



<details>

The scripts being in the header also caused lower scores and I added defer in some, defer in the Stripes linked caused it to stop working so I removed it.

***All pages scored 90% or above for accessibility.***

#### Index Page:
Accessibility was given a score of 90% first time around because of a missing ```<ul>``` element in the mobile header. Once that was added the score increased to 100% but the navbar stopped working on larger screens so I removed it.

<img src="readme/testing/rm-lighthouse-accessibility.png" width="70%"><br>

<img src="readme/testing/rm-lighthouse.png" width="70%"><br><br>

SEO was given a 100% score overall

<img src="readme/testing/rm-lighthouse-seo.png" width="70%"><br><br>

#### Registration Page:

<img src="readme/testing/rm-lighthouse-signup.png" width="70%"><br><br>

#### Login Page:

<img src="readme/testing/rm-lighthouse-login.png" width="70%"><br><br>

#### Forgotten Password Page:

<img src="readme/testing/rm-lighthouse-password-forgot.png" width="70%"><br><br>

#### Products Page:
PNG images reduced score and can be changed to webp
Test results the same across all pages e.g. sort category price high to low, a-z, z-a, low to high price.

<img src="readme/testing/rm-lighthouse-products.png" width="70%"><br><br>

#### Checkout Page:

<img src="readme/testing/rm-lighthouse-checkout.png" width="70%"><br><br>

#### Checkout Success Page:

<img src="readme/testing/rm-lighthouse-checkout-success.png" width="70%" height="auto"><br><br>

#### Profile Page:

<img src="readme/testing/rm-lighthouse-profile.png" width="70%"><br><br>

#### About Page:

<img src="readme/testing/rm-lighthouse-about.png" width="70%" height="auto"><br><br>

#### Contact Us Page:

<img src="readme/testing/rm-lighthouse-contact-us.png" width="70%"><br><br>

#### Newsletter Page:

<img src="readme/testing/rm-lighthouse-newsletter.png" width="70%"><br><br>

#### Event Page:

<img src="readme/testing/rm-lighthouse-eventpage.png" width="70%"><br><br>


## Automated Testing


### Bugs

  #### Secret Key commited
  - I added the SK to the Js in order_checkout js for testing purposes,
      as the payment was throuwing Invalid Client Secret errors.
      Then I forgot to remove it before committing changes and opened a can of worms.
      I received a fatal error that Github piscked up that a SK was commit and
      refused access. I then proceeded to do a major rebate on all commits. After
      that I once again received the same error, as the commit was stuck in the
      history eventhough I did the rebate. After some restless sleep, I throught
      of just changing my SK in Stripe and allowing the old SK to be sent through
      as a test SK to Guthub. On the surface it seems to have worked.

  #### order dynamically move from current to previous order on status change
  - I am sure this is not a difficult fix, but due to time constraint I will need
    to complete this in future rollouts. The order status shows in the profile, can
    be changed in the admin Order model. But the update does not trigger the switch.

  <img src="static/images/documentation/bug-previous-orders.png" width="70%"><br><br>

## Resources

- [Pep 8 for code standards](https://peps.python.org/pep-0008/)
- [Black code formatter](https://pypi.org/project/black/)
- [Code Institute Python Tool](https://pep8ci.herokuapp.com/)
- [JSHINT tool](https://jshint.com/)
- [HTML validator](https://validator.w3.org/nu/#textarea)
- [CSS validator](https://jigsaw.w3.org/css-validator/)
- [Google Lighthouse](https://chromewebstore.google.com/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk)
- [Django Testing](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing)

## Retrospective

At the end of this process, I feel pretty dissatisfied. With the previous 4 projects I had ample time to give it my best, learn some additional things on the side etc. This, the last and most important project, the time  limit was simply inadequate. I had major problems along the way that caused me immense time wastage (the error in accidentally commiting the secret key) and then also made the initial error in choosing products that have a fixed quantity to price combinations. that was not at all straight forward to figure out for correct pricing.

<p align="right">(<a href="#contents">back to top</a>)</p>