import pandas as pd
import requests
from bs4 import BeautifulSoup

def run_scraper():
    print("Hello from inside the Docker container!")
    print(f"Pandas version: {pd.__version__}")
    print(f"Requests version: {requests.__version__}")
    print(f"BeautifulSoup is ready.")
    print("--------------------------------")
    print("Now you can start building your scraper logic here.")

if __name__ == "__main__":
    run_scraper()