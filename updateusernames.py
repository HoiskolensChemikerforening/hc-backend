from django.contrib.auth.models import User

class updateUsernames():
    def __init__(self):
        self.users = User.objects.all()
        b = self.findDouble()
        if b:
            print("Ready to convert True")
        else:
            print("not ready to convert")

    def findDouble(self):
        """
        checks for similar usernames
        :return: True if usernames can be converted
        """
        d = {}
        for u in self.users:
            if u.username.lower() in d.keys():
                d[u.username.lower()] += 1
            else:
                d[u.username.lower()] = 1
        dm = {}
        for key, value in d.items():
            if value > 1:
                dm[key] = value
        if dm == {}:
            return True
        print("ERROR: samme brukernavn")
        print(dm)
        return False

    def lowercase(self):
        """
        Converts all usernames to lowercase
        Only runs if findDouble returns True
        :return:
        """
        if self.findDouble():
            for user in self.users:
                user.username = user.username.lower()
                user.save()
        else:
            print("cant run command. Double usernames")
        return "Success!"