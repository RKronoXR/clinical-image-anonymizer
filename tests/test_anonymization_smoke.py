from pathlib import Path

from src.anonymization.batch_validation import (
    all_images_same_size,
    batch_dimension_summary,
)
from src.anonymization.censoring import (
    clip_rectangle_to_image,
    validate_rgb_color,
)
from src.anonymization.metadata import (
    inspect_image_metadata,
    remove_image_metadata,
)
from src.anonymization.validators import (
    validate_non_empty_batch,
)


def main() -> None:
    assert clip_rectangle_to_image((-5, -5, 20, 20), (100, 100)) == (0, 0, 20, 20)
    assert clip_rectangle_to_image((150, 150, 200, 200), (100, 100)) is None

    validate_rgb_color((255, 255, 255))

    assert all_images_same_size({}) is True

    summary = batch_dimension_summary(
        {
            Path("a.png"): (100, 100),
            Path("b.png"): (100, 100),
            Path("c.png"): (50, 50),
        }
    )

    assert summary[(100, 100)] == 2
    assert summary[(50, 50)] == 1

    try:
        validate_non_empty_batch([])
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")

    print("Anonymization smoke test passed.")


if __name__ == "__main__":
    main()