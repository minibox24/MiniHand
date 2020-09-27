from minihand.cmd import commands, Command
from minihand.core import MiniHand
from importlib import reload as Reload


@commands.command(name="help", aliases=["도움", "도움말"], shorthelp="도움 커맨드입니다.")
def help(ctx, find: str=None):
    """기본 모든 커맨드 / 커맨드 검색기 입니다."""
    handler = ctx.handler
    helpstr = ""

    if find:
        found = []
        for cmd in handler.commands:
            names = cmd.aliases[:]
            names.append(cmd.name)
            for name in names:
                if find in name:
                    found.append(cmd)
                    break
        
        for cmd in found:
            if not cmd.shorthelp:
                helpstr += f"{cmd.name}:\n"
            else:
                helpstr += f"{cmd.name} - {cmd.shorthelp}:\n"
            helpstr += cmd.doc
            helpstr += "\n\n"

    else:
        for cmd in handler.commands:
            if not cmd.shorthelp:
                helpstr += f"{cmd.name} - {cmd.shorthelp}\n"
            else:
                helpstr += f"{cmd.name}\n"

    ctx.send(helpstr)

@commands.command(name="reload", aliases=["ㄹ", "리로드"], shorthelp="모든 커맨드 리로드.")
def reload(ctx):
    """핸들러에 등록되어 있는 모든 커맨드를 삭제하고, 다시 모든 파일에서 모든 커맨드를 찾아서 등록합니다."""
    handler = ctx.handler
    handler.commands = []
    cmds = MiniHand.getAllCommands()

    for package in handler.packages:
        Reload(package)
        for i in package.__dir__():
            attr = getattr(package, i)
            if type(attr) == Command:
                handler.commands.append(attr)

    ctx.send('완료')
