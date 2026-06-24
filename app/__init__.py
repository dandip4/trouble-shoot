from flask import Flask, render_template
from flask_login import LoginManager
from .config import Config
from .models import db, User


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


def load_user(user_id):
    return User.query.get(int(user_id))


def seed_admin():
    if User.query.filter_by(username="admin").first() is None:
        admin = User(
            username="admin",
            email="admin@troubleshoot.com",
            role="admin",
            is_active=True,
        )
        admin.set_password("admin123")
        db.session.add(admin)

    if User.query.filter_by(username="teknisi1").first() is None:
        teknisi = User(
            username="teknisi1",
            email="teknisi1@troubleshoot.com",
            role="teknisi",
            is_active=True,
        )
        teknisi.set_password("teknisi123")
        db.session.add(teknisi)

    if User.query.filter_by(username="manajer1").first() is None:
        manajer = User(
            username="manajer1",
            email="manajer1@troubleshoot.com",
            role="manajer",
            is_active=True,
        )
        manajer.set_password("manajer123")
        db.session.add(manajer)

    db.session.commit()


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.user_loader(load_user)

    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.troubleshoot import troubleshoot_bp
    from .routes.clustering import clustering_bp
    from .routes.laporan import laporan_bp
    from .routes.admin import admin_bp
    from .routes.pelanggan import pelanggan_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(troubleshoot_bp)
    app.register_blueprint(clustering_bp)
    app.register_blueprint(laporan_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(pelanggan_bp)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.after_request
    def set_security_headers(response):
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

    with app.app_context():
        db.create_all()
        seed_admin()

    return app
