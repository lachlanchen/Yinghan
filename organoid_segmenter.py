import base64
import io
import json
import os
import time
from dataclasses import dataclass
from typing import List, Tuple

from PIL import Image, ImageDraw
from openai import OpenAI


@dataclass
class SegmentationResult:
    width: int
    height: int
    polygon: List[Tuple[float, float]]
    confidence: float
    annotated_path: str
    mask_path: str
    json_path: str


def _encode_image_to_data_url(image_bytes: bytes) -> str:
    b64 = base64.b64encode(image_bytes).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"


def _extract_json(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Model response did not contain valid JSON")
    return text[start : end + 1]


def _validate_polygon(polygon: List[List[float]], width: int, height: int) -> List[Tuple[float, float]]:
    if not polygon or len(polygon) < 3:
        raise ValueError("Polygon must contain at least 3 points")

    cleaned = []
    for point in polygon:
        if not isinstance(point, list) or len(point) != 2:
            raise ValueError("Each polygon point must be a list of [x, y]")
        x, y = float(point[0]), float(point[1])
        # Clamp to image bounds
        x = max(0.0, min(float(width - 1), x))
        y = max(0.0, min(float(height - 1), y))
        cleaned.append((x, y))

    if len(cleaned) < 3:
        raise ValueError("Polygon must contain at least 3 valid points")
    return cleaned


def _draw_outputs(image: Image.Image, polygon: List[Tuple[float, float]], out_base: str) -> Tuple[str, str]:
    os.makedirs(os.path.dirname(out_base), exist_ok=True)

    annotated = image.convert("RGBA")
    overlay = Image.new("RGBA", annotated.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    # Semi-transparent fill and bold outline
    overlay_draw.polygon(polygon, fill=(255, 0, 0, 70), outline=(255, 0, 0, 200))
    annotated = Image.alpha_composite(annotated, overlay)

    mask = Image.new("L", annotated.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.polygon(polygon, fill=255)

    annotated_path = f"{out_base}_annotated.png"
    mask_path = f"{out_base}_mask.png"

    annotated.convert("RGB").save(annotated_path)
    mask.save(mask_path)

    return annotated_path, mask_path


def _segment_with_responses(client: OpenAI, model: str, image_bytes: bytes) -> dict:
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "You are a biomedical image annotator. Identify the organoid in the image and return a "
                            "single polygon that tightly traces the outer boundary of the organoid (the dark circular mass). "
                            "Return pixel coordinates in the original image coordinate space with origin at top-left. "
                            "Use 60-200 points to capture the boundary."
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": _encode_image_to_data_url(image_bytes),
                    },
                ],
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "organoid_segmentation",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "width": {"type": "integer"},
                            "height": {"type": "integer"},
                            "polygon": {
                                "type": "array",
                                "items": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "minItems": 2,
                                    "maxItems": 2,
                                },
                                "minItems": 3,
                            },
                            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                        },
                        "required": ["width", "height", "polygon", "confidence"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                },
            }
        },
    )
    return json.loads(response.output_text)


def _segment_with_chat(client: OpenAI, model: str, image_bytes: bytes, width: int, height: int) -> dict:
    prompt = (
        "You are a biomedical image annotator. Identify the organoid in the image and return a single polygon that "
        "tightly traces the outer boundary of the organoid (the dark circular mass). Return pixel coordinates in the "
        "original image coordinate space with origin at top-left. Use 60-200 points to capture the boundary. "
        "Return ONLY valid JSON with keys: width, height, polygon, confidence. "
        "Polygon must be a list of [x, y] pairs."
    )

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "organoid_segmentation",
            "schema": {
                "type": "object",
                "properties": {
                    "width": {"type": "integer"},
                    "height": {"type": "integer"},
                    "polygon": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 2,
                            "maxItems": 2,
                        },
                        "minItems": 3,
                    },
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                },
                "required": ["width", "height", "polygon", "confidence"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": _encode_image_to_data_url(image_bytes)}},
                    ],
                }
            ],
            temperature=0,
            response_format=response_format,
        )
        content = response.choices[0].message.content or ""
        data = json.loads(content)
    except Exception:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": _encode_image_to_data_url(image_bytes)}},
                    ],
                }
            ],
            temperature=0,
        )
        content = response.choices[0].message.content or ""
        try:
            data = json.loads(_extract_json(content))
        except Exception as exc:
            snippet = content[:800].replace("\n", " ")
            raise ValueError(f"Model response not JSON. Snippet: {snippet}") from exc

    if "width" not in data:
        data["width"] = width
    if "height" not in data:
        data["height"] = height
    if "confidence" not in data:
        data["confidence"] = 0.0
    return data


def segment_organoid(image_path: str, out_dir: str = "outputs", model: str = "gpt-4o-2024-08-06") -> SegmentationResult:
    client = OpenAI()

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image = Image.open(io.BytesIO(image_bytes))
    width, height = image.size

    if hasattr(client, "responses"):
        data = _segment_with_responses(client, model, image_bytes)
    else:
        data = _segment_with_chat(client, model, image_bytes, width, height)

    polygon = _validate_polygon(data["polygon"], width, height)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    out_base = os.path.join(out_dir, f"{base_name}_{timestamp}")

    annotated_path, mask_path = _draw_outputs(image, polygon, out_base)

    json_path = f"{out_base}_polygon.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "width": width,
                "height": height,
                "polygon": polygon,
                "confidence": float(data["confidence"]),
            },
            f,
            indent=2,
        )

    return SegmentationResult(
        width=width,
        height=height,
        polygon=polygon,
        confidence=float(data["confidence"]),
        annotated_path=annotated_path,
        mask_path=mask_path,
        json_path=json_path,
    )
