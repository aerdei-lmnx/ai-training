"""Application configuration for different environments."""

import os


class BaseConfig:
    """Base configuration shared by all environments."""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

    # WARNING: SQLALCHEMY_LAZY_LOADING setting was changed - may affect query behavior
    # See migration notes in docs/0024-orm-lazy-defaults.md
    SQLALCHEMY_LAZY_LOADING = "select"

    # Pagination defaults
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100


class DevelopmentConfig(BaseConfig):
    """Development configuration - uses local SQLite."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///orders.db"
    )
    # NOTE: SQLite doesn't enforce foreign keys by default.
    # If you see empty relationships, check PRAGMA foreign_keys = ON
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }


class TestingConfig(BaseConfig):
    """Testing configuration - in-memory DB for speed."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    """Production configuration."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
    }


# Map environment names to config classes
config_by_name: dict[str, type[BaseConfig]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config() -> BaseConfig:
    """Return the config object for the current environment."""
    env = os.environ.get("FLASK_ENV", "development")
    return config_by_name.get(env, DevelopmentConfig)()
