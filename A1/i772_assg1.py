__author__ = 'Pramod Bhandari' 

from util import count_list
# Task1
# This function includes a for loop that prints all elements of a list and their position in the list.
# The argument of the function is a list.
# The return value of the function should be a list of tuples. Each tuple includes an element and the index of the element.
def list_ele_idx(li):
    index = 0 # index
    lis = [] # initialze a list; you need to add a tuple that includes an element and its index to this list
    # your code here. You must use for loop to read items in li and add (item,index)tuples to the list lis
    for list_item in li:
        lis.append((list_item, index))
        index += 1
    return lis # return a list of tuples

# task 2: Write a program to reverse/inverse key:value like below.
def reverse_key_value(dict1):
    dict2 = {} # initialize an empty list.
    # your code here - use for k,v in dict1.items() to read the key values pair and then reverse them and add to dict2
    for key, value in dict1.items():
        dict2[value] = dict2.get(value, [])
        dict2[value].append(key)
    return dict2

# Task 3: Given a string s, return a string made of the first 2 and the last 2 chars of the original string,
# so 'student' yields 'stnt', 'an' yields 'anan' (since the first 2 and the last 2 chars are both 'an')
# However, if the string length# is less than 2, return instead the empty string.
# The following function takes a string s as its argument
def both_ends(s):
    result = ''
    # your code here
    if len(s) >= 2:
        first_two=s[0:2]
        last_two=s[(len(s)-2):len(s)]
        result = first_two+last_two

    return result

# Task 4: This function takes a string s as its input and output a dictionary.
# The keys of the dictionary include the characters in the string,
# and the value of a key (i.e., a character) represents the number of occurrences of the character in the string.
# print count_list(['a', 'a', 'a', ' ', ' ', 'b', 'b', 'c', 'b'])
# print 'oo yae ee yae'
def charcount(s):
    result = {}
    # your code here - converting a string to list of character is easy. You just call list(s). You then need to
    # call the count_list function in the util module.
    result = count_list(list(s))
    return result

# run the program using a main() function
def main():
    """ """
    print '---------------- task 1 test cases----------------'
    print '---------------- Expected output----------------'
    print '[(5, 0), (3, 1), (2, 2), (6, 3)]'
    print '---------------- Actual output----------------'
    print list_ele_idx([5, 3, 2, 6]) # output: [(5, 0), (3, 1), (2, 2), (6, 3)]

    """ """
    print '---------------- task 2 test cases----------------'
    print '---------------- Expected output----------------'
    print "{'A': ['Sarah', 'John'], 'C': ['Ken'], 'B': ['Karen']}"
    print '---------------- Actual output----------------'
    print reverse_key_value({"John": "A", "Sarah": "A", "Karen": "B", "Ken": "C"}) #output {'A': ['Sarah', 'John'], 'C': ['Ken'], 'B': ['Karen']}

    """ """
    print '---------------- task 3 test cases----------------'
    print "both_ends of '%s': '%s'" % ('student',both_ends('student')) # output: both_ends of 'student': 'stnt'
    print "both_ends of '%s': '%s'" % ('the',both_ends('the')) # output: both_ends of 'the': 'thhe'
    print "both_ends of '%s': '%s'" % ('an',both_ends('an')) # output: both_ends of 'an': 'anan'
    print "both_ends of '%s': '%s'" % ('a',both_ends('a')) # output: both_ends of 'a': ''

    """ """
    print '---------------- task 4 test cases----------------'
    print '---------------- Expected output----------------'
    print "{'a': 5, ' ': 9, 'c': 2, 'e': 9, 'd': 2, 'g': 1, 'i': 4, 'h': 3, 'm': 1, 's': 3, 'o': 3, 'n': 8, 'p': 4, 'S': 1, 'r': 5, 'u': 1, 't': 6, 'w': 1, 'y': 1, 'x': 2, 'l': 1}"
    print '---------------- Actual output----------------'
    print charcount("Smartphone industry has experienced an exponential growth in recent past")
    #output: {'a': 5, ' ': 9, 'c': 2, 'e': 9, 'd': 2, 'g': 1, 'i': 4, 'h': 3, 'm': 1, 's': 3, 'o': 3, 'n': 8, 'p': 4, 'S': 1, 'r': 5, 'u': 1, 't': 6, 'w': 1, 'y': 1, 'x': 2, 'l': 1}

# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    main()

