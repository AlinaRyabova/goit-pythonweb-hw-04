import asyncio
from pathlib import Path
import argparse
import logging
import shutil

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def copy_file(file: Path, output_folder: Path):
    """Асинхронне копіювання файлу у відповідну папку."""
    try:
        extension = file.suffix[1:].lower() or "unknown"
        target_folder = output_folder / extension
        target_folder.mkdir(parents=True, exist_ok=True)
        await asyncio.to_thread(shutil.copy2, file, target_folder / file.name)
        logging.info(f"Скопійовано файл: {file} -> {target_folder / file.name}")
    except Exception as e:
        logging.error(f"Помилка копіювання {file}: {e}")

async def read_folder(source_folder: Path, output_folder: Path):
    """Рекурсивне читання папки та обробка файлів."""
    try:
        for item in await asyncio.to_thread(lambda: list(source_folder.iterdir())):
            if item.is_file():
                await copy_file(item, output_folder)
            elif item.is_dir():
                await read_folder(item, output_folder)
    except Exception as e:
        logging.error(f"Помилка обробки папки {source_folder}: {e}")

async def main(source: str, output: str):
    """Головна функція."""
    source_path = Path(source)
    output_path = Path(output)

    if not source_path.exists() or not source_path.is_dir():
        logging.error(f"Вихідна папка {source} не існує або це не директорія.")
        return

    output_path.mkdir(parents=True, exist_ok=True)
    logging.info(f"Початок сортування файлів з {source_path} до {output_path}")
    await read_folder(source_path, output_path)
    logging.info("Сортування завершено!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Асинхронний сортувальник файлів")
    parser.add_argument("--source", required=True, help="Шлях до вихідної папки")
    parser.add_argument("--output", required=True, help="Шлях до цільової папки")
    args = parser.parse_args()

    asyncio.run(main(args.source, args.output))
