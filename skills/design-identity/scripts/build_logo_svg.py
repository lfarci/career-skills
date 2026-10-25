#!/usr/bin/env python3
"""Construct static logo SVGs from bounded JSON geometry; not an SVG sanitizer."""
import argparse
import json
import math
import re
import sys
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

GEOMETRY = {
    "circle": {"cx", "cy", "r"}, "ellipse": {"cx", "cy", "rx", "ry"},
    "rect": {"x", "y", "width", "height", "rx", "ry"},
    "line": {"x1", "y1", "x2", "y2"},
    "path": {"d"}, "polygon": {"points"}, "polyline": {"points"},
}
STYLE = {"fill", "stroke", "stroke-width", "fill-rule", "stroke-linecap", "stroke-linejoin"}
NUMBER = r"[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?"

def number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Expected numeric geometry")
    if not math.isfinite(value) or abs(value) > 100000:
        raise ValueError("Geometry must be finite and bounded")
    return str(value)

def coordinates(value, path=False):
    if not isinstance(value, str) or len(value) > 20000:
        raise ValueError("Invalid geometry string")
    remainder = re.sub(NUMBER, "", value)
    allowed = r"[\s,MmZzLlHhVvCcSsQqTtAa]*" if path else r"[\s,]*"
    if not re.fullmatch(allowed, remainder):
        raise ValueError("Unsupported geometry content")
    values = re.findall(NUMBER, value)
    if not values:
        raise ValueError("Empty geometry")
    for item in values:
        number(float(item))
    if not path and len(values) % 2:
        raise ValueError("Points require coordinate pairs")
    return value

def build(spec):
    if not isinstance(spec, dict) or set(spec) - {"viewBox", "title", "shapes"}:
        raise ValueError("Unknown top-level field")
    box = spec.get("viewBox")
    if not isinstance(box, list) or len(box) != 4:
        raise ValueError("viewBox requires four numbers")
    box_text = " ".join(number(v) for v in box)
    if box[2] <= 0 or box[3] <= 0:
        raise ValueError("viewBox dimensions must be positive")
    shapes = spec.get("shapes")
    if not isinstance(shapes, list) or not 1 <= len(shapes) <= 256:
        raise ValueError("Expected 1–256 shapes")
    root = Element("svg", {"xmlns": "http://www.w3.org/2000/svg", "viewBox": box_text})
    title = spec.get("title", "Logo exploration")
    if not isinstance(title, str) or len(title) > 500:
        raise ValueError("Invalid title")
    SubElement(root, "title").text = title
    for shape in shapes:
        if not isinstance(shape, dict):
            raise ValueError("Expected shape object")
        tag = shape.get("type")
        if tag not in GEOMETRY:
            raise ValueError("Unsupported shape")
        if set(shape) - (GEOMETRY[tag] | STYLE | {"type"}):
            raise ValueError("Unsupported attribute")
        attrs = {}
        for key, value in shape.items():
            if key == "type":
                continue
            if key in {"fill", "stroke"}:
                if not isinstance(value, str) or not re.fullmatch(r"(?:#[0-9a-fA-F]{3}|#[0-9a-fA-F]{6}|black|white|none)", value):
                    raise ValueError("Use literal colours; URLs and CSS are unsupported")
                attrs[key] = value
            elif key in {"fill-rule", "stroke-linecap", "stroke-linejoin"}:
                choices = {"fill-rule": {"nonzero", "evenodd"}, "stroke-linecap": {"butt", "round", "square"}, "stroke-linejoin": {"miter", "round", "bevel"}}
                if value not in choices[key]:
                    raise ValueError("Unsupported style value")
                attrs[key] = value
            elif key in {"d", "points"}:
                attrs[key] = coordinates(value, path=key == "d")
            else:
                attrs[key] = number(value)
                if key in {"r", "rx", "ry", "width", "height", "stroke-width"} and value < 0:
                    raise ValueError("Negative size")
        SubElement(root, tag, attrs)
    return tostring(root, encoding="unicode") + "\n"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        with args.spec.open("rb") as source:
            raw = source.read(100001)
        if len(raw) > 100000:
            raise ValueError("Specification exceeds 100 KB")
        svg = build(json.loads(raw))
        with args.output.open("x", encoding="utf-8") as output:
            output.write(svg)
    except (ValueError, TypeError, OSError, OverflowError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Created {args.output}; render and inspect before approval.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
