import discord
from discord.ext import commands
from discord import app_commands
import lyricsgenius
import os
import asyncio


genius = lyricsgenius.Genius(
    os.getenv("GENIUS_TOKEN"),
    timeout=10,
    retries=2,
    remove_section_headers=True
)

class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ────────────────────────────────────────────
    # SLASH COMMAND: /lyrics
    # ────────────────────────────────────────────
    @app_commands.command(name="lyrics", description="Tra lời bài hát")
    @app_commands.describe(
        bai_hat="Tên bài hát",
        ca_si="Tên ca sĩ (không bắt buộc)"
    )
    async def lyrics_slash(
        self,
        interaction: discord.Interaction,
        bai_hat: str,
        ca_si: str = None
    ):
        await interaction.response.defer()  # Bot đang xử lý...
        await self._send_lyrics(interaction, bai_hat, ca_si, is_slash=True)

    # ────────────────────────────────────────────
    # PREFIX COMMAND: !lyrics
    # ────────────────────────────────────────────
    @commands.command(name="lyrics", aliases=["loi", "l"])
    async def lyrics_prefix(self, ctx, *, query: str):
        """
        Cách dùng:
          !lyrics Shape of You
          !lyrics Nơi này có anh - Sơn Tùng
        """
        # Tách tên bài và ca sĩ nếu có dấu -
        if "-" in query:
            parts = query.split("-", 1)
            bai_hat = parts[0].strip()
            ca_si = parts[1].strip()
        else:
            bai_hat = query.strip()
            ca_si = None

        async with ctx.typing():  # Hiển thị "Bot đang gõ..."
            await self._send_lyrics(ctx, bai_hat, ca_si, is_slash=False)

    # ────────────────────────────────────────────
    # HÀM XỬ LÝ CHUNG
    # ────────────────────────────────────────────
    async def _send_lyrics(self, ctx_or_interaction, bai_hat, ca_si, is_slash):
        try:
            # Tìm kiếm bài hát (chạy trong thread riêng để không block bot)
            loop = asyncio.get_event_loop()
            song = await loop.run_in_executor(
                None,
                lambda: genius.search_song(bai_hat, ca_si)
            )

            if not song:
                embed = discord.Embed(
                    title="❌ Không tìm thấy",
                    description=f"Không tìm thấy lời bài **{bai_hat}**"
                                + (f" của **{ca_si}**" if ca_si else ""),
                    color=discord.Color.red()
                )
                await self._reply(ctx_or_interaction, embed=embed, is_slash=is_slash)
                return

            # Cắt lời nếu quá dài (Discord giới hạn 4096 ký tự/embed)
            lyrics = song.lyrics
            chunks = self._split_lyrics(lyrics, limit=4000)

            # Embed đầu tiên — thông tin bài hát
            first_embed = discord.Embed(
                title=f"🎵 {song.title}",
                description=chunks[0],
                color=discord.Color.purple(),
                url=song.url
            )
            first_embed.set_author(name=song.artist)
            if song.song_art_image_url:
                first_embed.set_thumbnail(url=song.song_art_image_url)
            first_embed.set_footer(text=f"Nguồn: Genius • Trang 1/{len(chunks)}")

            await self._reply(ctx_or_interaction, embed=first_embed, is_slash=is_slash)

            # Gửi tiếp các phần còn lại (nếu lời dài)
            channel = (
                ctx_or_interaction.channel
                if is_slash
                else ctx_or_interaction.channel
            )
            for i, chunk in enumerate(chunks[1:], start=2):
                next_embed = discord.Embed(
                    description=chunk,
                    color=discord.Color.purple()
                )
                next_embed.set_footer(text=f"Trang {i}/{len(chunks)}")
                await channel.send(embed=next_embed)

        except Exception as e:
            embed = discord.Embed(
                title="⚠️ Lỗi",
                description=f"Có lỗi xảy ra: `{str(e)}`",
                color=discord.Color.orange()
            )
            await self._reply(ctx_or_interaction, embed=embed, is_slash=is_slash)

    def _split_lyrics(self, text: str, limit: int = 4000) -> list[str]:
        """Cắt lời bài hát thành nhiều phần, ngắt theo dòng"""
        lines = text.split("\n")
        chunks, current = [], ""

        for line in lines:
            if len(current) + len(line) + 1 > limit:
                chunks.append(current.strip())
                current = line + "\n"
            else:
                current += line + "\n"

        if current.strip():
            chunks.append(current.strip())

        return chunks if chunks else [text[:limit]]

    async def _reply(self, ctx_or_interaction, embed, is_slash):
        """Gửi reply đúng cách cho cả slash và prefix command"""
        if is_slash:
            await ctx_or_interaction.followup.send(embed=embed)
        else:
            await ctx_or_interaction.reply(embed=embed)

    # ────────────────────────────────────────────
    # LỆNH HELP TÙY CHỈNH
    # ────────────────────────────────────────────
    @commands.command(name="help")
    async def help_cmd(self, ctx):
        embed = discord.Embed(
            title="📖 Hướng dẫn sử dụng",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Slash Command",
            value="`/lyrics <tên bài>` — Tra lời bài hát\n"
                  "`/lyrics <tên bài> <ca sĩ>` — Tìm chính xác hơn",
            inline=False
        )
        embed.add_field(
            name="Prefix Command",
            value="`!lyrics Shape of You`\n"
                  "`!lyrics Nơi này có anh | Sơn Tùng`\n"
                  "`!l <tên bài>` — Viết tắt",
            inline=False
        )
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Lyrics(bot))