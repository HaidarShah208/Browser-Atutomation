import time
from playwright.sync_api import sync_playwright
from fake_data import generate_user

TOTAL_USERS = 200

# Step 5 - Measure total execution time
start = time.perf_counter()

with sync_playwright() as p:

    # Step 1 - Optimized browser launch
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--no-sandbox",
        ],
    )

    # Step 3 - Reuse one browser context
    context = browser.new_context()

    for i in range(TOTAL_USERS):

        user = generate_user()

        page = context.new_page()

        # Step 2 - Block unnecessary resources
        page.route(
            "**/*",
            lambda route: (
                route.abort()
                if route.request.resource_type in ["image", "font", "media"]
                else route.continue_()
            ),
        )

        try:
            page.goto("https://www.champzones.com/signup")

            page.locator("#name").fill(user["fullName"])
            page.locator("#email").fill(user["email"])
            page.locator("#password").fill(user["password"])

            page.get_by_role("button", name="Sign up").click()

            page.wait_for_url("**/")

            # Step 4 - Print every 10 users
            if (i + 1) % 10 == 0:
                print(f"✅ {i + 1}/{TOTAL_USERS} users completed")

        except Exception as e:
            print(f"❌ Failed User {i + 1}")
            print(e)

        finally:
            page.close()

    context.close()
    browser.close()

# Step 5 - Show total execution time
end = time.perf_counter()

print(f"\nTotal Time : {end - start:.2f} seconds")
print("All users processed.")