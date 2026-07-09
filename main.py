from playwright.sync_api import sync_playwright
from fake_data import generate_user

user = generate_user()

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("http://localhost:5173/auth/register")

    page.locator("#fullName").fill(user["fullName"])
    page.locator("#email").fill(user["email"])
    page.locator("#phoneNumber").fill(user["phoneNumber"])
    page.locator("#password").fill(user["password"])
    page.locator("#confirmPassword").fill(user["password"])

    page.get_by_role("checkbox").click()

    page.get_by_role("button", name="Create account").click()

    page.wait_for_url("**/auth/verify-email")

    page.screenshot(path="success.png")

    browser.pause()

    browser.close()