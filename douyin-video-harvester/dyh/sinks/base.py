class Sink:
    """Base class. Override existing_names() and upload(). verify_size() is shared."""
    def __init__(self, cfg, **opts):
        self.cfg, self.opts = cfg, opts
    def existing_names(self):
        return set()
    def upload(self, path):
        raise NotImplementedError
