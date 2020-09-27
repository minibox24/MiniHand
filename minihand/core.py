from minihand.parser import Parser
from minihand.cmd import Command, Variables
from os import listdir
from importlib import import_module
from inspect import iscoroutinefunction
from asyncio import ensure_future
from types import FunctionType


class MiniHand:
    def __init__(self):
        cmds = self.getAllCommands()
        self.commands = cmds[0]
        self.packages = cmds[1]
        self.packageNames = cmds[2]

    @staticmethod
    def getAllCommands():
        commands = []
        packages = []
        packageNames = []

        packages_ = listdir('commands')
        packages_ = [f for f in packages_ if f.endswith(".py")]
        for package in packages_:
            packageName = package.replace(".py", "")
            packageName = f'commands.{packageName}'

            package = import_module(packageName)
            packages.append(package)
            packageNames.append(packageName)

            for i in package.__dir__():
                attr = getattr(package, i)
                if type(attr) == Command:
                    commands.append(attr)
        return (commands, packages, packageNames)

    def findCommand(self, cmdname):
        for cmd in self.commands:
            if cmd.name == cmdname:
                return cmd
            if cmdname in cmd.aliases:
                return cmd
        return None

    def Run(self, cmd, send=print, vars_=Variables()):
        # if not isinstance(send, FunctionType):
        #     raise TypeError('send에는 함수만 올 수 있습니다.')

        vars_.__handler__ = self

        parsing = Parser(cmd)
        command = self.findCommand(parsing[1])
        if not command:
            return

        args = parsing[2:]
        if iscoroutinefunction(send):
            command.execute(__send__=lambda msg: ensure_future(send(str(msg))), __vars__=vars_, *args, **parsing[0])
        else:
            command.execute(__send__=send, __vars__=vars_, *args, **parsing[0])
        return parsing

