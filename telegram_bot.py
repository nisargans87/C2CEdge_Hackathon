import os
import asyncio

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
# START COMMAND
# ============================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = """
👋 Welcome to FakeBreak!

🛡️ AI News Verification Bot

Send me a news image or screenshot.

I will check:

1️⃣ What is actually shown in the image

2️⃣ What factual claim is being made

3️⃣ Whether the claim is TRUE, FALSE,
   or UNCERTAIN

4️⃣ Why the verdict was given

5️⃣ What the correct information is

6️⃣ Related reliable sources

📌 Send an image to begin.
"""

    await update.message.reply_text(
        message
    )


# ============================================================
# FORMAT VERIFICATION RESULT
# ============================================================

def format_verification_result(
    result
):

    if not result:

        return (
            "⚠️ No verification result was returned."
        )

    image_description = result.get(
        "image_description",
        "Not available"
    )

    claim = result.get(
        "detected_claim",
        "Not available"
    )

    verdict = result.get(
        "verdict",
        "UNCERTAIN"
    )

    confidence = result.get(
        "confidence",
        0
    )

    reasoning = result.get(
        "reasoning",
        "Not available"
    )

    correct_information = result.get(
        "correct_information",
        "Not available"
    )

    sources = result.get(
        "sources",
        []
    )

    # --------------------------------------------------------
    # VERDICT ICON
    # --------------------------------------------------------

    if verdict == "TRUE":

        verdict_display = (
            "✅ TRUE"
        )

    elif verdict == "FALSE":

        verdict_display = (
            "❌ FALSE"
        )

    else:

        verdict_display = (
            "⚠️ UNCERTAIN"
        )

    # --------------------------------------------------------
    # MAIN REPORT
    # --------------------------------------------------------

    response = (
        "🔎 FAKEBREAK VERIFICATION REPORT\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"

        "🖼️ WHAT IS IN THE IMAGE?\n"
        f"{image_description}\n\n"

        "📌 MAIN CLAIM\n"
        f"{claim}\n\n"

        "⚖️ VERDICT\n"
        f"{verdict_display}\n\n"

        "📊 CONFIDENCE\n"
        f"{confidence}%\n\n"

        "🧠 WHY?\n"
        f"{reasoning}\n\n"

        "📖 CORRECT INFORMATION\n"
        f"{correct_information}\n"
    )

    # --------------------------------------------------------
    # SOURCES
    # --------------------------------------------------------

    if sources:

        response += (
            "\n🔗 RELATED RELIABLE SOURCES\n"
        )

        for index, source in enumerate(
            sources[:5],
            start=1
        ):

            if isinstance(
                source,
                dict
            ):

                title = source.get(
                    "title",
                    "Source"
                )

                url = source.get(
                    "url",
                    ""
                )

                source_type = source.get(
                    "source_type",
                    "Source"
                )

                response += (
                    f"\n{index}. {title}\n"
                    f"   {source_type}\n"
                    f"   {url}\n"
                )

            else:

                response += (
                    f"\n{index}. {source}\n"
                )

    else:

        response += (
            "\n🔗 RELATED SOURCES\n"
            "No reliable sources were returned."
        )

    # --------------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------------

    response += (
        "\n\n⚠️ NOTE\n"
        "This is an AI-assisted verification. "
        "Always review the linked sources before "
        "making important decisions."
    )

    return response


# ============================================================
# HANDLE IMAGE
# ============================================================

async def handle_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = update.message

    await message.reply_text(
        "🖼️ Image received!\n\n"
        "🔍 Step 1: Reading the image...\n"
        "🔎 Step 2: Checking the claim...\n"
        "🌐 Step 3: Checking reliable web sources...\n\n"
        "⏳ Please wait..."
    )

    image_path = None

    try:

        # ----------------------------------------------------
        # GET HIGHEST QUALITY TELEGRAM IMAGE
        # ----------------------------------------------------

        photo = message.photo[-1]

        telegram_file = (
            await context.bot.get_file(
                photo.file_id
            )
        )

        # ----------------------------------------------------
        # UNIQUE TEMP FILE
        # ----------------------------------------------------

        image_path = (
            f"telegram_"
            f"{message.chat_id}_"
            f"{message.message_id}.jpg"
        )

        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        await telegram_file.download_to_drive(
            image_path
        )

        print(
            "Image downloaded:",
            image_path
        )

        # ----------------------------------------------------
        # CALL REALITYCHECKER
        # ----------------------------------------------------

        result = await asyncio.to_thread(
            check_news_image,
            image_path
        )

        # ----------------------------------------------------
        # FORMAT RESULT
        # ----------------------------------------------------

        result_text = (
            format_verification_result(
                result
            )
        )

        # ----------------------------------------------------
        # TELEGRAM MESSAGE LIMIT
        # ----------------------------------------------------

        if len(result_text) > 4000:

            # Send first part
            await message.reply_text(
                result_text[:3900]
                + "\n\n[Report continues...]"
            )

            remaining = result_text[3900:]

            while remaining:

                chunk = remaining[:3900]

                remaining = remaining[3900:]

                await message.reply_text(
                    chunk
                )

        else:

            await message.reply_text(
                result_text
            )

    except Exception as error:

        print("\nBOT ERROR:")
        print(error)

        await message.reply_text(
            "❌ I could not complete the "
            "verification.\n\n"
            "Please try the image again.\n\n"
            f"Technical error: {error}"
        )

    finally:

        # ----------------------------------------------------
        # DELETE TEMPORARY IMAGE
        # ----------------------------------------------------

        if (
            image_path
            and os.path.exists(
                image_path
            )
        ):

            os.remove(
                image_path
            )

            print(
                "Temporary image deleted."
            )


# ============================================================
# HANDLE IMAGE SENT AS DOCUMENT
# ============================================================

async def handle_document(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    document = update.message.document

    if not document.mime_type:

        await update.message.reply_text(
            "❌ I could not identify this file."
        )

        return

    if not document.mime_type.startswith(
        "image/"
    ):

        await update.message.reply_text(
            "❌ Please send an image file."
        )

        return

    await update.message.reply_text(
        "📁 Image file received!\n\n"
        "🔎 Starting verification..."
    )

    image_path = None

    try:

        telegram_file = (
            await context.bot.get_file(
                document.file_id
            )
        )

        extension = "jpg"

        if (
            document.file_name
            and "." in document.file_name
        ):

            extension = (
                document.file_name
                .split(".")[-1]
                .lower()
            )

        image_path = (
            f"telegram_document_"
            f"{update.message.chat_id}_"
            f"{update.message.message_id}."
            f"{extension}"
        )

        await telegram_file.download_to_drive(
            image_path
        )

        result = await asyncio.to_thread(
            check_news_image,
            image_path
        )

        result_text = (
            format_verification_result(
                result
            )
        )

        if len(result_text) > 4000:

            result_text = (
                result_text[:3900]
                + "\n\n[Report shortened]"
            )

        await update.message.reply_text(
            result_text
        )

    except Exception as error:

        print(
            "DOCUMENT ERROR:",
            error
        )

        await update.message.reply_text(
            "❌ Verification failed.\n\n"
            f"{error}"
        )

    finally:

        if (
            image_path
            and os.path.exists(
                image_path
            )
        ):

            os.remove(
                image_path
            )


# ============================================================
# HANDLE TEXT
# ============================================================

async def handle_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    await update.message.reply_text(
        "📝 I received your text:\n\n"
        f"\"{text}\"\n\n"
        "🖼️ Image verification is currently "
        "enabled.\n\n"
        "Please send the news screenshot/image."
    )


# ============================================================
# MAIN
# ============================================================

def main():

    if not BOT_TOKEN:

        print(
            "❌ TELEGRAM_BOT_TOKEN is missing "
            "from .env"
        )

        return

    print(
        "===================================="
    )

    print(
        "       FAKEBREAK TELEGRAM BOT"
    )

    print(
        "===================================="
    )

    print(
        "🤖 Starting bot..."
    )

    print(
        "🧠 Verification engine: Gemini"
    )

    print(
        "🌐 Web grounding: Google Search"
    )

    print(
        "🖼️ Image verification: ENABLED"
    )

    print(
        "===================================="
    )

    application = (
        Application
        .builder()
        .token(
            BOT_TOKEN
        )
        .build()
    )

    # --------------------------------------------------------
    # /start
    # --------------------------------------------------------

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    # --------------------------------------------------------
    # NORMAL PHOTOS
    # --------------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_image
        )
    )

    # --------------------------------------------------------
    # IMAGE FILES
    # --------------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.Document.IMAGE,
            handle_document
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

    print(
        "✅ FakeBreak is running!"
    )

    print(
        "📱 Send an image to your Telegram bot."
    )

    # --------------------------------------------------------
    # START TELEGRAM
    # --------------------------------------------------------

    application.run_polling()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()