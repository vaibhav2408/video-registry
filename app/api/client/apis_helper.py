class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError


class Apis(Enum):
    # Youtube search API
    search_api = "/youtube/v3/search"
    # Youtube video details API
    video_details = "/youtube/v3/videos"
