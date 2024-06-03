from main import app, db
from flask_migrate import Migrate, upgrade as flask_upgrade, migrate as flask_migrate, init as flask_init, \
    revision as flask_revision
import sys

migrate = Migrate(app, db)


def main_db():
    if len(sys.argv) < 2:
        print("Usage: python manager.py <command>")
        return

    command = sys.argv[1]

    if command == "db":
        if len(sys.argv) < 3:
            print("Usage: python manager.py db <subcommand>")
            return
        subcommand = sys.argv[2]

        with app.app_context():
            if subcommand == "init":
                flask_init(directory="migrations")
            elif subcommand == "migrate":
                flask_migrate(message="Initial migration")
            elif subcommand == "upgrade":
                flask_upgrade()
            elif subcommand == "revision":
                flask_revision(message="New revision")
            else:
                print(f"Unknown subcommand '{subcommand}'")
    else:
        print(f"Unknown command '{command}'")


if __name__ == '__main__':
    main_db()

#
# if __name__ == '__main__':
#     migrate.init_app(app,db)
#     # manager.run()
