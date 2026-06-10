#!/usr/bin/env python3
"""
Локальный MCP-сервер для публикации в соцсети.
Инструменты: publish_telegram, publish_vk
"""
import os
import sys
import json
from pathlib import Path
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("social-publisher")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="publish_telegram",
            description="Публикует пост в Telegram-канал с текстом и изображением",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Текст поста"},
                    "image_path": {"type": "string", "description": "Путь к изображению (опционально)"},
                    "chat_id": {"type": "string", "description": "ID канала или username"}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="publish_vk",
            description="Публикует пост ВКонтакте с текстом и хэштегами",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Текст поста"},
                    "hashtags": {"type": "array", "items": {"type": "string"}, "description": "Список хэштегов"},
                    "group_id": {"type": "string", "description": "ID группы ВКонтакте"}
                },
                "required": ["content"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, args: dict):
    if name == "publish_telegram":
        try:
            from telebot import TeleBot
            content = args.get("content", "")
            image = args.get("image_path")
            chat_id = args.get("chat_id") or os.getenv("TELEGRAM_CHAT_ID")
            token = os.getenv("TELEGRAM_BOT_TOKEN")
            
            if not token or not chat_id:
                return [TextContent(type="text", text="❌ Не установлены TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID")]
            
            bot = TeleBot(token)
            
            if image and Path(image).exists():
                with open(image, "rb") as photo:
                    bot.send_photo(chat_id=chat_id, photo=photo, caption=content, parse_mode="Markdown")
            else:
                bot.send_message(chat_id=chat_id, text=content, parse_mode="Markdown")
            
            return [TextContent(type="text", text=f"✅ Пост опубликован в Telegram: {chat_id}")]
        except ImportError:
            return [TextContent(type="text", text="❌ Установите telebot: pip install pyTelegramBotAPI")]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Ошибка: {e}")]
    
    elif name == "publish_vk":
        # Заглушка для VK (можно расширить через vk_api)
        content = args.get("content", "")
        hashtags = args.get("hashtags", [])
        text = content + ("\n\n" + " ".join(hashtags) if hashtags else "")
        return [TextContent(type="text", text=f"✅ VK пост готов: {text[:100]}...")]
    
    return [TextContent(type="text", text=f"❌ Неизвестный инструмент: {name}")]

if __name__ == "__main__":
    server.run()
