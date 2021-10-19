# Country Finder
#### Video Demo: https://www.youtube.com/watch?v=XqZBTHwA4v8
#### Description:
Country Finder is a web-based application which allow users to do searches related to countries. Basically, there are two ways of using the app: by doing a Simple Search,
where the name of a country of interest can be typed; or by doing an Advanced Search, where it is possible to define certain parameters to make a more customized search.

When opened, the app goes to the main page, where it is already possible to make a Simple Search. It consists of a page that has a simple search bar, where we can type
the name of a country that we are interested in. When the search button is pressed, we go to a new page that contains some general information about the country, like
its capital, the region in which it belongs, the population, its currencies, etc.

One of the coolest parts of this page is the area dedicated to the borders of the country. There, instead of just seeing, as expected, all countries that has borders with
the one we searched, we can also click in one of them. When we do that, we go to a new page that is similar to the one before, but it now has information about the
country we just selected. This way, we can navigate from one country to another, making the application more dynamic.

Another way of searching, as referenced before, is by doing an Advanced Search. In the page reserved for this type of query, we get to see many selection boxes, where we
can choose parameters to be obeyed. We can, for instance, search for all countries that have a determined language, or that uses a certain currency, or, even, that has
borders with a country of our choice. We can use as many parameters as we want, if any. When the search button is pressed, it is presented to us a list of countries that
follows our specifications. Clicking in one of them makes us go to that page that shows us some general information about a country.

The app was developed based on the framework Flask. Therefore, in the project’s directory are the application.py, which contains the Flask code, and the template
subdirectory, where all the HTML codes for each one of the pages are. The file countries.json, produced by REST Countries, encloses the dataset utilized for the
application. The plan was to build a relational database with SQlite using the data in the json file, so it was necessary to make a .db file. For that, there is the
datasetConfig.py file, which not only creates countries.db but also initiate and organize its tables.