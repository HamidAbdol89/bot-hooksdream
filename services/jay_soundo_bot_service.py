"""
Jay Soundo Photography Bot Service
Handles automated content creation for Jay Soundo Photography Bot
Specializes in diverse photography content from @jaysoundo (1.2k+ photos)
"""

import asyncio
import random
import logging
from datetime import datetime
from typing import Dict, List, Optional
from services.unsplash_service import UnsplashService

logger = logging.getLogger(__name__)

class JaySoundoService:
    """Service for Jay Soundo Photography bot content generation"""
    
    def __init__(self):
        self.unsplash_service = UnsplashService()
        self.bot_username = "jay_soundo_photography"
        
        # Jay Soundo photography themes - diverse content
        self.photography_themes = [
            # Nature & Landscapes
            "nature", "landscape", "mountains", "forest", "ocean", "sunset", "sunrise",
            "clouds", "sky", "trees", "flowers", "wildlife", "beach", "desert",
            
            # Urban & Architecture  
            "architecture", "building", "city", "street", "urban", "bridge", "skyline",
            "modern", "vintage", "industrial", "geometric", "patterns",
            
            # People & Lifestyle
            "people", "portrait", "lifestyle", "travel", "culture", "fashion", "sport",
            "music", "art", "creative", "work", "business", "family",
            
            # Abstract & Creative
            "abstract", "minimalist", "texture", "color", "light", "shadow", "reflection",
            "symmetry", "composition", "artistic", "creative", "experimental",
            
            # Technology & Modern
            "technology", "digital", "innovation", "future", "design", "modern",
            "gadgets", "workspace", "startup", "creative workspace"
        ]
        
        # Caption templates for photography content
        self.caption_templates = [
            # Inspirational Photography
            "Capturing moments that tell stories 📸✨\n\n{description}\n\n#photography #jaysoundo #moment #storytelling #visual #art",
            "Through the lens of creativity 🎨📷\n\n{description}\n\n#photographer #creative #vision #capture #artistic #inspiration",
            "Every frame holds a universe 🌟📸\n\n{description}\n\n#photography #universe #frame #moment #beauty #perspective",
            
            # Technical Photography
            "The art of seeing light and shadow 💡🖤\n\n{description}\n\n#lightandshadow #photography #technique #composition #visual #art",
            "Composition meets creativity 🎯📸\n\n{description}\n\n#composition #photography #creative #technique #visual #storytelling",
            "Perspective changes everything 👁️✨\n\n{description}\n\n#perspective #photography #vision #creative #angle #unique",
            
            # Emotional Photography  
            "Emotions frozen in time ❄️💫\n\n{description}\n\n#emotions #photography #time #moment #feeling #capture #memory",
            "Stories without words 📖📸\n\n{description}\n\n#storytelling #photography #visual #narrative #silent #powerful",
            "Beauty in the everyday 🌸📷\n\n{description}\n\n#everyday #beauty #photography #simple #elegant #life #moment",
            
            # Professional Photography
            "Professional vision, artistic soul 🎨💼\n\n{description}\n\n#professional #photography #artistic #vision #quality #creative #work",
            "Crafting visual experiences 🛠️📸\n\n{description}\n\n#craft #visual #experience #photography #professional #creative #art"
        ]
        
    async def get_random_photo(self, theme: str = None) -> Optional[Dict]:
        """Get random photo from Jay Soundo's collection"""
        try:
            if not theme:
                theme = random.choice(self.photography_themes)
            
            # Search for photos by Jay Soundo with the theme
            photos = await self.unsplash_service.search_photos(
                query=f"{theme} @jaysoundo",
                per_page=30,
                orientation="all"
            )
            
            if not photos:
                # Fallback: get photos from Jay Soundo's profile
                photos = await self.unsplash_service.get_user_photos("jaysoundo", per_page=30)
            
            if photos:
                photo = random.choice(photos)
                return {
                    "id": photo["id"],
                    "url": photo["urls"]["regular"],
                    "download_url": photo["links"]["download_location"],
                    "description": photo.get("description") or photo.get("alt_description", ""),
                    "photographer": photo["user"]["name"],
                    "photographer_username": photo["user"]["username"],
                    "likes": photo.get("likes", 0),
                    "theme": theme,
                    "width": photo.get("width", 0),
                    "height": photo.get("height", 0)
                }
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error getting Jay Soundo photo: {str(e)}")
            return None
    
    def generate_caption(self, photo_data: Dict, theme: str) -> str:
        """Generate engaging caption for Jay Soundo photography"""
        try:
            # Use photo description or create theme-based description
            description = photo_data.get("description", "")
            if not description:
                description = f"Exploring {theme} through the lens of creativity"
            
            # Select random caption template
            template = random.choice(self.caption_templates)
            
            # Format caption with photo data
            caption = template.format(
                description=description,
                theme=theme,
                photographer=photo_data.get("photographer", "Jay Soundo")
            )
            
            return caption
            
        except Exception as e:
            logger.error(f"❌ Error generating Jay Soundo caption: {str(e)}")
            return f"Capturing the beauty of {theme} 📸✨\n\n#photography #jaysoundo #creative #visual #art"
    
    async def create_post_content(self, theme: str = None) -> Optional[Dict]:
        """Create complete post content for Jay Soundo bot"""
        try:
            # Get random photo
            photo_data = await self.get_random_photo(theme)
            if not photo_data:
                return None
            
            # Generate caption
            caption = self.generate_caption(photo_data, photo_data["theme"])
            
            # Trigger download tracking (Unsplash requirement)
            if photo_data.get("download_url"):
                await self.unsplash_service.download_photo(photo_data["id"])
            
            return {
                "success": True,
                "photo_data": photo_data,
                "caption": caption,
                "bot_username": self.bot_username,
                "theme": photo_data["theme"],
                "source": "unsplash_jaysoundo"
            }
            
        except Exception as e:
            logger.error(f"❌ Error creating Jay Soundo post: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_bot_info(self) -> Dict:
        """Get Jay Soundo bot information"""
        return {
            "username": self.bot_username,
            "displayName": "Jay Soundo Photography",
            "botType": "photography_diverse",
            "photographer": "Jay Soundo (@jaysoundo)",
            "total_photos": "1200+",
            "specialties": [
                "Nature & Landscapes",
                "Urban Architecture", 
                "People & Lifestyle",
                "Abstract & Creative",
                "Technology & Modern"
            ],
            "content_themes": self.photography_themes,
            "posting_style": "Professional photography with diverse themes",
            "engagement_style": "Visual storytelling and creative inspiration"
        }
