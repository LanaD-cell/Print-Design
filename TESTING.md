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


#### Home Page Features

|     |                 TEST                 |                            EXPECTED ACTION                                                                                                                              |     RESULT        |
| :-: | :----------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----------------|
| 01  |   Click navigation bar log           |                             User is redirected to the home page.          | Pass    |
| 02  |   Add term to search bar, e.g. abstract             |                               Products and images related to the term appear                                 | Pass    |
| 03  |   Click on My Account in navbar              |                              Menu dropdown with page options                                 | Pass    |
| 04  |   Click on shopping bag              |                        Taken to shopping bag page                               | Pass    |
| 05  |   Shop Now button clicked              |                        Taken to all products page                                               | Pass    |
| 06  |   Shop Now button clicked              |                        Taken to all products page                                               | Pass    |
| 07  |   Images under "Featured Products" clicked            |                        Taken to all product display page for that image                                             | Pass    |
| 08  |   Link in footer clicked           |                        Taken to approriate page on site and off site                                            | Pass    |


#### Navigation Bar Features


|     |                 TEST                 |                            EXPECTED ACTION                                                                                                                              |     RESULT        |
| :-: | :----------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----------------|
| 01  |   Click register page under MY Account logo       |                            Taken to page to sign up        | Pass    |
| 02  |   Click Contact Us link under My Account logo            |                   Taken to contact us form                                | Pass    |
| 03  |   Click on Login under My Account logo            |                              Taken to sign in page                             | Pass    |
| 04  |   Click on pages under MORE on navbar             |                        Taken to appropriate page                          | Pass    |
| 05  |   Click on SORT POSTERS menu in navbar              |                       Products are sorted in order selected e.g. a-z, z-a etc                                           | Pass    |
| 06  |   Click on category under Posters menu            |                        Taken to all appropriate category | Pass    |

#### Authentication Pages


|     |                 TEST                 |                            EXPECTED ACTION                                                                                                                              |     RESULT        |
| :-: | :----------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----------------|
| 01  |   Click on pages to register, login or logout      |                            Appropriate page is shown along with success message     | Pass    |
| 02  |   Click link for new password            |                   Taken to form to enter email and email sent out to user with password change link                               | Pass    |


#### Products Page


|     |                 TEST                 |                            EXPECTED ACTION                                                                                                                              |     RESULT        |
| :-: | :----------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----------------|
| 01  |   Visit products page      |                            All products show up     | Pass    |
| 02  |   Click on details button            |                   User taken to product display page | Pass    |
| 03  |   Click on 'Buy Now' button            |                   User adds product to their bag and success message is displayed.  | Pass    |

#### Product Detail Page


|     |                 TEST                 |                            EXPECTED ACTION                                                                                                                              |     RESULT        |
| :-: | :----------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----------------|
| 01  |   Visit product detail page      |                            All details are shown     | Pass    |
| 02  |   Click on specific product            |                   Taken to product display page | Pass    |
| 03  |   Click on add to wishlist           |                              Taken to signin if not registered or success message shows saying product added to wishlist                         | Pass    |
| 04  |   Click on quantity             |                        Quantity number is increased and decreased                         | Pass    |
| 05  |   Click on size             |                       Large or extra large size selected                                         | Pass    |
| 06  |   Add to cart without size             |                      User can not add the product without selecting a size                                       | Fail. Customers can add product. Needs further investigation.    |
| 07  |   Click on add review           |    Review can be added only if user is registered/logged in | Pass    |
| 08  |   Click add to cart           |    Product added to cart, success message shows to confirm                                         | Pass    |
| 09  |   Click go to secure checkout button          |                        Taken to checkout area                                            | Pass    |

#### Checkout Page

|     |                 TEST                 |                            EXPECTED ACTION                                                                                                                              |     RESULT        |
| :-: | :----------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----------------|
| 01  |   Order summary available    |                            Order summary appears with thumbnail product image | Pass    |
| 02  |   Cost of order is visible           |                   Order summary, total order, shipping and grand total all shown | Pass    |
| 03  |   Full personal details         |                              Form to take full customer details is visible. Any errors made are shown to user via messages                        | Pass    |
| 04  |   Credit card area visible            |       Area to add payment details is visible                       | Pass    |
| 05  |   Guest Checkout message            |          Message for guests to register for an account                                     | Pass    |
| 06  |   Adjust Bag Button          |    User can go back to bag - any details added are removed automatically | Pass    |
| 07  |   Complete order       |    Payment is taken and spinner appears                                         | Pass    |
| 08  |   Checkout Success          |                       Order summary appears on screen. Success message is shown. Email sent to customer. If logged in details saved to profile                                        | Pass    |

#### Profile Page


|     |                 TEST                 |                            EXPECTED ACTION                                                                                                                              |     RESULT        |
| :-: | :----------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----------------|
| 01  |   User registers    |                            Profile is created | Pass    |
| 02  |   User selects to save delivery details     |                   Delivery details and phone number shown on profile page | Pass    |
| 03  |   Orders saved to profile     |                 Past orders made by customers are available on their profile                     | Pass    |
| 04  |   Delivery details update           |      Delivery details can be updated in profile                     | Pass    |

#### Contact Us Page
|     |                 TEST                 |                            EXPECTED ACTION                                                                                                                              |     RESULT        |
| :-: | :----------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----------------|
| 01  |   User taken to contact us page via footer link  |                            Footer links work | Pass    |
| 02  |   User must select reason for contact    |                 Message shown if not selected                   | Pass    |
| 03  |   Email or username automatically added if registered          |      Email and user name added in Admin area | Pass    |
| 04  |   Thank you message       |    Thank you message appears after sending form. If user is registered their username and email appears in thank you message. If the user is not registered the username does not appear. | Pass    |
| 05  |   Offer button on page      |    User taken to clearance and deals categories                                | Pass    |


#### Wish List Page


|     |                 TEST                 |                            EXPECTED ACTION                                                                                                                              |     RESULT        |
| :-: | :----------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----------------|
| 01  |   Product Added to Wishlist    |                            Success message shows that item added | Pass    |
| 02  |   User visits wishlist         |                   Product shown with thumbnail image and description | Pass    |
| 03  |   Delete wish list item       |                              User can delete item. Success message shown that item will be deleted. Success message shows item has been removed.                     | Pass    |

#### Newsletter Page
|     |                 TEST                 |                            EXPECTED ACTION                                                                                                                              |     RESULT        |
| :-: | :----------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----------------|
| 01  |   User taken to newsletter page via footer link  |                            Footer links work | Pass    |
| 02  |   Register for newsletter     |                 User can sign up to newsletter via form on page                    | Pass    |
| 03  |   Register for newsletter           |      User can sign up to newsletter via pop out form on homepage                   | Pass    |
| 04  |   Thank you message       |    Thank you message appears after registering | Pass    |
| 05  |   Start shopping button on newsletter page      |    User taken to all products                                    | Pass    |


#### Events Page
|     |                 TEST                 |                            EXPECTED ACTION                                                                                                                              |     RESULT        |
| :-: | :----------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----------------|
| 01  |   User taken to events page via MORE menu in navbar   |                  Navbar link works | Pass    |
| 02  |   User can register for newsletter        |       Sign up form on events page works                                | Pass    |
| 03  |   Thank you message       |    Thank you message appears after registering | Pass    |
| 04  |   User can view pdf          |                     Link to PDF of winners opens in new window                                    | Pass    |
| 05  |   User can click on product images        |                     Product images take user to display page of relevant product                               | Pass    |


#### Compliance Pages

The links in the footer takes a user to the specific page as expected. This includes the shipping, terms & conditions, refund and privacy policy page - pass


#### Footer

All links lead to the correct pages. External links open in a new window.

</details>

## UI testing

Bootstrap is a responsive language so the mobile-first design approach has been taken care of for the most part, however, tests were performed to ensure the following:

| Test | Result |
|:---|:---: |
| Toggle navbar doesn’t convert to navbar until over 990px |  PASS  |
| Search bar placeholder is always fully visible  |  PASS  |
| Size of social button icons respond as space increases |  PASS  |
| Product list scales from two columns to four at medium breakpoint  |  PASS  |
| Footer scales according to screen size |  PASS  |
| Search features remain visible on all screen sizes  |  PASS  |


## Browser Compatibility

Layout: The layout and appearance of the site has been tested for consistency throughout browsers. Browers tested include the main four:

- Chrome
- Firefox
- Safari
- Microsoft Edge

All links were tested and working. All pages load as expected and all features work as expected.

<p align="right">(<a href="#contents">back to top</a>)</p>

## Responsiveness

The eCommerce store looks and functions as intended on different browsers.

| Test | Screenshot View |
|:---|:---: |
| 1700 px Desktop | <img src="readme/testing/rm-screen-1700.png" alt="Laptop" width="70%">  |
| Laptop  |  <img src="readme/testing/rm-screen-1280.png" alt="Laptop" width="70%">   |
| iPad Air - Tablet |  <img src="readme/testing/rm-screen-ipad-air.png" alt="iPad" width="70%">   |
| Mobile - Pixel 7  |  <img src="readme/testing/rm-screen-pixel7.png" alt="Mobile" width="50%">  |

## PEP8 Testing

I have been using linter in the Terminal, but tested the following pages in the CI Python Tool.

[Code Institute Python Tool](https://pep8ci.herokuapp.com/)

<img src="static/testing-docs/products-views-py.png" width="50%"><br><br>
Product - View.py

<img src="static/testing-docs/products-views-py.png" width="50%"><br><br>
Product - View.py

<img src="static/testing-docs/products-views-py.png" width="50%"><br><br>
Product - View.py

<img src="static/testing-docs/products-views-py.png" width="50%"><br><br>
Product - View.py

<img src="static/testing-docs/products-views-py.png" width="50%"><br><br>
Product - View.py

<img src="static/testing-docs/products-views-py.png" width="50%"><br><br>
Product - View.py

<img src="static/testing-docs/products-views-py.png" width="50%"><br><br>
Product - View.py

<img src="static/testing-docs/products-views-py.png" width="50%"><br><br>
Product - View.py

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

</details>

## Automated Testing


### Bugs

  #### Secret Key commited
    - I added the SK to the Js in order_checkout js for testing purposes, as the payment was throuwing Invalid Client Secret errors.
      Then I forgot to remove it before committing changes and opened a can of worms. I received a fatal error that Github piscked up that a SK was commit and refused access. I then proceeded to do a major rebate on all commits. After that I once again received the same error, as the commit was stuck in the history eventhough I did the rebate. After some restless sleep, I throught of just changing my SK in Stripe and allowing the old SK to be sent through as a test SK to Guthub. On the surface it seems to have worked.

</details>

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