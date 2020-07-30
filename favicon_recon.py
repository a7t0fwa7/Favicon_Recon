import shodan
import mmh3
import codecs
import socket
from anonbro import *

user_input = input("Enter Domain To Search (etc: google.com, facebook.com): ")
url = 'https://www.' + user_input + '/favicon.ico'
domain = 'https://www.' + user_input
ip_add = socket.gethostbyname(user_input)

response = anon_browser(url)
favicon = codecs.encode(response.content, 'base64')
hash = mmh3.hash(favicon)
print('\nShodan search query: http.favicon.hash:' + str(hash) + '\n')

query_to_search = 'http.favicon.hash:' + str(hash)
SHODAN_API_KEY = input('Enter Shodan API key: ')
api = shodan.Shodan(SHODAN_API_KEY)

print('1. Host Info\n'
      '2. Shodan Search (detailed)\n'
      '3. Return List Of IPs that related  to the domain\n'
      '4. Show Query Summery')
user_choise = int(input("\nSelect what to do? "))


def paid_shodan(query_to_search):
    try:
        # Search Shodan
        results = api.search(query_to_search)

        # Show the results
        print('Results found: {}'.format(results['total']))
        for result in results['matches']:
            print('IP: {}'.format(result['ip_str']))
            print(result['data'])
    except shodan.APIError as e:
        print('Error: {}'.format(e))


def host_info(ip):
    try:
        host = api.host(ip)
        print("""
                IP: {}
                Organization: {}
                Operating System: {}
        """.format(host['ip_str'], host.get('org', 'n/a'), host.get('os', 'n/a')))

        # Print all banners
        for item in host['data']:
            print("""
                        Port: {}
                        Banner: {}

                """.format(item['port'], item['data']))
    except Exception as error:
        print('Error:{}'.format(error))


def list_of_ip(api_key, query_to_search):
    try:
        # Setup the api
        api = shodan.Shodan(api_key)

        # Perform the search
        result = api.search(query_to_search)

        # Loop through the matches and print each IP
        for service in result['matches']:
            print(service['ip_str'])
    except Exception as e:
        print('Error: %s' % e)


def query_summery(query_to_search):
    # The list of properties we want summary information on
    FACETS = [
        'org',
        'domain',
        'port',
        'asn',

        # We only care about the top 3 countries, this is how we let Shodan know to return 3 instead of the
        # default 5 for a facet. If you want to see more than 5, you could do ('country', 1000) for example
        # to see the top 1,000 countries for a search query.
        ('country', 10),
    ]

    FACET_TITLES = {
        'org': 'Top 5 Organizations',
        'domain': 'Top 5 Domains',
        'port': 'Top 5 Ports',
        'asn': 'Top 5 Autonomous Systems',
        'country': 'Top 10 Countries',
    }

    try:
        api = shodan.Shodan(SHODAN_API_KEY)
        result = api.count(query_to_search, facets=FACETS)
        print('\nShodan Summary Information')
        print('Query: %s' % query_to_search)
        print('Total Results: %s\n' % result['total'])

        for facet in result['facets']:
            print(FACET_TITLES[facet])

            for term in result['facets'][facet]:
                print('%s: %s' % (term['value'], term['count']))
            print('')

    except Exception as e:
        print('Error: %s' % e)


def main():
    if user_choise == 1:
        host_info(ip_add)
    elif user_choise == 2:
        paid_shodan(query_to_search)
    elif user_choise == 3:
        list_of_ip(SHODAN_API_KEY, query_to_search)
    elif user_choise == 4:
        query_summery(query_to_search)
    elif user_choise < 1 or user_choise > 4:
        print('invaild option')


if __name__ == '__main__':
    main()
