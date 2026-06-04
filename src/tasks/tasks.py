import asyncio
import os
from time import sleep
from PIL import Image

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def test_tasks():
    sleep(5)
    print("test_tasks")


@celery_instance.task
def resize_image(image_path: str):
    sizes = [200, 500, 1000]
    output_folder = "src/static/images"
    img = Image.open(image_path)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        # Вычисляем новую высоту с сохранением пропорций
        ratio = size / img.width
        new_height = int(img.height * ratio)

        # Изменяем размер
        resized_img = img.resize((size, new_height), Image.Resampling.LANCZOS)

        # Формируем имя файла: имя_размер.jpg
        new_filename = f"{name}_{size}.jpg"
        new_path = os.path.join(output_folder, new_filename)

        # Сохраняем
        resized_img.save(new_path, 'JPEG', quality=85, optimize=True)
        print(f"✅ Сохранено: {new_path} ({size}x{new_height})")


async def get_bookings_today_halper():
    print("Начало")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@celery_instance.task(name="booking_today_checkin")
def booking_today_checkin():
    asyncio.run(get_bookings_today_halper())
