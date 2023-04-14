from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeChatAdministrators
from configs import config

async def set_commands(bot: Bot):
    await set_custom_commands(bot)
    await set_schedule_commands(bot)
    await set_crud_commands(bot)

async def set_custom_commands(bot: Bot):
    custom_commands = [
        BotCommand(command="start", description="Start of the bot"),
        BotCommand(command="schedule", description="Today's schedule")
    ]
    return await bot.set_my_commands(custom_commands, scope=BotCommandScopeDefault())


async def set_crud_commands(bot: Bot):
    crud_commands = [
        BotCommand(command="start", description="Start of the bot"),
        BotCommand(command="schedule", description="Today's schedule"),
        BotCommand(command="change",description="Change a day schedule"),
        BotCommand(command="update",description="Update a lesson"),
        BotCommand(command="add",description="Add a new lesson"),
        BotCommand(command="delete",description="Delete a lesson"),
        BotCommand(command="clear",description="Delete all lessons")
    ]
    
    return await bot.set_my_commands(
        crud_commands, 
        scope=BotCommandScopeAllPrivateChats()
    )
    
async def set_schedule_commands(bot: Bot):
    schedule_commands = [
        BotCommand(command="start", description="Start of the bot"),
        BotCommand(command="schedule", description="Today's schedule"),
        BotCommand(command="on",description="On notifications"),
        BotCommand(command="off",description="Off notifications")
    ]

    return bot.set_my_commands(
        schedule_commands, 
        scope=BotCommandScopeChatAdministrators(chat_id=config.chat_id)
    )