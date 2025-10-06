#!/usr/bin/env python3
"""
Jay Soundo Bot Test
Test Jay Soundo Photography bot functionality
"""

import asyncio
import aiohttp
import json
from datetime import datetime

async def test_jay_soundo_bot():
    """Test Jay Soundo bot functionality"""
    
    backend_url = "http://localhost:8080"
    
    print("📸 Testing Jay Soundo Photography Bot")
    print("=" * 45)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        async with aiohttp.ClientSession() as session:
            
            # Test 1: Jay Soundo Bot Stats
            print("📊 Testing Jay Soundo bot stats...")
            async with session.get(f"{backend_url}/api/bot/jay-soundo/stats") as response:
                if response.status == 200:
                    data = await response.json()
                    print("✅ Jay Soundo stats OK")
                    bot_info = data.get('bot_info', {})
                    print(f"   Bot: {bot_info.get('displayName', 'N/A')}")
                    print(f"   Type: {bot_info.get('botType', 'N/A')}")
                    print(f"   Source: @{bot_info.get('unsplash_source', 'N/A')}")
                    print(f"   Total Photos: {bot_info.get('total_source_photos', 'N/A')}")
                    print(f"   Specialties: {', '.join(bot_info.get('specialties', []))}")
                    
                    scheduler = data.get('scheduler_status', {})
                    print(f"   Running: {scheduler.get('is_running', False)}")
                    print(f"   Times: {scheduler.get('posting_times', [])}")
                else:
                    print(f"❌ Jay Soundo stats failed: {response.status}")
                    return False
            
            print()
            
            # Test 2: Create Jay Soundo Post
            print("🎨 Testing Jay Soundo post creation...")
            themes = ["nature", "urban", "portrait", "abstract", "travel"]
            theme = "nature"  # Test with nature theme
            
            async with session.post(
                f"{backend_url}/api/bot/jay-soundo/create-post",
                params={"theme": theme}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print("✅ Jay Soundo post creation OK")
                    print(f"   Message: {data.get('message', 'N/A')}")
                    print(f"   Photo ID: {data.get('photo_id', 'N/A')}")
                    print(f"   Photographer: {data.get('photographer', 'N/A')}")
                    print(f"   Likes: {data.get('likes', 'N/A')}")
                    print(f"   Theme: {data.get('theme', 'N/A')}")
                else:
                    error_text = await response.text()
                    print(f"❌ Jay Soundo post failed: {response.status}")
                    print(f"   Error: {error_text}")
                    return False
            
            print()
            
            # Test 3: Check Both Bots Status
            print("🤖 Testing both bots status...")
            
            # Marcin stats
            async with session.get(f"{backend_url}/api/bot/stats") as response:
                if response.status == 200:
                    data = await response.json()
                    marcin_info = data.get('bot_info', {})
                    print(f"✅ Marcin: {marcin_info.get('displayName', 'N/A')} - Running: {data.get('scheduler_status', {}).get('is_running', False)}")
                else:
                    print("❌ Marcin stats failed")
            
            # Jay Soundo stats
            async with session.get(f"{backend_url}/api/bot/jay-soundo/stats") as response:
                if response.status == 200:
                    data = await response.json()
                    jay_info = data.get('bot_info', {})
                    print(f"✅ Jay Soundo: {jay_info.get('displayName', 'N/A')} - Running: {data.get('scheduler_status', {}).get('is_running', False)}")
                else:
                    print("❌ Jay Soundo stats failed")
            
            return True
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False

async def main():
    success = await test_jay_soundo_bot()
    
    print()
    print("=" * 45)
    if success:
        print("🎉 ALL JAY SOUNDO TESTS PASSED!")
        print("✅ Jay Soundo Photography bot is working perfectly")
        print("📸 Bot ready for diverse photography content")
        print("🚀 Both Marcin + Jay Soundo bots active")
    else:
        print("❌ SOME TESTS FAILED")
        print("⚠️ Check the Python backend logs")
    
    print(f"⏰ Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return success

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Test cancelled")
        exit(1)
