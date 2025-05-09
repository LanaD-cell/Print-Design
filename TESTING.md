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

#### Homepage

<img src="static/testing-docs/lighthouse/lighthouse-homepage-desktop.png" width="70%"><br><br>
<img src="static/testing-docs/lighthouse/lighthouse-homepage-mobile.png" width="70%"><br><br>

#### Products

<img src="static/testing-docs/lighthouse/lighthouse-products-desktop.png" width="70%"><br><br>
<img src="static/testing-docs/lighthouse/lighthouse-products-mobil.png" width="70%"><br><br>

#### Signup

<img src="static/testing-docs/lighthouse/lighthouse-register-desktop.png" width="70%"><br><br>
<img src="static/testing-docs/lighthouse/lighthouse-register-mobile.png" width="70%"><br><br>

#### Login

<img src="static/testing-docs/lighthouse/lighthouse-login-desktop.png" width="70%"><br><br>
<img src="static/testing-docs/lighthouse/lighthouse-login-mobile.png" width="70%"><br><br>

#### Cart

<img src="static/testing-docs/lighthouse/lighthouse-cart-desktop.png" width="70%"><br><br>
<img src="static/testing-docs/lighthouse/lighthouse-cart-mobile.png" width="70%"><br><br>

#### Payment Success

<img src="static/testing-docs/lighthouse/lighthouse-pay-success-desktop.png" width="70%"><br><br>
<img src="static/testing-docs/lighthouse/lighthouse-pay-success-mobile.png" width="70%"><br><br>

#### Profile

<img src="static/testing-docs/lighthouse/lighthouse-profile-desktop.png" width="70%"><br><br>
<img src="static/testing-docs/lighthouse/lighthouse-profile-mobile.png" width="70%"><br><br>

#### Order Details

<img src="static/testing-docs/lighthouse/lighthouse-orderdetails.desktop.png" width="70%"><br><br>
<img src="static/testing-docs/lighthouse/lighthouse-orderdetails-mobile.png" width="70%"><br><br>

#### Newsletter

<img src="static/testing-docs/lighthouse/lighthouse-newsletter-desktop.png" width="70%"><br><br>
<img src="static/testing-docs/lighthouse/lighthouse-newsletter-mobile.png" width="70%"><br><br>

#### Product Management

<img src="static/testing-docs/lighthouse/lighthouse-prodmanagement-desktop.png" width="70%"><br><br>
<img src="static/testing-docs/lighthouse/lighthouse-prodmanagement-mobile.png" width="70%"><br><br>

#### Admin

<img src="static/testing-docs/lighthouse/lighthouse-admin-desktop.png" width="70%"><br><br>
<img src="static/testing-docs/lighthouse/lighthouse-admin-mobile.png" width="70%"><br><br>

## Bug Testing & Known Issues Report

####  Cart and Order
    What Works
    Cart Functionality:
    The cart is created successfully, and all totals (subtotal, tax, grand total) are calculated and displayed correctly.

    Stripe Payment Integration:
    Payments via Stripe are processed without issues, and transactions are successful.

    Admin Tracking:
    Both the Cart and Order are saved in the admin dashboard after checkout.

    What Does Not Work
    Cart Reset in Navbar:
    After a successful order, the cart does not reset in the navbar. It still displays the previous item count instead of clearing out.

    Cart ID Missing in Admin:
    The cart is saved in the admin, but no associated cart_id is shown, making it difficult to track specific carts.

    Order Missing Product Details:
    While the order is created and the user information is recorded in the admin panel, no product line items (name, quantity, price, etc.) are attached to the order.

    Notes
    These issues may stem from missing signals or incomplete save logic in the post-checkout process. Investigating the order and cart save functions and how cart data is transferred into the order model may help identify the root causes.

  #### Secret Key commited
    Secret Key Committed
    For testing purposes, the Stripe Secret Key (SK) was added directly to order_checkout.js.
    This triggered a fatal GitHub error due to detection of a sensitive credential.
    Even after rebasing and removing commits, the key remained in the commit history, causing repeated access denial.
    Resolution: The Stripe SK was regenerated, and the old SK is now treated as a test key, mitigating the issue on the surface.

  #### Order dynamically move from current to previous order on status change
  While order statuses can be updated in the Django admin panel, the order does not automatically move from "Current Orders" to "Previous Orders" in the user's profile.
  This appears to be a simple logic/update trigger issue but remains unresolved due to time constraints.
  Future Fix: Implement a dynamic check or post-save signal to update the order listing based on status.

  <img src="static/images/documentation/bug-previous-orders.png" width="70%"><br><br>

  #### Account Signup bug

  When users submit a weak password and encounter a validation error, then resubmit with a valid password:
  Django may create a User account but fail to attach a Profile due to a one-to-one constraint violation.
  This causes a server error due to a duplicate or missing homepage_profile object.
  Root Cause: The Profile creation is manually handled post-registration, without guarantees it only runs once per user.
  Recommended Fix: Implement a post_save signal (e.g., in homepage/signals.py) to automatically create a Profile instance whenever a User is successfully registered.

  <img src="static/testing-docs/account-signup-bug.png" width="70%"><br><br>

 #### Order_detail bug

  The Order Detail page is accessible via the Order Success screen.
  However, no product information is dynamically displayed.
  While not a system-breaking bug, it significantly impacts user clarity post-purchase.
  Deferred Fix: Consider enhancing the template or context logic in future sprints.

  <img src="static/testing-docs/order-detail.bug.png" width="70%"><br><br>

## Resources

- [Pep 8 for code standards](https://peps.python.org/pep-0008/)
- [Black code formatter](https://pypi.org/project/black/)
- [Code Institute Python Tool](https://pep8ci.herokuapp.com/)
- [JSHINT tool](https://jshint.com/)
- [HTML validator](https://validator.w3.org/nu/#textarea)
- [CSS validator](https://jigsaw.w3.org/css-validator/)
- [Google Lighthouse](https://chromewebstore.google.com/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk)

## Retrospective

At the end of this process, I feel pretty dissatisfied. With the previous 4 projects I had ample time to give it my best, learn some additional things on the side etc. This, the last and most important project, the time  limit was simply inadequate. I had major problems along the way that caused me immense time wastage (the error in accidentally commiting the secret key) and then also made the initial error in choosing products that have a fixed quantity to price combinations. That was not at all straight forward to figure out for correct pricing. Ontop of that I feel I folded a bit under the perceived timecontraints, causing me to make unnecesary mistakes and wasting further time.

That said, I am super proud of the progress I have made in a very short time and the projects I have put out... this one included. This project will become the jumping board for a realworld site we want to run.

<p align="right">(<a href="#contents">back to top</a>)</p>