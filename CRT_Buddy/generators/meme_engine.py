"""
CRT Buddy - Meme Generator Engine
Y2K style Meme generation engine
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random
import os
from datetime import datetime
from effects.y2k_styles import Y2KStyles
from effects.text_effects import TextEffects


class MemeEngine:
    """Y2K style Meme generation engine"""
    
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        self.y2k_styles = Y2KStyles()
        self.text_effects = TextEffects()
        
        # Create output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Y2K phrases
        self.y2k_phrases = [
            "UNDER CONSTRUCTION",
            "WELCOME TO MY WEBSITE",
            "BEST VIEWED IN NETSCAPE",
            "Y2K AESTHETIC",
            "CYBER DREAMS 2000",
            "POWERED BY GEOCITIES",
            "ENTER IF YOU DARE",
            "LOADING... PLEASE WAIT",
            "404 PAGE NOT FOUND",
            "GUESTBOOK - SIGN IN!",
            "WEBMASTER",
            "HIT COUNTER",
            "EMAIL ME",
            "NEW! UPDATED!",
            "COOL SITE AWARD",
            "MIDI MUSIC PLAYING",
            "FRAMES VERSION",
            "TEXT ONLY VERSION",
            "OPTIMIZED FOR 800x600",
            "MILLENNIUM BUG FREE"
        ]
    
    def generate_text_meme(self, text, style='random', size=(800, 600)):
        """Generate text-based meme"""
        # Create base image
        img = Image.new('RGB', size, color=(0, 0, 0))
        
        # Apply Y2K background
        img = self._apply_y2k_background(img)
        
        # Add text with effect
        if style == 'random':
            style = random.choice(['gradient', 'glitch', 'neon', 'chrome', 'retro'])
        
        img = self.text_effects.apply_effect(img, text, style)
        
        # Add decorations
        img = self._add_decorations(img)
        
        return img
    
    def generate_image_meme(self, image_path, text="", effect='random'):
        """Generate image-based meme with Y2K effects"""
        # Load image
        img = Image.open(image_path)
        img = img.convert('RGB')
        
        # Resize if too large
        max_size = 1200
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Apply Y2K effect
        if effect == 'random':
            effect = random.choice(['crt', 'vhs', 'holographic', 'chrome', 'neon', 'pixelate'])
        
        img = self.y2k_styles.apply_effect(img, effect)
        
        # Add text if provided
        if text:
            img = self._add_text_overlay(img, text)
        
        return img
    
    def generate_random_meme(self):
        """Generate completely random meme"""
        # Random phrase
        phrase = random.choice(self.y2k_phrases)
        
        # Random size
        sizes = [(800, 600), (640, 480), (1024, 768)]
        size = random.choice(sizes)
        
        # Generate
        return self.generate_text_meme(phrase, 'random', size)
    
    def save_meme(self, img, prefix="meme"):
        """Save meme to output directory"""
        # Generate filename
        counter = 1
        while True:
            filename = f"{prefix}_{counter}.png"
            filepath = os.path.join(self.output_dir, filename)
            if not os.path.exists(filepath):
                break
            counter += 1
        
        # Save
        img.save(filepath, 'PNG')
        print(f"Saved: {filepath}")
        return filepath
    
    def _apply_y2k_background(self, img):
        """Apply Y2K style background"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Gradient background
        for y in range(height):
            r = int(128 + 127 * (y / height))
            g = int(0 + 128 * (y / height))
            b = int(128 - 128 * (y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add grid
        for x in range(0, width, 50):
            draw.line([(x, 0), (x, height)], fill=(255, 0, 255, 30), width=1)
        for y in range(0, height, 50):
            draw.line([(0, y), (width, y)], fill=(255, 0, 255, 30), width=1)
        
        return img
    
    def _add_text_overlay(self, img, text):
        """Add text overlay to image"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Try to use a nice font
        try:
            font_size = int(height * 0.1)
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position (bottom center)
        x = (width - text_width) // 2
        y = height - text_height - 30
        
        # Draw shadow
        shadow_offset = 3
        draw.text((x + shadow_offset, y + shadow_offset), text, fill=(0, 0, 0), font=font)
        
        # Draw text
        draw.text((x, y), text, fill=(255, 255, 0), font=font)
        
        return img
    
    def _add_decorations(self, img):
        """Add Y2K style decorations"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Random stars
        for _ in range(20):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(2, 5)
            color = random.choice([(255, 0, 255), (0, 255, 255), (255, 255, 0)])
            draw.ellipse([x, y, x+size, y+size], fill=color)
        
        return img
