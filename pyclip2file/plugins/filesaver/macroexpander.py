class MacroExpander:
    def __init__(self):
        self._descriptions = {}
        self._map = {}

    def expand(self, path: str) -> str:
        for k in self._map:
            path = path.replace(k, self._map[k]())
        return path

    def register_variable(self, var: str, description: str, func):
        self._descriptions[var] = description
        self._map[var] = func


def datetime_expander():
    import datetime
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')