import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from PIL import Image
from io import BytesIO

# ========== CONFIG ==========
TOKEN = "7024911557:AAG0D2g11jZa5JK4NsuyTVh9Xl9_ibmwYok"
LOGO_PATH = "logo.png"
MARGIN = 50
# ============================

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("📸 Send a photo. Logo will be added bottom-right.")


@dp.message(F.photo)
async def add_logo(message: types.Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)

    # ⬇️ Download photo directly to RAM
    photo_buffer = BytesIO()
    await bot.download_file(file.file_path, photo_buffer)
    photo_buffer.seek(0)

    # 🖼 Open images from memory
    base = Image.open(photo_buffer).convert("RGBA")
    logo = Image.open(LOGO_PATH).convert("RGBA")

    bw, bh = base.size
    lw, lh = logo.size

    # 🔧 Resize logo (20% of width)
    max_w = int(bw * 0.2)
    if lw > max_w:
        ratio = max_w / lw
        logo = logo.resize(
            (int(lw * ratio), int(lh * ratio)),
            Image.Resampling.LANCZOS
        )
        lw, lh = logo.size

    # 📍 Bottom-right position
    x = bw - lw - MARGIN
    y = bh - lh - MARGIN

    base.paste(logo, (x, y), logo)

    # 📤 Save result to RAM
    result = BytesIO()
    base.convert("RGB").save(result, format="JPEG", quality=95)
    result.seek(0)

    await message.answer_photo(
        types.BufferedInputFile(
            result.read(),
            filename="result.jpg"
        )
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
