import uvicorn
import sentry_sdk

from src.application import mp_backend

if __name__ == '__main__':
    settings = mp_backend.config.settings
    print("Running Environment:", settings.environment)
    sentry_sdk.init(settings.sentry_key, environment=settings.environment)
    uvicorn.run(mp_backend.mpApi, host="0.0.0.0", port=8000, root_path=mp_backend.config.settings.api_prefix)