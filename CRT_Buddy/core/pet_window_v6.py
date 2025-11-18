"""
CRT Buddy - Pet Window v6.0
Y2K Desktop PC style with INPUT VISUALIZATION and keystroke tracking
"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QLinearGradient, QFont, QBrush, QPainterPath, QRadialGradient, QCursor, QFontDatabase, QKeyEvent
import random
import math
import os
import sys
from collections import deque
from datetime import datetime


class CRTBuddyWindow(QWidget):
    """Y2K Desktop PC style with input visualization and keystroke tracking"""
    
    # Signals
    image_dropped = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.load_pixel_font()
        self.init_keystroke_tracking()
        self.init_ui()
        self.setup_animations()
        
        # Drag variables
        self.dragging = False
        self.drag_position = QPoint()
        
        # Current mood
        self.current_mood = "idle"
        
        # Global mouse tracking for eyes
        self.global_mouse_pos = QCursor.pos()
        
        # Mascot properties
        self.blink_timer = 0
        self.is_blinking = False
        
    def init_keystroke_tracking(self):
        """Initialize keystroke tracking system"""
        # Keystroke history (last 10 keys)
        self.key_history = deque(maxlen=10)
        
        # Current active keystroke display
        self.active_keystroke = None
        self.keystroke_timer = 0
        self.keystroke_fade = 255
        
        # Input statistics
        self.total_keystrokes = 0
        self.last_keystroke_time = None
        self.typing_speed = 0  # characters per minute
        self.keystroke_times = deque(maxlen=60)  # Track last 60 keystrokes for speed calc
        
        # Visual effects
        self.keystroke_particles = []  # Particle effects when typing
        self.input_pulse = 0  # Pulse effect on input area
        
    def load_pixel_font(self):
        """Load DinkieBitmap pixel font"""
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)
        
        font_paths = [
            os.path.join(base_path, "DinkieBitmap-v1.5.0-KeDingKeMao", "ttf", "DinkieBitmap-9px.ttf"),
            os.path.join(base_path, "..", "..", "DinkieBitmap-v1.5.0-KeDingKeMao", "ttf", "DinkieBitmap-9px.ttf"),
            "../DinkieBitmap-v1.5.0-KeDingKeMao/ttf/DinkieBitmap-9px.ttf",
            "DinkieBitmap-v1.5.0-KeDingKeMao/ttf/DinkieBitmap-9px.ttf"
        ]
        
        for font_path in font_paths:
            abs_path = os.path.abspath(font_path)
            if os.path.exists(abs_path):
                font_id = QFontDatabase.addApplicationFont(abs_path)
                if font_id != -1:
                    font_families = QFontDatabase.applicationFontFamilies(font_id)
                    if font_families:
                        self.pixel_font_family = font_families[0]
                        print(f"✓ Loaded pixel font: {self.pixel_font_family} from {abs_path}")
                        return
        
        self.pixel_font_family = "DinkieBitmap 9px"
        print("⚠ WARNING: Pixel font file not found! Using font name anyway.")
        
    def init_ui(self):
        """Initialize user interface with input visualization"""
        # Window settings - wider for keystroke display
        self.setWindowTitle("CRT Buddy v6.0 - Input Visualization")
        self.setGeometry(100, 100, 520, 320)  # Wider and taller
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        
        # Main horizontal layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)
        
        # Left side - CRT Screen with mascot
        left_widget = QWidget()
        left_widget.setFixedWidth(240)
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        main_layout.addWidget(left_widget)
        
        # Right side - Controls
        right_layout = QVBoxLayout()
        right_layout.setSpacing(5)
        
        # Status display
        self.status_label = QLabel("CRT BUDDY v6.0 - INPUT VISUALIZER")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: #00FFFF;
                background-color: rgba(0, 20, 40, 200);
                border: 2px solid #0088FF;
                border-radius: 4px;
                padding: 5px;
                font-family: '{self.pixel_font_family}';
                font-size: 9px;
            }}
        """)
        right_layout.addWidget(self.status_label)
        
        # Input statistics display
        self.stats_label = QLabel("KEYS: 0 | SPEED: 0 CPM")
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_label.setStyleSheet(f"""
            QLabel {{
                color: #FFD700;
                background-color: rgba(20, 0, 40, 180);
                border: 2px solid #FF00FF;
                border-radius: 4px;
                padding: 3px;
                font-family: '{self.pixel_font_family}';
                font-size: 8px;
            }}
        """)
        right_layout.addWidget(self.stats_label)
        
        # Input area with custom event handling
        self.input_text = KeystrokeTextEdit(self)
        self.input_text.setPlaceholderText("Type here... watch the magic!")
        self.input_text.setMaximumHeight(60)
        self.input_text.setStyleSheet(f"""
            QTextEdit {{
                color: #00FFFF;
                background-color: rgba(0, 20, 40, 180);
                border: 2px solid #0066CC;
                border-radius: 4px;
                padding: 4px;
                font-family: '{self.pixel_font_family}';
                font-size: 9px;
            }}
        """)
        right_layout.addWidget(self.input_text)
        
        # Buttons
        self.generate_btn = QPushButton("GENERATE")
        self.generate_btn.setMinimumHeight(30)
        self.generate_btn.setStyleSheet(self.get_bar_button_style("#FF0080", "#FF66B3"))
        right_layout.addWidget(self.generate_btn)
        
        self.upload_btn = QPushButton("IMAGE")
        self.upload_btn.setMinimumHeight(30)
        self.upload_btn.setStyleSheet(self.get_bar_button_style("#00CCFF", "#66E0FF"))
        self.upload_btn.clicked.connect(self.upload_image)
        right_layout.addWidget(self.upload_btn)
        
        self.effect_btn = QPushButton("RANDOM")
        self.effect_btn.setMinimumHeight(30)
        self.effect_btn.setStyleSheet(self.get_bar_button_style("#FFD700", "#FFE766"))
        right_layout.addWidget(self.effect_btn)
        
        right_layout.addStretch()
        
        # Close button
        close_container = QHBoxLayout()
        close_container.addStretch()
        
        self.close_btn = QPushButton("X")
        self.close_btn.setFixedSize(45, 45)
        self.close_btn.setStyleSheet(self.get_round_button_style())
        self.close_btn.clicked.connect(self.close)
        close_container.addWidget(self.close_btn)
        
        right_layout.addLayout(close_container)
        
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)
        
    def get_bar_button_style(self, color1, color2):
        """Get long bar metallic button style"""
        return f"""
            QPushButton {{
                color: #A8A8A8;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(100, 100, 100, 200),
                    stop:0.2 rgba(140, 140, 140, 220),
                    stop:0.4 {color1},
                    stop:0.6 {color2},
                    stop:0.8 rgba(140, 140, 140, 220),
                    stop:1 rgba(100, 100, 100, 200));
                border: 2px solid rgba(160, 160, 160, 180);
                border-top: 3px solid rgba(220, 220, 220, 200);
                border-left: 2px solid rgba(200, 200, 200, 180);
                border-bottom: 3px solid rgba(80, 80, 80, 200);
                border-right: 2px solid rgba(100, 100, 100, 180);
                border-radius: 8px;
                padding: 8px;
                font-family: '{self.pixel_font_family}';
                font-size: 10px;
            }}
            QPushButton:hover {{
                color: #D0D0D0;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(120, 120, 120, 220),
                    stop:0.2 rgba(180, 180, 180, 240),
                    stop:0.4 {color2},
                    stop:0.6 white,
                    stop:0.8 rgba(180, 180, 180, 240),
                    stop:1 rgba(120, 120, 120, 220));
                border-top: 3px solid rgba(255, 255, 255, 240);
                border-left: 2px solid rgba(240, 240, 240, 220);
            }}
            QPushButton:pressed {{
                color: #808080;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(60, 60, 60, 220),
                    stop:0.2 rgba(80, 80, 80, 230),
                    stop:0.4 {color1},
                    stop:0.6 {color1},
                    stop:0.8 rgba(80, 80, 80, 230),
                    stop:1 rgba(60, 60, 60, 220));
                border-top: 2px solid rgba(60, 60, 60, 200);
                border-left: 2px solid rgba(70, 70, 70, 180);
                border-bottom: 2px solid rgba(180, 180, 180, 200);
                border-right: 2px solid rgba(160, 160, 160, 180);
                padding-top: 10px;
            }}
        """
    
    def get_round_button_style(self):
        """Get round metallic power button"""
        return f"""
            QPushButton {{
                color: #A8A8A8;
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    fx:0.35, fy:0.35,
                    stop:0 rgba(220, 220, 220, 250),
                    stop:0.5 rgba(180, 180, 180, 250),
                    stop:0.85 rgba(140, 140, 140, 240),
                    stop:1 rgba(100, 100, 100, 230));
                border: 3px solid rgba(160, 160, 160, 200);
                border-top: 4px solid rgba(240, 240, 240, 220);
                border-left: 3px solid rgba(220, 220, 220, 210);
                border-bottom: 4px solid rgba(80, 80, 80, 220);
                border-right: 3px solid rgba(100, 100, 100, 210);
                border-radius: 22px;
                font-family: '{self.pixel_font_family}';
                font-size: 16px;
            }}
            QPushButton:hover {{
                color: #D0D0D0;
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    fx:0.35, fy:0.35,
                    stop:0 rgba(240, 240, 240, 255),
                    stop:0.5 rgba(200, 200, 200, 255),
                    stop:0.85 rgba(160, 160, 160, 245),
                    stop:1 rgba(120, 120, 120, 235));
                border-top: 4px solid rgba(255, 255, 255, 250);
                border-left: 3px solid rgba(240, 240, 240, 240);
            }}
            QPushButton:pressed {{
                color: #808080;
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                    fx:0.5, fy:0.5,
                    stop:0 rgba(160, 160, 160, 245),
                    stop:0.5 rgba(120, 120, 120, 245),
                    stop:0.85 rgba(90, 90, 90, 235),
                    stop:1 rgba(60, 60, 60, 225));
                border-top: 2px solid rgba(80, 80, 80, 220);
                border-left: 2px solid rgba(100, 100, 100, 210);
                border-bottom: 3px solid rgba(200, 200, 200, 220);
                border-right: 3px solid rgba(180, 180, 180, 210);
            }}
        """
    
    def on_keystroke(self, key_text, key_code):
        """Handle keystroke event for visualization"""
        # Update active keystroke
        self.active_keystroke = key_text
        self.keystroke_timer = 0
        self.keystroke_fade = 255
        
        # Add to history
        self.key_history.append(key_text)
        
        # Update statistics
        self.total_keystrokes += 1
        current_time = datetime.now()
        self.keystroke_times.append(current_time)
        
        # Calculate typing speed (CPM - Characters Per Minute)
        if len(self.keystroke_times) >= 2:
            time_span = (self.keystroke_times[-1] - self.keystroke_times[0]).total_seconds()
            if time_span > 0:
                self.typing_speed = int((len(self.keystroke_times) / time_span) * 60)
        
        # Update stats display
        self.stats_label.setText(f"KEYS: {self.total_keystrokes} | SPEED: {self.typing_speed} CPM")
        
        # Create particle effect
        for _ in range(3):
            particle = {
                'x': 125 + random.randint(-20, 20),
                'y': 145 + random.randint(-15, 15),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-2, -0.5),
                'life': 30,
                'color': random.choice([
                    QColor(0, 255, 255),
                    QColor(255, 0, 255),
                    QColor(255, 255, 0),
                    QColor(0, 255, 0)
                ])
            }
            self.keystroke_particles.append(particle)
        
        # Input pulse effect
        self.input_pulse = 15
        
        # Make mascot react
        if self.total_keystrokes % 10 == 0:
            self.set_mood("happy")
            QTimer.singleShot(500, lambda: self.set_mood("idle"))
        
    def setup_animations(self):
        """Setup animations"""
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.animate)
        self.anim_timer.start(50)
        self.blink_counter = 0
        self.frame_count = 0
        
    def animate(self):
        """Main animation loop"""
        self.frame_count += 1
        self.global_mouse_pos = QCursor.pos()
        
        # Blink animation
        self.blink_counter += 1
        if self.blink_counter > random.randint(60, 100):
            self.is_blinking = True
            self.blink_timer = 0
            self.blink_counter = 0
        
        if self.is_blinking:
            self.blink_timer += 1
            if self.blink_timer > 3:
                self.is_blinking = False
        
        # Keystroke fade animation
        if self.keystroke_timer < 60:
            self.keystroke_timer += 1
            self.keystroke_fade = max(0, 255 - (self.keystroke_timer * 4))
        
        # Update particles
        for particle in self.keystroke_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.keystroke_particles.remove(particle)
        
        # Input pulse decay
        if self.input_pulse > 0:
            self.input_pulse -= 1
        
        self.update()
        
    def paintEvent(self, event):
        """Custom paint event"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        self.draw_metallic_body(painter)
        self.draw_crt_screen(painter)
        self.draw_mascot(painter)
        self.draw_keystroke_particles(painter)
        self.draw_keystroke_display(painter)
        self.draw_key_history(painter)
        self.draw_scanlines(painter)
        self.draw_chrome_accents(painter)
        
    def draw_keystroke_particles(self, painter):
        """Draw particle effects from keystrokes"""
        painter.setPen(Qt.PenStyle.NoPen)
        for particle in self.keystroke_particles:
            alpha = int(255 * (particle['life'] / 30))
            color = QColor(particle['color'])
            color.setAlpha(alpha)
            
            # Glow
            glow = QRadialGradient(particle['x'], particle['y'], 8)
            glow_color = QColor(color)
            glow_color.setAlpha(alpha // 2)
            glow.setColorAt(0, glow_color)
            glow_color.setAlpha(0)
            glow.setColorAt(1, glow_color)
            painter.setBrush(glow)
            painter.drawEllipse(QPoint(int(particle['x']), int(particle['y'])), 8, 8)
            
            # Particle
            painter.setBrush(color)
            painter.drawEllipse(QPoint(int(particle['x']), int(particle['y'])), 3, 3)
    
    def draw_keystroke_display(self, painter):
        """Draw current keystroke in large display"""
        if self.active_keystroke and self.keystroke_fade > 0:
            # Display position (center of screen)
            x = 125
            y = 80
            
            # Glow effect
            glow = QRadialGradient(x, y, 50)
            glow.setColorAt(0, QColor(255, 255, 0, self.keystroke_fade))
            glow.setColorAt(1, QColor(255, 255, 0, 0))
            painter.setBrush(glow)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPoint(x, y), 50, 50)
            
            # Key text
            painter.setPen(QColor(255, 255, 0, self.keystroke_fade))
            painter.setFont(QFont(self.pixel_font_family, 32))
            
            # Get text bounding box
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.active_keystroke)
            text_height = fm.height()
            
            # Draw centered
            painter.drawText(int(x - text_width/2), int(y + text_height/3), self.active_keystroke)
    
    def draw_key_history(self, painter):
        """Draw keystroke history at bottom of screen"""
        if not self.key_history:
            return
        
        # Draw history bar
        painter.setPen(QPen(QColor(0, 200, 255, 150), 1))
        painter.setBrush(QColor(0, 40, 80, 180))
        history_rect = QRect(25, 220, 190, 22)
        painter.drawRoundedRect(history_rect, 4, 4)
        
        # Draw keys
        painter.setFont(QFont(self.pixel_font_family, 8))
        x_offset = 30
        for i, key in enumerate(list(self.key_history)):
            # Fade older keys
            alpha = 100 + int(155 * (i / len(self.key_history)))
            painter.setPen(QColor(0, 255, 255, alpha))
            painter.drawText(x_offset, 236, key)
            x_offset += 18
    
    def draw_metallic_body(self, painter):
        """Draw metallic aluminum body"""
        width = self.width()
        height = self.height()
        
        body_gradient = QLinearGradient(0, 0, 0, height)
        body_gradient.setColorAt(0, QColor(180, 190, 200, 250))
        body_gradient.setColorAt(0.5, QColor(220, 230, 240, 250))
        body_gradient.setColorAt(1, QColor(160, 170, 180, 250))
        painter.setBrush(body_gradient)
        painter.setPen(QPen(QColor(100, 110, 120), 3))
        painter.drawRoundedRect(5, 5, width - 10, height - 10, 12, 12)
        
        highlight = QLinearGradient(0, 5, 0, 30)
        highlight.setColorAt(0, QColor(255, 255, 255, 150))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(highlight)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(8, 8, width - 16, 25, 10, 10)
        
        # Brand badge
        painter.setPen(QColor(70, 75, 80))
        painter.setFont(QFont(self.pixel_font_family, 9))
        painter.drawText(QRect(15, 11, 150, 14), 
                        Qt.AlignmentFlag.AlignLeft, "CRT BUDDY v6.0")
        
        # Power LED
        led_x = width - 25
        led_y = 18
        led_glow = QRadialGradient(led_x, led_y, 5)
        led_color = QColor(0, 255, 200, 180 + int(75 * math.sin(self.frame_count * 0.15)))
        led_glow.setColorAt(0, led_color)
        led_glow.setColorAt(1, QColor(0, 255, 200, 0))
        painter.setBrush(led_glow)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(led_x, led_y), 5, 5)
        painter.setBrush(QColor(0, 255, 200))
        painter.drawEllipse(QPoint(led_x, led_y), 2, 2)
        
    def draw_crt_screen(self, painter):
        """Draw CRT screen on left side"""
        # Screen bezel
        bezel_rect = QRect(15, 35, 230, 260)
        bezel_gradient = QLinearGradient(15, 35, 15, 295)
        bezel_gradient.setColorAt(0, QColor(20, 25, 30))
        bezel_gradient.setColorAt(1, QColor(10, 15, 20))
        painter.setBrush(bezel_gradient)
        painter.setPen(QPen(QColor(5, 10, 15), 2))
        painter.drawRoundedRect(bezel_rect, 8, 8)
        
        # CRT screen with input pulse
        screen_rect = QRect(20, 40, 220, 250)
        screen_gradient = QRadialGradient(130, 165, 140)
        
        # Pulse effect when typing
        pulse_brightness = self.input_pulse * 2
        screen_gradient.setColorAt(0, QColor(0, 40 + pulse_brightness, 80 + pulse_brightness, 240))
        screen_gradient.setColorAt(0.7, QColor(0, 30 + pulse_brightness//2, 60 + pulse_brightness//2, 250))
        screen_gradient.setColorAt(1, QColor(0, 20, 40, 255))
        painter.setBrush(screen_gradient)
        painter.setPen(QPen(QColor(0, 100 + pulse_brightness, 200 + pulse_brightness), 2))
        painter.drawRoundedRect(screen_rect, 6, 6)
        
        # Screen reflection
        reflection = QLinearGradient(20, 40, 20, 90)
        reflection.setColorAt(0, QColor(255, 255, 255, 50))
        reflection.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(reflection)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(22, 42, 216, 50, 5, 5)
        
    def draw_mascot(self, painter):
        """Draw mascot with reactions to input"""
        mascot_x = 125
        mascot_y = 165
        
        window_pos = self.mapToGlobal(QPoint(0, 0))
        mascot_screen_x = window_pos.x() + mascot_x
        mascot_screen_y = window_pos.y() + mascot_y
        
        dx = self.global_mouse_pos.x() - mascot_screen_x
        dy = self.global_mouse_pos.y() - mascot_screen_y
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > 0:
            eye_offset_x = (dx / distance) * 5
            eye_offset_y = (dy / distance) * 5
        else:
            eye_offset_x = 0
            eye_offset_y = 0
        
        # Head glow
        head_glow = QRadialGradient(mascot_x, mascot_y, 35)
        if self.current_mood == "happy":
            head_glow.setColorAt(0, QColor(0, 255, 150, 220))
            head_glow.setColorAt(1, QColor(0, 200, 100, 0))
        else:
            head_glow.setColorAt(0, QColor(0, 150, 255, 200))
            head_glow.setColorAt(1, QColor(0, 100, 200, 0))
        painter.setBrush(head_glow)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(mascot_x, mascot_y), 35, 35)
        
        # Head
        painter.setBrush(QColor(0, 100, 200, 220))
        painter.setPen(QPen(QColor(0, 150, 255), 2))
        painter.drawRoundedRect(mascot_x - 28, mascot_y - 22, 56, 44, 10, 10)
        
        # Inner screen
        painter.setBrush(QColor(0, 40, 80, 240))
        painter.setPen(QPen(QColor(0, 200, 255), 1))
        painter.drawRoundedRect(mascot_x - 23, mascot_y - 17, 46, 34, 6, 6)
        
        # Eyes
        if not self.is_blinking:
            eye_color = QColor(0, 255, 255)
            
            if self.current_mood == "happy":
                # Star eyes
                for offset_x in [-10, 10]:
                    eye_x = mascot_x + offset_x + eye_offset_x
                    eye_y = mascot_y - 5 + eye_offset_y
                    
                    eye_glow = QRadialGradient(eye_x, eye_y, 12)
                    eye_glow.setColorAt(0, QColor(0, 255, 255, 220))
                    eye_glow.setColorAt(1, QColor(0, 255, 255, 0))
                    painter.setBrush(eye_glow)
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawEllipse(QPoint(int(eye_x), int(eye_y)), 12, 12)
                    
                    painter.setPen(QPen(eye_color, 2))
                    for angle in range(0, 360, 72):
                        rad = math.radians(angle)
                        x1 = eye_x + math.cos(rad) * 3
                        y1 = eye_y + math.sin(rad) * 3
                        x2 = eye_x + math.cos(rad) * 6
                        y2 = eye_y + math.sin(rad) * 6
                        painter.drawLine(int(x1), int(y1), int(x2), int(y2))
            else:
                # Normal eyes
                for offset_x in [-10, 10]:
                    eye_x = mascot_x + offset_x + eye_offset_x
                    eye_y = mascot_y - 5 + eye_offset_y
                    
                    eye_glow = QRadialGradient(eye_x, eye_y, 10)
                    eye_glow.setColorAt(0, QColor(0, 255, 255, 200))
                    eye_glow.setColorAt(1, QColor(0, 255, 255, 0))
                    painter.setBrush(eye_glow)
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawEllipse(QPoint(int(eye_x), int(eye_y)), 10, 10)
                    
                    painter.setBrush(eye_color)
                    painter.drawEllipse(QPoint(int(eye_x), int(eye_y)), 5, 6)
                    
                    painter.setBrush(QColor(0, 100, 200))
                    painter.drawEllipse(QPoint(int(eye_x), int(eye_y)), 2, 3)
        else:
            painter.setPen(QPen(QColor(0, 255, 255), 2))
            painter.drawLine(mascot_x - 15, mascot_y - 4, mascot_x - 5, mascot_y - 4)
            painter.drawLine(mascot_x + 5, mascot_y - 4, mascot_x + 15, mascot_y - 4)
        
        # Mouth
        painter.setPen(QPen(QColor(0, 255, 255), 2))
        if self.current_mood == "happy":
            path = QPainterPath()
            path.moveTo(mascot_x - 12, mascot_y + 6)
            path.quadTo(mascot_x, mascot_y + 16, mascot_x + 12, mascot_y + 6)
            painter.drawPath(path)
            painter.drawLine(mascot_x - 18, mascot_y + 2, mascot_x - 14, mascot_y + 2)
            painter.drawLine(mascot_x + 14, mascot_y + 2, mascot_x + 18, mascot_y + 2)
        else:
            painter.drawLine(mascot_x - 10, mascot_y + 10, mascot_x + 10, mascot_y + 10)
        
        # Antenna
        painter.setPen(QPen(QColor(0, 200, 255), 2))
        painter.drawLine(mascot_x, mascot_y - 22, mascot_x, mascot_y - 32)
        
        # Antenna ball
        ball_glow = QRadialGradient(mascot_x, mascot_y - 37, 7)
        ball_color = QColor(255, 0, 255, 200 + int(55 * math.sin(self.frame_count * 0.1)))
        ball_glow.setColorAt(0, ball_color)
        ball_glow.setColorAt(1, QColor(ball_color.red(), ball_color.green(), ball_color.blue(), 0))
        painter.setBrush(ball_glow)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(mascot_x, mascot_y - 37), 7, 7)
        painter.setBrush(ball_color)
        painter.drawEllipse(QPoint(mascot_x, mascot_y - 37), 4, 4)
        
    def draw_scanlines(self, painter):
        """Draw CRT scanlines"""
        painter.setPen(QPen(QColor(0, 255, 255, 15), 1))
        for y in range(40, 290, 3):
            painter.drawLine(20, y, 240, y)
        
        scanline_y = 40 + (self.frame_count * 2) % 250
        gradient = QLinearGradient(0, scanline_y - 15, 0, scanline_y + 15)
        gradient.setColorAt(0, QColor(0, 255, 255, 0))
        gradient.setColorAt(0.5, QColor(0, 255, 255, 60))
        gradient.setColorAt(1, QColor(0, 255, 255, 0))
        painter.fillRect(20, scanline_y - 15, 220, 30, gradient)
        
    def draw_chrome_accents(self, painter):
        """Draw chrome accents"""
        width = self.width()
        height = self.height()
        
        chrome_gradient = QLinearGradient(0, height - 25, 0, height - 8)
        chrome_gradient.setColorAt(0, QColor(150, 160, 170))
        chrome_gradient.setColorAt(0.5, QColor(200, 210, 220))
        chrome_gradient.setColorAt(1, QColor(150, 160, 170))
        painter.setBrush(chrome_gradient)
        painter.setPen(QPen(QColor(100, 110, 120), 1))
        painter.drawRoundedRect(12, height - 23, width - 24, 14, 4, 4)
        
        painter.setPen(QPen(QColor(80, 90, 100), 1))
        for i in range(10):
            x = 20 + i * 12
            y = height - 17
            painter.drawLine(x, y, x + 6, y)
            painter.drawLine(x, y + 4, x + 6, y + 4)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                self.image_dropped.emit(file_path)
    
    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp)")
        if file_path:
            self.image_dropped.emit(file_path)
    
    def set_status(self, text):
        self.status_label.setText(text)
    
    def set_mood(self, mood):
        self.current_mood = mood
    
    def get_input_text(self):
        return self.input_text.toPlainText()
    
    def clear_input(self):
        self.input_text.clear()


class KeystrokeTextEdit(QTextEdit):
    """Custom QTextEdit that tracks keystrokes"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        
    def keyPressEvent(self, event: QKeyEvent):
        """Override to track keystrokes"""
        # Get key text
        key = event.key()
        text = event.text()
        
        # Format special keys
        if key == Qt.Key.Key_Space:
            display_text = "SPACE"
        elif key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            display_text = "ENTER"
        elif key == Qt.Key.Key_Backspace:
            display_text = "⌫"
        elif key == Qt.Key.Key_Tab:
            display_text = "TAB"
        elif key == Qt.Key.Key_Shift:
            display_text = "SHIFT"
        elif key == Qt.Key.Key_Control:
            display_text = "CTRL"
        elif key == Qt.Key.Key_Alt:
            display_text = "ALT"
        elif text and text.isprintable():
            display_text = text.upper()
        else:
            display_text = "·"
        
        # Notify parent window
        self.parent_window.on_keystroke(display_text, key)
        
        # Call original handler
        super().keyPressEvent(event)
