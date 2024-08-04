import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from gtts import gTTS
from datetime import datetime
import os
import asyncio
from collections import deque
from keep_alive import keep_alive
from discord.ui import Button, View
import random
from discord.ext import commands
os.system('clear')

class color():
    green = '\033[92m'
    pink = '\033[95m'
    red = '\33[91m'
    yellow = '\33[93m'
    blue = '\33[94m'
    gray = '\33[90m'
    reset = '\33[0m'
    bold = '\33[1m'
    italic = '\33[3m'
    unline = '\33[4m'

bot = commands.Bot(command_prefix=',', intents=discord.Intents.all())
bot.remove_command('help')
voice = None
playing = False
queue = deque()
keep_alive()

@bot.event
async def on_ready():
    print(f'{color.gray + color.bold}{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {color.blue}CONSOLE{color.reset}  {color.pink}discord.on_ready{color.reset} Đã đăng nhập bot {color.bold}{bot.user}{color.reset}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name='Bích Phương\'s playlist'))
  
@bot.command(name='join')
async def join(ctx):
    global voice

    if ctx.author.voice is None:
        await ctx.send('Tạo room voice chat đi bae ~')
        return

    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(ctx.author.voice.channel)
    else:
        voice = await ctx.author.voice.channel.connect()


@bot.command(name='s')
async def s(ctx, *, arg:str):
    global voice, playing

    if not arg:
        return

    if ctx.message.author.voice is None:
        await ctx.send('Tạo room voicechat đê!')
        return

    if ctx.guild.voice_client is None:
        try:
            voice = await ctx.message.author.voice.channel.connect()
        except Exception as e:
            print('error', e)
            return
    elif ctx.guild.voice_client.channel != ctx.message.author.voice.channel:
        await ctx.send('Đang ở room voice chat khác')
        return

    tts = gTTS(text=arg, lang='vi')
    tts.save('tts-audio.mp3')
    queue.append(('tts-audio.mp3', ctx))
    if not playing:
        await play_next()

async def play_next():
    global playing
    if queue:
        playing = True
        file, ctx = queue.popleft()
        voice.play(FFmpegPCMAudio(file), after=lambda e: asyncio.run_coroutine_threadsafe(play_next(), bot.loop))
        while voice.is_playing():
            await asyncio.sleep(1)
        os.remove(file)
        playing = False
    else:
        playing = False

@bot.command(name='leave')
async def leave(ctx):
    global voice, playing

    if ctx.guild.voice_client is None:
        await ctx.send('Bot không ở trong room này')
        return

    if voice is not None and voice.is_playing():
        voice.stop()

    await ctx.guild.voice_client.disconnect()
    voice = None
    playing = False
intents = discord.Intents.default()
intents.members = True

class ButtonView(View):
    def __init__(self, member):
        super().__init__(timeout=None)  # Đặt timeout thành None để View không bao giờ hết hạn
        self.member = member

    @discord.ui.button(label="Vẫy tay để chào", style=discord.ButtonStyle.secondary, emoji="👋", custom_id="greet_button")
    async def greet_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Kiểm tra nếu người dùng có role cần thiết
        required_role_id = 1268943736516378719
        if any(role.id == required_role_id for role in interaction.user.roles):
            # Danh sách các đường link sticker hoặc ảnh
            sticker_urls = [
                'https://cdn.discordapp.com/attachments/1269438411874504825/1269438464735187058/Screenshot_2024-08-01_051622.png?ex=66b01033&is=66aebeb3&hm=abee1e0d7c3a643788154946cf376f7610a86f3fec44bc908047d37aa81bc96f&',
                'https://media.discordapp.net/attachments/1269438411874504825/1269611938086785096/xinchao.gif?ex=66b0b1c2&is=66af6042&hm=4f99beb292444786dac861a94ace3616225a393b5c4db70faac11d797d075a26&=',
                'https://media.discordapp.net/attachments/1269438411874504825/1269611936870301757/xinchao3.gif?ex=66b0b1c1&is=66af6041&hm=7c551746a992f238df9d6bd3b989720cc7c8d0d95d1c6741d993e985d1c608b8&=',
                'https://media.discordapp.net/attachments/1269438411874504825/1269611936492818432/xinchao4.gif?ex=66b0b1c1&is=66af6041&hm=5801da56594ca8bf9c7d2a72d612facb314c30818a659050d0afa0f27bc46aa2&=',
                'https://media.discordapp.net/attachments/1269438411874504825/1269611936056873000/xinchao5.gif?ex=66b0b1c1&is=66af6041&hm=1cf59216361ad476f207f78c7ffc417f9a8000583f756c153ec9c5fe04b2a939&=',
                'https://media.discordapp.net/attachments/1269438411874504825/1269611935695896627/xinchao6.gif?ex=66b0b1c1&is=66af6041&hm=f210cfd46eb07c75278353d02fcdfc12dd8a5ea5ed0a602f80583d8207066f16&=',
                'https://media.discordapp.net/attachments/1269438411874504825/1269611935091921007/xinchao8.gif?ex=66b0b1c1&is=66af6041&hm=9f6a8c0802b1112f8e3bb5f4e5f027d4b5d1427015367cf3f6287db184eca165&=',
                'https://media.discordapp.net/attachments/1269438411874504825/1269611933921706156/xinchao7.gif?ex=66b0b1c1&is=66af6041&hm=9a7db583b304cf5663d5c5705ad71f293a298209ac593176031ce2a913e344db&=',
                'https://media.discordapp.net/attachments/1269438411874504825/1269611937470353448/xinchao2.gif?ex=66b0b1c2&is=66af6042&hm=1558bc13b5a9cd5be3e612f3a3205bc4a41329e4d3b3f0da384f42d81e3947cb&='
            ]
            # Danh sách các câu chào
            greetings = [
                f"Xin chào {self.member.mention}<a:lkn2:1269636424785723473>, thật vui vì bạn đã ở đây <a:lkn1:1269635885352226816>. Mình là {interaction.user.mention} thuộc bộ phận <@&1268943736516378719> <:lkn3:1269641694521856143> của server, rất vui được làm quen với bạn<a:lkn4:1269641958738100306>",
                f"Rất vui được đón tiếp bạn {self.member.mention}<a:lkn5:1269648486190551160>. Mình là {interaction.user.mention} thuộc bộ phận <@&1268943736516378719> <:lkn3:1269641694521856143> của server, cần giúp đỡ gọi mình nhé",
                f"Heyy {self.member.mention}<a:lkn5:1269648486190551160>, đập tay cái nào <a:lkn1:1269635885352226816>. Tớ là {interaction.user.mention} and nice to meet u bae~ <a:lkn6:1269649714484219987>"
            ]
            # Danh sách các câu ngẫu nhiên
            random_messages = [
                "Wishing you endless joy and laughter!",
                "May your days be filled with happiness and smiles.",
                "Hoping you always find reasons to smile.",
                "Sending you all the positive vibes for a happy life!",
                "May your life be as bright and cheerful as your smile.",
                "Here’s to a life full of joy and unforgettable moments!",
                "May happiness follow you wherever you go.",
                "Hope your days are filled with sunshine and joy.",
                "Wishing you a life full of laughter and love.",
                "May every day bring you a reason to smile."
            ]

            # Chọn ngẫu nhiên một đường link từ danh sách
            sticker_url = random.choice(sticker_urls)

            # Chọn ngẫu nhiên một câu chào từ danh sách
            greeting_message = random.choice(greetings)

            # Chọn ngẫu nhiên một câu ngẫu nhiên từ danh sách
            random_message = random.choice(random_messages)

            await interaction.response.send_message(
                content=greeting_message,
                embed=discord.Embed(
                    description=f"_**{random_message}**_ <a:lkn6:1269649714484219987>",
                    color=discord.Color.yellow()
                ).set_image(url=sticker_url)
            )
        else:
            await interaction.response.send_message(
                content="Chức năng này chỉ dành cho đội nghi lễ tiếp khách",
                ephemeral=True
            )

@bot.event
async def on_member_join(member):
    guild = member.guild
    welcome_channel = bot.get_channel(1154671456383414342)  # Sử dụng ID kênh cụ thể

    # Danh sách các câu chào mừng
    greetings = [
        f'Xin chào {member.mention}<a:lkn7:1269692492790501417>, cậu vừa gia nhập vào máy chủ {guild.name}<a:lkn8:1269693064876789873>,<@&1268943736516378719> <:lkn3:1269641694521856143> tiếp đón bạn nha <a:lkn9:1269693404099379242>',
    ]

    greeting_message = greetings[0]
    # Tạo embed màu đỏ không có tiêu đề
    embed = discord.Embed(
        description=greeting_message,
        color=discord.Color.red()  # Màu đỏ
    )

    # Kiểm tra nếu thành viên có avatar
    if member.avatar:
        # Thêm ảnh đại diện của thành viên vào embed
        embed.set_thumbnail(url=member.avatar.url)

    # Kiểm tra xem kênh có tồn tại không
    if welcome_channel is not None:
        # Tạo và gửi view với nút, truyền thông tin về thành viên mới vào
        view = ButtonView(member)
        await welcome_channel.send(embed=embed, view=view)
bot.run(os.environ.get('TOKEN'))
