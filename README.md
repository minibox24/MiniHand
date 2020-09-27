# MiniHand
다양한 커맨드 시스템에 사용 가능한 핸들러.

## 사용 예시 (discord.py)
```py
import discord
from minihand.core import MiniHand
from minihand.cmd import Variables

client = discord.Client()  # 간편한 사용을 위한 client
handler = MiniHand()

@client.event
async def on_message(msg):
    if msg.content.startswith('!'):
        handler.Run(
            msg.content[1:],  # 실행할 커맨드 내용
            msg.channel.send,  # ctx.send에 쓰일 함수
            Variables(message=msg)  # message 변수 전달
        )

client.run('TOKEN')
```

## 커맨드 스타일
discord.py cogs-like style

```py
from minihand.cmd import commands

@commands.command(name="안녕", aliases=["ㅎㅇ", "hi"], shorthelp="안녕커맨드")
def Hello(context):
    """'안녕!' 이라고 대답해주는 커맨드 입니다."""
    context.send("안녕!")
```

## 커맨드라인 사용법
```py
@commands.command()
def test(ctx, arg1, kwarg="없음"):
    ctx.send(arg1 + kwarg)
```
`test 테스트 --kwarg "와! 샌즈!"` => `테스트 와! 샌즈!`


## 라이선스
MiniHand는 MIT License를 적용합니다.

만약 이 핸들러를 사용한다면, 꼭 [출처](https://github.com/minibox724/minihand)를 남겨주세요.