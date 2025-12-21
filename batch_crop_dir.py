# -*- coding: utf-8 -*-

from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}

def crop_largest_component_by_background(
    img: Image.Image,
    thresh: float = 40.0,
    pad: int = 4,
    corner_frac: float = 0.025,
    min_area_ratio: float = 0.05,
) -> Image.Image:
    """
    提取图像中最大的内容区域，去掉边框和文字
    
    参数：
        img: 输入 PIL Image
        thresh: 像素与背景色的距离阈值（越大越保守）
        pad: 外扩像素数（避免贴边）
        corner_frac: 取角落的比例（默认2.5%）
        min_area_ratio: 最小连通域面积比例（默认5%）
    """
    im = img.convert("RGB")
    arr = np.asarray(im).astype(np.int16)
    h, w = arr.shape[:2]

    # 1) 从四个角落取样背景色
    k = max(2, int(min(h, w) * corner_frac))
    corners = np.concatenate(
        [
            arr[0:k, 0:k].reshape(-1, 3),
            arr[0:k, w - k : w].reshape(-1, 3),
            arr[h - k : h, 0:k].reshape(-1, 3),
            arr[h - k : h, w - k : w].reshape(-1, 3),
        ],
        axis=0,
    )
    bg = np.median(corners, axis=0)

    # 2) 计算到背景色的距离
    diff = arr - bg
    dist = np.sqrt((diff * diff).sum(axis=2))
    mask = dist > thresh

    # 3) 找最大连通域
    labeled, n = ndimage.label(mask)
    if n == 0:
        return im

    sizes = ndimage.sum(mask, labeled, index=range(1, n + 1))
    sizes = np.asarray(sizes)
    idx = int(sizes.argmax()) + 1

    # 如果最大连通域太小，放弃裁剪
    if sizes.max() < h * w * min_area_ratio:
        return im

    # 4) 找外接矩形并应用 padding
    ys, xs = np.where(labeled == idx)
    x0, x1 = xs.min(), xs.max()
    y0, y1 = ys.min(), ys.max()

    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(w - 1, x1 + pad)
    y1 = min(h - 1, y1 + pad)

    return im.crop((x0, y0, x1 + 1, y1 + 1))


def batch_crop(input_dir: Path, output_dir: Path, thresh: float = 40.0, pad: int = 4):
    """
    递归遍历输入目录，批量裁剪所有图片
    保持目录结构，所有输出为 PNG 格式
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    count_ok = 0
    count_fail = 0

    for p in input_dir.rglob("*"):
        if p.suffix.lower() not in IMG_EXTS:
            continue
        try:
            img = Image.open(p)
            cropped = crop_largest_component_by_background(img, thresh=thresh, pad=pad)

            # 保持目录结构
            rel = p.relative_to(input_dir)
            out_path = (output_dir / rel).with_suffix(".png")
            out_path.parent.mkdir(parents=True, exist_ok=True)

            cropped.save(out_path, optimize=True)
            count_ok += 1
            print(f"OK   {p} -> {out_path}")
        except Exception as e:
            count_fail += 1
            print(f"FAIL {p}: {e}")

    print(f"\nDone. OK={count_ok}, FAIL={count_fail}, out={output_dir}")


if __name__ == "__main__":
    input_dir = Path("/Users/zdl/projects/bob/lord_of_mysteries/img/charactor_split")
    output_dir = Path("/Users/zdl/projects/bob/lord_of_mysteries/img/charactor_split_cropped")

    # 经验值：白边/灰边常用 35~55；黑框明显可略调小
    batch_crop(input_dir, output_dir, thresh=40.0, pad=4)
