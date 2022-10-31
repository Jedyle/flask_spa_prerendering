import os

from flask import Flask
from flask_caching import Cache

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

config = {
    "CACHE_TYPE": "FileSystemCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": int(os.environ.get("CACHE_DEFAULT_TIMEOUT", 3600)),
    "CACHE_DIR": "/tmp",
}

app = Flask(__name__)
app.config.from_mapping(config)

cache = Cache(app)

BASE_URL = os.environ.get("BASE_URL")
DEFAULT_WAIT = int(os.environ.get("DEFAULT_WAIT", 2))


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
@cache.memoize()
def prerender(path):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(DEFAULT_WAIT)
    driver.get(f"{BASE_URL}/{path}")
    html = driver.page_source
    driver.close()
    return html


if __name__ == "__main__":
    app.run()
