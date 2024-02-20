from aiogram import Router

from Services.tgBot.handlers import user_handlers, admin_handlers


def get_routers() -> list[Router]:
    return [
        user_handlers.router,
        admin_handlers.router
    ]
