import os

from config_data.initial_settings import PathParams


def create_logs_catalogs():
    if not os.path.exists(PathParams.logs_catalog):
        os.makedirs(PathParams.logs_catalog, mode=0o755, exist_ok=True)

