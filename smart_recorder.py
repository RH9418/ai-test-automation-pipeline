import os
import re
import asyncio
import argparse
from datetime import datetime
from playwright.async_api import async_playwright

BASE_SCREENSHOT_DIR = "Test_Screenshots"
CODEGEN_LOGS_DIR = "Codegen_Logs"

async def run_smart_recorder(feature_name, start_url):
    # Setup directories
    screenshot_dir = os.path.join(BASE_SCREENSHOT_DIR, feature_name)
    os.makedirs(screenshot_dir, exist_ok=True)
    os.makedirs(CODEGEN_LOGS_DIR, exist_ok=True)
    
    counter = 0
    
    async with async_playwright() as p:
        # Launch maximized for best visibility
        browser = await p.chromium.launch(headless=False, args=['--start-maximized'])
        context = await browser.new_context(no_viewport=True)
        
        # 🟢 THE FIX: This asynchronous function runs in the background
        async def take_screenshot(page, action_type, tag_name, text):
            nonlocal counter
            counter += 1
            
            safe_text = re.sub(r'[^a-zA-Z0-9]', '_', text)[:30]
            timestamp = datetime.now().strftime("%H-%M-%S")
            filename = f"{timestamp}_{counter:02d}_{action_type}_{tag_name}_{safe_text}.png"
            filepath = os.path.join(screenshot_dir, filename)
            
            try:
                # Async sleep yields control! The browser doesn't freeze.
                # It allows the red box to render and Codegen to process the click.
                await asyncio.sleep(0.15)
                await page.screenshot(path=filepath, full_page=False)
                print(f"📸 Captured: {filename}")
            except Exception as e:
                print(f"⚠️ Failed to capture screenshot: {e}")

        # This binding is called by JS. It immediately delegates the work and returns.
        async def handle_action(source, action_type, tag_name, text):
            page = source['page']
            # Fire and forget the screenshot task! Prevents Codegen deadlocks.
            asyncio.create_task(take_screenshot(page, action_type, tag_name, text))
                
        # Bind the Python function
        await context.expose_binding("record_action", handle_action)
        
        # Inject the Spotlight and Floating Widget JS
        js_injection = """
            window.isScreenshotRecording = false;
            
            const widget = document.createElement('div');
            widget.innerHTML = '🔴 START Screenshot Recording';
            widget.style.position = 'fixed';
            widget.style.bottom = '20px';
            widget.style.right = '20px';
            widget.style.padding = '15px 25px';
            widget.style.backgroundColor = '#ff4444';
            widget.style.color = 'white';
            widget.style.fontWeight = 'bold';
            widget.style.fontSize = '16px';
            widget.style.borderRadius = '50px';
            widget.style.cursor = 'pointer';
            widget.style.zIndex = '2147483647';
            widget.style.boxShadow = '0 4px 6px rgba(0,0,0,0.3)';
            widget.style.fontFamily = 'Arial, sans-serif';
            widget.style.userSelect = 'none';
            
            widget.onclick = (e) => {
                e.stopPropagation(); 
                window.isScreenshotRecording = !window.isScreenshotRecording;
                if (window.isScreenshotRecording) {
                    widget.innerHTML = '✅ RECORDING ACTIVE (Click to Pause)';
                    widget.style.backgroundColor = '#00C851';
                } else {
                    widget.innerHTML = '🔴 START Screenshot Recording';
                    widget.style.backgroundColor = '#ff4444';
                }
            };
            
            document.addEventListener("DOMContentLoaded", () => {
                document.body.appendChild(widget);
            });

            document.addEventListener('mousedown', async (e) => {
                if (e.button !== 0) return; 
                if (!window.isScreenshotRecording) return; 
                if (e.target === widget) return; 
                
                const target = e.target;
                const rect = target.getBoundingClientRect();
                
                const box = document.createElement('div');
                box.style.position = 'absolute';
                box.style.left = (rect.left + window.scrollX) + 'px';
                box.style.top = (rect.top + window.scrollY) + 'px';
                box.style.width = rect.width + 'px';
                box.style.height = rect.height + 'px';
                box.style.border = '4px solid #FF0000';
                box.style.boxShadow = '0 0 15px 5px rgba(255, 0, 0, 0.7)';
                box.style.boxSizing = 'border-box';
                box.style.zIndex = '2147483646';
                box.style.pointerEvents = 'none'; 
                
                document.body.appendChild(box);
                
                setTimeout(() => { 
                    if (box && box.parentNode) box.parentNode.removeChild(box); 
                }, 400);
                
                let text = target.innerText || target.value || target.placeholder || target.name || target.className || 'element';
                text = String(text).substring(0, 40);
                
                try {
                    // Call Python asynchronously
                    window.record_action('click', target.tagName.toLowerCase(), text);
                } catch (err) {
                    console.error('Screenshot capture failed', err);
                }
            }, { capture: true });
        """
        
        await context.add_init_script(js_injection)
        
        page = await context.new_page()
        await page.goto(start_url)
        
        print("\n" + "="*80)
        print(f"🚀 SMART RECORDER ACTIVATED FOR: {feature_name}")
        print("="*80)
        
        # Await the pause so the Inspector opens and keeps the script alive
        await page.pause() 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Record Playwright scripts while capturing instant annotated screenshots.")
    parser.add_argument('--name', required=True, help="Name of the feature (e.g., By_Product_Daily)")
    parser.add_argument('--url', required=True, help="Starting URL to record")
    args = parser.parse_args()
    
    # Run the async event loop
    asyncio.run(run_smart_recorder(args.name, args.url))
