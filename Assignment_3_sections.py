import asyncio
import time
from playwright.async_api import async_playwright
async def verify_sorting_and_checkout_with_accessibility_tests():
    async with async_playwright() as p:
        
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.saucedemo.com/")
        await page.fill('#user-name', 'standard_user')
        await page.fill('#password', 'secret_sauce')
        await page.click('#login-button')
        await page.wait_for_load_state('networkidle')
        cart_link_locator = page.locator('.shopping_cart_link')
        await cart_link_locator.scroll_into_view_if_needed()  
        await page.wait_for_selector('.shopping_cart_link', timeout=5000)
        cart_link_handle = await cart_link_locator.element_handle()

        if cart_link_handle:
            
            is_visible = await cart_link_handle.is_visible()
            print(f"Shopping cart link visible: {is_visible}")
            if is_visible:
             cart_link_html = await cart_link_handle.evaluate('el => el.outerHTML')
                print(f"Shopping cart link HTML: {cart_link_html}")
                cart_accessibility = await page.accessibility.snapshot(root=cart_link_handle)
                
                if not cart_accessibility:
                    print("Failed to get the cart accessibility snapshot. Taking full page accessibility snapshot for debugging...")
                    full_page_accessibility = await page.accessibility.snapshot()
                    print("Full Page Accessibility Snapshot:", full_page_accessibility)  
                    raise AssertionError("Failed to get accessibility snapshot for the shopping cart link.")
                print("Cart Accessibility Snapshot:", cart_accessibility)  
                assert cart_accessibility.get('role') == 'link', "Shopping cart should have a 'link' role."
                assert cart_accessibility.get('name') == 'Shopping Cart', "Shopping cart link is missing an accessible name."
            else:
                raise AssertionError("Shopping cart link is not visible.")
        else:
            raise AssertionError("Shopping cart link not found.")
        
        await page.select_option('.product_sort_container', 'za')
        product_accessibility = await page.accessibility.snapshot(root=await page.locator('.inventory_list').element_handle())
        if product_accessibility:
            assert product_accessibility['role'] == 'list', "Product container should have a 'list' role."
        else:
            raise AssertionError("Product list accessibility snapshot failed.")
        
        await page.screenshot(path="screenshots/sorted_ZA.png")
       
        await page.select_option('.product_sort_container', 'hilo')
        sorting_accessibility = await page.accessibility.snapshot(root=await page.locator('.product_sort_container').element_handle())
        if sorting_accessibility:
            assert sorting_accessibility['role'] == 'combobox', "Sorting dropdown should have a 'combobox' role."
        else:
            raise AssertionError("Sorting dropdown accessibility snapshot failed.")
       
        add_to_cart_buttons = await page.locator('.btn_inventory').all()
        for i in range(3):
            await add_to_cart_buttons[i].click()
        print("Added 3 items to the cart.")
       
        await page.screenshot(path="screenshots/items_added_to_cart.png")
       
        await page.click('.shopping_cart_link')
        cart_items = await page.locator('.inventory_item_name').all_inner_texts()
        cart_items = [item.strip() for item in cart_items]  # Clean up cart item names
        print(f"Items in the cart: {cart_items}")
        await page.screenshot(path="screenshots/cart_page.png")
        await page.click('#checkout')
        await page.fill('#first-name', 'John')
        await page.fill('#last-name', 'Doe')
        await page.fill('#postal-code', '12345')
        await page.click('#continue')
        
        await page.screenshot(path="screenshots/checkout_info_filled.png")
        
        summary_items = await page.locator('.inventory_item_name').all_inner_texts()
        summary_items = [item.strip() for item in summary_items]  # Clean up summary item names
        print(f"Items in the checkout summary: {summary_items}")
       
        if sorted(cart_items) != sorted(summary_items):
            raise AssertionError("The items in the cart do not match the checkout summary.")
        print("Items in the cart match the checkout summary.")
          await page.click('#finish')
          await page.wait_for_selector('.complete-header', timeout=5000)  # Wait for confirmation
       
        confirmation_message = await page.text_content('.complete-header')
        confirmation_message = confirmation_message.strip().lower()  # Normalize the message to lowercase
        assert confirmation_message == 'thank you for your order!', f"Order confirmation failed. Got message: '{confirmation_message}'"
        print("Order completed successfully.")
        
        await page.screenshot(path="screenshots/order_confirmation.png")
        
        print(f"Keeping the browser open at: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        time.sleep(30)  # Keeps the browser open for 30 seconds
        await browser.close()

asyncio.run(verify_sorting_and_checkout_with_accessibility_tests())