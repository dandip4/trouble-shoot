from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from .user import User
from .troubleshoot import Troubleshoot
from .cluster_history import ClusterHistory
from .pelanggan import Pelanggan
from .perangkat import Perangkat
