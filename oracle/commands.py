from flask_script import Command, prompt_bool
from oracle import local_config as settings
from oracle import db
from oracle.services import logger
from organisation.model import OracleOrgUser, OracleOrgCustomer


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
    manager.add_command("dropdb", DropDB())
    #    manager.add_command( 'dropdb', DropDB())
    manager.add_command("descdb", DescDB())
