SauceDemo Playwright Test Suite

This project contains a Playwright-based test suite to verify sorting order, accessibility features, item management in the cart, and checkout functionality on the SauceDemo website.

Table of Contents
•	Requirements
•	Installation
•	Usage
•	Running the Tests
•	Test Scenarios
•	Sorting Functionality
•	Cart and Checkout Workflow
•	Accessibility Testing
•	Visual Comparison with Screenshots
•	Known Issues
•	Contributing
•	License

Requirements : 
To run the Playwright test suite, ensure the following dependencies are installed:
Python 3.7+
Node.js (optional for managing Playwright dependencies)
Playwright Python package

Installation :
1. Clone the repository:
git clone https://github.com/your-repo/saucedemo-playwright-tests.git
cd saucedemo-playwright-tests
2. Install Python dependencies:
pip install playwright
3. Install browser binaries for Playwright:
playwright install
Usage

Running the Tests :
1. Make sure you have all dependencies installed.
2. Run the test suite using the following command:
python run_tests.py
This script will open the SauceDemo website, log in as a user, and execute the following scenarios.

Test Scenarios :
1. Sorting Functionality
The test verifies the sorting functionality on the "All Items" page by performing two main checks:
Z-A Sorting: Select the "Name (Z to A)" sorting option from the dropdown and verify the sorting order.
Price Sorting (High to Low): Select the "Price (High to Low)" sorting option and validate the price order.
2. Cart and Checkout Workflow
The test adds multiple items to the cart and verifies the following:
Adding 3 items to the cart.
Checking if the correct items are listed in the cart.
Proceeding through the checkout process.
Filling in the customer details (first name, last name, postal code).
Verifying that the cart items match the items listed in the checkout summary.
Completing the order and validating the order confirmation message.
3. Accessibility Testing
Each phase of the test includes accessibility testing using Playwright's accessibility snapshot. Key accessibility checks include:
Verifying that the shopping cart link has the correct role (link) and an accessible name (Shopping Cart).
Ensuring that product lists have a list role and the sorting dropdown has the combobox role.
If the accessibility snapshot for an element fails, the test will capture and print the full accessibility tree for debugging.
4. Visual Comparison with Screenshots
Screenshots are captured during various steps of the test:
After sorting items Z-A.
After sorting items by price (High to Low).
After adding items to the cart.
After filling in the checkout information.
After completing the order (confirmation page).
The screenshots are saved in the screenshots/ folder for visual comparison and validation.

Known Issues :
Accessibility Snapshot Issues: In some cases, Playwright may fail to capture an accessibility snapshot for specific elements. A retry mechanism has been added to mitigate this issue.
Dynamic Content: The test includes small delays and retries to handle dynamic content loading. However, if the website changes significantly, adjustments to the selectors and logic may be required.

Contributing :
Contributions to this project are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes and add tests if necessary.
4. Commit and push your changes (git commit -m 'Add new feature' && git push origin feature-branch).
5. Create a pull request.
 
License :
This project is licensed under the MIT License.
