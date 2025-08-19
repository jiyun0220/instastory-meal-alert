from PIL import Image, ImageDraw, ImageFont

from .config import (
    BACKGROUND_IMAGE_PATH, MEAL_STORY_IMAGE_PATH, 
    FONT_BOLD_PATH, FONT_REGULAR_PATH
)

class ImageGenerator:
    def __init__(self):
        self.width = 1080
        self.height = 1920
        self.background = self._load_background()
        self.image = None
        self.draw = None

    def _load_background(self):
        try:
            return Image.open(BACKGROUND_IMAGE_PATH).convert("RGBA").resize((self.width, self.height))
        except FileNotFoundError:
            return Image.new("RGBA", (self.width, self.height), (255, 255, 255, 255))

    def _setup_drawing(self):
        overlay = Image.new("RGBA", self.background.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        draw.rounded_rectangle(
            (80, 150, self.width - 80, self.height - 350),
            radius=12,
            fill=(240, 244, 248, 210)
        )
        self.image = Image.alpha_composite(self.background, overlay)
        self.draw = ImageDraw.Draw(self.image)

    def _get_fonts(self):
        try:
            title_font = ImageFont.truetype(FONT_BOLD_PATH, size=50)
            menu_font = ImageFont.truetype(FONT_REGULAR_PATH, size=40)
        except IOError:
            title_font = ImageFont.load_default()
            menu_font = ImageFont.load_default()
        return title_font, menu_font

    def _draw_meal_section(self, title, menu_text, start_y, title_font, menu_font):
        title_color = "#001f3f"
        text_color = "#333333"
        
        self.draw.text((180, start_y), title, font=title_font, fill=title_color)
        
        menu_items = [item for item in menu_text.split('\n') if item]
        mid_point = (len(menu_items) + 1) // 2
        col1_items = menu_items[:mid_point]
        col2_items = menu_items[mid_point:]
        
        col1_text = "\n".join(col1_items)
        col2_text = "\n".join(col2_items)
        
        self.draw.text((180, start_y + 110), col1_text, font=menu_font, fill=text_color, spacing=25)
        self.draw.text((630, start_y + 110), col2_text, font=menu_font, fill=text_color, spacing=25)
        
        lines_in_col1 = len(col1_items)
        return start_y + 120 + (lines_in_col1 * 65) + 130

    def create(self, breakfast: str, lunch: str, dinner: str) -> str:
        self._setup_drawing()
        title_font, menu_font = self._get_fonts()

        y = 220
        y = self._draw_meal_section("조식", breakfast, y, title_font, menu_font)
        y = self._draw_meal_section("중식", lunch, y, title_font, menu_font)
        self._draw_meal_section("석식", dinner, y, title_font, menu_font)

        self.image.convert("RGB").save(MEAL_STORY_IMAGE_PATH)
        return MEAL_STORY_IMAGE_PATH