"""
CRT Buddy - Text Effects
Y2K style text rendering effects
"""
from PIL import Image, ImageDraw, ImageFont
import random


class TextEffects:
    """Y2K style text effects"""
    
    def apply_effect(self, img, text, style):
        """Apply specified text effect"""
        effects = {
            'gradient': self.gradient_text,
            'glitch': self.glitch_text,
            'neon': self.neon_text,
            'chrome': self.chrome_text,
            'retro': self.retro_text
        }
        
        effect_func = effects.get(style, self.gradient_text)
        return effect_func(img, text)
    
    def gradient_text(self, img, text):
        """Gradient text effect"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Get font
        try:
            font_size = min(width, height) // 8
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw each character with different color
        colors = [(255, 0, 255), (0, 255, 255), (255, 255, 0), (0, 255, 0)]
        char_x = x
        
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            draw.text((char_x, y), char, fill=color, font=font)
            char_bbox = draw.textbbox((char_x, y), char, font=font)
            char_x += char_bbox[2] - char_bbox[0]
        
        return img
    
    def glitch_text(self, img, text):
        """Glitch/RGB split text effect"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Get font
        try:
            font_size = min(width, height) // 8
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw RGB layers with offsets
        offsets = [(0, -3), (3, 0), (-3, 3)]
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        
        for offset, color in zip(offsets, colors):
            draw.text((x + offset[0], y + offset[1]), text, fill=color, font=font)
        
        return img
    
    def neon_text(self, img, text):
        """Neon glow text effect"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Get font
        try:
            font_size = min(width, height) // 8
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw glow layers
        glow_color = (255, 0, 255)
        for i in range(10, 0, -2):
            alpha = int(255 * (i / 10))
            draw.text((x, y), text, fill=glow_color + (alpha,), font=font)
        
        # Draw main text
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        
        return img
    
    def chrome_text(self, img, text):
        """Chrome/metallic text effect"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Get font
        try:
            font_size = min(width, height) // 8
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw shadow
        draw.text((x + 5, y + 5), text, fill=(0, 0, 0), font=font)
        
        # Draw gradient
        for i in range(0, text_height, 2):
            shade = int(128 + 127 * (i / text_height))
            draw.text((x, y + i), text, fill=(shade, shade, shade + 50), font=font)
        
        # Draw highlight
        draw.text((x - 1, y - 1), text, fill=(255, 255, 255, 100), font=font)
        
        return img
    
    def retro_text(self, img, text):
        """Retro rainbow text effect"""
        draw = ImageDraw.Draw(img)
        width, height = img.size
        
        # Get font
        try:
            font_size = min(width, height) // 8
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Rainbow colors
        colors = [
            (255, 0, 0),    # Red
            (255, 127, 0),  # Orange
            (255, 255, 0),  # Yellow
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (75, 0, 130),   # Indigo
            (148, 0, 211)   # Violet
        ]
        
        # Draw each character with rainbow colors
        char_x = x
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            draw.text((char_x, y), char, fill=color, font=font)
            char_bbox = draw.textbbox((char_x, y), char, font=font)
            char_x += char_bbox[2] - char_bbox[0]
        
        return img
