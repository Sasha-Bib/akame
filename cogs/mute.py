import datetime

import disnake
from disnake.ext import commands

class Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.slash_command(name='mute', description='Выдать мут участнику.')
    async def mute(self, interaction, member: disnake.Member, time: str, reason: str):
        time = datetime.datetime.now() + datetime.timedelta(minutes=int(time))
        await member.timeout(reason=reason, until=time)
        cool_time = disnake.utils.format_dt(time, style="R")
        embed = disnake.Embed(description=f'**{member.mention} получил мут и сможет писать {cool_time}.**', title='Модерация', color=0x2f3136)
        embed.add_field(name='Причина', value=f'{reason}', inline=True)
        embed.add_field(name='Модератор', value=f'{interaction.author.mention}', inline=True)
        channel = interaction.bot.get_channel(1043910785690247398)
        await channel.send(embed=embed)
        embed1 = disnake.Embed(description=f'**{member.mention} был выдан мут на {time} минут.**/nВся информация в {channel.mention}', title='Модерация', color=0x2f3136)
        await interaction.response.send_message(embed=embed1, ephemeral=True)
    
    
    @commands.slash_command(name='unmute', description="Размутить участника.")
    async def unmute(self, interaction, member: disnake.Member):
         await member.timeout(reason=None, until=None)
         await interaction.response.send_message(f"Размучен {member.mention}", ephemeral=True)
            
def setup(bot):
    bot.add_cog(Timeout(bot))