import asyncio
import nodriver as uc

async def main():
    browser = await uc.start()
    page = await browser.get('https://uae.dubizzle.com/motors/used-cars/toyota/camry/')
    
    # Wait for content to load or for Imperva to appear
    await asyncio.sleep(10)
    
    # Check for keywords in content
    content = await page.get_content()
    if "Access denied" in content:
        print("BLOCKED by Imperva")
    elif "listing-card" in content:
        print("SUCCESS: Found listing cards")
    else:
        print("UNSURE: Capturing screenshot")
        
    await page.save_screenshot('nodriver_test.png')
    await browser.stop()

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
