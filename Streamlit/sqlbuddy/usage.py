"""Free-tier request limiter (per session). Swap for per-user storage when you add accounts."""


class UsageLimiter:
    def __init__(self, limit: int):
        self.limit = max(0, int(limit))
        self.used = 0

    @property
    def remaining(self) -> int:
        return max(0, self.limit - self.used)

    def consume(self) -> bool:
        """Count one request. Returns False (and counts nothing) when the limit is reached."""
        if self.used >= self.limit:
            return False
        self.used += 1
        return True
