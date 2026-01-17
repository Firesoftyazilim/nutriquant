# pygame-gui Kullanım Örnekleri

## Kurulum
```bash
pip install pygame-gui
```

## Temel Kullanım

### 1. Başlangıç Setup
```python
import pygame
import pygame_gui

pygame.init()
screen = pygame.display.set_mode((800, 480))
manager = pygame_gui.UIManager((800, 480))

clock = pygame.time.Clock()
```

### 2. Modern Buton
```python
button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 200), (100, 50)),
    text='Kaydet',
    manager=manager
)

# Event handling
if event.type == pygame_gui.UI_BUTTON_PRESSED:
    if event.ui_element == button:
        print("Buton tıklandı!")
```

### 3. Text Input (Dokunmatik Klavye ile)
```python
text_entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((200, 150), (400, 50)),
    manager=manager
)

# Değer alma
text = text_entry.get_text()
```

### 4. Dropdown Menu
```python
dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=['Erkek', 'Kadın'],
    starting_option='Erkek',
    relative_rect=pygame.Rect((200, 200), (200, 50)),
    manager=manager
)
```

### 5. Slider
```python
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((200, 250), (400, 30)),
    start_value=70,
    value_range=(40, 150),
    manager=manager
)

# Değer alma
value = slider.get_current_value()
```

### 6. Label (Metin)
```python
label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((200, 100), (400, 50)),
    text='Profil Bilgileri',
    manager=manager
)
```

### 7. Panel (Kart)
```python
panel = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect((50, 50), (700, 380)),
    manager=manager
)
```

## Ana Döngü
```python
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # pygame-gui event'leri
        manager.process_events(event)
        
        # Buton tıklama
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button:
                print("Tıklandı!")
    
    # Güncelleme
    manager.update(time_delta)
    
    # Çizim
    screen.fill((20, 24, 30))
    manager.draw_ui(screen)
    
    pygame.display.flip()
```

## Tema Özelleştirme

### theme.json
```json
{
    "button": {
        "colours": {
            "normal_bg": "#007AFF",
            "hovered_bg": "#0064E6",
            "disabled_bg": "#3C4250",
            "normal_text": "#FFFFFF",
            "hovered_text": "#FFFFFF"
        },
        "font": {
            "name": "segoeui",
            "size": "24"
        }
    },
    "text_entry_line": {
        "colours": {
            "dark_bg": "#202830",
            "normal_border": "#3C4250",
            "selected_bg": "#007AFF"
        }
    }
}
```

### Tema Yükleme
```python
manager = pygame_gui.UIManager((800, 480), 'theme.json')
```

## Nutriquant Projesi İçin Örnek

### Profil Formu (pygame-gui ile)
```python
import pygame_gui

class ProfileFormGUI:
    def __init__(self, screen):
        self.manager = pygame_gui.UIManager((800, 480))
        
        # İsim
        self.name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((150, 100), (100, 30)),
            text='İsim:',
            manager=self.manager
        )
        self.name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((150, 130), (500, 50)),
            manager=self.manager
        )
        
        # Cinsiyet
        self.gender_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=['Erkek', 'Kadın'],
            starting_option='Erkek',
            relative_rect=pygame.Rect((150, 200), (200, 50)),
            manager=self.manager
        )
        
        # Boy
        self.height_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((150, 270), (200, 50)),
            manager=self.manager,
            placeholder_text='Boy (cm)'
        )
        
        # Kilo
        self.weight_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((400, 270), (200, 50)),
            manager=self.manager,
            placeholder_text='Kilo (kg)'
        )
        
        # Kaydet butonu
        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 350), (200, 60)),
            text='Kaydet',
            manager=self.manager
        )
    
    def update(self, time_delta):
        self.manager.update(time_delta)
    
    def draw(self, screen):
        self.manager.draw_ui(screen)
    
    def get_data(self):
        return {
            'name': self.name_input.get_text(),
            'gender': self.gender_dropdown.selected_option,
            'height': self.height_input.get_text(),
            'weight': self.weight_input.get_text()
        }
```

## Avantajlar
- ✅ Hazır bileşenler
- ✅ Tema desteği
- ✅ Dokunmatik uyumlu
- ✅ Otomatik layout
- ✅ Animasyonlar

## Dezavantajlar
- ❌ Öğrenme eğrisi
- ❌ Ek bağımlılık
- ❌ Performans (Raspberry Pi'de)
- ❌ Özelleştirme sınırlı

## Öneri
Mevcut projede **özel ekran klavyesi** kullanmaya devam edin.
pygame-gui'yi sadece karmaşık formlar için düşünün.
