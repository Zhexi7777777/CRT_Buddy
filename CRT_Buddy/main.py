"""
CRT Buddy - Main Application v6.0
Y2K Desktop Pet and Meme Generator with Input Visualization
"""
import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from core.pet_window_v6 import CRTBuddyWindow
from generators.meme_engine import MemeEngine


class CRTBuddyApp:
    """CRT Buddy Application Main Class"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("CRT Buddy")
        
        self.meme_engine = MemeEngine(output_dir="output")
        self.window = CRTBuddyWindow()
        self.setup_connections()
        
        QTimer.singleShot(500, self.show_welcome)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.window.image_dropped.connect(self.handle_image_drop)
        self.window.generate_btn.clicked.connect(self.handle_generate)
        self.window.effect_btn.clicked.connect(self.handle_random_effect)
    
    def show_welcome(self):
        """Show welcome message"""
        self.window.set_status("WELCOME TO CRT BUDDY")
        self.window.set_mood("happy")
        
        QTimer.singleShot(3000, lambda: self.window.set_status(
            "READY TO GENERATE Y2K VIBES"
        ))
    
    def handle_image_drop(self, image_path):
        """Handle image drop"""
        self.window.set_mood("processing")
        self.window.set_status("PROCESSING IMAGE...")
        
        QTimer.singleShot(500, lambda: self.process_image(image_path))
    
    def process_image(self, image_path):
        """Process image and apply effects"""
        try:
            text = self.window.get_input_text()
            
            result_img = self.meme_engine.generate_image_meme(
                image_path, 
                text=text,
                effect='random'
            )
            
            if result_img:
                output_path = self.meme_engine.save_meme(result_img, "y2k_image")
                
                if output_path:
                    self.window.set_mood("happy")
                    self.window.set_status(f"SAVED: {os.path.basename(output_path)}")
                    QTimer.singleShot(2000, self.show_success_message)
                else:
                    self.window.set_status("Failed to save meme")
            else:
                self.window.set_status("Failed to process image")
                self.window.set_mood("idle")
                
        except Exception as e:
            print(f"Error processing image: {e}")
            self.window.set_status(f"ERROR: {str(e)}")
            self.window.set_mood("idle")
    
    def handle_generate(self):
        """Handle generate meme button"""
        text = self.window.get_input_text().strip()
        
        if not text:
            self.window.set_status("Please enter some text first!")
            return
        
        self.window.set_mood("processing")
        self.window.set_status("GENERATING Y2K MEME...")
        
        QTimer.singleShot(500, lambda: self.generate_text_meme(text))
    
    def generate_text_meme(self, text):
        """Generate text meme"""
        try:
            result_img = self.meme_engine.generate_text_meme(text, style='random')
            
            if result_img:
                output_path = self.meme_engine.save_meme(result_img, "y2k_text")
                
                if output_path:
                    self.window.set_mood("happy")
                    self.window.set_status(f"SAVED: {os.path.basename(output_path)}")
                    self.window.clear_input()
                    
                    QTimer.singleShot(2000, self.show_success_message)
                else:
                    self.window.set_status("Failed to save meme")
            else:
                self.window.set_status("Failed to generate meme")
                
        except Exception as e:
            print(f"Error generating text meme: {e}")
            self.window.set_status(f"ERROR: {str(e)}")
        
        finally:
            QTimer.singleShot(3000, lambda: self.window.set_mood("idle"))
    
    def handle_random_effect(self):
        """Handle random effect button"""
        self.window.set_mood("processing")
        self.window.set_status("GENERATING RANDOM Y2K MAGIC...")
        
        QTimer.singleShot(500, self.generate_random_meme)
    
    def generate_random_meme(self):
        """Generate completely random meme"""
        try:
            result_img = self.meme_engine.generate_random_meme()
            
            if result_img:
                output_path = self.meme_engine.save_meme(result_img, "y2k_random")
                
                if output_path:
                    self.window.set_mood("happy")
                    self.window.set_status(f"SAVED: {os.path.basename(output_path)}")
                    
                    QTimer.singleShot(2000, self.show_success_message)
                else:
                    self.window.set_status("Failed to save meme")
            else:
                self.window.set_status("Failed to generate meme")
                
        except Exception as e:
            print(f"Error generating random meme: {e}")
            self.window.set_status(f"ERROR: {str(e)}")
        
        finally:
            QTimer.singleShot(3000, lambda: self.window.set_mood("idle"))
    
    def show_success_message(self):
        """Show success message and reset status"""
        self.window.set_status("CHECK THE 'output' FOLDER!")
        QTimer.singleShot(3000, lambda: self.window.set_status(
            "READY TO GENERATE Y2K VIBES"
        ))
    
    def run(self):
        """Run application"""
        self.window.show()
        return self.app.exec()


def main():
    """Main function"""
    print("=" * 50)
    print("  CRT BUDDY - Y2K Desktop Pet")
    print("  Y2K Desktop Pet & Meme Generator")
    print("=" * 50)
    print("\nStarting CRT Buddy...\n")
    
    app = CRTBuddyApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
