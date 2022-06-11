from bs4 import BeautifulSoup

# Global Variables #
cf_url = "https://codeforces.com"


def get_page(session, url):
    request = session.get(url)
    plain = request.text
    page = BeautifulSoup(plain, "html.parser")
    return page


def get_lists_table(session, url):
    page = get_page(session, url)
    table_div = page.find('div', {'class': 'datatable'})
    table = table_div.find('table')
    table_rows = table.find_all('tr')
    return table_rows


def get_lists_urls(table):
    urls = {}
    for row in table:
        if row.find('a'):
            organization = row.find('a').text
            organization_list_url = cf_url + row.find('a')['href']
            urls[organization] = organization_list_url
    return urls


def get_active_countries_dict(organizations_dict):
    active_organizations_dict = {}
    for organization, users in organizations_dict.items():
        active_organizations_dict[organization] = 0
        for user in users:
            if user[0]:
                active_organizations_dict[organization] += 1
    return active_organizations_dict


def get_handles(organization_handles):
    handles = []
    for user in organization_handles[:1000]:
        handles.append(user[2])
    return handles
