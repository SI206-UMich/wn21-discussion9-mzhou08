from bs4 import BeautifulSoup
import re
import requests
import unittest

# Task 1: Get the URL that links to the Pokemon Charmander's webpage.
# HINT: You will have to add https://pokemondb.net to the URL retrieved using BeautifulSoup
def getCharmanderLink(soup):
    url = 'https://pokemondb.net'
    tags = soup.find_all('a', class_ = 'ent-name')
    for tag in tags:
        if tag.text == 'Charmander':
            ext = tag['href']

    return url + ext

# Task 2: Get the details from the box below "Egg moves". Get all the move names and store
#         them into a list. The function should return that list of moves.
def getEggMoves(pokemon):
    url = 'https://pokemondb.net/pokedex/' + pokemon
    #add code here
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    head = soup.find('h3', text = 'Egg moves')
    table = head.findNext('table', class_ = 'data-table')
    cells = table.find_all('td', class_ = 'cell-name')
    moves = [cell.text for cell in cells]
    '''
    discarded code:
    tried to go onto egg moves page to get stuff, but found out about find_next_siblings

    links = soup.find_all('em')
    for link in links:
        if link.text.lower() == pokemon.lower():
            l = link.find('a')['href']'''
    return moves
# Task 3: Create a regex expression that will find all the times that have these formats: @2pm @5 pm @10am
# Return a list of these times without the '@' symbol. E.g. ['2pm', '5 pm', '10am']

def findLetters(sentences):
    # initialize an empty list
    words = []
    lasts = []

    # define the regular expression
    reg = '@((?:[1-9]|1[0-2])\s?(?:am|pm))'

    # loop through each sentence or phrase in sentences
    for sentence in sentences:

    # find all the words that match the regular expression in each sentence
        temp = re.findall(reg, sentence)

    # loop through the found words and add the words to your empty list
        words.extend(temp)

    #return the list of the last letter of all words that begin or end with a capital letter
    '''for word in words:
        if re.search('^[A-Z]', words) or re.search('[A-Z]$', words):
            lasts.append(word[-1])
    '''
    return words

def main():
    url = 'https://pokemondb.net/pokedex/national'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    getCharmanderLink(soup)
    #getEggMoves('scizor')

class TestAllMethods(unittest.TestCase):
    def setUp(self):
        self.soup = BeautifulSoup(requests.get('https://pokemondb.net/pokedex/national').text, 'html.parser')

    def test_link_Charmander(self):
        self.assertEqual(getCharmanderLink(self.soup), 'https://pokemondb.net/pokedex/charmander')

    def test_egg_moves(self):
        self.assertEqual(getEggMoves('scizor'), ['Counter', 'Defog', 'Feint', 'Night Slash', 'Quick Guard'])

    def test_findLetters(self):
        self.assertEqual(findLetters(['Come eat lunch at 12','there"s a party @2pm', 'practice @7am','nothing']), ['2pm', '7am'])
        self.assertEqual(findLetters(['There is show @12pm if you want to join','I will be there @ 2pm', 'come at @3 pm will be better']), ['12pm', '3 pm'])

if __name__ == "__main__":
    main()
    unittest.main(exit = False, verbosity = 2)