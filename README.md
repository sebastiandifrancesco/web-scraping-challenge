# web-scraping-challenge

## Step 1: Scraping

Scarping from the following websites was done using Jupyter Notebook, BeautifulSoup, Pandas, and Splinter

* [NASA Mars News Site](https://mars.nasa.gov/news/): 
  * The latest news title 
  * The latest news paragraph text

* [JPL Featured Space Image](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars): 
  * The image url for the current Featured Space image
  
* [Mars Facts](https://space-facts.com/mars/): 
  * the Mars facts table: Pandas was used to convert the data to a HTML table string

* [USGS Astrogeology](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars): 
  * The full-resolution image url of each hemisphere
## Step 2: MongoDB and Flask Application:

MongoDB and Flask templating were used to create new HTML pages that displayed the scraped information.

* The Jupyter notebook was converted into a Python script called `scrape_mars.py` with a function called `scrape` that executes all of the scraping code from above and returns one Python dictionary containing all of the scraped data.

* A root route `/` was created, that simply displays a cover page with a button to begin the initial scraping (index.html).

* A route called `/scrape` was created, that imports the `scrape_mars.py` script and calls the `.scrape()` function. This returns a Python dictionary that is stored in Mongo. Splinter's browser has been given a `headless` value of **True** so that scraping runs in the background (takes ~40 seconds). 

* After scraping is complete, the `/scrape` route redirects to the `/data` route for display.

* The `/data` route queries the Mongo database and passes the Mars data into an HTML template for display (data.html).

## Screenshots

### Landing page ('/')

Bootstrap was used to create landing page with button to scrape data calling the '/scrape' route.

### Data display ('/data')

The `/scrape` route redirects to a `/data` route that renders a second html template.
