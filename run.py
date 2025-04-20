from menu import Menu
import logging

LOGGER: logging.Logger = logging.getLogger("Menu")

if __name__ == '__main__':
    menu = Menu()
    try:
        menu.run()
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt...")

    