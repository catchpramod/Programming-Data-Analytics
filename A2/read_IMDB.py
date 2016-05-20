__author__ = 'Pramod Bhandari'

import urllib2
from bs4 import BeautifulSoup
import json
import util_imdb as util

m_per_page = 50  # by default, imdb return 50 movies page url. You need to use this variable as a global variable in you code. I shouldn't see 50 in your code below


def read_m_by_rating(first_year, last_year, top_number):
    # This method takes two years and a number (top_number) as inputs. If we have first year = 2005, and
    # last_year =2014, and top_number = 256, we want to retrieve top 256 movies that were released between 2004 and 2015
    # You need to do two things
    # 1. Construct a url. An example url can be http://www.imdb.com/search/title?at=0&sort=user_rating&start=1&title_type=feature&year=2005,2014
    # This URL means that the web page will display movies based on user_rating between year 2005 and 2014 (i.e.,"year = 2005,2014" - you need
    #    to replace the years with first_year and last_year in your code).It will start from the first movie (i.e., start = 1 - you need to use
    #    start_index in the url in your code).
    #    The issue here is is that IMDB will display just 50 movies based on this URL. So in order to review more movies, you need to click "next"
    #    on the web page.By clicking the next button,
    #    you will see a new url http://www.imdb.com/search/title?at=0&sort=user_rating&start=51&title_type=feature&year=2005,2014
    #    If you compare the two urls above, you can easily see that in the second url, start=51, i.e., IMDB provides another 50 movies,
    #    starting from movie No 51.If you want to retrieve the top 61 movies, you need to open two web pages with two urls.
    #    And if you want to retrieve top 256 movies, you need to open 6 different URLs
    #    Obviously, you want to use a loop to construct the different URLs.
    # 2. Read movies from the URL: You will implement a method called "read_m_from_url". What this method does is that it opens a url and
    #    read numbers_of_movies_you_need_to_read_on_the_page. For example, if you want to read top 61 movies, you will need to first open
    #    a url http://www.imdb.com/search/title?at=0&sort=user_rating&start=1&title_type=feature&year=2005,2014, you need to read
    #    all 50 movies on the page by calling read_m_from_url(url), and then you need to open the second url
    #    http://www.imdb.com/search/title?at=0&sort=user_rating&start=1&title_type=feature&year=2005,2014, but you just need
    #    to read 61-50=11 movies from the page. Now, let's set current_index = 51 and top_number = 61, you actually need to retrieve
    #    (top_number - current_index + 1) movies. You can do this by calling read_m_from_url(url, top_number - the current_index)
    #    Hence, you need to use if statement here. Based on top_number, you may need to open multiple urls (e.g., if top 256, you need to open 6 urls)
    #
    # To summarize, I have the following pseudo code:

    # current_index = 1 # initialize current_index. In the first iteration, you need to have start = 1.
    final_list = []  # initialize the return value. This method returns a list. Each item in the list is a dictionary. Each dictionary includes information regarding a movie
    ''' TODO your code here.... based on the pseudo code below.
    loop: # as long as you need to read more url
        url = a_url # in each loop, you construct a url, you need to change the "start" value in the url by setting start=current_index
        if I am on the last url:
             lis = read_m_from_url(url, top_number - current_index + 1) # you need to track the current_index, which is the index you will use in the url, i.e.,in the url start=current_index
        else: # if not the last url
             lis = read_m_from_url(url, m_per_page) # you read all 50 movies.
        add lis to final_list   # This read_m_from_url function will return a list of movies, you need to this list to final_list
        update current_index # after reading a number of movies, you need to update current_index.
    '''

    for current_index in range(0, top_number, m_per_page):
        url = "http://www.imdb.com/search/title?at=0&sort=user_rating&start=" + str(current_index+1) + "&title_type=feature&year=" + str(first_year) + "," + str(last_year)
        if top_number - current_index <= 50:
            lis = read_m_from_url(url, top_number - current_index)
        else:
            lis = read_m_from_url(url)
        final_list.extend(lis)

    return final_list


def test_read_m_by_rating():
    """output:
    [{'rating': '10.0', 'genres': ['Comedy', 'Family'], 'title': 'How to Beat a Bully', 'rank': '1', 'year': '2014', 'runtime': '90'}, {'rating': '9.4', 'genres': ['Animation'], 'title': 'Chaar Sahibzaade', 'rank': '2', 'year': '2014', 'runtime': '128'}, {'rating': '8.9', 'genres': ['Action', 'Fantasy', 'Sci-Fi'], 'title': 'Voice of the Vespers', 'rank': '3', 'year': '2014', 'runtime': '98'}, {'rating': '9.2', 'genres': ['Action', 'Biography', 'Drama', 'History'], 'title': 'Queen of the Mountains', 'rank': '4', 'year': '2014', 'runtime': '135'}, {'rating': '9.1', 'genres': ['Comedy'], 'title': 'The Phantom Menace Review', 'rank': '5', 'year': '2009', 'runtime': '69'}, {'rating': '9.1', 'genres': ['Action'], 'title': 'SynCop', 'rank': '6', 'year': '2010', 'runtime': ''}, {'rating': '9.0', 'genres': ['Action', 'Crime', 'Thriller'], 'title': 'Baby', 'rank': '7', 'year': '2015', 'runtime': '160'}, {'rating': '9.0', 'genres': ['Action', 'Crime', 'Drama'], 'title': 'The Dark Knight', 'rank': '8', 'year': '2008', 'runtime': '152'}, {'rating': '8.1', 'genres': ['Drama'], 'title': 'Take Me to the River', 'rank': '9', 'year': '2015', 'runtime': '90'}, {'rating': '9.0', 'genres': ['Action', 'Comedy', 'Crime', 'Musical'], 'title': 'Jewel Fools', 'rank': '10', 'year': '2014', 'runtime': '100'}, {'rating': '9.0', 'genres': ['Comedy', 'Drama', 'Family', 'Music'], 'title': 'The Beat Beneath My Feet', 'rank': '11', 'year': '2014', 'runtime': '89'}, {'rating': '9.0', 'genres': ['Drama'], 'title': 'Potential Inertia', 'rank': '12', 'year': '2014', 'runtime': ''}, {'rating': '8.9', 'genres': ['Drama'], 'title': 'East Side Sushi', 'rank': '13', 'year': '2014', 'runtime': '100'}, {'rating': '8.9', 'genres': ['Drama', 'Family', 'Thriller'], 'title': 'Drishyam', 'rank': '14', 'year': '2013', 'runtime': '160'}, {'rating': '8.9', 'genres': ['Drama'], 'title': 'The Crucible', 'rank': '15', 'year': '2014', 'runtime': '190'}, {'rating': '8.9', 'genres': ['Animation', 'Adventure', 'Family'], 'title': 'Shaun the Sheep Movie', 'rank': '16', 'year': '2015', 'runtime': '85'}, {'rating': '8.9', 'genres': ['Action', 'Mystery', 'Thriller'], 'title': '1', 'rank': '17', 'year': '2014', 'runtime': '170'}, {'rating': '8.9', 'genres': ['Drama', 'History', 'Mystery', 'Thriller'], 'title': 'The Zohar Secret', 'rank': '18', 'year': '2015', 'runtime': '124'}, {'rating': '8.9', 'genres': ['Music'], 'title': 'Basedworld', 'rank': '19', 'year': '2014', 'runtime': '95'}, {'rating': '8.9', 'genres': ['Crime', 'Drama', 'Thriller'], 'title': "The Tailor's Apprentice", 'rank': '20', 'year': '2014', 'runtime': '84'}, {'rating': '8.9', 'genres': ['Drama', 'Music', 'Musical', 'Romance', 'Thriller'], 'title': 'The Phantom of the Opera at the Royal Albert Hall', 'rank': '21', 'year': '2011', 'runtime': '137'}, {'rating': '8.8', 'genres': ['Comedy'], 'title': 'Attack of the Clones Review', 'rank': '22', 'year': '2010', 'runtime': '86'}, {'rating': '8.8', 'genres': ['Adventure', 'Sci-Fi'], 'title': 'Interstellar', 'rank': '23', 'year': '2014', 'runtime': '169'}, {'rating': '8.8', 'genres': ['Comedy'], 'title': 'Home Sweet Home (Konkani)', 'rank': '24', 'year': '2014', 'runtime': ''}, {'rating': '8.8', 'genres': ['Drama', 'Fantasy'], 'title': 'Flea', 'rank': '25', 'year': '2014', 'runtime': ''}, {'rating': '8.5', 'genres': [], 'title': 'Shuruaat Ka Interval', 'rank': '26', 'year': '2014', 'runtime': '99'}, {'rating': '8.8', 'genres': ['Comedy', 'Drama', 'Family'], 'title': 'Bey Yaar', 'rank': '27', 'year': '2014', 'runtime': '150'}, {'rating': '8.8', 'genres': ['Action', 'Mystery', 'Sci-Fi', 'Thriller'], 'title': 'Inception', 'rank': '28', 'year': '2010', 'runtime': '148'}, {'rating': '9.0', 'genres': ['Drama'], 'title': 'Me & Earl & the Dying Girl', 'rank': '29', 'year': '2015', 'runtime': '104'}, {'rating': '8.8', 'genres': ['Drama', 'Music'], 'title': 'First Time Loser', 'rank': '30', 'year': '2012', 'runtime': '90'}, {'rating': '8.8', 'genres': ['Drama'], 'title': 'Wheels', 'rank': '31', 'year': '2014', 'runtime': '115'}, {'rating': '8.8', 'genres': ['Comedy', 'Musical'], 'title': 'A Very Potter Musical', 'rank': '32', 'year': '2009', 'runtime': '166'}, {'rating': '8.8', 'genres': ['Comedy'], 'title': 'Flock of Dudes', 'rank': '33', 'year': '2014', 'runtime': '90'}, {'rating': '8.8', 'genres': ['Comedy'], 'title': 'Lars the Emo Kid', 'rank': '34', 'year': '2014', 'runtime': ''}, {'rating': '8.8', 'genres': ['Drama'], 'title': 'Pretty Rosebud', 'rank': '35', 'year': '2014', 'runtime': ''}, {'rating': '8.8', 'genres': ['History'], 'title': 'Maharaja Gemunu', 'rank': '36', 'year': '2015', 'runtime': ''}, {'rating': '8.8', 'genres': ['Drama'], 'title': 'The Dark Horse', 'rank': '37', 'year': '2014', 'runtime': '124'}, {'rating': '8.8', 'genres': ['Action', 'Drama', 'Thriller'], 'title': 'Waar', 'rank': '38', 'year': '2013', 'runtime': '130'}, {'rating': '8.8', 'genres': ['Animation', 'Action', 'Fantasy'], 'title': 'Attack on Titan Crimson Bow and Arrow', 'rank': '39', 'year': '2014', 'runtime': '119'}, {'rating': '8.8', 'genres': [], 'title': 'Nigger', 'rank': '40', 'year': '2009', 'runtime': '47'}, {'rating': '8.8', 'genres': ['Comedy', 'Thriller'], 'title': 'Na Maloom Afraad', 'rank': '41', 'year': '2014', 'runtime': ''}, {'rating': '8.5', 'genres': ['Drama'], 'title': 'Min lilla syster', 'rank': '42', 'year': '2015', 'runtime': '105'}, {'rating': '8.7', 'genres': ['Adventure', 'Drama', 'History'], 'title': "Jack London's Love of Life", 'rank': '43', 'year': '2012', 'runtime': '109'}, {'rating': '8.7', 'genres': ['Musical'], 'title': 'Les Misrables in Concert: The 25th Anniversary', 'rank': '44', 'year': '2010', 'runtime': '178'}, {'rating': '8.7', 'genres': ['Comedy'], 'title': 'Half Time and Down', 'rank': '45', 'year': '2014', 'runtime': '47'}, {'rating': '8.7', 'genres': ['Comedy'], 'title': '30 Days in Atlanta', 'rank': '46', 'year': '2014', 'runtime': ''}, {'rating': '8.7', 'genres': ['Family', 'Romance'], 'title': 'Camilla Dickinson', 'rank': '47', 'year': '2012', 'runtime': '117'}, {'rating': '8.7', 'genres': [], 'title': 'The Best Red vs. Blue. Ever. Of All Time', 'rank': '48', 'year': '2012', 'runtime': '150'}, {'rating': '8.7', 'genres': ['Thriller'], 'title': 'Dissonance', 'rank': '49', 'year': '2008', 'runtime': '80'}, {'rating': '8.7', 'genres': ['Drama'], 'title': 'Ajana Batas', 'rank': '50', 'year': '2013', 'runtime': '102'}, {'rating': '8.7', 'genres': ['Drama'], 'title': 'Qandil Mountains', 'rank': '51', 'year': '2010', 'runtime': '94'}, {'rating': '8.7', 'genres': ['Biography', 'Drama', 'History'], 'title': 'Dr. Prakash Baba Amte: The Real Hero', 'rank': '52', 'year': '2014', 'runtime': '119'}, {'rating': '8.7', 'genres': ['Drama'], 'title': 'Hero of the Day', 'rank': '53', 'year': '2012', 'runtime': '95'}, {'rating': '8.7', 'genres': ['Comedy', 'Drama'], 'title': 'The Racket Boys', 'rank': '54', 'year': '2011', 'runtime': '85'}, {'rating': '8.7', 'genres': ['Drama', 'War'], 'title': 'Brtan', 'rank': '55', 'year': '2006', 'runtime': '162'}, {'rating': '8.9', 'genres': ['Comedy', 'Drama', 'Romance'], 'title': 'Brooklyn', 'rank': '56', 'year': '2015', 'runtime': '105'}, {'rating': '8.7', 'genres': ['History'], 'title': 'How to Act and Eat at the Same Time', 'rank': '57', 'year': '2012', 'runtime': '51'}, {'rating': '8.7', 'genres': ['Drama'], 'title': 'Mount Joy', 'rank': '58', 'year': '2014', 'runtime': '86'}, {'rating': '8.7', 'genres': ['Comedy', 'Fantasy'], 'title': 'Tut Szn', 'rank': '59', 'year': '2015', 'runtime': ''}, {'rating': '8.7', 'genres': ['Drama', 'Music'], 'title': 'Whiplash', 'rank': '60', 'year': '2014', 'runtime': '107'}, {'rating': '8.7', 'genres': ['Drama', 'Family'], 'title': 'Simply gay le film', 'rank': '61', 'year': '2014', 'runtime': '71'}]
    """

    expected = [{'rating': '10.0', 'genres': ['Comedy', 'Family'], 'title': 'How to Beat a Bully', 'rank': '1', 'year': '2014', 'runtime': '90'}, {'rating': '9.4', 'genres': ['Animation'], 'title': 'Chaar Sahibzaade', 'rank': '2', 'year': '2014', 'runtime': '128'}, {'rating': '8.9', 'genres': ['Action', 'Fantasy', 'Sci-Fi'], 'title': 'Voice of the Vespers', 'rank': '3', 'year': '2014', 'runtime': '98'}, {'rating': '9.2', 'genres': ['Action', 'Biography', 'Drama', 'History'], 'title': 'Queen of the Mountains', 'rank': '4', 'year': '2014', 'runtime': '135'}, {'rating': '9.1', 'genres': ['Comedy'], 'title': 'The Phantom Menace Review', 'rank': '5', 'year': '2009', 'runtime': '69'}, {'rating': '9.1', 'genres': ['Action'], 'title': 'SynCop', 'rank': '6', 'year': '2010', 'runtime': ''}, {'rating': '9.0', 'genres': ['Action', 'Crime', 'Thriller'], 'title': 'Baby', 'rank': '7', 'year': '2015', 'runtime': '160'}, {'rating': '9.0', 'genres': ['Action', 'Crime', 'Drama'], 'title': 'The Dark Knight', 'rank': '8', 'year': '2008', 'runtime': '152'}, {'rating': '8.1', 'genres': ['Drama'], 'title': 'Take Me to the River', 'rank': '9', 'year': '2015', 'runtime': '90'}, {'rating': '9.0', 'genres': ['Action', 'Comedy', 'Crime', 'Musical'], 'title': 'Jewel Fools', 'rank': '10', 'year': '2014', 'runtime': '100'}, {'rating': '9.0', 'genres': ['Comedy', 'Drama', 'Family', 'Music'], 'title': 'The Beat Beneath My Feet', 'rank': '11', 'year': '2014', 'runtime': '89'}, {'rating': '9.0', 'genres': ['Drama'], 'title': 'Potential Inertia', 'rank': '12', 'year': '2014', 'runtime': ''}, {'rating': '8.9', 'genres': ['Drama'], 'title': 'East Side Sushi', 'rank': '13', 'year': '2014', 'runtime': '100'}, {'rating': '8.9', 'genres': ['Drama', 'Family', 'Thriller'], 'title': 'Drishyam', 'rank': '14', 'year': '2013', 'runtime': '160'}, {'rating': '8.9', 'genres': ['Drama'], 'title': 'The Crucible', 'rank': '15', 'year': '2014', 'runtime': '190'}, {'rating': '8.9', 'genres': ['Animation', 'Adventure', 'Family'], 'title': 'Shaun the Sheep Movie', 'rank': '16', 'year': '2015', 'runtime': '85'}, {'rating': '8.9', 'genres': ['Action', 'Mystery', 'Thriller'], 'title': '1', 'rank': '17', 'year': '2014', 'runtime': '170'}, {'rating': '8.9', 'genres': ['Drama', 'History', 'Mystery', 'Thriller'], 'title': 'The Zohar Secret', 'rank': '18', 'year': '2015', 'runtime': '124'}, {'rating': '8.9', 'genres': ['Music'], 'title': 'Basedworld', 'rank': '19', 'year': '2014', 'runtime': '95'}, {'rating': '8.9', 'genres': ['Crime', 'Drama', 'Thriller'], 'title': "The Tailor's Apprentice", 'rank': '20', 'year': '2014', 'runtime': '84'}, {'rating': '8.9', 'genres': ['Drama', 'Music', 'Musical', 'Romance', 'Thriller'], 'title': 'The Phantom of the Opera at the Royal Albert Hall', 'rank': '21', 'year': '2011', 'runtime': '137'}, {'rating': '8.8', 'genres': ['Comedy'], 'title': 'Attack of the Clones Review', 'rank': '22', 'year': '2010', 'runtime': '86'}, {'rating': '8.8', 'genres': ['Adventure', 'Sci-Fi'], 'title': 'Interstellar', 'rank': '23', 'year': '2014', 'runtime': '169'}, {'rating': '8.8', 'genres': ['Comedy'], 'title': 'Home Sweet Home (Konkani)', 'rank': '24', 'year': '2014', 'runtime': ''}, {'rating': '8.8', 'genres': ['Drama', 'Fantasy'], 'title': 'Flea', 'rank': '25', 'year': '2014', 'runtime': ''}, {'rating': '8.5', 'genres': [], 'title': 'Shuruaat Ka Interval', 'rank': '26', 'year': '2014', 'runtime': '99'}, {'rating': '8.8', 'genres': ['Comedy', 'Drama', 'Family'], 'title': 'Bey Yaar', 'rank': '27', 'year': '2014', 'runtime': '150'}, {'rating': '8.8', 'genres': ['Action', 'Mystery', 'Sci-Fi', 'Thriller'], 'title': 'Inception', 'rank': '28', 'year': '2010', 'runtime': '148'}, {'rating': '9.0', 'genres': ['Drama'], 'title': 'Me & Earl & the Dying Girl', 'rank': '29', 'year': '2015', 'runtime': '104'}, {'rating': '8.8', 'genres': ['Drama', 'Music'], 'title': 'First Time Loser', 'rank': '30', 'year': '2012', 'runtime': '90'}, {'rating': '8.8', 'genres': ['Drama'], 'title': 'Wheels', 'rank': '31', 'year': '2014', 'runtime': '115'}, {'rating': '8.8', 'genres': ['Comedy', 'Musical'], 'title': 'A Very Potter Musical', 'rank': '32', 'year': '2009', 'runtime': '166'}, {'rating': '8.8', 'genres': ['Comedy'], 'title': 'Flock of Dudes', 'rank': '33', 'year': '2014', 'runtime': '90'}, {'rating': '8.8', 'genres': ['Comedy'], 'title': 'Lars the Emo Kid', 'rank': '34', 'year': '2014', 'runtime': ''}, {'rating': '8.8', 'genres': ['Drama'], 'title': 'Pretty Rosebud', 'rank': '35', 'year': '2014', 'runtime': ''}, {'rating': '8.8', 'genres': ['History'], 'title': 'Maharaja Gemunu', 'rank': '36', 'year': '2015', 'runtime': ''}, {'rating': '8.8', 'genres': ['Drama'], 'title': 'The Dark Horse', 'rank': '37', 'year': '2014', 'runtime': '124'}, {'rating': '8.8', 'genres': ['Action', 'Drama', 'Thriller'], 'title': 'Waar', 'rank': '38', 'year': '2013', 'runtime': '130'}, {'rating': '8.8', 'genres': ['Animation', 'Action', 'Fantasy'], 'title': 'Attack on Titan Crimson Bow and Arrow', 'rank': '39', 'year': '2014', 'runtime': '119'}, {'rating': '8.8', 'genres': [], 'title': 'Nigger', 'rank': '40', 'year': '2009', 'runtime': '47'}, {'rating': '8.8', 'genres': ['Comedy', 'Thriller'], 'title': 'Na Maloom Afraad', 'rank': '41', 'year': '2014', 'runtime': ''}, {'rating': '8.5', 'genres': ['Drama'], 'title': 'Min lilla syster', 'rank': '42', 'year': '2015', 'runtime': '105'}, {'rating': '8.7', 'genres': ['Adventure', 'Drama', 'History'], 'title': "Jack London's Love of Life", 'rank': '43', 'year': '2012', 'runtime': '109'}, {'rating': '8.7', 'genres': ['Musical'], 'title': 'Les Misrables in Concert: The 25th Anniversary', 'rank': '44', 'year': '2010', 'runtime': '178'}, {'rating': '8.7', 'genres': ['Comedy'], 'title': 'Half Time and Down', 'rank': '45', 'year': '2014', 'runtime': '47'}, {'rating': '8.7', 'genres': ['Comedy'], 'title': '30 Days in Atlanta', 'rank': '46', 'year': '2014', 'runtime': ''}, {'rating': '8.7', 'genres': ['Family', 'Romance'], 'title': 'Camilla Dickinson', 'rank': '47', 'year': '2012', 'runtime': '117'}, {'rating': '8.7', 'genres': [], 'title': 'The Best Red vs. Blue. Ever. Of All Time', 'rank': '48', 'year': '2012', 'runtime': '150'}, {'rating': '8.7', 'genres': ['Thriller'], 'title': 'Dissonance', 'rank': '49', 'year': '2008', 'runtime': '80'}, {'rating': '8.7', 'genres': ['Drama'], 'title': 'Ajana Batas', 'rank': '50', 'year': '2013', 'runtime': '102'}, {'rating': '8.7', 'genres': ['Drama'], 'title': 'Qandil Mountains', 'rank': '51', 'year': '2010', 'runtime': '94'}, {'rating': '8.7', 'genres': ['Biography', 'Drama', 'History'], 'title': 'Dr. Prakash Baba Amte: The Real Hero', 'rank': '52', 'year': '2014', 'runtime': '119'}, {'rating': '8.7', 'genres': ['Drama'], 'title': 'Hero of the Day', 'rank': '53', 'year': '2012', 'runtime': '95'}, {'rating': '8.7', 'genres': ['Comedy', 'Drama'], 'title': 'The Racket Boys', 'rank': '54', 'year': '2011', 'runtime': '85'}, {'rating': '8.7', 'genres': ['Drama', 'War'], 'title': 'Brtan', 'rank': '55', 'year': '2006', 'runtime': '162'}, {'rating': '8.9', 'genres': ['Comedy', 'Drama', 'Romance'], 'title': 'Brooklyn', 'rank': '56', 'year': '2015', 'runtime': '105'}, {'rating': '8.7', 'genres': ['History'], 'title': 'How to Act and Eat at the Same Time', 'rank': '57', 'year': '2012', 'runtime': '51'}, {'rating': '8.7', 'genres': ['Drama'], 'title': 'Mount Joy', 'rank': '58', 'year': '2014', 'runtime': '86'}, {'rating': '8.7', 'genres': ['Comedy', 'Fantasy'], 'title': 'Tut Szn', 'rank': '59', 'year': '2015', 'runtime': ''}, {'rating': '8.7', 'genres': ['Drama', 'Music'], 'title': 'Whiplash', 'rank': '60', 'year': '2014', 'runtime': '107'}, {'rating': '8.7', 'genres': ['Drama', 'Family'], 'title': 'Simply gay le film', 'rank': '61', 'year': '2014', 'runtime': '71'}]

    print "Expected:"


    expected= sorted(expected, key=lambda k: k['rank'].rjust(3,'0'))
    print expected
    for rec in expected:
        print rec['rank']
    url = "http://www.imdb.com/search/title?at=0&sort=user_rating&start=51&title_type=feature&year=2005,2014"
    output = read_m_by_rating(2005, 2015, 61)
    output = sorted(output, key=lambda k: k['rank'].rjust(3,'0'))
    print "Output:"
    print output
    for rec in output:
        print rec['title']


def read_m_from_url(url, num_of_m=50):
    # print url
    # this function, read a number of movies from a url. That's say you set num_of_m=25, you want to read 25 movies from the page. The default value is 50
    html_string = util.read_html(url)  # given a url you need to read the hmtl file as a string. I have implemented this read_html function in util_imdb.py. Please take a look
    # create a soup object
    soup = BeautifulSoup(html_string)
    # Fetching a table that includes all the movies. In our lecture, we talked about find and find_all functions.
    # for example, find_all('table') will give you all tables on the page. Actually, this find or find_all function can have two parameters,
    # in the code below 'table' is the tag name and 'results' is an attribute value of the tag. You can also do
    # movie_table = soup.find('table', {'class':'result'}). Here you explicitly say: I want to find a table with attribute class = 'result'.
    # Since on each imdb page, there's only one table with class = 'results', we can use find rather than find_all. Find_all will return a list of table tags, while
    # find() will return only one table
    movie_table = soup.find('table', 'results')  # equivalent to  movie_table = soup.find('table', {'class':'result'})
    list_movies = []  # initialize the return value, a list of movies
    # Using count track the number of movies processed. now it's 0 - No movie has been processed yet.
    count = 0

    '''
    Add TODO your code here...., based on the following pseudo code.

    for each table row: # each row represents information of a movie
      dict_each_movie = {} # create an empty dictionary

      fetch title first.
      title = title.encode("ascii", "ignore") # convert the unicode string into an ascii string
      util.process_str_with_comma(title) # this method is in util_imdb.py and needs to be implemented by you.
                                         # Sometimes, a title can include a comma (e.g. "Oh, My God!"). This will cause a problem
                                         # if your code outputs the title to a csv file. To deal with this problem,
                                         # we use quotation marks to enclose the title. When you load the csv using the python package pandas
                                         # (or SAS or many other packages for processing csv), when pandas sees a string in csv enclosed in "",
                                         # it will recognized it as a cvs field with commas within it.
      dict_each_movie["title"] = title

      fetch year
      year = year.encode("ascii","ignore")
      dict_each_movie["year"] = year

      fetch rank # rank here means the number (such as 1.,2.) in front of the image of each image
      rank = rank.encode("ascii","ignore")
      remove the .
      dict_each_movie["year"] = rank

      # Fetching Genres
      genres = [] # a movie can have a list of or none genre values
      try: # you need to deal with exception, since a movie may not have a tag for genres. If there are genres:
            find_all genres
            add all the genres to the list "genres". Remember first encode('ascii', ignore) and then add to the list
      except:
            do nothing. genres is still [], an empty list
      finally: # whether an exception or not, you want to do the following
            dict_each_movie["genres"]=genres

      Fetch runtime: # again some movies do not have runtime value
      runtime = ""
      try:
           find runtime
           runtime = runtime.encode('ascii','ignore')
           a runtime string looks like "90 mins." you need to remove " mins."
      except:
           do nothing
      finally:
           dict_each_movie["runtime"] = runtime

      fetch rating
      rating = rating.runtime.encode('ascii','ignore')
      dict_each_movie["rating"] = rating

      list_movies.append(dict_each_movie)
      now we are done with processing a movie, increment count
      check if we have processed num_of_m movies (if count == num_of_m)? if so, break.
    '''
    for tr in movie_table.find_all('tr'):
        if tr.find_next().name != 'th':
            dict_each_movie ={}
            # get the movie rank
            rank_td =tr.find('td','number')
            rank = rank_td.text[:-1]
            rank = rank.encode("ascii", "ignore")
            dict_each_movie["rank"] = rank
            # get title td
            title_td =tr.find('td','title')
            # print(title_td)
            # get movie title
            title = title_td.find_next('a').string
            title = title.encode("ascii", "ignore")
            title = util.process_str_with_comma(title)
            dict_each_movie["title"] = title
            # get movie year
            year = title_td.find('span','year_type').string
            year = year[1:-1]
            year = year.encode("ascii","ignore")
            dict_each_movie["year"] = year
            # get genre
            genres = [] # a movie can have a list of or none genre values
            try:
                genre_span = title_td.find('span','genre')
                genres=[genre_link.string.encode("ascii","ignore") for genre_link in genre_span.find_all('a')]
            except:
                pass
            finally: # whether an exception or not, you want to do the following
                dict_each_movie["genres"]=genres


            # Fetch runtime: again some movies do not have runtime value
            runtime = ""
            try:
                runtime_span = title_td.find('span','runtime')
                runtime=runtime_span.string.encode("ascii","ignore")
                runtime = runtime.replace(' mins.','')
            except:
                # do nothing
                pass
            finally:
                dict_each_movie["runtime"] = runtime

            # fetch rating
            rating_rating_span = title_td.find('span','rating-rating')
            rating_span = rating_rating_span.find('span','value')
            rating = rating_span.string.encode('ascii','ignore')
            dict_each_movie["rating"] = rating

            list_movies.append(dict_each_movie)

            count = count+1
            if count==num_of_m:
                break

    return list_movies


def test_read_m_from_url():
    expected = [{'rating': '8.7', 'genres': ['Drama', 'Music'], 'title': 'Whiplash', 'rank': '51', 'year': '2014', 'runtime': '107'}, {'rating': '8.7', 'genres': ['Drama', 'Family'], 'title': 'Simply gay le film', 'rank': '52', 'year': '2014', 'runtime': '71'}, {'rating': '8.7', 'genres': ['Comedy', 'Drama', 'Romance'], 'title': 'Jane Wants a Boyfriend', 'rank': '53', 'year': '2014', 'runtime': '101'}, {'rating': '8.7', 'genres': ['Drama', 'Mystery'], 'title': 'The sinking of Sozopol', 'rank': '54', 'year': '2014', 'runtime': '101'}, {'rating': '8.7', 'genres': ['Drama'], 'title': 'Victims of Fun', 'rank': '55', 'year': '2014', 'runtime': '120'}, {'rating': '8.7', 'genres': ['Drama', 'History'], 'title': 'The Guide', 'rank': '56', 'year': '2014', 'runtime': '122'}, {'rating': '8.7', 'genres': ['Drama', 'War'], 'title': 'Tangerines', 'rank': '57', 'year': '2013', 'runtime': '87'}, {'rating': '8.6', 'genres': ['Drama'], 'title': 'Arrange to Settle', 'rank': '58', 'year': '2014', 'runtime': ''}, {'rating': '8.6', 'genres': ['Drama'], 'title': 'Touching Down', 'rank': '59', 'year': '2005', 'runtime': '115'}, {'rating': '8.6', 'genres': ['Drama'], 'title': 'Yume no mani mani', 'rank': '60', 'year': '2008', 'runtime': '106'}, {'rating': '8.6', 'genres': ['Action'], 'title': 'Trapped Abroad', 'rank': '61', 'year': '2014', 'runtime': '100'}, {'rating': '8.6', 'genres': ['Comedy', 'Drama', 'Fantasy', 'Mystery', 'Romance'], 'title': 'PK', 'rank': '62', 'year': '2014', 'runtime': '153'}, {'rating': '8.6', 'genres': ['Comedy', 'Drama', 'History', 'Music'], 'title': 'The Midnight Orchestra', 'rank': '63', 'year': '2014', 'runtime': '110'}, {'rating': '8.6', 'genres': ['Drama'], 'title': 'Talakjung vs Tulke', 'rank': '64', 'year': '2014', 'runtime': ''}, {'rating': '7.8', 'genres': ['Adventure', 'Drama', 'Mystery'], 'title': 'The Lost Salesman of Delhi', 'rank': '65', 'year': '2014', 'runtime': '97'}, {'rating': '8.6', 'genres': ['Drama'], 'title': 'Janeane from Des Moines', 'rank': '66', 'year': '2012', 'runtime': '78'}, {'rating': '8.6', 'genres': ['Crime', 'Drama', 'Musical', 'Thriller'], 'title': 'Jigarthanda', 'rank': '67', 'year': '2014', 'runtime': '171'}, {'rating': '8.6', 'genres': ['Crime', 'Drama', 'Romance', 'Thriller'], 'title': 'Haider', 'rank': '68', 'year': '2014', 'runtime': '160'}, {'rating': '8.6', 'genres': ['Drama'], 'title': 'Vacuum', 'rank': '69', 'year': '2012', 'runtime': ''}, {'rating': '8.7', 'genres': ['Action'], 'title': 'Gates of the Sun', 'rank': '70', 'year': '2014', 'runtime': '90'}, {'rating': '8.6', 'genres': ['Drama'], 'title': 'Shades of Gray', 'rank': '71', 'year': '2014', 'runtime': '108'}]
    print "Expected:"
    for r in expected:
        r['rank']=r['rank'].rjust(3,'0')
        print r['rank']
    expected= sorted(expected, key=lambda k: k['rank'])
    print expected
    url = "http://www.imdb.com/search/title?at=0&sort=user_rating&start=51&title_type=feature&year=2005,2014"
    output = read_m_from_url(url, 21)
    output = sorted(output, key=lambda k: k['rank'])
    print "Output:"
    print output


def write_movies_json(final_list, filename):
    # write the list of movies to a json file. The parameter final_list includes a number of movies, which is the output
    # of the function read_m_by_rating. The filename represents the output file name, the name of your json file
    f = None
    # TODO your code here....: open a file object f. Your filename must end with .json
    f = open(filename, "w")
    json.dump(final_list, f, indent=4,
              separators=(",", ": "))  # a json file can include a dictionary or a list of dictionary.
    # Here we call dump to write a list of diction to a json file.
    # The other parameters (indentation and separators ) are used to make your json file
    # look nicer
    f.close()
    return


def test_write_movies_json():  # output of the test is in "movies.json"
    li = read_m_by_rating(2005, 2014, 456)
    write_movies_json(li, "movies.json")  # movies.json is in the zip file.


def write_movies_csv(final_list, filename):
    # write the movies to a csv file; each row represents a movie. The parameter final_list includes a number of movies, which is the output of the function read_m_by_rating. The filename represents the output file name
    lis = []  # to write the file, we create a list of strings
    # below you want to create dummy variables for genre. The idea is that a movie can have different genre values. you want to
    # create dummy variables for all possible different genres.
    genre_variables = ""
    genre_list = []  # you want to put all possible genres in this list
    ''' TODO your code here.... based on my pseudo code below
    for each movie in final_list
        add a genre of the motive to the list, if the genre is not in the genre_list # there are a lot of different genres including Mystery,Romance,Sport,Sci-Fi,Family,Adventure,Horror,Crime,Drama,Fantasy,War,Animation,Music,Thriller,Action,Reality-TV,Western,Comedy,Musical,Biography,History
    # after the for loop, you should have a list that includes all possible genre values of all movies in the set
    convert the genre_list into a comma seperated string "genre_variable"  # you want to get a string like Mystery,Romance,Sport,Sci-Fi,Family,Adventure,Horror,Crime,Drama,Fantasy,War,Animation,Music,Thriller,Action,Reality-TV,Western,Comedy,Musical,Biography,History
    '''
    for movie in final_list:
        genre_list.extend(movie["genres"])

    genre_list = list(set(genre_list))
    genre_variables= ','.join(genre_list)


    header = "rank," + "title," + "year," + "rating," + "runtime," + genre_variables
    lis.append(header)  # add the header to the list
    for movie in final_list:
        # You need to implement the create_dummy_values function in util_imdb.py. What this function does is that it will take
        # the genres of a movie and represent the genres using 0s and 1s. Let's suppose the genre_list you just finish constructing includes
        # six different genres ['Mystery','Romance','Sport','Sci-Fi','Family','Adventure'], and a specific movie includes just 2 genre values, ["Romance","Family"],
        # then we need to create a list [0,1,0,0,1,0] to represent the genre of the movie. There are one-to-one mappings
        # between this list of 1s and 0s and the genre_list. 1 here means yes, and 0 no. So this list of 1s and 0s means that
        # this movies has 1s at index 1 and 4, and hence it has genre values including "Romance" and "Family"

        genre_string = ",".join(map(str, util.create_dummy_values(movie["genres"], list(
            genre_list))))  # we convert the list of 1s and 0s to a string ('0,1,0,0,1,0')
        # we need to use ",".join(). Since each item in the list is a number, we also use map - mapping the str function to each element in the list.
        string = movie["rank"] + "," + movie["title"] + "," + movie["year"] + "," + movie["rating"] + "," + movie[
            "runtime"] + "," + genre_string
        lis.append(string)  # add the string to the list
        '''
        TODO your code here: write lis (a list of strings) to a file. Please remember to close the file when you are done
        '''
        f = open(filename, "w")
        for line in lis:
            f.write(line+"\n")

        f.close()



def test_write_movies_csv():  # output of the test method is in "movies.csv"
    li = read_m_by_rating(2005, 2014, 456)
    write_movies_csv(li, "movies.csv")  # movies.csv is in the zip file


def main():
    # test_write_movies_json()
    test_write_movies_csv()
    # test_read_m_from_url()
    # test_read_m_by_rating()
    return


if __name__ == '__main__':
    main()