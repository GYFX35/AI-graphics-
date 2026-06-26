import asyncio
from playwright.async_api import async_playwright
import os
import time

async def verify_sponsorship():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Give some time for servers to be up if they were just started
        # but I'll assume they are handled by the environment or I'll start them

        try:
            await page.goto("http://localhost:3000", wait_until="networkidle")

            # Check for sponsorship stats
            # From App.jsx: <span className="stat-value">{sponsorStats.count || '500'}+</span>
            # <span className="stat-value">${(sponsorStats.amount / 1000).toFixed(0)}k+</span>

            # Since mock data is 524 and 12500
            # count should be 524+
            # amount should be 13k+ (toFixed(0) of 12.5 is 13)

            await page.wait_for_selector("text=524+")
            await page.wait_for_selector("text=$13k+")

            print("Verification Successful: Sponsorship stats are displayed correctly.")

            # Take a screenshot
            os.makedirs("verification", exist_ok=True)
            await page.screenshot(path="verification/sponsorship_stats.png")
            print("Screenshot saved to verification/sponsorship_stats.png")

        except Exception as e:
            print(f"Verification Failed: {e}")
            # Take screenshot of failure
            os.makedirs("verification", exist_ok=True)
            await page.screenshot(path="verification/sponsorship_error.png")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(verify_sponsorship())
