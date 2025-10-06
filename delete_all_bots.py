#!/usr/bin/env python3
"""
Delete All Bots Script
Deletes all users with isBot: true from the database
"""

import asyncio
import aiohttp
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def delete_all_bots():
    """Delete all bot users via Node.js backend"""
    
    node_backend_url = os.getenv('NODE_BACKEND_URL', 'http://localhost:5000')
    
    try:
        async with aiohttp.ClientSession() as session:
            # First, get all bot users
            async with session.get(
                f"{node_backend_url}/api/bot/premium-status",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    premium_bots = data.get("premium_bots", [])
                    
                    if not premium_bots:
                        print("✅ No bot users found to delete")
                        return True
                    
                    print(f"🔍 Found {len(premium_bots)} bot users:")
                    print("-" * 50)
                    
                    for i, bot in enumerate(premium_bots, 1):
                        print(f"{i}. {bot['displayName']} (@{bot['username']})")
                        print(f"   Type: {bot['botType']}")
                        print(f"   Followers: {bot['followerCount']}")
                        print(f"   Posts: {bot['postCount']}")
                        print(f"   Created: {bot['createdAt'][:10]}")
                        print()
                    
                    # Confirm deletion
                    print("⚠️  WARNING: This will delete ALL bot users and their posts!")
                    confirm = input(f"Are you sure you want to delete all {len(premium_bots)} bots? (type 'DELETE ALL' to confirm): ").strip()
                    
                    if confirm != 'DELETE ALL':
                        print("❌ Deletion cancelled - confirmation text didn't match")
                        return False
                    
                    print(f"\n🗑️ Deleting {len(premium_bots)} bot users...")
                    print("=" * 60)
                    
                    deleted_count = 0
                    failed_count = 0
                    total_deleted_posts = 0
                    
                    # Delete each bot
                    for bot in premium_bots:
                        username = bot['username']
                        print(f"🗑️ Deleting {bot['displayName']} (@{username})...")
                        
                        try:
                            async with session.delete(
                                f"{node_backend_url}/api/bot/delete-user/{username}",
                                timeout=aiohttp.ClientTimeout(total=15)
                            ) as delete_response:
                                
                                if delete_response.status == 200:
                                    delete_data = await delete_response.json()
                                    deleted_posts = delete_data.get('deleted_posts', 0)
                                    total_deleted_posts += deleted_posts
                                    deleted_count += 1
                                    print(f"   ✅ Deleted successfully ({deleted_posts} posts)")
                                else:
                                    error_text = await delete_response.text()
                                    failed_count += 1
                                    print(f"   ❌ Failed: HTTP {delete_response.status} - {error_text}")
                                    
                        except Exception as e:
                            failed_count += 1
                            print(f"   ❌ Error: {str(e)}")
                        
                        # Small delay between deletions
                        await asyncio.sleep(0.5)
                    
                    # Summary
                    print("\n" + "=" * 60)
                    print("📊 DELETION SUMMARY:")
                    print("-" * 30)
                    print(f"Total bots found: {len(premium_bots)}")
                    print(f"Successfully deleted: {deleted_count}")
                    print(f"Failed to delete: {failed_count}")
                    print(f"Total posts deleted: {total_deleted_posts}")
                    
                    if deleted_count > 0:
                        print(f"\n✅ Successfully deleted {deleted_count} bot users!")
                    
                    if failed_count > 0:
                        print(f"\n⚠️ {failed_count} deletions failed - check logs above")
                    
                    return failed_count == 0
                    
                else:
                    print(f"❌ Failed to get bot list: HTTP {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ Error during deletion process: {str(e)}")
        return False

async def delete_all_bots_direct():
    """Alternative method: Delete all bots via direct API call (if implemented)"""
    
    node_backend_url = os.getenv('NODE_BACKEND_URL', 'http://localhost:5000')
    
    try:
        async with aiohttp.ClientSession() as session:
            print("🗑️ Attempting bulk bot deletion...")
            
            # This would require a new endpoint in the backend
            async with session.delete(
                f"{node_backend_url}/api/bot/delete-all-bots",
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ {data.get('message', 'All bots deleted successfully')}")
                    print(f"   Deleted bots: {data.get('deleted_bots', 0)}")
                    print(f"   Deleted posts: {data.get('deleted_posts', 0)}")
                    print(f"   Deleted Cloudinary images: {data.get('deleted_cloudinary_images', 0)}")
                    print(f"   Cleaned bot folders: {data.get('cleaned_bot_folders', 0)}")
                    
                    bot_usernames = data.get('bot_usernames', [])
                    if bot_usernames:
                        print(f"   Deleted bot usernames: {', '.join(bot_usernames)}")
                    
                    return True
                elif response.status == 404:
                    print("⚠️ Bulk deletion endpoint not available, using individual deletion method...")
                    return await delete_all_bots()
                else:
                    error_text = await response.text()
                    print(f"❌ Bulk deletion failed: HTTP {response.status} - {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ Error in bulk deletion: {str(e)}")
        print("🔄 Falling back to individual deletion method...")
        return await delete_all_bots()

async def main():
    """Main function"""
    
    print("🗑️ HooksDream Bot Mass Deletion Tool")
    print("=" * 50)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--force":
            print("⚡ Force mode enabled - skipping confirmations")
            # For automated scripts - still requires manual confirmation for safety
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python delete_all_bots.py          # Interactive deletion")
            print("  python delete_all_bots.py --force  # Force mode (still requires confirmation)")
            print("  python delete_all_bots.py --help   # Show this help")
            return True
    
    # Try bulk deletion first, fallback to individual
    success = await delete_all_bots_direct()
    
    if success:
        print(f"\n🎉 Bot mass deletion completed successfully!")
        print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"\n❌ Bot mass deletion failed!")
        print("💡 You may need to check the backend logs or delete manually")
    
    return success

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Deletion cancelled by user (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
