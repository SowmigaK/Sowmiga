from sqlbuddy.usage import UsageLimiter


def test_limiter_counts_down_then_blocks():
    limiter = UsageLimiter(2)
    assert limiter.consume() and limiter.consume()
    assert not limiter.consume()
    assert limiter.remaining == 0 and limiter.used == 2


def test_zero_or_negative_limit_blocks_everything():
    assert not UsageLimiter(0).consume()
    assert UsageLimiter(-5).remaining == 0
