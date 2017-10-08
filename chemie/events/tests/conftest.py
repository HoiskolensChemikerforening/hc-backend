from customprofile.factories import RandomUserFactory


def logged_in_client(client):
    new_user = RandomUserFactory.create()
    new_user.email = 'adam@test.ntnu.no'
    new_user.set_password('defaultpassword')
    client = client.login(username=new_user.username, password='defaultpassword')
    return new_user, client

def generic_user(email):
    pass