import shutil
from pathlib import Path


CATEGORIES = {
    "Images": [".jpg", ".png", ".jpeg", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Music": [".mp3", ".wav"],
    "Videos": [".mp4", ".mkv"],
    "Code": [".py", ".js", ".java"],
}


def get_category(file: Path):
    for category, extensions in CATEGORIES.items():
        if file.suffix.lower() in extensions:
            return category
    return "Others"


def move_file_safely(file: Path, destination: Path):
    """
    Prevent overwriting files by renaming duplicates.
    example:
    photo.jpg -> photo_1.jpg
    """

    new_file = destination / file.name
    counter = 1

    while new_file.exists():
        new_file = destination / f"{file.stem}_{counter}{file.suffix}"
        counter += 1

    shutil.move(str(file), str(new_file))


def organize_folder(folder_path):

    source = Path(folder_path.strip('"'))

    if not source.exists() or not source.is_dir():
        print("Invalid folder path.")
        return

    files = [f for f in source.iterdir() if f.is_file()]

    if not files:
        print("⚠️ Folder is empty.")
        return

    moved = 0

    for file in files:

        try:
            category = get_category(file)

            category_folder = source / category
            category_folder.mkdir(exist_ok=True)

            print(f"Moving: {file.name} → {category}/")

            move_file_safely(file, category_folder)

            moved += 1

        except Exception as e:
            print(f"Error moving {file.name}: {e}")

    print(f"\n Finished! {moved} files organized.")


if __name__ == "__main__":

    folder = input("Enter folder path: ")
    organize_folder(folder)
