# Print and Design Testing Information

This is the testing information for my project 5 eCommerce store Print & Design

[READ ME IS HERE](https://github.com/LanaD-cell/Print-Design) | DEVELOPER: Illana De Beer | [LinkedIn](https://linkedin.com/in/illana-de-beer-026332198)

<br>

# Table of Contents

1. [PEP8 Testing](#pep8-testing)
   - [Product - View.py](#product---viewpy)
   - [Product - Urls.py](#product---urlspy)
   - [Product - Models.py](#product---modelspy)
   - [Product - Forms.py](#product---formspy)
   - [Product - App.py](#product---app-py)
   - [Product - Admin.py](#product---admin-py)
   - [Print Design - Sitemaps.py](#print-design---sitemaps-py)
   - [Print Design - Urls.py](#print-design---urlspy)
   - [Manage.py](#managepy)
   - [Homepage - View.py](#homepage---viewpy)
   - [Homepage - Urls.py](#homepage---urlspy)
   - [Homepage - Signals.py](#homepage---signalspy)
   - [Homepage - Forms.py](#homepage---formspy)
   - [Homepage - Model.py](#homepage---modelpy)
   - [Homepage - App.py](#homepage---app-py)
   - [Homepage - Admin.py](#homepage---admin-py)
   - [Checkout - Webhooks.py](#checkout---webhookspy)
   - [Checkout - Webhook-handler.py](#checkout---webhook-handlerpy)

2. [CSS Validation](#css-validation)

3. [JavaScript Validation](#javascript-validation)

4. [HTML Validation](#html-validation)

5. [Lighthouse Validation](#lighthouse-validation)
   - [Homepage](#homepage)
   - [Products](#products)
   - [Signup](#signup)
   - [Login](#login)
   - [Cart](#cart)
   - [Payment Success](#payment-success)
   - [Profile](#profile)
   - [Order Details](#order-details)
   - [Newsletter](#newsletter)
   - [Product Management](#product-management)
   - [Admin](#admin)

6. [Bug Testing & Known Issues Report](#bug-testing--known-issues-report)
   - [Cart and Order](#cart-and-order)
   - [Secret Key Committed](#secret-key-committed)
   - [Order dynamically move from current to previous order on status change](#order-dynamically-move-from-current-to-previous-order-on-status-change)
   - [Account Signup bug](#account-signup-bug)
   - [Order_detail bug](#order-detail-bug)

7. [Resources](#resources)

8. [Retrospective](#retrospective)




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

