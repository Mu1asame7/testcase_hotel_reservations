import os
from time import sleep
from PIL import Image

from src.tasks.celery_app import celery_instance


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