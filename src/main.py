import uvicorn
import sentry_sdk

from application import mp_backend

if __name__ == '__main__':
    settings = mp_backend.config.settings
    sentry_sdk.init(settings.sentry_key)
    uvicorn.run(mp_backend.mpApi, host="0.0.0.0", port=8000)
