import argparse
import json

from organoid_segmenter import segment_organoid


def main() -> None:
    parser = argparse.ArgumentParser(description="Segment an organoid in a microscopy image using OpenAI 4o.")
    parser.add_argument("image_path", help="Path to the input image")
    parser.add_argument("--out-dir", default="outputs", help="Directory for outputs")
    parser.add_argument("--model", default="gpt-4o-2024-08-06", help="OpenAI model name")
    args = parser.parse_args()

    result = segment_organoid(args.image_path, out_dir=args.out_dir, model=args.model)

    print("Annotated:", result.annotated_path)
    print("Mask:", result.mask_path)
    print("Polygon JSON:", result.json_path)
    print("Confidence:", result.confidence)
    print(json.dumps({"width": result.width, "height": result.height, "points": len(result.polygon)}, indent=2))


if __name__ == "__main__":
    main()
