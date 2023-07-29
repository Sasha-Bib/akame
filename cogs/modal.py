import disnake
from disnake.ext import commands

class RecruitmentModal(disnake.ui.Modal):
    def __init__(self, arg):
        self.arg = arg
        components = [
            disnake.ui.TextInput(label="Ваше имя.", placeholder="Введите ваше имя.", custom_id="name"),
            disnake.ui.TextInput(label="Ваш возраст", placeholder="Введите ваш возраст", custom_id="age")
        ]
        if self.arg == "moderator":
            title = "Набор на должность модератора."
        else:
            title = "Набор в банду **Akame**."
        super().__init__(title=title, components=components, custom_id="recruitmentModal")
        
    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        name = interaction.text_values["name"]
        age = interaction.text_values["age"]
        await interaction.response.send_message(f"Заявка отправлена!", ephemeral=True)
        channel = interaction.guild.get_channel(1043910785690247398)
        await channel.send(f"Заявка на должность {self.arg} от {name} {interaction.author.mention} ({age} лет)")

class RecruitementSelect(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Akame", value="akameuser", description="Участник банды **Akame**."),
            disnake.SelectOption(label="Модератор", value="moderator", description="Модератора сервера.")
        
        ]
        super().__init__(
            placeholder="Выберети желаемую роль.", options=options, min_values=0, max_values=1, custom_id="recruitment"
        )
        
    async def callback(self, interaction: disnake.MessageInteraction):
        if not interaction.values:
            await interaction.response.defer()
        else: 
            await interaction.response.send_modal(RecruitmentModal(interaction.values[0]))
            
class Recruitment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False    
    
    @commands.command()
    async def recruit(self, ctx):
        view = disnake.ui.View()
        view.add_item(RecruitementSelect())
        await ctx.send("Выбери желаемую роль", view=view)
        
        @commands.Cog.listener()
        async def on_connect(self):
            if self.persistents_views_added:
                return
            
        view = disnake.ui.View(timeout=None)
        view.add_item(RecruitementSelect())
        self.bot.add_view(view, message_id=1050105664611033168)
        
        
def setup(bot):
    bot.add_cog(Recruitment(bot))