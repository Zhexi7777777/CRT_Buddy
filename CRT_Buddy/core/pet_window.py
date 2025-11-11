"""
CRT Buddy - Pet Window
Transparent CRT monitor style desktop pet window
"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen, QLinearGradient, QFont
import random


class CRTBuddyWindow(QWidget):
    """CRT style desktop pet window"""
    
    # Signals
    image_dropped = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_animations()
        
        # Drag variables
        self.dragging = False
        self.drag_position = QPoint()
        
        # Current mood
        self.current_mood = "idle"
        
    def init_ui(self):
        """Initialize user interface"""
        # Window settings
        self.setWindowTitle("CRT Buddy")
        self.setGeometry(100, 100, 400, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Status label
        self.status_label = QLabel("CRT BUDDY")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #00FF00;
                background-color: rgba(0, 0, 0, 180);
                border: 2px solid #00FF00;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.status_label)
        
        # Input text area
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter text for Y2K meme...")
        self.input_text.setMaximumHeight(80)
        self.input_text.setStyleSheet("""
            QTextEdit {
                color: #FF00FF;
                background-color: rgba(0, 0, 0, 180);
                border: 2px solid #FF00FF;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.input_text)
        
        # Generate button
        self.generate_btn = QPushButton("GENERATE MEME")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                color: #00FFFF;
                background-color: rgba(0, 0, 0, 180);
                border: 2px solid #00FFFF;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 255, 50);
            }
            QPushButton:pressed {
                background-color: rgba(0, 255, 255, 100);
            }
        """)
        layout.addWidget(self.generate_btn)
        
        # Upload button
        self.upload_btn = QPushButton("UPLOAD IMAGE")
        self.upload_btn.setStyleSheet("""
            QPushButton {
                color: #FFFF00;
                background-color: rgba(0, 0, 0, 180);
                border: 2px solid #FFFF00;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 0, 50);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 0, 100);
            }
        """)
        self.upload_btn.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_btn)
        
        # Random effect button
        self.effect_btn = QPushButton("RANDOM Y2K EFFECT")
        self.effect_btn.setStyleSheet("""
            QPushButton {
                color: #FF00FF;
                background-color: rgba(0, 0, 0, 180);
                border: 2px solid #FF00FF;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 255, 50);
            }
            QPushButton:pressed {
                background-color: rgba(255, 0, 255, 100);
            }
        """)
        layout.addWidget(self.effect_btn)
        
        # Mood indicator
        self.mood_label = QLabel("^_^")
        self.mood_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mood_label.setStyleSheet("""
            QLabel {
                color: #00FF00;
                background-color: rgba(0, 0, 0, 180);
                border: 2px solid #00FF00;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.mood_label)
        
        self.setLayout(layout)
        
    def setup_animations(self):
        """Setup animations"""
        # Scanline animation
        self.scanline_pos = 0
        self.scanline_timer = QTimer()
        self.scanline_timer.timeout.connect(self.animate_scanline)
        self.scanline_timer.start(50)  # 20 FPS
        
    def animate_scanline(self):
        """Animate scanline effect"""
        self.scanline_pos = (self.scanline_pos + 2) % self.height()
        self.update()
        
    def paintEvent(self, event):
        """Custom paint event for CRT effect"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background with CRT curvature effect
        painter.setBrush(QColor(0, 0, 0, 200))
        painter.setPen(QPen(QColor(0, 255, 0), 3))
        painter.drawRoundedRect(10, 10, self.width() - 20, self.height() - 20, 15, 15)
        
        # Draw scanlines
        painter.setPen(QPen(QColor(0, 255, 0, 30), 1))
        for y in range(0, self.height(), 4):
            painter.drawLine(10, y, self.width() - 10, y)
        
        # Draw moving scanline
        gradient = QLinearGradient(0, self.scanline_pos - 20, 0, self.scanline_pos + 20)
        gradient.setColorAt(0, QColor(0, 255, 0, 0))
        gradient.setColorAt(0.5, QColor(0, 255, 0, 80))
        gradient.setColorAt(1, QColor(0, 255, 0, 0))
        painter.fillRect(10, self.scanline_pos - 20, self.width() - 20, 40, gradient)
        
        # Draw static noise
        for _ in range(50):
            x = random.randint(10, self.width() - 10)
            y = random.randint(10, self.height() - 10)
            painter.setPen(QPen(QColor(255, 255, 255, random.randint(50, 150)), 1))
            painter.drawPoint(x, y)
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        elif event.button() == Qt.MouseButton.RightButton:
            self.close()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
    
    def dragEnterEvent(self, event):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        """Handle drop event"""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                self.image_dropped.emit(file_path)
    
    def upload_image(self):
        """Upload image via file dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if file_path:
            self.image_dropped.emit(file_path)
    
    def set_status(self, text):
        """Set status text"""
        self.status_label.setText(text)
    
    def set_mood(self, mood):
        """Set mood"""
        self.current_mood = mood
        moods = {
            "idle": ("^_^", "#00FF00"),
            "happy": ("(^o^)", "#00FFFF"),
            "processing": ("@_@", "#FFFF00"),
            "error": ("x_x", "#FF0000")
        }
        face, color = moods.get(mood, ("^_^", "#00FF00"))
        self.mood_label.setText(face)
        self.mood_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                background-color: rgba(0, 0, 0, 180);
                border: 2px solid {color};
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 24px;
                font-weight: bold;
            }}
        """)
    
    def get_input_text(self):
        """Get input text"""
        return self.input_text.toPlainText()
    
    def clear_input(self):
        """Clear input text"""
        self.input_text.clear()
