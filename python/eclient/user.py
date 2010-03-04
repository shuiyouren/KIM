class user:
    "Store user data"
    def __init__(self, user, nick, subnick, media, status, avatar_hash, avatar_path, ip, localip ):
        self.user = user
        self.nick = nick
        self.subnick = subnick
        self.media = media
        self.status = status
        self.avatar_hash = avatar_hash
        self.avatar_path = avatar_path
        self.ip = ip
        self.localip = localip
