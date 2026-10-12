# The Degen Desk call ledger

Every trade call The Degen Desk publishes is written here before the issue goes out. A newsletter post can be edited after it is published. This file cannot be quietly changed.

## How it works

- `calls.jsonl` holds one call per line: when it was published, the instrument, the direction, the entry, the stop, the target and the invalidation level. Each call has one entry price, so `entry_low` and `entry_high` are equal; only the first call (SUI, 11 October 2026) was published with a zone.
- Each line carries `prev_hash`, the SHA-256 hash of the line before it, and `hash`, the SHA-256 of its own contents plus `prev_hash`.
- Changing any past call changes its hash, which breaks the link from every line after it.
- Each call is its own commit, so the git history adds an outside timestamp.

This repository started on 12 October 2026. The first call (SUI, 11 October 2026) was carried over unchanged from the desk's first ledger, so its commit is later than its `published_at`. Every call after it is committed before its issue goes out.

## Verify it yourself

```
python3 verify.py calls.jsonl
```

No dependencies. It recomputes every hash and names the first line that does not match.

## How calls are graded

Calls are graded on hourly Binance perpetual candles, starting from the first full hour after publication, so nothing that traded before the issue went out counts. A call fills once a candle reaches its entry price, and results are reported in multiples of the risk taken from that price (R), losses included. A target reached in the same hour as the fill does not count, because the order of moves inside one candle is unknown.

The SUI zone call is graded from the edge of its zone that is worst for the trade, 1.0985, because price was already there when the issue went out.

From 12 October 2026 every stop sits no more than 6% from the entry, so on a 10x position it is hit before liquidation. The SUI call's stop is 11.9% from 1.0985.

Not financial advice.
