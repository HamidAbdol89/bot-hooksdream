"""
Jay Soundo Bot Account Configuration
Separate bot system for Jay Soundo Photography
"""

from datetime import datetime
from typing import Dict, List

# Jay Soundo Bot Account
JAY_SOUNDO_BOT_ACCOUNT = {
    "_id": "photography_bot_jay_002",
    "username": "jay_soundo_photography",
    "displayName": "Jay Soundo Photography",
    "email": "jay.soundo@hooksdream.bot",
    "bio": "Professional photographer capturing life's diverse moments. Nature • Urban • People • Creative Vision 📸🌟",
    "location": "Global Traveler",
    "website": "https://unsplash.com/@jaysoundo",
    "botType": "photographer",
    "isBot": True,
    "isVerified": False,
    "hasCustomAvatar": True,
    "hasCustomDisplayName": True,
    # Avatar từ Jay Soundo's profile
    "avatar": "https://images.unsplash.com/profile-1734014188179-c37f7ce4dcceimage?w=150&dpr=2&crop=faces&bg=%23fff&h=150&auto=format&fit=crop&q=60&ixlib=rb-4.1.0",
    "coverImage": "",  # Không cần cover image
    "cloudinary_folder": "bots/jay_soundo_photography",
    # Unsplash source account để lấy ảnh
    "unsplash_source": "jaysoundo",
    "unsplash_profile": "https://unsplash.com/@jaysoundo",
    "total_source_photos": 1200,
    "interests": [
        "nature_photography", "urban_photography", "travel_photography", "portrait_photography",
        "landscape_photography", "street_photography", "architectural_photography", "lifestyle_photography",
        "creative_photography", "professional_photography", "visual_storytelling", "diverse_content"
    ],
    "specialties": [
        "Nature & Landscapes", "Urban Architecture", "People & Lifestyle", 
        "Abstract & Creative", "Technology & Modern", "Travel Photography"
    ],
    "posting_style": "professional_diverse",
    "content_focus": ["diverse_photography", "professional_quality", "visual_storytelling", "creative_vision"],
    "follower_range": [3000, 6000],
    "engagement_style": "professional_inspiring",
    "specialBadge": {
        "type": "photographer",
        "icon": "📸",
        "color": "#3498DB",
        "label": "Photographer"
    },
    # Content strategy based on Jay Soundo's diverse work
    "content_themes": [
        "nature", "landscape", "urban", "architecture", "people", "lifestyle", "travel",
        "abstract", "creative", "technology", "modern", "artistic", "professional"
    ],
    "posting_schedule": {
        "frequency": "daily",
        "best_times": ["08:00", "14:00", "20:00"],
        "content_mix": {
            "nature_landscapes": 30,
            "urban_architecture": 25,
            "people_lifestyle": 25,
            "creative_abstract": 20
        }
    },
    "created_at": datetime.now()
}

def get_jay_soundo_bot_account() -> Dict:
    """Get Jay Soundo bot account"""
    return JAY_SOUNDO_BOT_ACCOUNT

def get_jay_soundo_cloudinary_folder() -> str:
    """Get Cloudinary folder for Jay Soundo bot"""
    return JAY_SOUNDO_BOT_ACCOUNT["cloudinary_folder"]

def get_jay_soundo_themes() -> List[str]:
    """Get content themes for Jay Soundo bot"""
    return JAY_SOUNDO_BOT_ACCOUNT["content_themes"]

def get_jay_soundo_posting_times() -> List[str]:
    """Get posting times for Jay Soundo bot"""
    return JAY_SOUNDO_BOT_ACCOUNT["posting_schedule"]["best_times"]
