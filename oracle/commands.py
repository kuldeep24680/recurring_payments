import datetime

from flask_script import Command, prompt_bool
from oracle import local_config as settings
from oracle import db
from oracle.local_config import ADMIN, MONGODB_SETTINGS
from oracle.services import logger
from oracle.utils import generate_bcrypt_hash
from organisation.model import OracleOrgUser, OracleOrgCustomer



class InitDB(Command):
    """Initialize new database."""

    def run(self):
        dbname = MONGODB_SETTINGS["DB"]
        user = OracleOrgUser.objects.create(email_id = ADMIN["email_id"])
        user.set_password(ADMIN["password"])
        user.username="oracle admin"
        user.is_head_merchant = False
        user.is_admin = True
        user.save()
        print("creating database {database} successful.".format(database=dbname))



class DropDB(Command):
    """Drop existing database."""

    def run(self):
        if prompt_bool(
            "Are you sure you want to loose all data for {DB}@{HOST}:{PORT}?".format(
                **settings.MONGODB_SETTINGS
            )
        ):
            logger.info(
                "\ndropping db: {DB} on {HOST}:{PORT} started.\n".format(
                    **settings.MONGODB_SETTINGS
                )
            )
            dbname = settings.MONGODB_SETTINGS["DB"]
            db.connection.drop_database(dbname)
            logger.info("dropping database {database} successful.".format(database=dbname))


class DescDB(Command):
    """Describes the db"""

    def run(self):
        print("merchants    count : %s" % OracleOrgUser.objects.all().count())
        print("customers  count : %s " % OracleOrgCustomer.objects.all().count())



def add_commands(manager):
    manager.add_command("initdb", InitDB())
    #    manager.add_command( 'dropdb', DropDB())
    manager.add_command("descdb", DescDB())
