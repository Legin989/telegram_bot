from pathlib import Path

RESOURCE_DIR = Path(__file__).resolve().parent /"resources"


def image_path(filename):
    path = RESOURCE_DIR / "images" / f"{filename}.jpg"

    if not path.exists():
        raise FileNotFoundError(f"{path} такого файлу не існує")
    return path


def load_message(filename):
    path =  RESOURCE_DIR / "messages" / f"{filename}.txt"


    if not path.exists():
        raise FileNotFoundError(f"{path} такого файлу не існує")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_prompt(filename):
    path =  RESOURCE_DIR / "prompts" / f"{filename}.txt"

    if not path.exists():
        raise FileNotFoundError(f"{path} такого промту не існує")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()