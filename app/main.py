import uvicorn
import sentry_sdk

from application import mp_backend

if __name__ == '__main__':
    settings = mp_backend.config.settings
    sentry_sdk.init(settings.sentry_key, environment=settings.environment)
    if mp_backend.config.settings.environment == "production":
        uvicorn.run(mp_backend.mpApi, host="0.0.0.0", port=mp_backend.config.settings.port, root_path=mp_backend.config.settings.api_prefix,ssl_keyfile="ssl/private.key",ssl_certfile="ssl/certificate.crt",ssl_ca_certs="ssl/ca_bundle.crt")
    else:
        uvicorn.run(mp_backend.mpApi, host="0.0.0.0", port=mp_backend.config.settings.port, root_path=mp_backend.config.settings.api_prefix)
    