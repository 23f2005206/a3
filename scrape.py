import asyncio
from playwright.async_api import async_playwright

async def run():
    seeds = range(73, 83)
    base_url = "https://sanand0.github.io/tdsdata/js_table/?seed="
    total_sum = 0

    async with async_playwright() as p:
        # Launch a "headless" browser (no UI)
        browser = await p.chromium.launch()
        page = await browser.new_page()

        for seed in seeds:
            url = f"{base_url}{seed}"
            await page.goto(url)
            
            # These tables are dynamic, so we wait for cells to load
            await page.wait_for_selector("td")
            
            # Extract all table cell (td) values
            cells = await page.query_selector_all("td")
            for cell in cells:
                text = await cell.inner_text()
                try:
                    # Clean the text and add to sum if it's a number
                    total_sum += float(text.strip())
                except ValueError:
                    continue
        
        print(f"FINAL_TOTAL_SUM: {total_sum}")
        await browser.close()

asyncio.run(run())
