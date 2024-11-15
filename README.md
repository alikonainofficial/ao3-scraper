AO3 Scraper

This script is designed to scrape story metadata and content from Archive of Our Own (AO3), allowing users to extract story details and download stories in EPUB format.

Features

	•	Scrapes metadata including:
	•	Title, Author, Fandom, Tags
	•	Characters, Relationships, Ratings
	•	Warnings, Categories, Word Count
	•	Chapters, Language, Status
	•	Comments, Kudos, Bookmarks, Collections, Hits
	•	Summary
	•	Downloads stories in EPUB format.
	•	Saves metadata in a CSV file.
	•	Supports pagination and retry mechanisms for robust scraping.

Usage

	1.	Clone this repository:

git clone <repository-url>
cd ao3-scraper


	2.	Install dependencies:

pip install -r requirements.txt


	3.	Run the script:

python ao3_scraper.py


	4.	Provide the following inputs:
	•	The main AO3 search URL (with page=1 in the query).
	•	The number of stories to scrape.
	5.	Scraped metadata will be saved in stories_metadata.csv. EPUB files will be stored in the content directory.

Dependencies

	•	Python 3.7+
	•	Required libraries: os, time, requests, beautifulsoup4, uuid, csv, logging

Install Python libraries using:

pip install requests beautifulsoup4

Logging

Logs are saved in scrape_ao3_story_content.log for tracking progress and errors.

Notes

	•	This script is for personal use only and should not be used to violate AO3’s Terms of Service.
	•	Large-scale scraping may lead to your IP being blocked by AO3. Use responsibly.

License

This project is licensed under the MIT License.

Disclaimer

This script is provided as-is, without any guarantees. Use it responsibly and comply with AO3’s Terms of Service.