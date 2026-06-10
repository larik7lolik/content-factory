Архитектура Content Factory
Обзор
Content Factory — мультиагентная система на базе OpenCode со скилл-ориентированной архитектурой. Специализация: вайб-маркетологи в EdTech, продвигающие онлайн-школы и репетиторов иностранных языков.
Компоненты
1. Оркестратор (content-factory Skill)
Файл: .opencode/skills/content-factory/SKILL.md
Координирует 4 субагентов, валидирует входные данные, управляет потоком выполнения.
2. Субагенты
@researcher — сбор фактов из веба (webfetch, bash)
@content-writer — создание контента для 5 платформ с адаптацией под Tone of Voice
@image-creator — генерация обложек через gpt-image-2
@publisher — публикация через MCP-сервер или Telegram Bot API
3. MCP-сервер (social_publisher)
Файл: scripts/social_mcp.py
Локальный сервер, предоставляющий инструменты publish_telegram и publish_vk.
Поток данных
User Input → content-factory → @researcher → @content-writer → @image-creator → @publisher → Telegram/VK/Дзен
Производительность
Время выполнения: 3-5 минут
Токенов на пайплайн: ~10-15K
Стоимость: ~$0.10-0.20 за пост
