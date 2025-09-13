# settings.py

# Konfigurationseinstellungen für das ColorChecker-Projekt

class Config:
    # Allgemeine Einstellungen
    DEBUG = False
    TESTING = False

    # Kamera Einstellungen
    CAMERA_RESOLUTION = (640, 480)  # Standardauflösung
    FRAME_RATE = 30  # Standard Bildrate

    # OLED Einstellungen
    OLED_UPDATE_INTERVAL = 1  # Update-Intervall in Sekunden

    # LED Einstellungen
    LED_COUNT = 10  # Anzahl der LEDs im System

    # Datenbank Einstellungen
    JSON_DATA_PATH = 'data/color_references.json'  # Pfad zur JSON-Datenbank

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass

# Konfigurationen können je nach Umgebung ausgewählt werden
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}