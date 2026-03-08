from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
from nova.database.repository import (
    get_user_by_telegram_id,
    create_user,
    get_graph_state,
    update_graph_state,
    save_message,
)
from nova.agent.orchestrator import process_message
from nova.utils.logging import get_logger

logger = get_logger(__name__)

# Conversation states
NAME, WEIGHT, HEIGHT = range(3)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the /start command and initiate onboarding if needed."""
    user = update.effective_user
    if not user:
        return ConversationHandler.END

    telegram_id = user.id
    db_user = get_user_by_telegram_id(telegram_id)

    if db_user:
        await update.message.reply_text(
            f"Welcome back to N.O.V.A., {db_user.name or 'Operator'}. Systems are online. What's our next objective?"
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "Initializing N.O.V.A. Agent Protocol...\n\n"
        "Welcome, operator. To properly calculate your HP and Stamina metrics, "
        "I need some baseline data.\n\n"
        "What is your preferred Name/Callsign?"
    )
    return NAME


async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store the user's name and ask for weight."""
    context.user_data["name"] = update.message.text
    await update.message.reply_text(
        "Acknowledged. What is your current weight (in kg)?"
    )
    return WEIGHT


async def handle_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store weight and ask for height."""
    text = update.message.text
    try:
        weight = float(text)
        context.user_data["weight"] = weight
    except ValueError:
        await update.message.reply_text(
            "Invalid input. Please provide a numerical value for your weight (e.g., 80.5):"
        )
        return WEIGHT

    await update.message.reply_text("Logged. Finally, what is your height (in cm)?")
    return HEIGHT


async def handle_height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store height and finalize registration."""
    text = update.message.text
    try:
        height = float(text)
        context.user_data["height"] = height
    except ValueError:
        await update.message.reply_text(
            "Invalid input. Please provide a numerical value for your height (e.g., 180):"
        )
        return HEIGHT

    user = update.effective_user
    if not user:
        return ConversationHandler.END

    telegram_id = user.id
    name = context.user_data.get("name")
    weight = context.user_data.get("weight")

    try:
        create_user(telegram_id=telegram_id, name=name, weight=weight, height=height)
        logger.info(f"New user registered: {telegram_id} - {name}")
        await update.message.reply_text(
            f"Registration complete, {name}. Profile synchronized. "
            "I am N.O.V.A., your gamified health and longevity AI. Send a message to begin tracking."
        )
    except Exception as e:
        logger.error(f"Failed to register user: {e}")
        await update.message.reply_text(
            "A system error occurred during registration. Please try /start again later."
        )

    return ConversationHandler.END


async def cancel_onboarding(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the onboarding conversation."""
    await update.message.reply_text(
        "Onboarding canceled. Type /start to initialize your profile when ready."
    )
    return ConversationHandler.END


async def handle_text_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle standard text messages and route to LangGraph."""
    user = update.effective_user
    if not user or not update.message or not update.message.text:
        return

    text = update.message.text
    chat_id = update.effective_chat.id
    is_private = update.effective_chat.type == "private"
    chat_context = "private" if is_private else str(chat_id)

    logger.debug(
        f"Received message payload in chat_id: {chat_id}, type: {update.effective_chat.type}, thread_id: {update.message.message_thread_id}"
    )

    # Group chat explicitly requires bot mention
    if not is_private:
        bot_username = context.bot.username
        mention = f"@{bot_username}"
        if mention not in text:
            return  # Ignore messages not mentioning the bot

        logger.debug(
            f"Mention detected in chat_id: {chat_id}, thread_id: {update.message.message_thread_id}"
        )

        # Strip the mention out so the LLM doesn't read it
        text = text.replace(mention, "").strip()
        if not text:
            await update.message.reply_text("Operator, how can I assist you?")
            return

    db_user = get_user_by_telegram_id(user.id)
    if not db_user:
        await update.message.reply_text(
            "Operator not recognized. Please use /start to initialize your profile."
        )
        return

    # Save incoming message
    save_message(
        user_id=db_user.id, content=text, role="user", chat_context=chat_context
    )

    # Get state
    db_state = get_graph_state(db_user.id)

    try:
        response, new_history = process_message(db_user, text, db_state)

        # Save updated state
        update_graph_state(
            user_id=db_user.id,
            current_message=text,
            chat_history=new_history,
            current_step="completed",
        )

        # Save outgoing message
        save_message(
            user_id=db_user.id,
            content=response,
            role="assistant",
            chat_context=chat_context,
        )

        # T020 routing directly to chat_id
        send_kwargs = {"chat_id": chat_id, "text": response}
        if update.message.message_thread_id:
            send_kwargs["message_thread_id"] = update.message.message_thread_id

        logger.debug(
            f"Routing response to chat_id: {chat_id}, thread_id: {update.message.message_thread_id}"
        )
        await context.bot.send_message(**send_kwargs)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await context.bot.send_message(
            chat_id=chat_id,
            text="N.O.V.A system error. Connection to cognitive core failed.",
        )


async def handle_non_text_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Fallback for non-text messages."""
    await update.message.reply_text(
        "N.O.V.A currently only processes text-based communications."
    )


def register_handlers(app: Application) -> None:
    """Register bot handlers with the application."""
    onboarding_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)],
            WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_weight)],
            HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_height)],
        },
        fallbacks=[CommandHandler("cancel", cancel_onboarding)],
    )
    app.add_handler(onboarding_handler)

    # Standard text messages
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message)
    )

    # Non-text messages
    app.add_handler(
        MessageHandler(~filters.TEXT & ~filters.COMMAND, handle_non_text_message)
    )
