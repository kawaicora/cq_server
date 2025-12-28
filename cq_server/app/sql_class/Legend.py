from typing import Any, Optional

from sqlalchemy import BINARY, BigInteger, Column, DateTime, Float, Identity, Index, Integer, PrimaryKeyConstraint, SmallInteger, String, Table, Uuid, text
from sqlalchemy.dialects.mssql import MONEY, TIMESTAMP, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime
import uuid

class Base(DeclarativeBase):
    pass


t_Game_Config = Table(
    'Game_Config', Base.metadata,
    Column('open_time', String(50, 'Chinese_PRC_CI_AS')),
    Column('merge_time', String(50, 'Chinese_PRC_CI_AS')),
    Column('merge_num', Integer),
    Column('kuafu_ip', String(50, 'Chinese_PRC_CI_AS')),
    Column('kuafu_port', Integer),
    Column('kuafu_state', Integer),
    Column('cs3v3_ip', String(50, 'Chinese_PRC_CI_AS')),
    Column('cs3v3_port2', Integer),
    Column('kuafu_date', String(50, 'Chinese_PRC_CI_AS')),
    Column('cs3v3_port', Integer),
    Column('createchr_day', Integer),
    Column('hefu_flag', Integer)
)


class MirDisbleChat(Base):
    __tablename__ = 'Mir_Disble_Chat'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK__Mir_Disb__3214EC079888A157'),
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    sUserId: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    nChannel: Mapped[Optional[int]] = mapped_column(Integer)
    nTime: Mapped[Optional[int]] = mapped_column(Integer)
    sTab: Mapped[Optional[str]] = mapped_column(String(100, 'Chinese_PRC_CI_AS'))
    dCreateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('(getdate())'))


class MirDisbleList(Base):
    __tablename__ = 'Mir_Disble_List'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK__Mir_Disb__3214EC079929075C'),
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    sAccount: Mapped[Optional[str]] = mapped_column(String(128, 'Chinese_PRC_CI_AS'))
    sUserId: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    sIpAddr: Mapped[Optional[str]] = mapped_column(String(20, 'Chinese_PRC_CI_AS'))
    nVerify: Mapped[Optional[int]] = mapped_column(Integer)
    sTab: Mapped[Optional[str]] = mapped_column(String(100, 'Chinese_PRC_CI_AS'))
    dCreateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('(getdate())'))


t_TBL_BLACK = Table(
    'TBL_BLACK', Base.metadata,
    Column('FLD_USERID', String(50, 'Chinese_PRC_CI_AS'), nullable=False),
    Column('FLD_BUSERID', String(50, 'Chinese_PRC_CI_AS'), nullable=False),
    Column('FLD_JOB', String(10, 'Chinese_PRC_CI_AS'))
)


class TBLBOXSELL(Base):
    __tablename__ = 'TBL_BOX_SELL'
    __table_args__ = (
        PrimaryKeyConstraint('FLD_ID', name='PK__TBL_BOX___84774207A5B56D0B'),
        Index('FLD_ID_IDX', 'FLD_ID', unique=True),
        Index('IX_TBL_BOX_SELL_FLD_ORDER', 'FLD_ORDER'),
        Index('IX_TBL_BOX_SELL_FLD_STATE', 'FLD_STATE'),
        Index('IX_TBL_BOX_SELL_FLD_USERID', 'FLD_USERID')
    )

    FLD_ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    FLD_USERID: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    FLD_BUYUSERID: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    FLD_PAYORDER: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_CI_AS'), server_default=text("('')"))
    FLD_STATUS: Mapped[int] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_MONEYID: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))
    FLD_MONEY: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_ORDER: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    FLD_CREATEDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    FLD_UPDATEEDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    FLD_STATE: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))
    FLD_DECSTATE: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))
    FLD_GETSTATE: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))


class TBLBOXSELLITEM(Base):
    __tablename__ = 'TBL_BOX_SELLITEM'
    __table_args__ = (
        PrimaryKeyConstraint('FLD_ID', name='PK__TBL_BOX_SELLITEM'),
        Index('TBL_BOX_SELLITEM_FLD_ID', 'FLD_ID', unique=True)
    )

    FLD_ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    FLD_USERID: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    FLD_BUYUSERID: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    FLD_ITEMINFO: Mapped[str] = mapped_column(String(4096, 'Chinese_PRC_CI_AS'))
    FLD_ORDER: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    FLD_CREATEDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    FLD_UPDATEEDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    FLD_STATE: Mapped[Optional[int]] = mapped_column(SmallInteger)


class TBLCHARACTER(Base):
    __tablename__ = 'TBL_CHARACTER'
    __table_args__ = (
        PrimaryKeyConstraint('FLD_ID', name='PK__TBL_CHAR__8477420780A495D1'),
        Index('IX_TBL_CHARACTER_FLD_ACCOUNT', 'FLD_ACCOUNT'),
        Index('IX_TBL_CHARACTER_FLD_CHARACTER', 'FLD_CHARACTER'),
        Index('IX_TBL_CHARACTER_FLD_REALACCOUNT', 'FLD_REALACCOUNT'),
        Index('IX_TBL_CHARACTER_FLD_UPDATEDATETIME', 'FLD_UPDATEDATETIME'),
        Index('IX_TBL_CHARACTER_FLD_USERID', 'FLD_USERID')
    )

    FLD_ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    FLD_LOCKHUM: Mapped[int] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_ISBUYCHAR: Mapped[int] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_REALACCOUNT: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_CI_AS'), server_default=text("('')"))
    FLD_PAYORDER: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_CI_AS'), server_default=text("('')"))
    FLD_STATUS: Mapped[int] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_HEROUSERID: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'), server_default=text("('')"))
    FLD_HERONAME: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'), server_default=text("('')"))
    FLD_ACCOUNT: Mapped[Optional[str]] = mapped_column(String(128, 'Chinese_PRC_CI_AS'))
    FLD_CHARACTER: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    FLD_USERID: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_CI_AS'), server_default=text("('')"))
    FLD_DELETED: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_UPDATEDATETIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    FLD_DBVERSION: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_MAPNAME: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_CI_AS'), server_default=text("('')"))
    FLD_CX: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))
    FLD_CY: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))
    FLD_DIR: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_HAIR: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((1))'))
    FLD_SEX: Mapped[Optional[int]] = mapped_column(TINYINT)
    FLD_JOB: Mapped[Optional[int]] = mapped_column(TINYINT)
    FLD_LEVEL: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_HP: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text('((0))'))
    FLD_MP: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text('((0))'))
    FLD_EXP: Mapped[Optional[int]] = mapped_column(BigInteger, server_default=text('((0))'))
    FLD_GOLD: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_HOMEMAP: Mapped[Optional[str]] = mapped_column(String(20, 'Chinese_PRC_CI_AS'), server_default=text("('')"))
    FLD_HOMEX: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))
    FLD_HOMEY: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))
    FLD_PKPOINT: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_ALLOWGROUP: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_ATTACKMODE: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_FIGHTZONEDIE: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_BODYLUCK: Mapped[Optional[float]] = mapped_column(Float(53), server_default=text('((0))'))
    FLD_INCHEALTH: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_INCSPELL: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_INCHEALING: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_BONUSPOINT: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_HUNGRYSTATE: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_MAKEDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    FLD_ISFIRSTCHAR: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_StatusTimeArr: Mapped[Optional[bytes]] = mapped_column(BINARY(24), server_default=text('((0))'))
    FLD_RELEVEL: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_GAMEGOLD: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_CREDITPOINT: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_MASTERNAME: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_CI_AS'), server_default=text("('')"))
    FLD_MASTER: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_DEARNAME: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_CI_AS'), server_default=text("('')"))
    FLD_STORAGEPWD: Mapped[Optional[str]] = mapped_column(String(10, 'Chinese_PRC_CI_AS'), server_default=text("('')"))
    FLD_GAMEPOINT: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_PAYMENTPOINT: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_LOCKLOGON: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_CONTRIBUTION: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_ALLOWGUILDRECALL: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_GROUPRECALLTIME: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_ALLOWGROUPRECALL: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_QUESTUNITOPEN: Mapped[Optional[bytes]] = mapped_column(BINARY(128), server_default=text('((0))'))
    FLD_QUESTUNIT: Mapped[Optional[bytes]] = mapped_column(BINARY(128), server_default=text('((0))'))
    FLD_QUESTFLAG: Mapped[Optional[bytes]] = mapped_column(BINARY(128), server_default=text('((0))'))
    FLD_MARRYCOUNT: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_BONUS_DC: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_BONUS_MC: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_BONUS_SC: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_BONUS_AC: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_BONUS_MAC: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_BONUS_HP: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_BONUS_MP: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_BONUS_HIT: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_BONUS_SPEED: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_BONUS_X2: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_SELECTID: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_MONEY: Mapped[Optional[bytes]] = mapped_column(BINARY(400), server_default=text('((0))'))
    FLD_BTF9: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_SYSVAR: Mapped[Optional[bytes]] = mapped_column(BINARY(400), server_default=text('((0))'))
    FLD_EE: Mapped[Optional[int]] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_UVAR: Mapped[Optional[bytes]] = mapped_column(BINARY(1020), server_default=text('((0))'))
    FLD_FEATURE: Mapped[Optional[str]] = mapped_column(String(200, 'Chinese_PRC_CI_AS'))
    FLD_OFFLINE_TIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('(NULL)'))
    FLD_SUCKDAMAGECOUNT: Mapped[Optional[int]] = mapped_column(BigInteger)
    FLD_SUCKDAMAGERATE: Mapped[Optional[int]] = mapped_column(TINYINT)
    FLD_SUCKDAMAGEBILI: Mapped[Optional[int]] = mapped_column(Integer)
    FLD_SNDAITEMBOXOPENED: Mapped[Optional[int]] = mapped_column(TINYINT)
    FLD_SDKID: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    FLD_SERVERID: Mapped[Optional[int]] = mapped_column(Integer)
    FLD_DC: Mapped[Optional[int]] = mapped_column(BigInteger)
    FLD_TOTAL_RECHARGE: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_CHARACTER_OLD: Mapped[Optional[str]] = mapped_column(String(100, 'Chinese_PRC_CI_AS'), server_default=text("('')"))
    FLD_JVAR: Mapped[Optional[bytes]] = mapped_column(BINARY(2000))
    FLD_BVAR: Mapped[Optional[bytes]] = mapped_column(BINARY(800))
    FLD_VARCLEARTIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    FLD_HumParams: Mapped[Optional[str]] = mapped_column(String(collation='Chinese_PRC_CI_AS'))
    FLD_LOCKDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('(NULL)'))


t_TBL_CONFIG = Table(
    'TBL_CONFIG', Base.metadata,
    Column('StartTime', DateTime),
    Column('recharge_config', String(8000, 'Chinese_PRC_CI_AS')),
    Column('Regis', Integer, nullable=False, server_default=text('((0))')),
    Column('iRegCount', Integer, server_default=text('((0))')),
    Column('sRegionServerName', String(50, 'Chinese_PRC_CI_AS'), server_default=text("('')")),
    Column('HfCount', Integer, server_default=text('((0))')),
    Column('HfTime', DateTime),
    Column('TongServerIP', String(30, 'Chinese_PRC_CI_AS'), server_default=text("('')")),
    Column('TongServerPort', Integer, server_default=text('((0))')),
    Column('kuafuip', String(50, 'Chinese_PRC_CI_AS')),
    Column('kuafuport', Integer),
    Column('kuafustate', Integer),
    Column('kuafuinfo', String(200, 'Chinese_PRC_CI_AS')),
    Column('sshowtime', DateTime),
    Column('FLD_JYHCannelID', String(8000, 'Chinese_PRC_CI_AS')),
    Column('FLD_TTSQCannelID', String(8000, 'Chinese_PRC_CI_AS')),
    Column('MainTongServer', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_SERCONFIG', String(collation='Chinese_PRC_CI_AS')),
    Column('FLD_SVRSTATE', SmallInteger, server_default=text('((0))')),
    Column('FLD_ADDRLIST', String(collation='Chinese_PRC_CI_AS')),
    Column('RegistWhiteList', String(collation='Chinese_PRC_CI_AS')),
    Column('DisableTime', DateTime),
    Column('DisableHFCount', Integer, server_default=text('((0))'))
)


t_TBL_FRIEND = Table(
    'TBL_FRIEND', Base.metadata,
    Column('FLD_USERID', String(50, 'Chinese_PRC_CI_AS')),
    Column('FLD_FUSERID', String(50, 'Chinese_PRC_CI_AS')),
    Column('FLD_JOB', String(10, 'Chinese_PRC_CI_AS'))
)


t_TBL_GUILD_INFO = Table(
    'TBL_GUILD_INFO', Base.metadata,
    Column('sGuildID', String(50, 'Chinese_PRC_CI_AS')),
    Column('sGuildName', String(128, 'Chinese_PRC_CI_AS')),
    Column('sNotice', String(256, 'Chinese_PRC_CI_AS')),
    Column('Level', SmallInteger, server_default=text('((0))')),
    Column('nGold', Integer, server_default=text('((0))')),
    Column('nExp', Integer, server_default=text('((0))')),
    Column('btAutoJoin', SmallInteger, server_default=text('((0))')),
    Column('dCreateTime', DateTime),
    Column('btDeleted', SmallInteger, server_default=text('((0))')),
    Column('nJoinLevel', Integer, server_default=text('((0))')),
    Column('btContriLvl', SmallInteger, server_default=text('((0))')),
    Column('nMemberCount', Integer, server_default=text('((100))')),
    Column('nBuildPoint', Integer, server_default=text('((0))')),
    Column('nAurae', Integer, server_default=text('((0))')),
    Column('nStability', Integer, server_default=text('((0))')),
    Column('nFlourishing', Integer, server_default=text('((0))')),
    Column('sRank1', String(50, 'Chinese_PRC_CI_AS')),
    Column('sRank2', String(50, 'Chinese_PRC_CI_AS')),
    Column('sRank3', String(50, 'Chinese_PRC_CI_AS')),
    Column('sRank4', String(50, 'Chinese_PRC_CI_AS')),
    Column('sRank5', String(50, 'Chinese_PRC_CI_AS')),
    Column('FLD_SERVERID', Integer),
    Column('sGuildName_old', String(128, 'Chinese_PRC_CI_AS'))
)


t_TBL_GUILD_MEMBER = Table(
    'TBL_GUILD_MEMBER', Base.metadata,
    Column('sGuildID', String(50, 'Chinese_PRC_CI_AS')),
    Column('sGuildName', String(50, 'Chinese_PRC_CI_AS')),
    Column('sUserID', String(50, 'Chinese_PRC_CI_AS')),
    Column('btRank', SmallInteger, server_default=text('((0))')),
    Column('btJob', SmallInteger, server_default=text('((0))')),
    Column('btJoin', SmallInteger, server_default=text('((0))')),
    Column('nLevel', Integer, server_default=text('((0))')),
    Index('IX_TBL_GUILD_MEMBER_sGuildID', 'sGuildID'),
    Index('IX_TBL_GUILD_MEMBER_sUserID', 'sUserID')
)


t_TBL_HERO = Table(
    'TBL_HERO', Base.metadata,
    Column('FLD_ID', Integer, Identity(start=1, increment=1), nullable=False),
    Column('FLD_HEROMASTERUSERID', String(128, 'Chinese_PRC_CI_AS')),
    Column('FLD_CHARACTER', String(50, 'Chinese_PRC_CI_AS')),
    Column('FLD_USERID', String(50, 'Chinese_PRC_CI_AS')),
    Column('FLD_DELETED', TINYINT, nullable=False, server_default=text('((0))')),
    Column('FLD_UPDATEDATETIME', DateTime),
    Column('FLD_MAPNAME', String(50, 'Chinese_PRC_CI_AS'), server_default=text("('')")),
    Column('FLD_CX', SmallInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_CY', SmallInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_DIR', TINYINT, nullable=False, server_default=text('((0))')),
    Column('FLD_HAIR', TINYINT, nullable=False, server_default=text('((1))')),
    Column('FLD_SEX', TINYINT, nullable=False, server_default=text('((0))')),
    Column('FLD_JOB', TINYINT, nullable=False, server_default=text('((0))')),
    Column('FLD_LEVEL', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_HP', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_MP', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_EXP', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_PKPOINT', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_BODYLUCK', Float(53), nullable=False, server_default=text('((0))')),
    Column('FLD_INCHEALTH', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_INCSPELL', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_INCHEALING', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUSPOINT', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_HUNGRYSTATE', TINYINT, nullable=False, server_default=text('((0))')),
    Column('FLD_MAKEDATE', DateTime),
    Column('FLD_StatusTimeArr', BINARY(24), nullable=False, server_default=text('((0))')),
    Column('FLD_RELEVEL', TINYINT, nullable=False, server_default=text('((0))')),
    Column('FLD_MASTERNAME', String(50, 'Chinese_PRC_CI_AS'), server_default=text("('')")),
    Column('FLD_QUESTUNITOPEN', BINARY(128), nullable=False, server_default=text('((0))')),
    Column('FLD_QUESTUNIT', BINARY(128), nullable=False, server_default=text('((0))')),
    Column('FLD_QUESTFLAG', BINARY(128), nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_DC', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_MC', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_SC', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_AC', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_MAC', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_HP', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_MP', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_HIT', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_SPEED', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_X2', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_SELECTID', TINYINT, nullable=False, server_default=text('((0))')),
    Column('FLD_BTF9', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_SYSVAR', BINARY(400), nullable=False, server_default=text('((0))')),
    Column('FLD_EE', TINYINT, nullable=False, server_default=text('((0))')),
    Column('FLD_UVAR', BINARY(1020), nullable=False, server_default=text('((0))')),
    Column('FLD_FEATURE', String(200, 'Chinese_PRC_CI_AS'), server_default=text("('')")),
    Column('FLD_SUCKDAMAGECOUNT', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_SUCKDAMAGERATE', TINYINT, nullable=False, server_default=text('((0))')),
    Column('FLD_SUCKDAMAGEBILI', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_SNDAITEMBOXOPENED', TINYINT, nullable=False, server_default=text('((0))')),
    Column('FLD_SDKID', String(50, 'Chinese_PRC_CI_AS'), server_default=text("('')")),
    Column('FLD_SERVERID', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_DC', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_HumParams', String(collation='Chinese_PRC_CI_AS')),
    Index('IX_TBL_HERO_FLD_CHARACTER', 'FLD_CHARACTER'),
    Index('IX_TBL_HERO_FLD_UPDATEDATETIME', 'FLD_UPDATEDATETIME'),
    Index('IX_TBL_HERO_FLD_USERID', 'FLD_USERID')
)


t_TBL_HERO_BAG = Table(
    'TBL_HERO_BAG', Base.metadata,
    Column('FLD_USERID', String(50, 'Chinese_PRC_CI_AS')),
    Column('FLD_MAKEINDEX', Integer, nullable=False),
    Column('FLD_INDEX', Integer),
    Column('FLD_DURA', Integer),
    Column('FLD_DURAMAX', Integer),
    Column('FLD_BTVALUE', BINARY(200)),
    Column('FLD_WHERE', Integer),
    Column('FLD_OVERLAP', Integer),
    Column('FLD_AddVale', BINARY(80)),
    Column('FLD_EXTEND', String(500, 'Chinese_PRC_CI_AS')),
    Index('IX_TBL_HERO_BAG_FLD_MAKEINDEX', 'FLD_MAKEINDEX'),
    Index('IX_TBL_HERO_BAG_FLD_USERID', 'FLD_USERID')
)


t_TBL_HERO_BODY = Table(
    'TBL_HERO_BODY', Base.metadata,
    Column('FLD_USERID', String(50, 'Chinese_PRC_CI_AS')),
    Column('FLD_MAKEINDEX', Integer, nullable=False),
    Column('FLD_INDEX', Integer),
    Column('FLD_DURA', Integer),
    Column('FLD_DURAMAX', Integer),
    Column('FLD_BTVALUE', BINARY(200)),
    Column('FLD_WHERE', Integer),
    Column('FLD_OVERLAP', Integer),
    Column('FLD_AddVale', BINARY(80)),
    Column('FLD_EXTEND', String(500, 'Chinese_PRC_CI_AS')),
    Index('IX_TBL_HERO_BODY_FLD_MAKEINDEX', 'FLD_MAKEINDEX'),
    Index('IX_TBL_HERO_BODY_FLD_USERID', 'FLD_USERID')
)


t_TBL_HERO_MAGIC = Table(
    'TBL_HERO_MAGIC', Base.metadata,
    Column('FLD_USERID', String(50, 'Chinese_PRC_CI_AS')),
    Column('FLD_MAGICID', Integer, nullable=False),
    Column('FLD_LEVEL', TINYINT),
    Column('FLD_KEY', TINYINT),
    Column('FLD_CURTRAIN', Integer),
    Column('FLD_LEVEL_UP', Integer),
    Index('IX_TBL_HERO_MAGIC_FLD_USERID', 'FLD_USERID')
)


t_TBL_ITEM_BAG = Table(
    'TBL_ITEM_BAG', Base.metadata,
    Column('FLD_USERID', String(50, 'Chinese_PRC_CI_AS')),
    Column('FLD_MAKEINDEX', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_INDEX', Integer),
    Column('FLD_DURA', Integer),
    Column('FLD_DURAMAX', Integer),
    Column('FLD_BTVALUE', BINARY(200)),
    Column('FLD_WHERE', Integer),
    Column('FLD_OVERLAP', Integer),
    Column('FLD_AddVale', BINARY(80)),
    Column('FLD_EXTEND', String(500, 'Chinese_PRC_CI_AS')),
    Index('IX_TBL_ITEM_BAG_FLD_MAKEINDEX', 'FLD_MAKEINDEX'),
    Index('IX_TBL_ITEM_BAG_FLD_USERID', 'FLD_USERID')
)


t_TBL_ITEM_BODY = Table(
    'TBL_ITEM_BODY', Base.metadata,
    Column('FLD_USERID', String(50, 'Chinese_PRC_CI_AS')),
    Column('FLD_MAKEINDEX', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_INDEX', Integer),
    Column('FLD_DURA', Integer),
    Column('FLD_DURAMAX', Integer),
    Column('FLD_BTVALUE', BINARY(200)),
    Column('FLD_WHERE', Integer),
    Column('FLD_OVERLAP', Integer),
    Column('FLD_AddVale', BINARY(80)),
    Column('FLD_EXTEND', String(500, 'Chinese_PRC_CI_AS')),
    Index('IX_TBL_ITEM_BODY_FLD_MAKEINDEX', 'FLD_MAKEINDEX'),
    Index('IX_TBL_ITEM_BODY_FLD_USERID', 'FLD_USERID')
)


t_TBL_ITEM_EX_ABIL = Table(
    'TBL_ITEM_EX_ABIL', Base.metadata,
    Column('FLD_MAKEINDEX', Integer, nullable=False),
    Column('FLD_EX_ABIL', String(8000, 'Chinese_PRC_CI_AS')),
    Column('fld_Params', String(collation='Chinese_PRC_CI_AS')),
    Index('IX_TBL_ITEM_EX_ABIL_FLD_MAKEINDEX', 'FLD_MAKEINDEX')
)


t_TBL_ITEM_GUILD_STORAGE = Table(
    'TBL_ITEM_GUILD_STORAGE', Base.metadata,
    Column('FLD_MAKEINDEX', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_INDEX', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_DURA', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_DURAMAX', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_BTVALUE', BINARY(200), server_default=text('((0))')),
    Column('FLD_WHERE', Integer, nullable=False, server_default=text('((-1))')),
    Column('FLD_OVERLAP', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_GUILDID', String(50, 'Chinese_PRC_CI_AS'), nullable=False, server_default=text("('')")),
    Column('FLD_AddVale', BINARY(80)),
    Column('FLD_EXTEND', String(500, 'Chinese_PRC_CI_AS')),
    Index('IX_TBL_ITEM_GUILD_STORAGE_FLD_MAKEINDEX', 'FLD_MAKEINDEX')
)


t_TBL_ITEM_JISHOU = Table(
    'TBL_ITEM_JISHOU', Base.metadata,
    Column('FLD_MAKEINDEX', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_INDEX', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_DURA', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_DURAMAX', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_BTVALUE', BINARY(200), server_default=text('((0))')),
    Column('FLD_WHERE', Integer, nullable=False, server_default=text('((-1))')),
    Column('FLD_OVERLAP', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_USERID', String(50, 'Chinese_PRC_CI_AS'), nullable=False, server_default=text("('')")),
    Column('FLD_TYPE', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_PRICE', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_ADDTIME', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_AddVale', BINARY(80)),
    Column('FLD_EXTEND', String(500, 'Chinese_PRC_CI_AS')),
    Index('IX_TBL_ITEM_JISHOU_FLD_MAKEINDEX', 'FLD_MAKEINDEX')
)


t_TBL_ITEM_LEVELVALUE = Table(
    'TBL_ITEM_LEVELVALUE', Base.metadata,
    Column('nIdx', Integer),
    Column('ItemValue', SmallInteger, nullable=False),
    Column('MakeDate', DateTime, nullable=False),
    Column('wIndex', Integer, nullable=False),
    Column('sChrName', String(50, 'Chinese_PRC_CI_AS'), nullable=False),
    Column('sMap', String(16, 'Chinese_PRC_CI_AS'), nullable=False),
    Column('sMonName', String(50, 'Chinese_PRC_CI_AS'), nullable=False),
    Column('sUserID', String(30, 'Chinese_PRC_CI_AS'))
)


t_TBL_ITEM_PAIMAI = Table(
    'TBL_ITEM_PAIMAI', Base.metadata,
    Column('FLD_MAKEINDEX', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_INDEX', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_DURA', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_DURAMAX', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_BTVALUE', BINARY(200), server_default=text('((0))')),
    Column('FLD_ADDVALUE', BINARY(80), nullable=False),
    Column('FLD_WHERE', Integer, nullable=False, server_default=text('((-1))')),
    Column('FLD_OVERLAP', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_USERID', String(50, 'Chinese_PRC_CI_AS'), nullable=False, server_default=text("('')")),
    Column('FLD_TYPE', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_PRICE', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_ADDTIME', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_USERLIST', String(3000, 'Chinese_PRC_CI_AS'), nullable=False, server_default=text("('')")),
    Column('FLD_JOINUSERLIST', String(1500, 'Chinese_PRC_CI_AS'), nullable=False, server_default=text("('')")),
    Column('FLD_LASTPRICE', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_CURRUSERID', String(50, 'Chinese_PRC_CI_AS'), nullable=False, server_default=text("('')")),
    Column('FLD_PAGE', SmallInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_LASTTIME', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_FLAG', SmallInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_ID', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_GUILDID', String(50, 'Chinese_PRC_CI_AS'), nullable=False, server_default=text("('')")),
    Column('FLD_MEGUILDRATE', Integer, nullable=False, server_default=text('((90))')),
    Column('FLD_STDMODE', Integer, nullable=False),
    Column('FLD_QUALITY', Integer, nullable=False),
    Column('FLD_JOB', SmallInteger, nullable=False),
    Column('FLD_LEVEL', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_EXTENDINFO', String(500, 'Chinese_PRC_CI_AS')),
    Index('IX_TBL_ITEM_PAIMAI_FLD_ADDTIME', 'FLD_ADDTIME'),
    Index('IX_TBL_ITEM_PAIMAI_FLD_GUILDID', 'FLD_GUILDID'),
    Index('IX_TBL_ITEM_PAIMAI_FLD_LEVEL', 'FLD_LEVEL'),
    Index('IX_TBL_ITEM_PAIMAI_FLD_PRICE', 'FLD_PRICE'),
    Index('IX_TBL_ITEM_PAIMAI_MAKEINDEX', 'FLD_MAKEINDEX')
)


t_TBL_ITEM_STORAGE = Table(
    'TBL_ITEM_STORAGE', Base.metadata,
    Column('FLD_USERID', String(50, 'Chinese_PRC_CI_AS')),
    Column('FLD_MAKEINDEX', Integer, nullable=False),
    Column('FLD_INDEX', Integer),
    Column('FLD_DURA', Integer),
    Column('FLD_DURAMAX', Integer),
    Column('FLD_BTVALUE', BINARY(200)),
    Column('FLD_WHERE', Integer),
    Column('FLD_OVERLAP', Integer),
    Column('FLD_AddVale', BINARY(80)),
    Column('FLD_EXTEND', String(500, 'Chinese_PRC_CI_AS')),
    Index('IX_TBL_ITEM_STORAGE_FLD_MAKEINDEX', 'FLD_MAKEINDEX'),
    Index('IX_TBL_ITEM_STORAGE_FLD_USERID', 'FLD_USERID')
)


t_TBL_LINE = Table(
    'TBL_LINE', Base.metadata,
    Column('nId', Integer, Identity(start=1, increment=1), nullable=False),
    Column('Time', Integer),
    Column('Num', Integer)
)


t_TBL_MAGIC = Table(
    'TBL_MAGIC', Base.metadata,
    Column('FLD_USERID', String(50, 'Chinese_PRC_CI_AS')),
    Column('FLD_MAGICID', Integer, nullable=False),
    Column('FLD_LEVEL', TINYINT),
    Column('FLD_KEY', TINYINT),
    Column('FLD_CURTRAIN', Integer),
    Column('FLD_LEVEL_UP', Integer, server_default=text('((0))')),
    Index('IX_TBL_MAGIC_FLD_USERID', 'FLD_USERID')
)


class TBLMAIL(Base):
    __tablename__ = 'TBL_MAIL'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='PK__TBL_MAIL__3214EC27740C2988'),
        Index('IX_TBL_MAIL_UserID', 'UserID'),
        Index('IX_TBL_MAIL_dCreateTime', 'dCreateTime')
    )

    ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    UserID: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    SendName: Mapped[Optional[str]] = mapped_column(String(128, 'Chinese_PRC_CI_AS'))
    Type: Mapped[Optional[int]] = mapped_column(Integer)
    Lable: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    Memo: Mapped[Optional[str]] = mapped_column(String(1024, 'Chinese_PRC_CI_AS'))
    Item: Mapped[Optional[str]] = mapped_column(String(4096, 'Chinese_PRC_CI_AS'))
    dCreateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    dRecvTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ReadFlag: Mapped[Optional[int]] = mapped_column(SmallInteger)
    RecvFlag: Mapped[Optional[int]] = mapped_column(SmallInteger)
    Deleted: Mapped[Optional[int]] = mapped_column(SmallInteger)
    dDeleteTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class TBLNATIONINFO(Base):
    __tablename__ = 'TBL_NATION_INFO'
    __table_args__ = (
        PrimaryKeyConstraint('sNationUID', name='PK__TBL_NATI__2AD156350D5A9384'),
    )

    nIdx: Mapped[int] = mapped_column(Integer, server_default=text('((0))'))
    sNationUID: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'), primary_key=True)
    sNationName: Mapped[Optional[str]] = mapped_column(String(128, 'Chinese_PRC_CI_AS'))
    nLevel: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))
    nGold: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    nExp: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    dCreateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    btDeleted: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))
    nMemberCount: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    nAdvValue: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    sRanks: Mapped[Optional[str]] = mapped_column(String(500, 'Chinese_PRC_CI_AS'), server_default=text("('')"))
    nServerID: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))


t_TBL_NATION_MEMBER = Table(
    'TBL_NATION_MEMBER', Base.metadata,
    Column('nIdx', String(50, 'Chinese_PRC_CI_AS'), server_default=text('((0))')),
    Column('sUserID', String(50, 'Chinese_PRC_CI_AS'), server_default=text('((0))')),
    Column('btRank', SmallInteger, server_default=text('((0))')),
    Column('btJob', SmallInteger, server_default=text('((0))')),
    Column('btJoin', SmallInteger, server_default=text('((0))')),
    Column('nLevel', Integer, server_default=text('((0))')),
    Column('nAdvValue', Integer, server_default=text('((0))'))
)


t_TBL_PET = Table(
    'TBL_PET', Base.metadata,
    Column('FLD_ID', Integer, Identity(start=1, increment=1), nullable=False),
    Column('FLD_MASTERUSERID', String(128, 'Chinese_PRC_CI_AS'), nullable=False),
    Column('FLD_PETIDX', Integer, server_default=text('((0))')),
    Column('FLD_PETNAME', String(50, 'Chinese_PRC_CI_AS'), nullable=False),
    Column('FLD_USERID', String(50, 'Chinese_PRC_CI_AS')),
    Column('FLD_DELETED', TINYINT, nullable=False, server_default=text('((0))')),
    Column('FLD_UPDATEDATETIME', DateTime),
    Column('FLD_RELEVEL', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_LEVEL', Integer, nullable=False, server_default=text('((0))')),
    Column('FLD_HP', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_MP', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_EXP', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_MAKEDATE', DateTime),
    Column('FLD_StatusTimeArr', BINARY(24), nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_DC', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_MC', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_SC', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_AC', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_MAC', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_HP', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_MP', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_HIT', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_BONUS_SPEED', BigInteger, nullable=False, server_default=text('((0))')),
    Column('FLD_FEATURE', String(200, 'Chinese_PRC_CI_AS'), server_default=text("('')")),
    Column('FLD_BODYITEM', String(200, 'Chinese_PRC_CI_AS'), server_default=text("('')")),
    Column('FLD_MASTERNAME', String(50, 'Chinese_PRC_CI_AS')),
    Column('FLD_BONUSPOINT', BigInteger, server_default=text('((0))')),
    Column('FLD_BONUS_X2', BigInteger, server_default=text('((0))')),
    Column('FLD_STATE', TINYINT, server_default=text('((1))')),
    Index('IX_TBL_PET_FLD_USERID', 'FLD_USERID')
)


t_TBL_QUESTINFO = Table(
    'TBL_QUESTINFO', Base.metadata,
    Column('FLD_ID', Integer, Identity(start=1, increment=1), nullable=False),
    Column('questid', String(30, 'Chinese_PRC_CI_AS'), server_default=text('((0))')),
    Column('questStatus', SmallInteger, server_default=text('((0))')),
    Column('questMsg', String(30, 'Chinese_PRC_CI_AS'), server_default=text("('')")),
    Column('questdate', DateTime)
)


class TBLVAR(Base):
    __tablename__ = 'TBL_VAR'
    __table_args__ = (
        PrimaryKeyConstraint('uGuid', name='PK__TBL_VAR__7182A455B81EAFB8'),
        Index('TBL_VAR_FLD_USERID', 'FLD_USERID'),
        Index('TBL_VAR_FLD_VAR_NAME', 'FLD_VAR_NAME')
    )

    uGuid: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('(newid())'))
    FLD_USERID: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    FLD_VAR_NAME: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    FLD_TYPE: Mapped[int] = mapped_column(SmallInteger, server_default=text('((0))'))
    FLD_TIMESTAMP: Mapped[bytes] = mapped_column(TIMESTAMP)
    FLD_VAR_VALUE: Mapped[Optional[str]] = mapped_column(String(collation='Chinese_PRC_CI_AS'))
    tUpdateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('(getdate())'))
    FLD_JOINTYPE: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))


class TLOGBOXSELL(Base):
    __tablename__ = 'TLOG_BOX_SELL'
    __table_args__ = (
        PrimaryKeyConstraint('FLD_ID', name='PK__TLOG_BOX_SELL'),
        Index('FLD_ID_IDX', 'FLD_ID', unique=True),
        Index('IX_TLOG_BOX_SELL_FLD_ORDER', 'FLD_ORDER'),
        Index('IX_TLOG_BOX_SELL_FLD_STATE', 'FLD_STATE'),
        Index('IX_TLOG_BOX_SELL_FLD_USERID', 'FLD_USERID')
    )

    FLD_ID: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    FLD_USERID: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    FLD_BUYUSERID: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    FLD_PAYORDER: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_CI_AS'), server_default=text("('')"))
    FLD_STATUS: Mapped[int] = mapped_column(TINYINT, server_default=text('((0))'))
    FLD_MONEYID: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))
    FLD_MONEY: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('((0))'))
    FLD_ORDER: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    FLD_CREATEDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    FLD_UPDATEEDATE: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    FLD_STATE: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))
    FLD_DECSTATE: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))
    FLD_GETSTATE: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('((0))'))


class Diypay(Base):
    __tablename__ = 'diypay'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK__diypay__3214EC07A0A8F97B'),
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    PayId: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_CI_AS'))
    sGameOrder: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_CI_AS'))
    sRoleId: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_CI_AS'))
    Account: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_CI_AS'))
    SdkId: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    ServerId: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    ProductId: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    Gold: Mapped[Any] = mapped_column(MONEY)
    ExtData: Mapped[Optional[str]] = mapped_column(String(512, 'Chinese_PRC_CI_AS'))
    SecSdkId: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    DrawOut: Mapped[Optional[int]] = mapped_column(Integer)
    DrawLevel: Mapped[Optional[int]] = mapped_column(Integer)
    DrawTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    sChrName: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    CreateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    nExtid: Mapped[Optional[int]] = mapped_column(Integer)
    nExt1: Mapped[Optional[int]] = mapped_column(Integer)


class Pay(Base):
    __tablename__ = 'pay'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK__pay__3214EC07A0A8F97B'),
        Index('PayGameOrder', 'sGameOrder', unique=True)
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    PayId: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_CI_AS'))
    sGameOrder: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_CI_AS'))
    sRoleId: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_CI_AS'))
    Account: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_CI_AS'))
    SdkId: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    ServerId: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    ProductId: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    Gold: Mapped[Any] = mapped_column(MONEY)
    ExtData: Mapped[Optional[str]] = mapped_column(String(512, 'Chinese_PRC_CI_AS'))
    SecSdkId: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    nRealGold: Mapped[Optional[Any]] = mapped_column(MONEY)
    DrawOut: Mapped[Optional[int]] = mapped_column(Integer)
    DrawLevel: Mapped[Optional[int]] = mapped_column(Integer)
    DrawTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    sChrName: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_CI_AS'))
    CreateTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    nExtid: Mapped[Optional[int]] = mapped_column(Integer)
    nExt1: Mapped[Optional[int]] = mapped_column(Integer)
    OldGold: Mapped[Optional[Any]] = mapped_column(MONEY)
