from django.apps import AppConfig
import sys


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        #print("--- CoreConfig.ready() called ---", file=sys.stderr) # DEBUG: Force print to stderr
        try:
            import core.signals # noqa
            #print("--- core.signals imported successfully in CoreConfig.ready() ---", file=sys.stderr) # DEBUG
        except ImportError as e:
            print(f"--- ERROR importing core.signals in CoreConfig.ready(): {e} ---", file=sys.stderr) # DEBUG
        except Exception as e:
            print(f"--- UNEXPECTED ERROR in CoreConfig.ready(): {e} ---", file=sys.stderr) # DEBUG