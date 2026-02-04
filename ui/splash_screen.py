"""
Splash screen for the database application.
"""
import sys
from PyQt6.QtWidgets import QSplashScreen, QApplication, QProgressBar
from PyQt6.QtGui import QPixmap, QFont, QPainter, QColor
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QBrush


class SplashScreen(QSplashScreen):
    def __init__(self):
        # Create a pixmap for the splash screen
        pixmap = QPixmap(600, 400)
        pixmap.fill(QColor(43, 43, 43))  # Dark grey background

        # Draw content on the pixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw title with rainbow gradient effect
        font = QFont("Arial", 24, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor(240, 240, 240))  # Light grey/white text
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
                        "Database Management System")

        # Draw subtitle
        font = QFont("Arial", 14)
        painter.setFont(font)
        painter.setPen(QColor(176, 176, 176))  # Light grey text
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter,
                        "Loading Application...")

        # Draw footer
        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.setPen(QColor(128, 128, 128))  # Medium grey
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
                        "© 2025 Database Management System. All rights reserved.")

        # Draw progress bar area with rainbow accent
        progress_rect = QRect(50, pixmap.height() - 60, pixmap.width() - 100, 20)
        painter.setPen(QColor(64, 64, 64))  # Dark grey border
        painter.drawRect(progress_rect)

        painter.end()

        super().__init__(pixmap, Qt.WindowType.WindowStaysOnTopHint)

        # Create animated progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(50, 340, 500, 20)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(
            "QProgressBar {"
            "    border: 1px solid #404040;"
            "    border-radius: 5px;"
            "    background-color: #2b2b2b;"
            "    text-align: center;"
            "    color: white;"
            "    font-weight: bold;"
            "    height: 15px;"
            "}"
            "QProgressBar::chunk {"
            "    background-color: #e74c3c;"  # Start with red
            "    border-radius: 5px;"
            "}"
        )

        # Set the splash screen in the center of the screen
        self.center_on_screen()

        # Animation timer for progress bar - use a faster timer for smoother animation
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_progress)
        self.progress_value = 0
        self.animation_step = 0.3  # Even smaller step for ultra-smooth animation
        self.animation_start_time = None  # For time-based smooth animation
        self.total_animation_duration = 4000  # Total animation time in ms (4 seconds)

    def center_on_screen(self):
        """Center the splash screen on the screen"""
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def update_progress(self):
        """Update the progress bar for animation"""
        import time

        if self.animation_start_time is None:
            self.animation_start_time = time.time()

        # Calculate elapsed time in milliseconds
        elapsed_time = (time.time() - self.animation_start_time) * 1000

        if elapsed_time < self.total_animation_duration:
            # Use a smooth easing function (ease-out) for natural movement
            # Progress from 0 to 1 over the animation duration
            t = elapsed_time / self.total_animation_duration

            # Apply smooth easing function (ease-out cubic): 1 - (1 - t)^3
            eased_progress = 1 - pow(1 - t, 3)

            # Calculate the current progress value (0-100)
            self.progress_value = min(eased_progress * 100, 100)

            self.progress_bar.setValue(int(self.progress_value))

            # Update the progress bar color based on progress percentage
            self.update_progress_color()
        else:
            # Animation complete
            self.progress_value = 100
            self.progress_bar.setValue(100)

            # Final color update
            self.update_progress_color()
            self.animation_timer.stop()

            # Call the finish slot only after progress is complete
            if hasattr(self, 'finish_slot'):
                self.finish_slot()
    
    def update_progress_color(self):
        """Update the progress bar color based on current progress value with ultra-smooth transitions"""
        progress_percent = min(self.progress_value, 100)  # Ensure it's capped at 100

        # Smooth interpolation across the entire range: red(0%) -> orange(25%) -> yellow(50%) -> green(75%)
        # Define color values:
        # Red: #e74c3c (R:231, G:76, B:60)
        # Orange: #e67e22 (R:230, G:126, B:34)
        # Yellow: #f1c40f (R:241, G:196, B:15)
        # Green: #2ecc71 (R:46, G:204, B:113)

        # Determine which phase we're in
        if progress_percent <= 25:
            # Phase 1: Red to Orange (0-25%)
            t = progress_percent / 25.0  # Normalize to 0-1 range
            r = int(231 * (1 - t) + 230 * t)
            g = int(76 * (1 - t) + 126 * t)
            b = int(60 * (1 - t) + 34 * t)
        elif progress_percent <= 50:
            # Phase 2: Orange to Yellow (25-50%)
            t = (progress_percent - 25) / 25.0  # Normalize to 0-1 range
            r = int(230 * (1 - t) + 241 * t)
            g = int(126 * (1 - t) + 196 * t)
            b = int(34 * (1 - t) + 15 * t)
        elif progress_percent <= 75:
            # Phase 3: Yellow to Green (50-75%)
            t = (progress_percent - 50) / 25.0  # Normalize to 0-1 range
            r = int(241 * (1 - t) + 46 * t)
            g = int(196 * (1 - t) + 204 * t)
            b = int(15 * (1 - t) + 113 * t)
        else:
            # Phase 4: Green (75-100%)
            # We can still interpolate in this phase or just hold green
            # Let's hold green for the last 25% or transition to another color if desired
            t = (progress_percent - 75) / 25.0  # Normalize to 0-1 range
            # Hold green (this keeps it green throughout 75-100%)
            r = int(46)
            g = int(204)
            b = int(113)
            # Or we could transition to another color, for now keeping it as green

        color_style = f"#{r:02x}{g:02x}{b:02x}"

        # Update the progress bar style to reflect the smooth color transition
        self.progress_bar.setStyleSheet(
            f"""
            QProgressBar {{
                border: 1px solid #404040;
                border-radius: 5px;
                background-color: #2b2b2b;
                text-align: center;
                color: white;
                font-weight: bold;
                height: 15px;
            }}
            QProgressBar::chunk {{
                background-color: {color_style};
                border-radius: 5px;
            }}
            """
        )

    def show_and_load(self, finish_slot):
        """Show the splash screen and set up a timer to finish loading"""
        self.show()

        # Store the finish slot to call when progress is complete
        self.finish_slot = finish_slot

        # Start the progress animation with an even faster interval for ultra-smooth movement
        self.animation_timer.start(16)  # Update every 16ms (~60 FPS) for ultra-smooth animation