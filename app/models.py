from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func

from dpkt.icmp import ICMP
from dpkt.udp import UDP
from dpkt.tcp import TCP
import dpkt

from flask_login import UserMixin

from app import db, bcrypt


class User(db.Model, UserMixin):

    ''' A user who has an account on the website. '''

    __tablename__ = 'users'

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, primary_key=True)
    confirmation = db.Column(db.Boolean)
    _password = db.Column(db.String)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password, plaintext)

    def get_id(self):
        return self.email


class Timeframes(db.Model):
    """Sqlalchemy timeframes model"""

    def __init__(self, time_frame, tcp, udp, icmp, ip):
        self.time_frame = int(time_frame)
        self.tcp_total = tcp
        self.udp_total = udp
        self.icmp_total = icmp
        self.ip_total = ip

    __tablename__ = 'time_frames'
    __bind_key__ = 'ddos2'

    time_frame = db.Column('time_frame', db.BIGINT, primary_key=True)
    tcp_total = db.Column('tcp_total', db.Integer, nullable=True, default=0)
    udp_total = db.Column('udp_total', db.Integer, nullable=True, default=0)
    icmp_total = db.Column('icmp_total', db.Integer, nullable=True, default=0)
    ip_total = db.Column('ip_total', db.Integer, nullable=True, default=0)


class UniqueVictims(db.Model):
    """Sqlalchemy unique victims model"""

    def __init__(self, ip, lat=0, long=0):
        self.ip = ip
        self.lat = lat
        self.long = long
        self.udp_count = 0
        self.tcp_count = 0
        self.icmp_count = 0
        self.timeframe_count = 0
        self.rate = 0

    __tablename__ = 'unique_victims'
    __bind_key__ = 'ddos2'

    ip = db.Column('ip', db.String, primary_key=True)
    lat = db.Column('lat', db.Numeric(10, 6), default=0)
    long = db.Column('long', db.Numeric(10, 6), default=0)
    udp_count = db.Column('udp_count', db.Integer, default=0)
    tcp_count = db.Column('tcp_count', db.Integer, default=0)
    icmp_count = db.Column('icmp_count', db.Integer, default=0)
    time_frame_count = db.Column('time_frame_count', db.Integer, default=0)
    rate = db.Column('rate', db.Numeric(10, 2), default=0)
    city = db.Column('city', db.String)
    country = db.Column('country', db.String)
    isp = db.Column('isp', db.String)


class Victims(db.Model):
    """Sqlalchemy victims model"""

    def __init__(self, ip, tcp, udp, icmp, time_frame):
        self.ip = ip
        self.tcp_count = tcp
        self.udp_count = udp
        self.icmp_count = icmp
        self.time_frame = time_frame

    __tablename__ = 'victims'
    __bind_key__ = 'ddos2'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ip = db.Column('ip', db.String, db.ForeignKey("unique_victims.ip", onupdate="CASCADE", ondelete="CASCADE"),
                   primary_key=True)
    tcp_count = db.Column('tcp_count', db.Integer, nullable=True, default=0)
    udp_count = db.Column('udp_count', db.Integer, nullable=True, default=0)
    icmp_count = db.Column('icmp_count', db.Integer, nullable=True, default=0)
    time_frame = db.Column('time_frame', db.BIGINT, db.ForeignKey("time_frames.time_frame"), primary_key=True)

# class Timeframes(db.Model):
#     """Sqlalchemy timeframes model"""
#
#     def __init__(self, timeframe, tcp, udp, icmp, ip):
#         self.timeframe = timeframe
#         self.tcp_total = tcp
#         self.udp_total = udp
#         self.icmp_total = icmp
#         self.ip_total = ip
#
#     __tablename__ = 'timeframes'
#     __bind_key__ = 'ddos'
#
#     timeframe = db.Column('timeframe', db.BIGINT, primary_key=True)
#     tcp_total = db.Column('tcp_total', db.Integer, nullable=True, default=0)
#     udp_total = db.Column('udp_total', db.Integer, nullable=True, default=0)
#     icmp_total = db.Column('icmp_total', db.Integer, nullable=True, default=0)
#     ip_total = db.Column('ip_total', db.Integer, nullable=True, default=0)


# class UniqueLocation(db.Model):
#     """Sqlalchemy Unique Location models"""
#     def __init__(self, lat, long, ip_count, tcp_count, udp_count, icmp_count):
#         self.lat = lat
#         self.long = long
#         self.ip_count = ip_count
#         self.tcp_count = tcp_count
#         self.udp_count = udp_count
#         self.icmp_count = icmp_count
#
#     __tablename__ = 'unique_location'
#     __bind_key__ = 'ddos'
#
#     lat = db.Column('lat', db.Numeric(10, 6), primary_key=True)
#     long = db.Column('long', db.Numeric(10, 6), primary_key=True)
#     ip_count = db.Column('ip_count', db.Integer)
#     tcp_count = db.Column('tcp_count', db.Integer)
#     udp_count = db.Column('udp_count', db.Integer)
#     icmp_count = db.Column('icmp_count', db.Integer)


# class UniqueVictims(db.Model):
#     """Sqlalchemy unique victims model"""
#
#     def __init__(self, ip, lat, long):
#         self.ip = ip
#         self.lat = lat
#         self.long = long
#
#     __tablename__ = 'uniquevictims'
#     __bind_key__ = 'ddos'
#
#     ip = db.Column('ip', db.String, primary_key=True)
#     lat = db.Column('lat', db.Numeric(10, 6), default=0)
#     long = db.Column('long', db.Numeric(10, 6), default=0)


# class Victims(db.Model):
#     """Sqlalchemy victims model"""
#
#     def __init__(self, ip, tcp, udp, icmp, timeframe):
#         self.ip = ip
#         self.tcp_count = tcp
#         self.udp_count = udp
#         self.icmp_count = icmp
#         self.timeframe = timeframe
#
#     __tablename__ = 'victims'
#     __bind_key__ = 'ddos'
#
#     ip = db.Column('ip', db.String, db.ForeignKey("uniquevictims.ip"), primary_key=True)
#     tcp_count = db.Column('tcp_count', db.Integer, nullable=True, default=0)
#     udp_count = db.Column('udp_count', db.Integer, nullable=True, default=0)
#     icmp_count = db.Column('icmp_count', db.Integer, nullable=True, default=0)
#     timeframe = db.Column('timeframe', db.BIGINT, db.ForeignKey("timeframes.timeframe"), primary_key=True)

# class AuthorizedClients(db.Model):
#
#     ''' A client which is authorized to use the webhook system '''
#
#     __tablename__ = 'authorized_clients'
#
#     client_ip = db.Column(db.String, primary_key=True)
#     pub_time = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
#
#     @property
#     def ip(self):
#         return '{}'.format(self.client_ip)
