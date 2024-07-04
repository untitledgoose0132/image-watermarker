from functools import partial
from multiprocessing import Pool, cpu_count
from os import environ, path
from tkinter.filedialog import askopenfilename, askopenfilenames

from PIL import Image

ImageT = list[tuple[str, str | tuple[str, ...]]]
IMAGE_FTYTPES: ImageT = [
    ("All image files", (
        "*.png",
        "*.jpg",
        "*.jpeg",
        "*.jpe",
        "*.jfif",
        "*.tif",
        "*.tiff"
    )),
    ("JPEG", ("*.jpg", "*.jpeg", "*.jpe", "*.jfif")),
    ("TIFF", ("*.tif", "*.tiff")),
    ("PNG", "*.png"),
    ("All files", "*")
]
WATERMARK_FTYPES: ImageT = [("PNG", "*.png"), ("All files", "*")]
INIT_DIR: str = f"{environ["HOMEDRIVE"]}{environ["HOMEPATH"]}\\Downloads"


def choose() -> tuple[list[str], str]:

    img_paths: list[str] = list(askopenfilenames(
        title="Chọn ảnh để chèn logo",
        filetypes=IMAGE_FTYTPES,
        initialdir=INIT_DIR
    ))

    if not img_paths:
        exit()

    watermark_path: str = askopenfilename(
        title="Chọn logo để chèn vào ảnh",
        filetypes=WATERMARK_FTYPES,
        initialdir=INIT_DIR
    )

    if not img_paths:
        exit()

    return img_paths, watermark_path


def apply_watermark(image_path: str, watermark_path: str) -> None:

    image = Image.open(image_path).convert("RGBA")
    watermark = Image.open(watermark_path).convert("RGBA")

    x, y = image.size

    modif: int = (x if x <= y else y) // 10
    small, large = sorted(watermark.size)
    ratio: float = small / large
    watermark = watermark.resize((modif, round(modif * ratio)))

    mask = Image.new("RGBA", image.size)
    mask.paste(watermark, (10, 10), watermark)

    new_img = Image.alpha_composite(image, mask)

    img_path_name, _ = path.splitext(image_path)
    new_img.save(f"{img_path_name}_wtrmrk.png", format="PNG")


def main() -> None:

    img_paths, watermark_path = choose()

    func = partial(apply_watermark, watermark_path=watermark_path)
    with Pool(cpu_count()) as pool:
        pool.imap_unordered(func, img_paths)


if __name__ == "__main__":
    main()
