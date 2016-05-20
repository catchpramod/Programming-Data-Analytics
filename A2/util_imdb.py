__author__ = 'Pramod Bhandari'
import urllib2

def create_dummy_values(small_list, large_list):
    result = []
    '''
      you code here...

      you want to read items from the large list one by one. If an item is not in the small list, you append 0 to result list, 
      otherwise you append 1 to the result list
      
      An example and test code is below.
    '''
    for l_item in large_list:
        # a if test else b
        result.append(1 if l_item in small_list else 0)

    return result

def test_create_dummy_values():
    large_list = ['Mystery','Romance','Sport','Sci-Fi','Family','Adventure','Horror']
    small_list = ['Romance','Sport','Family']
    print create_dummy_values(small_list,large_list)# output:[0, 1, 1, 0, 1, 0, 0]


# read url and output the html file as a string
def read_html(url):
    test_url = urllib2.urlopen(url)
    readHtml = test_url.read()
    return readHtml

def test_read_html():
    print read_html('http://www.imdb.com/search/title?at=0&sort=user_rating&start=1&title_type=feature&year=2005,2015')

# if a string contains comma, use "" to enclose the string
def process_str_with_comma(string):
    # you code here....
    if "," in string: string='"'+string+'"'
    return string

def test_process_str_with_comma():
    """output:
    string: it is a string
    string: "it is a string, right"
    """
    string = 'it is a string'
    print "string: " + process_str_with_comma(string)
    string = 'it is a string, right'
    print "string: " + process_str_with_comma(string)

def main():
    test_create_dummy_values()
    #test_read_html()
    #test_process_str_with_comma()

    return

if __name__ == '__main__':
    main()