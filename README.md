# AO3 Scraper

This script is designed to scrape story metadata and content from Archive of Our Own (AO3), allowing users to extract story details and download stories in EPUB format.

## Features

1. Scrapes metadata including:

	Title, Author, Fandom, Tags,
	Characters, Relationships, Ratings
	Warnings, Categories, Word Count,
	Chapters, Language, Status,
	Comments, Kudos, Bookmarks, Collections, Hits,
	Summary
2. Downloads stories in EPUB format.
3. Saves metadata in a CSV file.
4. Supports pagination and retry mechanisms for robust scraping.

## Usage

 1. Clone this repository:

	```bash
 	git clone <repository-url>
	cd ao3-scraper
	```

 2. Install dependencies:
 
 	```bash
  	pip install -r requirements.txt
	```

 3. Run the script:

   	```bash
  	python3 ao3_scraper.py
	```
    
 4. Provide the following inputs:

	• The main AO3 search URL (with page=1 in the query and any other filters that you want to apply). e.g. 

	```bash
	https://archiveofourown.org/tags/Marvel/works?page=1&work_search%5Bcomplete%5D=T&work_search%5Blanguage_id%5D=en&work_search%5Bsort_column%5D=hits
 	```
	
	• The number of stories to scrape.

    **Note:** _Some popular fandom links are available in ```scraping links``` file. You can simply copy any link from that file and paste it in the console input when prompted._
 6. Scraped metadata will be saved in stories_metadata.csv. EPUB files will be stored in the content directory.

## Dependencies

	• Python 3.7+
	• Required libraries: os, time, requests, beautifulsoup4, uuid, csv, logging


## Logging

Logs are saved in ```scrape_ao3_story_content.log``` for tracking progress and errors.

## Notes

• This script is for personal use only and should not be used to violate AO3’s Terms of Service.

• Large-scale scraping may lead to your IP being blocked by AO3. Use responsibly.
 

## License

This project is licensed under the MIT License.

## Disclaimer

This script is provided as-is, without any guarantees. Use it responsibly and comply with AO3’s Terms of Service.
