# Constructing and inspecting SVG logos

Use the bundled standard-library Python script to construct a static SVG from JSON primitives:

```bash
python3 <skill-dir>/scripts/build_logo_svg.py concept.json concept.svg
```

Example specification (geometry demonstration, not a design recommendation):
```json
{"viewBox":[0,0,100,100],"title":"Geometry study","shapes":[
  {"type":"rect","x":20,"y":20,"width":60,"height":60,"rx":12,"fill":"#2563EB"},
  {"type":"path","d":"M35 50 L65 50","fill":"none","stroke":"white","stroke-width":8}
]}
```

The script bounds input size, shape count and numeric values, accepts only listed primitives and literal colours, escapes XML text, refuses existing output paths and uses no network. It excludes scripts, event handlers, external references, images, CSS, filters, animation and embedded fonts. It constructs new documents rather than parsing or sanitizing imported SVG.

Supported shapes: circle, ellipse, rect, line, path, polygon, polyline. Paths are restricted to command characters and bounded numbers; grammar correctness, visibility, clipping and aesthetics still require rendering. No transforms or groups are supported; use explicit coordinates or an available vector editor for advanced work. Keep editable type sources separately and convert approved wordmarks to outlines with an available vector tool when appropriate.

Render using an available vector editor, renderer or browser and inspect the result after meaningful geometry changes. For example, if CairoSVG is already available:

```bash
cairosvg concept.svg --output-width 512 --output-height 512 -o concept-preview.png
```

Do not use CairoSVG's unsafe option. Inspect requested actual-size icon exports separately; a large preview does not validate a favicon. Do not claim this construction tool certifies arbitrary SVG security, visual quality, originality or approval.

Technical references: [ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html), [SVG script elements](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/script), [CairoSVG](https://cairosvg.org/documentation/).
