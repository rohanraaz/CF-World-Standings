from login import get_csrf
from get_lists import get_page, get_lists_table, get_lists_urls, \
                      get_active_organizations_dict, get_handles

# Global Variables #
lists_url = "https://codeforces.com/lists"
new_list_url = "https://codeforces.com/lists/new"
edit_list_url = "https://codeforces.com/data/lists"


def create_lists(session, organizations_dict):
    table = get_lists_table(session, lists_url)
    lists_urls = get_lists_urls(table)
    active_organization_users = get_active_organizations_dict(organizations_dict)
    organizations_list = []
    for organization in organizations_dict:
        if organization not in lists_urls and active_organization_users[organization] >= 50:
            request = session.get(new_list_url)
            csrf = get_csrf(request)
            params = {'csrf_token': csrf,
                      'action': 'saveList',
                      'englishName': organization,
                      '_tta': 90}
            n = session.post(new_list_url, data=params)
            organizations_list.append(organization)
            print(f"\tList of {organization} created! {n}")
        else:
            print(f"\tList of {organization} skipped!")


def clear_diff_lists(session, organizations_dict):
    table = get_lists_table(session, lists_url)
    lists_urls = get_lists_urls(table)
    for organization in lists_urls:
        url = lists_urls[organization]
        request = session.get(url)
        csrf = get_csrf(request)
        table = get_lists_table(session, url)
        page = get_page(session, url)
        list_a = page.find('a', {'class': 'delete-user-list-link'})
        list_id = list_a["data-userlistid"]
        handles = set(get_handles(organizations_dict[organization]))
        count = 0
        for row in table:
            try:
                user_id = row.findAll('td')[-1]["data-userid"]
                user_handle = row.findAll('td')[1].find('a').getText()
                if user_handle in handles:
                    continue
                params = {'action': 'deleteMember',
                          'listId': list_id,
                          'userId': user_id,
                          'csrf_token': csrf}
                session.post(edit_list_url, data=params)
                count += 1
            except (KeyError, IndexError):
                pass
        print(f'\t{count} users of {organization} removed!')


def populate_list(session, handles, list_url):
    request = session.get(list_url)
    csrf = get_csrf(request)
    params = {'csrf_token': csrf,
              'action': 'addMembers',
              'handlesToAdd': handles}
    session.post(list_url, data=params)


def populate_lists(session, organizations_dict):
    table = get_lists_table(session, lists_url)
    lists_urls = get_lists_urls(table)
    for organization in lists_urls:
        if organization in organizations_dict:
            handles = get_handles(organizations_dict[organization])
            handles = " ".join(handles)
            populate_list(session, handles, lists_urls[organization])
            print(f"\tList of {organization} populated!")
