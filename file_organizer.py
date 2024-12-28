import asyncio
import shutil
from pathlib import Path
import argparse
import logging

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def process_file(file: Path, output_folder: Path):
    """Асинхронне копіювання файлу до відповідної підпапки."""
    try:
        extension = file.suffix[1:].lower() or "unknown"
        target_folder = output_folder / extension
        target_folder.mkdir(parents=True, exist_ok=True)
        await asyncio.to_thread(shutil.copy2, file, target_folder / file.name)
        logging.info(f"Скопійовано: {file} -> {target_folder / file.name}")
    except Exception as e:
        logging.error(f"Помилка копіювання {file}: {e}")

async def process_folder(source_folder: Path, output_folder: Path):
    """Асинхронне читання папки та обробка файлів."""
    try:
        tasks = []
        for item in await asyncio.to_thread(lambda: list(source_folder.iterdir())):
            if item.is_file():
                tasks.append(process_file(item, output_folder))
            elif item.is_dir():
                tasks.append(process_folder(item, output_folder))
        await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Помилка обробки {source_folder}: {e}")

async def main(source: str, output: str):
    source_path = Path(source)
    output_path = Path(output)
    if not source_path.exists() or not source_path.is_dir():
        logging.error(f"Вихідна папка {source} не існує або це не директорія.")
        return
    output_path.mkdir(parents=True, exist_ok=True)
    await process_folder(source_path, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Асинхронний сортувальник файлів")
    parser.add_argument("--source", required=True, help="Шлях до вихідної папки")
    parser.add_argument("--output", required=True, help="Шлях до цільової папки")
    args = parser.parse_args()

    asyncio.run(main(args.source, args.output))
