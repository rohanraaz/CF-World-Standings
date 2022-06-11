from login import login
from get_users import get_all_active_users, separate_by_organization
from set_lists import create_lists, clear_diff_lists, populate_lists

if __name__ == "__main__":
    print("Please login first\n")
    session = login()
    print("Getting Users..")
    users = get_all_active_users()
    print("Creating Dictionary..")
    organizations_dict = separate_by_organization(users)
    print("Creating Lists..")
    create_lists(session, organizations_dict)
    print("Emptying Lists..")
    clear_diff_lists(session, organizations_dict)
    print("Populating Lists..")
    populate_lists(session, organizations_dict)
