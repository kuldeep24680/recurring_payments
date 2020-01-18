import os, sys
from oracle import mainapp
from flask_script import Manager, Server

manager = Manager(mainapp)

# Turn on debugger by default and reloader
manager.add_command(
    "runserver", Server(use_debugger=True, use_reloader=True, host="0.0.0.0", port=8080)
)

from deploy.GunicornServer import GunicornServer

manager.add_command("rungunicorn", GunicornServer())

from oracle import commands

commands.add_commands(manager)


if __name__ == "__main__":
    manager.run()
