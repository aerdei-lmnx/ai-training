"""Task Management REST API built with Flask and SQLAlchemy."""

from datetime import date, datetime, timezone

from flask import Flask, jsonify, request

from models import Task, db


def create_app(testing: bool = False) -> Flask:
    """Application factory."""
    app = Flask(__name__)

    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)

    return app


def register_routes(app: Flask) -> None:
    """Register all API routes."""

    @app.get("/tasks")
    def list_tasks():
        """List all tasks with optional status filter."""
        status_filter = request.args.get("status")

        query = Task.query

        if status_filter:
            if status_filter not in Task.VALID_STATUSES:
                return jsonify({"error": f"Invalid status: {status_filter}"}), 400
            query = query.filter_by(status=status_filter)

        tasks = query.order_by(Task.created_at.desc()).all()
        return jsonify({"data": [task.to_dict() for task in tasks]})

    @app.get("/tasks/<int:task_id>")
    def get_task(task_id: int):
        """Get a single task by ID."""
        task = db.session.get(Task, task_id)
        if task is None:
            return jsonify({"error": "Task not found"}), 404
        return jsonify({"data": task.to_dict()})

    @app.post("/tasks")
    def create_task():
        """Create a new task."""
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        title = data.get("title")
        if not title or not title.strip():
            return jsonify({"error": "Title is required"}), 400

        status = data.get("status", "pending")
        if status not in Task.VALID_STATUSES:
            return jsonify({"error": f"Invalid status: {status}"}), 400

        priority = data.get("priority", "medium")
        if priority not in Task.VALID_PRIORITIES:
            return jsonify({"error": f"Invalid priority: {priority}"}), 400

        due_date = None
        if data.get("due_date"):
            try:
                due_date = date.fromisoformat(data["due_date"])
            except ValueError:
                return jsonify({"error": "Invalid due_date format, use YYYY-MM-DD"}), 400

        task = Task(
            title=title.strip(),
            description=data.get("description", "").strip() or None,
            status=status,
            priority=priority,
            due_date=due_date,
        )

        db.session.add(task)
        db.session.commit()

        return jsonify({"data": task.to_dict()}), 201

    @app.patch("/tasks/<int:task_id>")
    def update_task(task_id: int):
        """Update an existing task."""
        task = db.session.get(Task, task_id)
        if task is None:
            return jsonify({"error": "Task not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        if "title" in data:
            title = data["title"]
            if not title or not str(title).strip():
                return jsonify({"error": "Title cannot be empty"}), 400
            task.title = str(title).strip()

        if "description" in data:
            task.description = str(data["description"]).strip() or None

        if "status" in data:
            if data["status"] not in Task.VALID_STATUSES:
                return jsonify({"error": f"Invalid status: {data['status']}"}), 400
            task.status = data["status"]

        if "priority" in data:
            if data["priority"] not in Task.VALID_PRIORITIES:
                return jsonify({"error": f"Invalid priority: {data['priority']}"}), 400
            task.priority = data["priority"]

        if "due_date" in data:
            if data["due_date"] is None:
                task.due_date = None
            else:
                try:
                    task.due_date = date.fromisoformat(data["due_date"])
                except (ValueError, TypeError):
                    return jsonify({"error": "Invalid due_date format, use YYYY-MM-DD"}), 400

        task.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        return jsonify({"data": task.to_dict()})


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
