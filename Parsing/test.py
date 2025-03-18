import asyncio
import re
import pandas as pd
from pyppeteer import launch


async def scraper():
    browser = await launch({
        "headless": False,
        "executablePath": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    })
    page = await browser.newPage()
    await page.goto("https://www.kinopoisk.ru/lists/movies/top250/")

    # Wait for the movie elements to load
    await page.waitForSelector('[data-test-id="movie-list-item"]')

    # Select all movie elements by their data-test-id attribute
    movie_elements = await page.querySelectorAll('[data-test-id="movie-list-item"]')

    movies_data = []
    for movie in movie_elements:
        title_elem = await movie.querySelector('.styles_mainTitle__IFQyZ')
        title = await (await title_elem.getProperty('textContent')).jsonValue() if title_elem else 'N/A'
        title = title.strip()

        # Extract secondary text (contains year, runtime, etc.)
        secondary_elem = await movie.querySelector('.desktop-list-main-info_secondaryText__M_aus')
        secondary_text = await (
            await secondary_elem.getProperty('textContent')).jsonValue() if secondary_elem else 'N/A'
        secondary_text = secondary_text.strip()

        match = re.search(r'\b(19|20)\d{2}\b', secondary_text)
        year = match.group(0) if match else 'N/A'

        rating_elem = await movie.querySelector('.styles_kinopoiskValuePositive__7AAZG')
        rating = await (await rating_elem.getProperty('textContent')).jsonValue() if rating_elem else 'N/A'
        rating = rating.strip()

        movies_data.append({
            'title': title,
            'year': year,
            'rating': rating
        })

    df = pd.DataFrame(movies_data)
    print(df)

    await browser.close()


asyncio.run(scraper())
