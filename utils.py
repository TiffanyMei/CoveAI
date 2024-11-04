from selenium import webdriver
from selenium.webdriver.common.by import By
from collections import deque
from datetime import datetime


def _crawl_helper(driver: webdriver, url: str, base_url: str, visited: set[str], to_crawl: deque):
    """Helper function to crawl(). Executes scraping."""
    print(url)

    # read current page
    driver.get(url)
    content = driver.find_element(By.XPATH, "/html/body").text
    visited.add(url)

    # find links on current page, add to to_crawl
    elements = driver.find_elements(By.XPATH, "//a[@href]")
    for e in elements:
        try:
            href = e.get_attribute("href")
        except Exception as e:
            print(e)
            continue
        if base_url in href and href not in visited and href not in to_crawl:
            to_crawl.append(href)

    return content


def crawl(base_url: str, depth_limit: int) -> str:
    """
    Crawls the base_url and links that starts with base_url and can be reached from base_url via embedded web links.
    Pages are scraped following BFS order.
    :param base_url: base URL to crawl
    :param depth_limit: number of web pages to scrape starting from and including base_url
    :return: all scraped text content
    """
    t0 = datetime.now()
    print(f"Crawling {base_url=}, {depth_limit=}")

    driver = webdriver.Chrome()
    visited = set()
    content = ""
    to_crawl = deque()
    to_crawl.append(base_url)

    while len(to_crawl):
        if len(visited) >= depth_limit:
            print("reached depth limit")
            break
        content += _crawl_helper(driver=driver, url=to_crawl.popleft(), base_url=base_url, visited=visited, to_crawl=to_crawl)

    driver.close()
    print(f"Crawl took {(datetime.now() - t0).seconds}s")
    return content