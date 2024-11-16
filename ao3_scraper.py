"""
ao3_scraper.py

This script is designed to scrape story metadata and content from Archive of Our Own (AO3).
It fetches details such as title, author, fandom, tags, characters, relationships, ratings,
warnings, categories, word counts, chapters, language, and more.

The script also downloads stories in EPUB format and saves their metadata to a CSV file.
It supports pagination and retry mechanisms for robust scraping.

Usage:
    Run the script, provide the main AO3 search link, and specify the number of stories to scrape.

Dependencies:
    - os
    - time
    - requests
    - BeautifulSoup4
    - uuid
    - csv
    - logging
"""

import os
import logging
import uuid
import time
import csv
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="scrape_ao3_story_content.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def log_to_console_and_file(level, message, *args):
    """
    Helper function to log messages to both console and file with lazy formatting.
    """
    if level == "info":
        logger.info(message, *args)
        print(message % args)
    elif level == "warning":
        logger.warning(message, *args)
        print(message % args)
    elif level == "error":
        logger.error(message, *args)
        print(message % args)


def populate_metadata(story_id, story_url, story_soup):
    """
    Extract metadata from a story's BeautifulSoup object.

    Args:
        story_id (str): The unique identifier for the story.
        story_soup (BeautifulSoup): Parsed HTML content of the story page.

    Returns:
        dict: A dictionary containing metadata fields such as title, author, fandom, tags, and more.
    """
    metadata = {}

    metadata["ID"] = str(uuid.uuid4())

    metadata["Work ID"] = story_id
    metadata["Story Link"] = story_url
    metadata["Title"] = (
        story_soup.find("h2", class_="title heading").text.strip().replace("’", "'")
        if story_soup.find("h2", class_="title heading")
        else ""
    )
    metadata["Author"] = (
        story_soup.find("a", rel="author").text.strip().replace("’", "'")
        if story_soup.find("a", rel="author")
        else ""
    )
    metadata["Fandom"] = (
        ", ".join(
            [fandom.text.replace("’", "'") for fandom in story_soup.select(".fandom.tags .tag")]
        )
        or ""
    )
    metadata["Tags"] = (
        ", ".join([tag.text.replace("’", "'") for tag in story_soup.select(".freeform.tags .tag")])
        or ""
    )
    metadata["Characters"] = (
        ", ".join(
            [
                character.text.replace("’", "'")
                for character in story_soup.select(".character.tags .tag")
            ]
        )
        or ""
    )
    metadata["Relationships"] = (
        ", ".join(
            [
                relationship.text.replace("’", "'")
                for relationship in story_soup.select(".relationship.tags .tag")
            ]
        )
        or ""
    )
    metadata["Ratings"] = (
        ", ".join(
            [rating.text.replace("’", "'") for rating in story_soup.select(".rating.tags .tag")]
        )
        or ""
    )
    metadata["Warnings"] = (
        ", ".join(
            [warning.text.replace("’", "'") for warning in story_soup.select(".warning.tags .tag")]
        )
        or ""
    )
    metadata["Categories"] = (
        ", ".join(
            [
                category.text.replace("’", "'")
                for category in story_soup.select(".category.tags .tag")
            ]
        )
        or ""
    )

    # Convert text to integer or assign 0 if missing
    metadata["Words"] = (
        int(story_soup.find("dd", class_="words").text.strip().replace(",", ""))
        if story_soup.find("dd", class_="words")
        else 0
    )

    # Extract numeric value from Chapters
    chapters_text = (
        story_soup.find("dd", class_="chapters").text.strip()
        if story_soup.find("dd", class_="chapters")
        else "0"
    )
    metadata["Chapters"] = int(chapters_text.split("/")[0])

    metadata["Language"] = (
        story_soup.find("dd", class_="language").text.strip()
        if story_soup.find("dd", class_="language")
        else "English"
    )
    metadata["Status"] = (
        story_soup.find("dd", class_="status").text.strip()
        if story_soup.find("dd", class_="status")
        else ""
    )

    # Convert text to integer or assign 0 if missing for Comments, Kudos, Bookmarks, Hits
    metadata["Comments"] = (
        int(story_soup.find("dd", class_="comments").text.strip().replace(",", ""))
        if story_soup.find("dd", class_="comments")
        else 0
    )
    metadata["Kudos"] = (
        int(story_soup.find("dd", class_="kudos").text.strip().replace(",", ""))
        if story_soup.find("dd", class_="kudos")
        else 0
    )
    metadata["Bookmarks"] = (
        int(story_soup.find("dd", class_="bookmarks").text.strip().replace(",", ""))
        if story_soup.find("dd", class_="bookmarks")
        else 0
    )
    metadata["Collections"] = (
        ", ".join(
            [
                collection.text.replace("’", "'")
                for collection in story_soup.select(".collections a")
            ]
        )
        or ""
    )
    metadata["Hits"] = (
        int(story_soup.find("dd", class_="hits").text.strip().replace(",", ""))
        if story_soup.find("dd", class_="hits")
        else 0
    )

    # Assign default value for Summary if missing
    metadata["Summary"] = (
        story_soup.find("div", class_="summary module")
        .find("blockquote", class_="userstuff")
        .text.strip()
        .replace("’", "'")
        if story_soup.find("div", class_="summary module")
        and story_soup.find("div", class_="summary module").find("blockquote", class_="userstuff")
        else ""
    )
    return metadata


# Function to make a request with exponential backoff and delay adjustments
def make_request(url, headers=None, retries=5, initial_delay=2, max_delay=60, timeout=30):
    """
    Make a request with exponential backoff and skip if retries are exhausted.

    Args:
        url (str): The URL to request.
        headers (dict): Optional headers for the request.
        retries (int): Number of retry attempts.
        initial_delay (int): Initial wait time in seconds.
        max_delay (int): Maximum wait time in seconds.
        timeout (int): Request timeout in seconds.

    Returns:
        requests.Response or None: The response if successful, None if retries are exhausted.
    """
    wait_time = initial_delay
    response = None
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            if wait_time > initial_delay:
                wait_time = max(
                    initial_delay, wait_time // 2
                )  # Reduce delay if it was increased before
            return response
        except requests.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            if response and response.status_code == 429:
                logging.warning(f"Rate limited (429) for {url}. Adjusting backoff.")
            if i < retries - 1:
                logging.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                wait_time = min(max_delay, wait_time * 2)  # Exponential backoff
            else:
                logging.error(f"Failed to fetch {url} after {retries} retries")
                return None


def scrape_ao3_stories(main_link, num_stories):
    """
    Scrape metadata and content from AO3 stories.

    Args:
        main_link (str): The main URL for the AO3 story search results, with `page=1` specified.
        num_stories (int): Number of stories to scrape.

    Returns:
        None
    """
    # Constants and setup
    headers = {"User-Agent": "Mozilla/5.0"}
    content_dir = "content"
    scraped_file = "scraped_stories.txt"
    output_csv = "stories_metadata.csv"

    # Ensure content directory exists
    os.makedirs(content_dir, exist_ok=True)

    # Load already scraped story IDs
    scraped_ids = set()
    if os.path.exists(scraped_file):
        with open(scraped_file, "r", encoding="utf-8") as file:
            scraped_ids = set(line.strip() for line in file)

    # Prepare CSV file for metadata
    if not os.path.exists(output_csv):
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "ID",
                    "Work ID",
                    "Story Link",
                    "Title",
                    "Author",
                    "Fandom",
                    "Tags",
                    "Characters",
                    "Relationships",
                    "Rating",
                    "Warnings",
                    "Categories",
                    "Words",
                    "Chapters",
                    "Language",
                    "Status",
                    "Comments",
                    "Kudos",
                    "Bookmarks",
                    "Collections",
                    "Hits",
                    "Summary",
                ]
            )

    # Start scraping
    scraped_count = 0
    current_page = 1

    while scraped_count < num_stories:
        page_url = main_link.replace("page=1", f"page={current_page}")
        response = make_request(page_url, headers=headers, retries=5, initial_delay=2, max_delay=60)
        if not response:
            log_to_console_and_file("warning", "Skipping page due to repeated errors: %s", page_url)
            current_page += 1
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        works = soup.find_all("li", class_="work")

        soup = BeautifulSoup(response.content, "html.parser")
        works = soup.find_all("li", class_="work")

        for i, work in enumerate(works):
            if scraped_count >= num_stories:
                break

            heading = work.find("h4", class_="heading")
            if heading:

                link = heading.find("a")
                if link and "href" in link.attrs:
                    story_link = link["href"]
                    story_id = story_link.split("/")[-1]
                    story_url = f"https://archiveofourown.org{story_link}?view_adult=true"
                    if story_id in scraped_ids:
                        continue
                    story_response = make_request(
                        story_url, headers=headers, retries=5, initial_delay=2, max_delay=60
                    )
                    if not story_response:
                        log_to_console_and_file(
                            "warning", "Skipping story due to repeated errors: %s", story_url
                        )
                        continue
                    story_soup = BeautifulSoup(story_response.content, "html.parser")

                    try:
                        # Scrape metadata
                        metadata = populate_metadata(story_id, story_url, story_soup)

                        # Append metadata to CSV
                        with open(output_csv, "a", newline="", encoding="utf-8") as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(metadata.values())

                        # Download EPUB
                        download_link = story_soup.find("li", class_="download").find(
                            "a", href=True, string="EPUB"
                        )["href"]
                        epub_url = f"https://archiveofourown.org{download_link}"
                        epub_response = make_request(
                            epub_url, headers=headers, retries=5, initial_delay=2, max_delay=60
                        )
                        epub_file_path = os.path.join(content_dir, f"{metadata['ID']}.epub")

                        with open(epub_file_path, "wb") as epub_file:
                            epub_file.write(epub_response.content)

                        # Mark as scraped
                        with open(scraped_file, "a", encoding="utf-8") as file:
                            file.write(f"{story_id}\n")
                        scraped_ids.add(story_id)

                        scraped_count += 1
                        log_to_console_and_file(
                            "info",
                            "Scraped story %d/%d: %s",
                            scraped_count,
                            num_stories,
                            metadata["Title"],
                        )

                    except Exception as e:
                        log_to_console_and_file(
                            "error", "Failed to scrape story %s: %s", story_url, e
                        )
                        continue

                else:
                    log_to_console_and_file(
                        "warning", "Missing story link in work item %d on page %s", i, page_url
                    )

            else:
                log_to_console_and_file(
                    "warning", "Missing heading in work item %d on page %s", i, page_url
                )
        current_page += 1


if __name__ == "__main__":
    start_page_link = input("Enter the main AO3 link: ")
    stories_to_scrape = int(input("Enter the number of stories to scrape: "))
    scrape_ao3_stories(start_page_link, stories_to_scrape)
