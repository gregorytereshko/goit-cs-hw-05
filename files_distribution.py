import asyncio
import argparse
from pathlib import Path
import shutil
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


async def read_folder(folder_path):
    """Асинхронно читає всі файли у вказаній папці та її підпапках."""
    folder_path = Path(folder_path)
    try:
        for filepath in folder_path.rglob('*'):
            if filepath.is_file():
                yield filepath
    except Exception as e:
        logging.error(f"Помилка при читанні файлів з папки {folder_path}: {e}")


async def copy_file(file_path, output_folder):
    """Асинхронно копіює файл у відповідну підпапку на основі розширення файла."""
    try:
        extension = file_path.suffix[1:]  # Видаляємо крапку з розширення файла
        target_folder = Path(output_folder) / extension
        target_folder.mkdir(parents=True, exist_ok=True)
        target_file = target_folder / file_path.name
        await asyncio.to_thread(shutil.copy, str(file_path), str(target_file))
        logging.info(f"Файл {file_path} скопійовано до {target_file}")
    except Exception as e:
        logging.error(
            f"Помилка при копіюванні файлу {file_path} до {target_folder}: {e}")


async def main(source_folder, output_folder):
    """Головна асинхронна функція для читання та копіювання файлів."""
    async for file_path in read_folder(source_folder):
        await copy_file(file_path, output_folder)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Асинхронне копіювання файлів по папках згідно розширень.")
    parser.add_argument('--source', type=str, required=True,
                        help='Вихідна папка з файлами для копіювання')
    parser.add_argument('--output', type=str, required=True,
                        help='Цільова папка для розподілених файлів')
    args = parser.parse_args()

    asyncio.run(main(args.source, args.output))
