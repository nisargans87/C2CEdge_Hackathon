import os
import json
import asyncio
import traceback
from pathlib import Path

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from realitychecker import check_news_image


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)


# ============================================================
# TEMP FOLDER
# ============================================================

TEMP_FOLDER = Path(
    "telegram_temp"
)

TEMP_FOLDER.mkdir(
    exist_ok=True
)


# ============================================================
# TELEGRAM MESSAGE LIMIT
# ============================================================

MAX_MESSAGE_LENGTH = 3900


# ============================================================
# CLEAN AI TEXT
# ============================================================

def clean_text(text):

    if text is None:
        return ""

    text = str(text).strip()

    # Remove code blocks
    text = text.replace(
        "```json",
        ""
    )

    text = text.replace(
        "```JSON",
        ""
    )

    text = text.replace(
        "```",
        ""
    )

    # Remove Markdown bold
    text = text.replace(
        "**",
        ""
    )

    # Remove Markdown italic
    text = text.replace(
        "__",
        ""
    )

    # Remove backticks
    text = text.replace(
        "`",
        ""
    )

    # Remove HTML
    html_tags = [
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
    ]

    for tag in html_tags:

        text = text.replace(
            tag,
            ""
        )

    # Remove unnecessary quotation marks
    text = text.replace(
        '"',
        ""
    )

    text = text.replace(
        "“",
        ""
    )

    text = text.replace(
        "”",
        ""
    )

    # Clean excessive spaces
    while "  " in text:

        text = text.replace(
            "  ",
            " "
        )

    # Clean excessive blank lines
    while "\n\n\n" in text:

        text = text.replace(
            "\n\n\n",
            "\n\n"
        )

    return text.strip()


# ============================================================
# FORMAT IMAGE DESCRIPTION
# ============================================================

def format_image_description(data):

    if not isinstance(
        data,
        dict
    ):
        return (
            "The image could not be described."
        )

    visuals = clean_text(
        data.get(
            "visuals",
            "Not clearly visible."
        )
    )

    text = clean_text(
        data.get(
            "text",
            "Not clearly visible."
        )
    )

    body_text = clean_text(
        data.get(
            "body_text",
            "Not clearly visible."
        )
    )

    watermark = clean_text(
        data.get(
            "watermark",
            "Not clearly visible."
        )
    )

    interface = clean_text(
        data.get(
            "interface",
            "Not clearly visible."
        )
    )

    return (
        "👁️ VISUALS\n"
        f"{visuals}\n\n"

        "📝 TEXT\n"
        f"{text}\n\n"

        "📄 BODY TEXT\n"
        f"{body_text}\n\n"

        "🏷️ WATERMARK\n"
        f"{watermark}\n\n"

        "📱 INTERFACE\n"
        f"{interface}"
    )


# ============================================================
# FORMAT SOURCES
# ============================================================

def format_sources(sources):

    if not sources:

        return (
            "No reliable sources were returned."
        )

    if isinstance(
        sources,
        str
    ):

        return clean_text(
            sources
        )

    output = []

    count = 0

    for source in sources:

        if not isinstance(
            source,
            dict
        ):
            continue

        title = clean_text(
            source.get(
                "title",
                "Source"
            )
        )

        url = clean_text(
            source.get(
                "url",
                ""
            )
        )

        if not url:
            continue

        count += 1

        output.append(
            f"{count}. {title}\n"
            f"{url}"
        )

        if count >= 6:
            break

    if not output:

        return (
            "No reliable sources were returned."
        )

    return "\n\n".join(
        output
    )


# ============================================================
# CREATE VERIFICATION REPORT
# ============================================================

def create_report(result):

    # --------------------------------------------------------
    # SAFETY
    # --------------------------------------------------------

    if result is None:

        return (
            "❌ VERIFICATION FAILED\n\n"
            "The AI did not return a result."
        )

    # --------------------------------------------------------
    # IF RESULT IS JSON STRING
    # --------------------------------------------------------

    if isinstance(
        result,
        str
    ):

        try:

            result = json.loads(
                result
            )

        except Exception:

            return clean_text(
                result
            )

    # --------------------------------------------------------
    # CHECK DICT
    # --------------------------------------------------------

    if not isinstance(
        result,
        dict
    ):

        return clean_text(
            result
        )

    # --------------------------------------------------------
    # IMAGE DESCRIPTION
    # --------------------------------------------------------

    image_description = format_image_description(
        result.get(
            "what_is_in_image",
            {}
        )
    )

    # --------------------------------------------------------
    # CLAIM
    # --------------------------------------------------------

    main_claim = clean_text(
        result.get(
            "main_claim",
            "No clear factual claim was identified."
        )
    )

    # --------------------------------------------------------
    # VERDICT
    # --------------------------------------------------------

    verdict = clean_text(
        result.get(
            "verdict",
            "UNCERTAIN"
        )
    ).upper()

    if verdict == "TRUE":

        verdict_display = (
            "✅ TRUE"
        )

    elif verdict == "FALSE":

        verdict_display = (
            "❌ FALSE"
        )

    elif verdict == "MISLEADING":

        verdict_display = (
            "⚠️ MISLEADING"
        )

    else:

        verdict_display = (
            "⚠️ UNCERTAIN"
        )

    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    confidence = result.get(
        "confidence",
        0
    )

    try:

        confidence = float(
            confidence
        )

        confidence = max(
            0,
            min(
                100,
                confidence
            )
        )

        confidence_text = (
            f"{confidence:.0f}%"
        )

    except Exception:

        confidence_text = (
            "Not available"
        )

    # --------------------------------------------------------
    # REASON
    # --------------------------------------------------------

    reason = clean_text(
        result.get(
            "reason",
            "No reasoning was returned."
        )
    )

    # --------------------------------------------------------
    # EVIDENCE
    # --------------------------------------------------------

    evidence = clean_text(
        result.get(
            "evidence",
            ""
        )
    )

    # --------------------------------------------------------
    # CORRECT INFORMATION
    # --------------------------------------------------------

    correct_information = clean_text(
        result.get(
            "correct_information",
            "No corrected information was returned."
        )
    )

    # --------------------------------------------------------
    # SOURCES
    # --------------------------------------------------------

    sources = format_sources(
        result.get(
            "sources",
            []
        )
    )

    # --------------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------------

    report = (
        "🔎 FAKEBREAK VERIFICATION REPORT\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

        "🖼️ WHAT IS IN THE IMAGE?\n"
        "──────────────────────────\n\n"
        f"{image_description}\n\n"

        "📌 MAIN CLAIM\n"
        "──────────────────────────\n"
        f"{main_claim}\n\n"

        "⚖️ VERDICT\n"
        "──────────────────────────\n"
        f"{verdict_display}\n\n"

        "📊 CONFIDENCE\n"
        "──────────────────────────\n"
        f"{confidence_text}\n\n"

        "🧠 WHY?\n"
        "──────────────────────────\n"
        f"{reason}\n\n"
    )

    # Add evidence only when available
    if evidence:

        report += (
            "🔍 EVIDENCE\n"
            "──────────────────────────\n"
            f"{evidence}\n\n"
        )

    report += (
        "📖 CORRECT INFORMATION\n"
        "──────────────────────────\n"
        f"{correct_information}\n\n"

        "🔗 RELATED RELIABLE SOURCES\n"
        "──────────────────────────\n"
        f"{sources}\n\n"

        "⚠️ NOTE\n"
        "──────────────────────────\n"
        "This is an AI-assisted verification. "
        "Review the linked sources before making "
        "important decisions."
    )

    return clean_text(
        report
    )


# ============================================================
# SAFE TELEGRAM SENDER
# ============================================================

async def send_safe_message(
    update,
    text
):

    text = clean_text(
        text
    )

    if not text:

        text = (
            "No result was generated."
        )

    # --------------------------------------------------------
    # SPLIT LONG MESSAGE
    # --------------------------------------------------------

    while len(text) > MAX_MESSAGE_LENGTH:

        split_position = text.rfind(
            "\n",
            0,
            MAX_MESSAGE_LENGTH
        )

        if split_position <= 0:

            split_position = (
                MAX_MESSAGE_LENGTH
            )

        part = text[
            :split_position
        ].strip()

        await update.effective_message.reply_text(
            part,

            # IMPORTANT:
            # Plain text only.
            parse_mode=None,

            # No preview clutter.
            disable_web_page_preview=True
        )

        text = text[
            split_position:
        ].strip()

    # --------------------------------------------------------
    # SEND REMAINING TEXT
    # --------------------------------------------------------

    if text:

        await update.effective_message.reply_text(
            text,
            parse_mode=None,
            disable_web_page_preview=True
        )


# ============================================================
# START
# ============================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = (
        "👋 WELCOME TO FAKEBREAK\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"

        "🛡️ AI NEWS VERIFICATION BOT\n\n"

        "Send me a news image or screenshot.\n\n"

        "I will analyze:\n\n"

        "🖼️ What is in the image\n"
        "👁️ Visuals\n"
        "📝 Text\n"
        "📄 Body text\n"
        "🏷️ Watermark\n"
        "📱 Interface\n"
        "📌 Main claim\n"
        "⚖️ TRUE / FALSE / MISLEADING / UNCERTAIN\n"
        "📊 Confidence\n"
        "🧠 Reasoning\n"
        "📖 Correct information\n"
        "🔗 Related reliable sources\n\n"

        "📷 Send an image to begin."
    )

    await send_safe_message(
        update,
        message
    )


# ============================================================
# HELP
# ============================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = (
        "ℹ️ HOW TO USE FAKEBREAK\n\n"

        "📷 Upload a news image.\n\n"

        "The bot will understand the image, "
        "extract the claim and provide an "
        "AI-assisted verification report."
    )

    await send_safe_message(
        update,
        message
    )


# ============================================================
# IMAGE HANDLER
# ============================================================

async def handle_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    image_path = None

    try:

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        await send_safe_message(
            update,

            "🖼️ IMAGE RECEIVED!\n\n"

            "🔎 Step 1: Reading the image...\n"
            "📌 Step 2: Understanding the claim...\n"
            "🌐 Step 3: Checking available evidence...\n\n"

            "⏳ Please wait..."
        )

        # ----------------------------------------------------
        # GET PHOTO
        # ----------------------------------------------------

        photo = (
            update
            .effective_message
            .photo[-1]
        )

        # ----------------------------------------------------
        # TELEGRAM FILE
        # ----------------------------------------------------

        telegram_file = (
            await context.bot.get_file(
                photo.file_id
            )
        )

        # ----------------------------------------------------
        # TEMP FILE
        # ----------------------------------------------------

        message_id = (
            update
            .effective_message
            .message_id
        )

        image_path = (
            TEMP_FOLDER /
            f"image_{message_id}.jpg"
        )

        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        await telegram_file.download_to_drive(
            custom_path=str(
                image_path
            )
        )

        print(
            "[FakeBreak] Image downloaded:",
            image_path
        )

        # ----------------------------------------------------
        # CALL REALITY CHECKER
        # ----------------------------------------------------

        result = await asyncio.to_thread(
            check_news_image,
            str(image_path)
        )

        print(
            "[FakeBreak] AI result received."
        )

        print(
            result
        )

        # ----------------------------------------------------
        # CREATE REPORT
        # ----------------------------------------------------

        report = create_report(
            result
        )

        # ----------------------------------------------------
        # SEND REPORT
        # ----------------------------------------------------

        await send_safe_message(
            update,
            report
        )

    except Exception as error:

        print()
        print(
            "================================"
        )
        print(
            "FAKEBREAK TELEGRAM ERROR"
        )
        print(
            "================================"
        )

        print(
            error
        )

        traceback.print_exc()

        print(
            "================================"
        )

        error_message = (
            "❌ VERIFICATION FAILED\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

            "I could not complete the image "
            "verification.\n\n"

            "Please try the image again.\n\n"

            "Technical error:\n"
            f"{error}"
        )

        try:

            await send_safe_message(
                update,
                error_message
            )

        except Exception as send_error:

            print(
                "Telegram error message failed:",
                send_error
            )

    finally:

        # ----------------------------------------------------
        # DELETE TEMP IMAGE
        # ----------------------------------------------------

        try:

            if (
                image_path
                and image_path.exists()
            ):

                image_path.unlink()

                print(
                    "[FakeBreak] Temporary image deleted."
                )

        except Exception as cleanup_error:

            print(
                "Cleanup error:",
                cleanup_error
            )


# ============================================================
# TEXT HANDLER
# ============================================================

async def handle_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = (
        update
        .effective_message
        .text
        or ""
    ).strip()

    if not text:
        return

    message = (
        "📝 TEXT RECEIVED\n\n"

        "For news verification, please "
        "upload the screenshot or image.\n\n"

        "📷 Send an image to begin."
    )

    await send_safe_message(
        update,
        message
    )


# ============================================================
# ERROR HANDLER
# ============================================================

async def error_handler(
    update,
    context
):

    print(
        "\n========== TELEGRAM ERROR =========="
    )

    print(
        context.error
    )

    traceback.print_exception(
        type(context.error),
        context.error,
        context.error.__traceback__
    )

    print(
        "====================================\n"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print(
        "=============================================="
    )
    print(
        "             FAKEBREAK TELEGRAM BOT"
    )
    print(
        "=============================================="
    )

    # --------------------------------------------------------
    # TOKEN
    # --------------------------------------------------------

    if not BOT_TOKEN:

        print()
        print(
            "❌ TELEGRAM_BOT_TOKEN is missing."
        )

        print(
            "Add it to .env"
        )

        return

    print(
        "✅ Telegram token found."
    )

    print(
        "✅ RealityChecker imported."
    )

    print(
        "🖼️ Image analysis enabled."
    )

    print(
        "🛡️ Plain-text Telegram formatting enabled."
    )

    print(
        "✨ Clean report formatting enabled."
    )

    print()

    # --------------------------------------------------------
    # APPLICATION
    # --------------------------------------------------------

    application = (
        Application
        .builder()
        .token(
            BOT_TOKEN
        )
        .build()
    )

    # --------------------------------------------------------
    # COMMANDS
    # --------------------------------------------------------

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )

    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_image
        )
    )

    # --------------------------------------------------------
    # TEXT
    # --------------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND,
            handle_text
        )
    )

    # --------------------------------------------------------
    # ERRORS
    # --------------------------------------------------------

    application.add_error_handler(
        error_handler
    )

    # --------------------------------------------------------
    # START
    # --------------------------------------------------------

    print(
        "🚀 FAKEBREAK BOT IS RUNNING!"
    )

    print(
        "📷 Send an image from Telegram."
    )

    print(
        "Press Ctrl+C to stop."
    )

    print()

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()