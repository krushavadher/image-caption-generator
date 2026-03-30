import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

app = Flask(__name__)

# Load Azure credentials
endpoint = os.getenv("VISION_ENDPOINT")
key = os.getenv("VISION_KEY")

client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
) if endpoint and key else None


# ----------- ANALYZE IMAGE FROM URL -----------
def analyze_image_url(image_url: str) -> dict:
    result = client.analyze_from_url(
        image_url=image_url,
        visual_features=["Caption", "Tags", "Objects", "DenseCaptions"]
    )
    return parse_result(result)


# ----------- ANALYZE IMAGE FROM UPLOAD -----------
def analyze_image_bytes(image_data: bytes) -> dict:
    result = client.analyze(
        image_data=image_data,
        visual_features=["Caption", "Tags", "Objects", "DenseCaptions"]
    )
    return parse_result(result)


# ----------- PARSE RESULT -----------
def parse_result(result) -> dict:
    caption = ""
    confidence = 0.0
    tags = []
    objects = []
    dense_captions = []

    if result.caption:
        caption = result.caption.text
        confidence = round(result.caption.confidence * 100, 1)

    if result.tags:
        tags = [t.name for t in result.tags.list[:10]]

    if result.objects:
        seen = set()
        for o in result.objects.list:
            name = o.tags[0].name
            if name not in seen:
                objects.append(name)
                seen.add(name)

    if result.dense_captions:
        dense_captions = [
            {
                "text": c.text,
                "confidence": round(c.confidence * 100, 1)
            }
            for c in result.dense_captions.list[:4]
        ]

    return {
        "caption": caption,
        "confidence": confidence,
        "tags": tags,
        "objects": objects,
        "dense_captions": dense_captions,
    }


# ----------- ROUTES -----------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if not client:
        return jsonify({"error": "Azure Vision not configured. Check .env file"}), 500

    data = request.get_json(silent=True) or {}
    image_url = data.get("image_url", "").strip()

    if not image_url:
        return jsonify({"error": "No image URL provided"}), 400

    try:
        result = analyze_image_url(image_url)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/analyze-upload", methods=["POST"])
def analyze_upload():
    if not client:
        return jsonify({"error": "Azure Vision not configured. Check .env file"}), 500

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    image_data = file.read()

    try:
        result = analyze_image_bytes(image_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ----------- RUN APP -----------



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)