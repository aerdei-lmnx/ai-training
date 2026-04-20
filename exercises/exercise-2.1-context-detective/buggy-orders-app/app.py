"""Application factory for the Orders API."""

from flask import Flask

from config import get_config
from models import db
from routes import register_blueprints


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(get_config())

    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_blueprints(app)

    # Health-check endpoint
    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, port=5001)
