import random
import uuid
from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from .constants import (
    AVATAR_COLORS,
    AVATAR_FONT_SIZE,
    AVATAR_SIZE,
    AVATAR_TEXT_ANCHOR,
    AVATAR_TEXT_COLOR,
)

AVATAR_CENTER = (AVATAR_SIZE // 2, AVATAR_SIZE // 2)
AVATAR_FONT = (
    settings.BASE_DIR / "static/fonts/Neue_Haas_Grotesk_Display_Pro_75_Bold.otf"
)


def generate_avatar(name):
    image = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), random.choice(AVATAR_COLORS))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(AVATAR_FONT), AVATAR_FONT_SIZE)
    draw.text(
        AVATAR_CENTER,
        name[:1].upper(),
        fill=AVATAR_TEXT_COLOR,
        font=font,
        anchor=AVATAR_TEXT_ANCHOR,
    )
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name=f"{uuid.uuid4().hex}.png")
