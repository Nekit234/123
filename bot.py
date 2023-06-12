import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

applications = {}  # Словарь для хранения поданных заявок

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def apply(ctx):
    # Проверка, была ли уже подана заявка от пользователя
    if ctx.author.id in applications:
        await ctx.send('Вы уже подали заявку.')
        return

    # Удаление команды из отправленного сообщения
    content = ctx.message.content.replace('!apply', '')

    # Код заявки

    # Удаление сообщения пользователя
    await ctx.message.delete()

    # Создание канала заявки, если нет активной заявки
    if ctx.author.id not in applications.values():
        guild = ctx.guild
        category = discord.utils.get(guild.categories, name='Заявки')
        if not category:
            category = await guild.create_category('Заявки')

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await category.create_text_channel(f'заявка-{ctx.author.name}', overwrites=overwrites)

        # Отправка сообщения в канал заявки
        message_content = f'Новая заявка от {ctx.author.mention}:\n\n{content}'
        message = await channel.send(message_content)

        applications[ctx.author.id] = channel.id  # Сохранение информации о заявке
    else:
        await ctx.send('У вас уже есть активная заявка.')

@bot.command()
async def clear(ctx, amount: int):
    # Проверка разрешений пользователя
    if not ctx.author.guild_permissions.administrator:
        await ctx.send('У вас недостаточно прав для выполнения этой команды.')
        return

    # Удаление сообщений
    await ctx.channel.purge(limit=amount + 1)  # +1 для удаления самой команды

    # Отправка подтверждающего сообщения
    await ctx.send(f'Удалено {amount} сообщений.')



@bot.command()
async def ban(ctx, member: discord.Member):
    await ctx.guild.ban(member)
    await ctx.send(f'{member.name} был забанен.')

@bot.command()
async def kick(ctx, member: discord.Member):
    await ctx.guild.kick(member)
    await ctx.send(f'{member.name} был кикнут.')

@bot.command()
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.add_roles(role)
    await ctx.send(f'{member.name} был замучен.')

@bot.command()
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(role)
    await ctx.send(f'{member.name} был размучен.')

bot.run('MTExNzUwNjg2MTQ1ODAxMDEzMg.G7OEZ3.zo6eaDpkHoA-n4S7vyDSy7j-3dLa8fj2IuUz50')

