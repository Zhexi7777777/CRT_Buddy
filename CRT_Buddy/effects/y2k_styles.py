"""
CRT Buddy - Y2K Style Effects
Y2K style image filters and effects
"""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
import random


class Y2KStyles:
    """Y2K style image effects"""
    
    def apply_effect(self, img, effect_name):
        """Apply specified effect to image"""
        effects = {
            'crt': self.crt_effect,
            'vhs': self.vhs_effect,
            'holographic': self.holographic_effect,
            'chrome': self.chrome_effect,
            'neon': self.neon_effect,
            'pixelate': self.pixelate_effect
        }
        
        effect_func = effects.get(effect_name, self.crt_effect)
        return effect_func(img)
    
    def crt_effect(self, img):
        """CRT monitor effect with scanlines and RGB shift"""
        img = img.copy()
        width, height = img.size
        
        # RGB shift
        img_array = np.array(img)
        shifted = img_array.copy()
        shifted[:, 2:, 0] = img_array[:, :-2, 0]  # Red shift
        shifted[:, :-2, 2] = img_array[:, 2:, 2]  # Blue shift
        img = Image.fromarray(shifted)
        
        # Add scanlines
        draw = ImageDraw.Draw(img)
        for y in range(0, height, 3):
            draw.line([(0, y), (width, y)], fill=(0, 0, 0, 50), width=1)
        
        # Slight blur
        img = img.filter(ImageFilter.GaussianBlur(0.5))
        
        return img
    
    def vhs_effect(self, img):
        """VHS tape glitch effect"""
        img = img.copy()
        width, height = img.size
        img_array = np.array(img)
        
        # Horizontal displacement
        for _ in range(random.randint(3, 8)):
            y = random.randint(0, height - 50)
            h = random.randint(5, 30)
            shift = random.randint(-20, 20)
            
            if shift > 0:
                img_array[y:y+h, shift:] = img_array[y:y+h, :-shift]
            else:
                img_array[y:y+h, :shift] = img_array[y:y+h, -shift:]
        
        img = Image.fromarray(img_array)
        
        # Color distortion
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.3)
        
        # Add noise
        img_array = np.array(img)
        noise = np.random.randint(-20, 20, img_array.shape, dtype=np.int16)
        noisy = np.clip(img_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(noisy)
        
        return img
    
    def holographic_effect(self, img):
        """Holographic rainbow gradient effect"""
        img = img.copy()
        width, height = img.size
        
        # Create rainbow overlay
        overlay = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(overlay)
        
        for y in range(height):
            hue = (y / height) * 255
            r = int(128 + 127 * np.sin(hue * 0.02))
            g = int(128 + 127 * np.sin(hue * 0.02 + 2))
            b = int(128 + 127 * np.sin(hue * 0.02 + 4))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Blend
        img = Image.blend(img, overlay, 0.3)
        
        # Enhance
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.2)
        
        return img
    
    def chrome_effect(self, img):
        """Metallic chrome effect"""
        # Convert to grayscale
        img = img.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        
        # Apply edge enhancement
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        
        # Convert back to RGB with silver tint
        img = img.convert('RGB')
        img_array = np.array(img)
        img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 1.1, 0, 255)  # More red
        img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 1.1, 0, 255)  # More blue
        img = Image.fromarray(img_array.astype(np.uint8))
        
        return img
    
    def neon_effect(self, img):
        """Neon glow effect"""
        img = img.copy()
        
        # Enhance colors
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(2.0)
        
        # Edge detection
        edges = img.filter(ImageFilter.FIND_EDGES)
        
        # Blur edges for glow
        glow = edges.filter(ImageFilter.GaussianBlur(5))
        
        # Composite
        img = Image.blend(img, glow, 0.5)
        
        # Brighten
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.3)
        
        return img
    
    def pixelate_effect(self, img):
        """Retro pixelation effect"""
        width, height = img.size
        
        # Shrink
        pixel_size = 8
        small_size = (width // pixel_size, height // pixel_size)
        img_small = img.resize(small_size, Image.Resampling.NEAREST)
        
        # Enlarge back
        img = img_small.resize((width, height), Image.Resampling.NEAREST)
        
        # Reduce colors
        img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=32)
        img = img.convert('RGB')
        
        return img
