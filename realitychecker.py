import os
import json
import base64
import time
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL = os.getenv(
    "GROQ_MODEL",
    "qwen/qwen3.6-27b"
)


# ============================================================
# CHECK API KEY
# ============================================================

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing from your .env file."
    )


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# IMAGE ENCODING
# ============================================================

def encode_image(image_path):

    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    with open(path, "rb") as image_file:

        encoded = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    return encoded


# ============================================================
# DETERMINE MIME TYPE
# ============================================================

def get_mime_type(image_path):

    extension = Path(
        image_path
    ).suffix.lower()

    if extension == ".png":
        return "image/png"

    if extension in [".jpg", ".jpeg"]:
        return "image/jpeg"

    if extension == ".webp":
        return "image/webp"

    if extension == ".gif":
        return "image/gif"

    return "image/jpeg"


# ============================================================
# CLEAN STRING
# ============================================================

def clean_string(value):

    if value is None:
        return ""

    value = str(value)

    # Remove Markdown
    value = value.replace("**", "")
    value = value.replace("__", "")
    value = value.replace("```", "")
    value = value.replace("`", "")

    # Remove common HTML
    for tag in [
        "<b>",
        "</b>",
        "<strong>",
        "</strong>",
        "<i>",
        "</i>",
        "<em>",
        "</em>",
        "<u>",
        "</u>",
        "<br>",
        "<br/>",
        "<br />"
    ]:
        value = value.replace(tag, "")

    # Remove unnecessary quotation marks
    value = value.replace('"', "")
    value = value.replace("“", "")
    value = value.replace("”", "")

    return value.strip()


# ============================================================
# SAFE JSON PARSER
# ============================================================

def parse_json_response(text):

    if not text:
        return {}

    text = text.strip()

    # Remove code fences if model accidentally adds them
    text = text.replace("```json", "")
    text = text.replace("```JSON", "")
    text = text.replace("```", "")
    text = text.strip()

    try:

        return json.loads(text)

    except json.JSONDecodeError:

        # Try extracting JSON object
        start = text.find("{")
        end = text.rfind("}")

        if start >= 0 and end > start:

            possible_json = text[
                start:end + 1
            ]

            try:
                return json.loads(
                    possible_json
                )

            except Exception:
                pass

    return {}


# ============================================================
# MAIN IMAGE VERIFICATION
# ============================================================

def check_news_image(image_path):

    print()
    print("==========================================")
    print("FAKEBREAK REALITY CHECKER")
    print("==========================================")
    print(
        "Image:",
        image_path
    )
    print(
        "Model:",
        MODEL
    )

    # --------------------------------------------------------
    # ENCODE IMAGE
    # --------------------------------------------------------

    base64_image = encode_image(
        image_path
    )

    mime_type = get_mime_type(
        image_path
    )

    image_url = (
        f"data:{mime_type};base64,"
        f"{base64_image}"
    )

    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    prompt = r"""
You are FakeBreak, an AI-assisted news verification system.

Analyze the uploaded image carefully.

Your job has TWO major stages.

STAGE 1 — UNDERSTAND THE IMAGE

First identify what is actually visible in the image.

Separate the observation into:

1. visuals
2. text
3. body_text
4. watermark
5. interface

Do NOT assume that a claim in the image is true.

Only describe what can actually be observed.

STAGE 2 — FACT CHECK THE CLAIM

Identify the main factual claim contained in the image.

Then determine whether the claim is:

TRUE
FALSE
MISLEADING
UNCERTAIN

Use your knowledge and careful reasoning.

IMPORTANT:

Do NOT invent evidence.

Do NOT claim that a source was checked if it was not actually checked.

If you cannot confidently establish the truth, use UNCERTAIN.

Do not automatically choose TRUE.

Do not automatically choose FALSE.

Give a realistic confidence value between 0 and 100.

Explain why the verdict was selected.

Give the best corrected information you can provide.

SOURCE RULE:

Only include sources that you are reasonably confident are relevant.

Prefer official government sources, recognized organizations, major reputable news organizations, court websites, research organizations, or other authoritative sources.

IMPORTANT OUTPUT RULES:

Return ONLY valid JSON.

Do NOT use Markdown.

Do NOT use asterisks.

Do NOT use double asterisks.

Do NOT use HTML.

Do NOT use <b>, </b>, <strong>, </strong>.

Do NOT use backticks.

Do NOT put quotation marks inside the actual descriptive text unless they are necessary to reproduce the wording visible in the image.

Do NOT create headings using Markdown.

The JSON must contain exactly these fields:

{
  "what_is_in_image": {
    "visuals": "",
    "text": "",
    "body_text": "",
    "watermark": "",
    "interface": ""
  },
  "main_claim": "",
  "verdict": "",
  "confidence": 0,
  "reason": "",
  "correct_information": "",
  "evidence": "",
  "sources": [
    {
      "title": "",
      "url": ""
    }
  ]
}

For the verdict use only:

TRUE
FALSE
MISLEADING
UNCERTAIN

For confidence use a number from 0 to 100.

If a visual field is not visible, write:

Not clearly visible.

Do not use Markdown formatting anywhere.
"""

    # --------------------------------------------------------
    # API CALL
    # --------------------------------------------------------

    last_error = None

    for attempt in range(2):

        try:

            print(
                f"Sending image to Groq... "
                f"attempt {attempt + 1}"
            )

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
                                    "url": image_url
                                }
                            }

                        ]
                    }
                ],

                temperature=0.1,

                max_completion_tokens=2500,

                response_format={
                    "type": "json_object"
                }
            )

            content = (
                response
                .choices[0]
                .message
                .content
            )

            print()
            print("RAW AI RESPONSE:")
            print(content)
            print()

            result = parse_json_response(
                content
            )

            if result:

                # ------------------------------------------------
                # NORMALIZE RESULT
                # ------------------------------------------------

                image_info = result.get(
                    "what_is_in_image",
                    {}
                )

                if not isinstance(
                    image_info,
                    dict
                ):
                    image_info = {}

                final_result = {

                    "what_is_in_image": {

                        "visuals":
                            clean_string(
                                image_info.get(
                                    "visuals",
                                    "Not clearly visible."
                                )
                            ),

                        "text":
                            clean_string(
                                image_info.get(
                                    "text",
                                    "Not clearly visible."
                                )
                            ),

                        "body_text":
                            clean_string(
                                image_info.get(
                                    "body_text",
                                    "Not clearly visible."
                                )
                            ),

                        "watermark":
                            clean_string(
                                image_info.get(
                                    "watermark",
                                    "Not clearly visible."
                                )
                            ),

                        "interface":
                            clean_string(
                                image_info.get(
                                    "interface",
                                    "Not clearly visible."
                                )
                            )
                    },

                    "main_claim":
                        clean_string(
                            result.get(
                                "main_claim",
                                "No clear factual claim was identified."
                            )
                        ),

                    "verdict":
                        clean_string(
                            result.get(
                                "verdict",
                                "UNCERTAIN"
                            )
                        ).upper(),

                    "confidence":
                        result.get(
                            "confidence",
                            0
                        ),

                    "reason":
                        clean_string(
                            result.get(
                                "reason",
                                "No detailed reasoning was returned."
                            )
                        ),

                    "correct_information":
                        clean_string(
                            result.get(
                                "correct_information",
                                "No corrected information was returned."
                            )
                        ),

                    "evidence":
                        clean_string(
                            result.get(
                                "evidence",
                                "No specific evidence was returned."
                            )
                        ),

                    "sources":
                        result.get(
                            "sources",
                            []
                        )
                }

                # ------------------------------------------------
                # NORMALIZE VERDICT
                # ------------------------------------------------

                if final_result[
                    "verdict"
                ] not in [
                    "TRUE",
                    "FALSE",
                    "MISLEADING",
                    "UNCERTAIN"
                ]:

                    final_result[
                        "verdict"
                    ] = "UNCERTAIN"

                # ------------------------------------------------
                # NORMALIZE CONFIDENCE
                # ------------------------------------------------

                try:

                    confidence = float(
                        final_result[
                            "confidence"
                        ]
                    )

                    confidence = max(
                        0,
                        min(
                            100,
                            confidence
                        )
                    )

                    final_result[
                        "confidence"
                    ] = int(
                        confidence
                    )

                except Exception:

                    final_result[
                        "confidence"
                    ] = 0

                # ------------------------------------------------
                # NORMALIZE SOURCES
                # ------------------------------------------------

                sources = []

                if isinstance(
                    final_result["sources"],
                    list
                ):

                    for source in final_result[
                        "sources"
                    ]:

                        if isinstance(
                            source,
                            dict
                        ):

                            title = clean_string(
                                source.get(
                                    "title",
                                    "Source"
                                )
                            )

                            url = clean_string(
                                source.get(
                                    "url",
                                    ""
                                )
                            )

                            if url:

                                sources.append({
                                    "title": title,
                                    "url": url
                                })

                final_result[
                    "sources"
                ] = sources

                print(
                    "✅ Verification completed."
                )

                return final_result

        except Exception as error:

            last_error = error

            print()
            print(
                "Groq error:"
            )
            print(error)
            print()

            # Small retry delay
            if attempt == 0:
                time.sleep(2)

    # --------------------------------------------------------
    # RETURN ERROR AS RESULT
    # --------------------------------------------------------

    raise RuntimeError(
        "AI verification failed: "
        + str(last_error)
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "FakeBreak RealityChecker loaded successfully."
    )

    print(
        "Vision model:",
        MODEL
    )