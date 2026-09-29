import os
import json
import base64
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env")

client = Groq(api_key=GROQ_API_KEY)

MODEL = "qwen/qwen3-vl-32b-instruct"


# =========================================================
# ENCODE IMAGE
# =========================================================

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


# =========================================================
# EXTRACT JSON
# =========================================================

def extract_json(text):

    if not text:
        return None

    text = text.strip()

    # Remove markdown code blocks
    if "```json" in text:
        text = text.replace("```json", "")

    if "```" in text:
        text = text.replace("```", "")

    text = text.strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    json_text = text[start:end + 1]

    try:
        return json.loads(json_text)

    except Exception:
        return None


# =========================================================
# GET VALUE FROM MULTIPLE POSSIBLE FIELD NAMES
# =========================================================

def get_value(data, possible_names, default):

    for name in possible_names:

        value = data.get(name)

        if value is not None:

            if isinstance(value, str):

                if value.strip() != "":
                    return value.strip()

            else:
                return value

    return default


# =========================================================
# NORMALIZE AI RESULT
# =========================================================

def normalize_result(data):

    if not isinstance(data, dict):

        return {
            "what_is_in_image": "Unable to describe the image.",
            "claim": "Unable to extract the main claim.",
            "verdict": "UNCERTAIN",
            "confidence": 0,
            "reason": "The AI did not return a structured result.",
            "correct_information": "Please try the image again.",
            "sources": []
        }

    # -----------------------------------------------------
    # IMAGE DESCRIPTION
    # -----------------------------------------------------

    image_description = get_value(
        data,
        [
            "what_is_in_image",
            "image_description",
            "description",
            "what_is_shown",
            "image_content",
            "content"
        ],
        "The image contains information that could not be fully described."
    )

    # -----------------------------------------------------
    # CLAIM
    # -----------------------------------------------------

    claim = get_value(
        data,
        [
            "claim",
            "main_claim",
            "factual_claim",
            "claim_in_image",
            "headline",
            "statement"
        ],
        "No clear factual claim could be extracted."
    )

    # -----------------------------------------------------
    # VERDICT
    # -----------------------------------------------------

    verdict = get_value(
        data,
        [
            "verdict",
            "classification",
            "result",
            "assessment"
        ],
        "UNCERTAIN"
    )

    verdict = str(verdict).upper().strip()

    # Normalize common outputs

    if "TRUE" in verdict and "FALSE" not in verdict:
        verdict = "TRUE"

    elif "FALSE" in verdict:
        verdict = "FALSE"

    elif "MISLEADING" in verdict:
        verdict = "MISLEADING"

    else:
        verdict = "UNCERTAIN"

    # -----------------------------------------------------
    # CONFIDENCE
    # -----------------------------------------------------

    confidence = get_value(
        data,
        [
            "confidence",
            "confidence_score",
            "score",
            "certainty"
        ],
        0
    )

    try:

        confidence = float(confidence)

        # Convert 0.95 → 95
        if confidence <= 1:
            confidence = confidence * 100

        confidence = round(
            max(0, min(100, confidence))
        )

    except Exception:

        confidence = 0

    # -----------------------------------------------------
    # REASON
    # -----------------------------------------------------

    reason = get_value(
        data,
        [
            "reason",
            "reasoning",
            "why",
            "explanation",
            "analysis"
        ],
        "The AI could not provide a detailed explanation."
    )

    # -----------------------------------------------------
    # CORRECT INFORMATION
    # -----------------------------------------------------

    correct_information = get_value(
        data,
        [
            "correct_information",
            "correct_info",
            "accurate_information",
            "actual_information",
            "fact",
            "facts",
            "context"
        ],
        "No additional verified information was returned."
    )

    # -----------------------------------------------------
    # SOURCES
    # -----------------------------------------------------

    sources = get_value(
        data,
        [
            "sources",
            "related_sources",
            "reliable_sources",
            "references",
            "links"
        ],
        []
    )

    if not isinstance(sources, list):
        sources = []

    return {
        "what_is_in_image": image_description,
        "claim": claim,
        "verdict": verdict,
        "confidence": confidence,
        "reason": reason,
        "correct_information": correct_information,
        "sources": sources
    }


# =========================================================
# MAIN VERIFICATION FUNCTION
# =========================================================

def check_news_image(image_path):

    try:

        print("\n======================================")
        print("FAKEBREAK AI VERIFICATION")
        print("======================================")

        if not os.path.exists(image_path):

            return {
                "what_is_in_image": "Image file not found.",
                "claim": "Unable to read image.",
                "verdict": "UNCERTAIN",
                "confidence": 0,
                "reason": "Image file could not be found.",
                "correct_information": "Please upload the image again.",
                "sources": []
            }

        print("Reading image...")

        base64_image = encode_image(image_path)

        # =================================================
        # PROMPT
        # =================================================

        prompt = """
You are FakeBreak AI, a news verification assistant.

Carefully inspect the uploaded image.

You MUST perform these tasks:

1. DESCRIBE THE IMAGE
Explain exactly what is visible:
- people
- objects
- logos
- screenshots
- headlines
- social media posts
- visible text
- dates
- locations
- other relevant details

2. IDENTIFY THE MAIN CLAIM
Find the main factual statement being communicated.

3. VERIFY THE CLAIM
Classify it as exactly one of:

TRUE
FALSE
MISLEADING
UNCERTAIN

4. GIVE REASONING
Explain clearly why the verdict was selected.

5. GIVE CORRECT INFORMATION
Explain what the user should actually know.

6. GIVE RELATED SOURCES
Provide reliable sources that are relevant to the claim.

IMPORTANT:

Do NOT assume that an image is true simply because it looks like a professional news graphic.

Do NOT invent facts.

Do NOT invent URLs.

If there is insufficient evidence, use UNCERTAIN.

Return ONLY JSON.

Use EXACTLY these field names:

{
    "what_is_in_image": "Detailed description of the image",
    "claim": "Main factual claim",
    "verdict": "TRUE",
    "confidence": 85,
    "reason": "Detailed reasoning",
    "correct_information": "Accurate information",
    "sources": [
        {
            "title": "Source title",
            "url": "https://example.com"
        }
    ]
}

The verdict MUST be TRUE, FALSE, MISLEADING, or UNCERTAIN.

Confidence must be a number between 0 and 100.

The image description MUST describe the actual uploaded image.

The claim MUST describe the actual claim in the uploaded image.

The reasoning MUST explain the verdict.

Do not leave these fields empty.
"""

        print("Sending image to Groq...")
        print("Model:", MODEL)

        # =================================================
        # GROQ
        # =================================================

        response = client.chat.completions.create(

            model=MODEL,

            messages=[
                {
                    "role": "user",

                    "content": [

                        {
                            "type": "text",
                            "text": prompt
                        },

                        {
                            "type": "image_url",

                            "image_url": {
                                "url":
                                f"data:image/jpeg;base64,{base64_image}"
                            }
                        }

                    ]
                }
            ],

            temperature=0.1,

            max_completion_tokens=2500
        )

        # =================================================
        # RAW RESPONSE
        # =================================================

        text = response.choices[0].message.content

        print("\n======================================")
        print("RAW GROQ RESPONSE")
        print("======================================")

        print(text)

        print("======================================")

        # =================================================
        # PARSE
        # =================================================

        data = extract_json(text)

        # =================================================
        # IF JSON FAILED
        # =================================================

        if data is None:

            print("Could not parse JSON.")

            return {
                "what_is_in_image":
                "The AI analyzed the image, but the structured image description could not be extracted.",

                "claim":
                "The AI returned an unstructured response.",

                "verdict":
                "UNCERTAIN",

                "confidence":
                0,

                "reason":
                text,

                "correct_information":
                "Please review the AI analysis above.",

                "sources":
                []
            }

        # =================================================
        # NORMALIZE
        # =================================================

        result = normalize_result(data)

        print("\n======================================")
        print("FINAL RESULT")
        print("======================================")

        print(json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        ))

        print("======================================")

        return result

    except Exception as error:

        print("\n======================================")
        print("ERROR")
        print("======================================")

        print(error)

        print("======================================")

        return {
            "what_is_in_image":
            "The image could not be analyzed.",

            "claim":
            "Verification failed.",

            "verdict":
            "UNCERTAIN",

            "confidence":
            0,

            "reason":
            str(error),

            "correct_information":
            "Please try again.",

            "sources":
            []
        }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("FakeBreak RealityChecker loaded successfully.")