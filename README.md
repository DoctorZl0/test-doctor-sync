# Test Doctor orders synchronizer

Small Python service that fetches raw orders, normalizes Russian phone numbers,
merges duplicates by maximum amount and latest creation date, and returns the
required JSON response at `/api/orders`.

## Run

```bash
python3 server.py
python3 -m unittest -v test_sync_service.py
```

The upstream URL is configured in `sync_service.py`.
