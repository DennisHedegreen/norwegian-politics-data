import os
import os

os.environ.setdefault("WPD_PROFILE", "norway_only")
os.environ.setdefault("WPD_PUBLIC_PREVIEW", "true")
os.environ.setdefault("WPD_APP_TITLE", "Norwegian Politics Data")
os.environ.setdefault("WPD_EXPOSE_COUNTRIES", "norway")

from engine_app import main


main()
