"""Image comparison helpers for visual regression tests."""

import io

from PIL import Image, ImageChops


def images_within_tolerance(
    actual: bytes,
    expected: bytes,
    *,
    max_diff_ratio: float = 0.05,
) -> bool:
    """Return True when two PNG screenshots are visually similar enough."""
    img_a = Image.open(io.BytesIO(actual)).convert("RGB")
    img_b = Image.open(io.BytesIO(expected)).convert("RGB")

    if img_a.size != img_b.size:
        img_b = img_b.resize(img_a.size)

    diff = ImageChops.difference(img_a, img_b)
    histogram = diff.histogram()
    # RGB channels: count pixels with any channel difference
    diff_pixels = sum(histogram[1:256]) + sum(histogram[257:512]) + sum(histogram[513:768])
    total_pixels = img_a.size[0] * img_a.size[1]
    return (diff_pixels / total_pixels) <= max_diff_ratio
