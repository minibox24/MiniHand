from traceback import format_exc


class Variables:
    def __init__(self, **kwargs):
        self.dict = kwargs
        for i in kwargs:
            setattr(self, i, kwargs[i])


class Context:
    def __init__(self, handler, vars_, send=print):
        self.handler = handler
        self.send = send
        self.vars = vars_


class Command:
    def __init__(self, func, **kwargs):
        self.func = func
        self.name = func.__name__ if not kwargs.get('name') else kwargs.get('name')
        self.shorthelp = kwargs.get('shorthelp')
        self.doc = kwargs.get('doc') if kwargs.get('doc') else func.__doc__
        self.aliases = [] if not kwargs.get('aliases') else kwargs.get('aliases')

    def __repr__(self):
        return f"<Command {self.func.__name__}: name='{self.name}' aliases={self.aliases} shorthelp='{self.shorthelp}' doc='{self.doc}'>"

    def execute(self, *args, **kwargs):
        send = print
        if kwargs.get("__send__"):
            send = kwargs.get("__send__")
            del kwargs['__send__']

        vars_ = kwargs.get("__vars__")
        del kwargs['__vars__']

        handler = vars_.__handler__
        delattr(vars_, "__handler__")
    
        ctx = Context(handler, vars_, send=send)

        try:
            self.func(ctx, *args, **kwargs)
        except:
            ctx.send(f"커맨드 {self.name} 실행 중 오류가 발생했습니다.\n\n{format_exc()}")

class commands:
    @staticmethod
    def command(**kwargs):
        def wrapper(func):
            return Command(func, **kwargs)
        return wrapper
