"""
Jay Soundo Bot Service - Automated Photography Posting
Handles automated content creation for Jay Soundo Photography Bot
"""

import asyncio
import aiohttp
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os

from .jay_soundo_accounts import get_jay_soundo_bot_account, get_jay_soundo_posting_times
from .jay_soundo_service import JaySoundoService
from .schedule_tracker_service import can_post_now, mark_post_created, get_schedule_stats, is_posting_time, get_vietnam_time
from .photo_tracker_service import PhotoTrackerService

logger = logging.getLogger(__name__)

class JaySoundoBotService:
    def __init__(self):
        self.node_backend_url = os.getenv('NODE_BACKEND_URL', 'http://localhost:5000')
        self.is_running = False
        self.scheduler_task = None
        self.jay_soundo_service = JaySoundoService()
        self.photo_tracker = PhotoTrackerService()
        
        # Get Jay Soundo bot configuration
        self.jay_soundo_bot = get_jay_soundo_bot_account()
        self.bot_username = self.jay_soundo_bot["username"]
        
        logger.info(f"🤖 Jay Soundo Bot Service initialized for {self.bot_username}")
    
    async def start_scheduler(self):
        """Start the automated posting scheduler for Jay Soundo"""
        if self.is_running:
            logger.warning("⚠️ Jay Soundo scheduler already running")
            return
        
        self.is_running = True
        logger.info("🚀 Starting Jay Soundo bot scheduler...")
        
        # Start the scheduler loop
        self.scheduler_task = asyncio.create_task(self._scheduler_loop())
        logger.info("✅ Jay Soundo bot scheduler started")
    
    async def stop_scheduler(self):
        """Stop the automated posting scheduler"""
        if not self.is_running:
            return
        
        self.is_running = False
        if self.scheduler_task:
            self.scheduler_task.cancel()
            try:
                await self.scheduler_task
            except asyncio.CancelledError:
                pass
        
        logger.info("🛑 Jay Soundo bot scheduler stopped")
    
    async def _scheduler_loop(self):
        """Main scheduler loop for Jay Soundo bot"""
        while self.is_running:
            try:
                current_time = get_vietnam_time()
                logger.info(f"⏰ Jay Soundo scheduler check at {current_time.strftime('%H:%M:%S')}")
                
                # Check if it's time to post (08:00, 14:00, 20:00)
                if is_posting_time(current_time, get_jay_soundo_posting_times()):
                    if can_post_now(self.bot_username):
                        logger.info("📝 Jay Soundo posting time - creating post...")
                        await self._create_scheduled_post()
                    else:
                        logger.info("⏭️ Jay Soundo already posted at this time today")
                
                # Wait 5 minutes before next check
                await asyncio.sleep(300)  # 5 minutes
                
            except Exception as e:
                logger.error(f"❌ Jay Soundo scheduler error: {str(e)}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    async def _create_scheduled_post(self):
        """Create a scheduled post for Jay Soundo"""
        try:
            # Get random theme
            themes = self.jay_soundo_bot["content_themes"]
            theme = random.choice(themes)
            
            # Create post content
            result = await self.jay_soundo_service.create_post_content(theme)
            
            if result and result.get("success"):
                # Check if photo already used
                photo_id = result["photo_data"]["id"]
                if self.photo_tracker.is_photo_used(self.bot_username, photo_id):
                    logger.warning(f"⚠️ Photo {photo_id} already used, skipping...")
                    return
                
                # Send to Node.js backend
                post_success = await self._send_to_backend(result)
                
                if post_success:
                    # Mark photo as used
                    self.photo_tracker.mark_photo_used(self.bot_username, photo_id)
                    # Mark post time
                    mark_post_created(self.bot_username)
                    logger.info(f"✅ Jay Soundo scheduled post created successfully - Theme: {theme}")
                else:
                    logger.error("❌ Failed to send Jay Soundo post to backend")
            else:
                logger.error(f"❌ Failed to create Jay Soundo post content: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"❌ Error creating Jay Soundo scheduled post: {str(e)}")
    
    async def create_manual_post(self, theme: str = "random") -> Dict:
        """Create a manual post for Jay Soundo"""
        try:
            logger.info(f"🎨 Creating manual Jay Soundo post - Theme: {theme}")
            
            # Create post content
            result = await self.jay_soundo_service.create_post_content(theme if theme != "random" else None)
            
            if result and result.get("success"):
                # Check if photo already used
                photo_id = result["photo_data"]["id"]
                if self.photo_tracker.is_photo_used(self.bot_username, photo_id):
                    return {
                        "success": False,
                        "error": f"Photo {photo_id} already used by {self.bot_username}"
                    }
                
                # Send to Node.js backend
                post_success = await self._send_to_backend(result)
                
                if post_success:
                    # Mark photo as used
                    self.photo_tracker.mark_photo_used(self.bot_username, photo_id)
                    
                    return {
                        "success": True,
                        "message": "Jay Soundo manual post created successfully",
                        "photo_id": photo_id,
                        "photographer": result["photo_data"].get("photographer"),
                        "likes": result["photo_data"].get("likes", 0),
                        "theme": result.get("theme", theme)
                    }
                else:
                    return {
                        "success": False,
                        "error": "Failed to send post to backend"
                    }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Failed to create post content")
                }
                
        except Exception as e:
            logger.error(f"❌ Error creating Jay Soundo manual post: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _send_to_backend(self, post_data: Dict) -> bool:
        """Send post data to Node.js backend"""
        try:
            # Prepare payload for Node.js backend
            payload = {
                "botUsername": self.bot_username,
                "displayName": self.jay_soundo_bot["displayName"],
                "avatar": self.jay_soundo_bot["avatar"],
                "bio": self.jay_soundo_bot["bio"],
                "isBot": True,
                "botMetadata": {
                    "botType": self.jay_soundo_bot["botType"],
                    "source": "jay_soundo_photography",
                    "theme": post_data.get("theme"),
                    "photographer": post_data["photo_data"].get("photographer"),
                    "unsplash_id": post_data["photo_data"]["id"]
                },
                "content": post_data["caption"],
                "imageUrl": post_data["photo_data"]["url"],
                "cloudinaryFolder": self.jay_soundo_bot["cloudinary_folder"]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.node_backend_url}/api/bot/create-post",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"✅ Jay Soundo post sent to backend successfully")
                        return True
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Backend error for Jay Soundo: {response.status} - {error_text}")
                        return False
                        
        except Exception as e:
            logger.error(f"❌ Error sending Jay Soundo post to backend: {str(e)}")
            return False
    
    def get_bot_stats(self) -> Dict:
        """Get Jay Soundo bot statistics"""
        try:
            schedule_stats = get_schedule_stats(self.bot_username)
            photo_stats = self.photo_tracker.get_photo_stats(self.bot_username)
            
            return {
                "bot_info": {
                    "username": self.jay_soundo_bot["username"],
                    "displayName": self.jay_soundo_bot["displayName"],
                    "botType": self.jay_soundo_bot["botType"],
                    "unsplash_source": self.jay_soundo_bot["unsplash_source"],
                    "total_source_photos": self.jay_soundo_bot["total_source_photos"],
                    "specialties": self.jay_soundo_bot["specialties"]
                },
                "scheduler_status": {
                    "is_running": self.is_running,
                    "posting_times": get_jay_soundo_posting_times(),
                    "timezone": "Asia/Ho_Chi_Minh"
                },
                "schedule_stats": schedule_stats,
                "photo_stats": photo_stats,
                "content_strategy": {
                    "themes": self.jay_soundo_bot["content_themes"],
                    "content_mix": self.jay_soundo_bot["posting_schedule"]["content_mix"],
                    "engagement_style": self.jay_soundo_bot["engagement_style"]
                }
            }
        except Exception as e:
            logger.error(f"❌ Error getting Jay Soundo bot stats: {str(e)}")
            return {"error": str(e)}
