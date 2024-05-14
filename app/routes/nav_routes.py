from flask import Blueprint, current_app, render_template
from func_timeout import FunctionTimedOut, func_timeout
from sqlalchemy import text
from app.cache import redis_cache

from app.auth import auth_required


nav_blueprint = Blueprint("nav_blueprint", __name__)


@nav_blueprint.route("/landing_page")
@auth_required
def landing_page():
    # protected page
    return render_template("landing_page.html")


@nav_blueprint.route("/")
def home():
    return render_template("index.html")


@nav_blueprint.route("/api/data")
@auth_required
def data():
    return "Super secret info"


@nav_blueprint.route("/redis-health-check")
def redis_health_check():
    timeout: int = 5  # s
    try:
        ping = func_timeout(timeout, redis_cache.ping)
        return "Redis ping returned with value: " + str(ping), 200
    except FunctionTimedOut as fto:
        current_app.logger.error("Redis ping timed out " + str(fto))
        return f"Redis ping timed out after {timeout} seconds", 200
    except Exception as e:
        current_app.logger.error("Redis ping failed with " + str(e))
        return "Redis failed to ping", 200


@nav_blueprint.route("/rds-health-check")
def rds_health_check():
    try:
        with current_app.Session() as sess:
            res = sess.execute(text("SELECT 1"))
            if res.scalar() == 1:
                return "DB connection is healthy!", 200
            else:
                return "DB connection failed but query executed", 200
    except Exception as e:
        current_app.logger.error("DB health check failed with " + str(e))
        return "DB connection failed with " + str(e), 200
