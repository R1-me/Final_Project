import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from utils.tmdb_client import search_media, get_random_recommendation
from utils.data_manager import save_favorite, get_favorites, remove_favorite

BOT_TOKEN = "8947889804:AAHGoRUtTy2MC7eEME79jGip_c-4vOJo460"

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

# Dictionary to handle user states (waiting for text input... etc... :-) )
user_states = {}

# HELPER FUNCS
def get_movie_keyboard(title: str):
    "Generates an inline keyboard with an (Add to Favorites) button"
    callback_data = f"fav_{title[:30]}"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❤️ Add to Favorites", callback_data=callback_data)]
    ])
    return keyboard

async def perform_search(message: types.Message, query: str):
    "Executes the search logic and formats the output"
    await message.answer(f"🔍 Searching for '{query}'...")
    try:
        media = search_media(query)

        if media:
            keyboard = get_movie_keyboard(media.title)

            if media.poster_url:
                await message.answer_photo(photo=media.poster_url, caption=media.get_info(), reply_markup=keyboard)
            else:
                await message.answer(media.get_info(), reply_markup=keyboard)
        else:
            await message.answer("❌ Media not found. Please try another title")

    except Exception as e:
        # Fallback logging for debugging purposes
        print(f"ERROR IN PERFORM_SEARCH: {e}")
        await message.answer("⚠️ An internal error occurred while formatting the movie data")


#COMMAND HANDLERS
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    "Handler for the /start command"
    welcome_text = (
        "🍿 Welcome to the Movie Recommendation Bot!\n\n"
        "Here is what I can do:\n"
        "• `/search` - Find a movie or series\n"
        "• `/random` - Get a random trending movie/series\n"
        "• `/favorites` - View your favorite list\n"
        "• `/remove` - Remove a movie/series from favorites"
    )
    await message.answer(welcome_text)

@dp.message(Command("search"))
async def cmd_search(message: types.Message):
    "Handles the user search request"
    command_parts = message.text.split(maxsplit=1)

    if len(command_parts) < 2:
        user_states[message.from_user.id] = "waiting_for_movie_name"
        await message.answer("🍿 Please enter the name of the movie or series:")
        return

    await perform_search(message, command_parts[1])

@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    "Provides a random media recommendation"
    await message.answer("🎲 Finding a great movie/series for you...")
    media = get_random_recommendation()

    if media:
        keyboard = get_movie_keyboard(media.title)
        if media.poster_url:
            await message.answer_photo(photo=media.poster_url, caption=f"🎲 *Random Recommendation:*\n\n{media.get_info()}", reply_markup=keyboard)
        else:
            await message.answer(f"🎲 *Random Recommendation:*\n\n{media.get_info()}", reply_markup=keyboard)
    else:
        await message.answer("❌ Could not fetch a random movie right now.")

@dp.message(Command("favorites"))
async def cmd_favorites(message: types.Message):
    "Retrieves and displays the user's favorite list"
    try:
        user_id = str(message.from_user.id)
        favorites = get_favorites(user_id)

        if not favorites:
            await message.answer("Your favorites list is empty! Search for a movie and click '❤️ Add to Favorites'.")
            return

        response = "⭐ *Your Favorite Movies:*\n\n"
        for i, fav in enumerate(favorites, 1):
            # Clean title to prevent Telegram Markdown parsing errors
            clean_fav = fav.replace("*", "").replace("_", "").replace("`", "")
            response += f"{i}. {clean_fav}\n"

        await message.answer(response)
    except Exception as e:
        print(f"ERROR IN CMD_FAVORITES: {e}")
        await message.answer("⚠️ An error occurred while formatting your favorites list.")

async def perform_remove(message: types.Message, movie_title: str):
    "Executes the remove logic safely"
    user_id = str(message.from_user.id)
    success = remove_favorite(user_id, movie_title)

    if success:
        await message.answer(f"🗑️ '{movie_title}' has been removed from your favorites.")
    else:
        await message.answer(f"⚠️ '{movie_title}' was not found in your favorites. Check the exact spelling in /favorites.")

@dp.message(Command("remove"))
async def cmd_remove(message: types.Message):
    "Handles the removal of an item from favorites"
    command_parts = message.text.split(maxsplit=1)

    if len(command_parts) < 2:
        user_states[message.from_user.id] = "waiting_for_remove_title"
        await message.answer("🗑️ Please enter the exact name of the movie or series you want to remove:")
        return

    await perform_remove(message, command_parts[1])

#callback and text handlers

@dp.callback_query(F.data.startswith("fav_"))
async def handle_favorite_callback(callback: CallbackQuery):
    "Catches the inline button press and saves the movie"
    movie_title = callback.data[4:]
    user_id = str(callback.from_user.id)

    success = save_favorite(user_id, movie_title)

    if success:
        await callback.answer(f"✅ '{movie_title}' added to favorites!", show_alert=False)
    else:
        await callback.answer("❌ Error saving to favorites.", show_alert=True)

@dp.message(F.text)
async def handle_regular_text(message: types.Message):
    "Routes regular text messages based on the current user state"
    user_id = message.from_user.id
    current_state = user_states.get(user_id)

    if current_state == "waiting_for_movie_name":
        user_states[user_id] = None
        await perform_search(message, message.text)

    elif current_state == "waiting_for_remove_title":
        user_states[user_id] = None
        await perform_remove(message, message.text)

    else:
        await message.answer("I only understand commands. Please use the Menu!")


async def main():
    "Main function to start the bot polling"
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())