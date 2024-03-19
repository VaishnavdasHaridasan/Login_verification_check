def get_event_date(event):
    return event.date

def current_users(events):
    events.sort(key=get_event_date)
    machines = {}
    warnings = False  # Initialize warnings flag
    for event in events:
        if event.machine not in machines:
            machines[event.machine] = set()
        if event.type == "login":
            machines[event.machine].add(event.user)
        elif event.type == "logout":
            if event.user in machines[event.machine]:
                machines[event.machine].remove(event.user)
            else:
                print("Warning: User {} was not logged into machine {}.".format(event.user, event.machine))
                warnings = True  # Set warnings flag to True
    return machines, warnings  # Return warnings flag along with machines dictionary



def generate_report(machines):
    for machine, users in machines.items():
        if users:  # Check if users set is not empty
            user_list = ", ".join(users)
            print("{}: {}".format(machine, user_list))

class Event:
    def __init__(self, event_date, event_type, machine_name, user):
        self.date = event_date
        self.type = event_type
        self.machine = machine_name
        self.user = user


events = [
    Event('2020-01-21 12:45:56', 'login', 'myworkstation.local', 'jordan'),
    Event('2020-01-22 15:53:42', 'logout', 'webserver.local', 'jordan'),
    Event('2020-01-21 18:53:21', 'login', 'webserver.local', 'lane'),
    Event('2020-01-22 10:25:34', 'logout', 'myworkstation.local', 'jordan'),
    Event('2020-01-21 08:20:01', 'login', 'webserver.local', 'jordan'),
    Event('2020-01-23 11:24:35', 'logout', 'mailserver.local', 'chris'),
    Event('2020-01-21 18:55:21', 'logout', 'webserver.local', 'lane'),
    Event('2020-01-23 11:22:35', 'login', 'mailserver.local', 'chris'),
]

users, warnings = current_users(events)
generate_report(users)

# Check if there were any warning messages during user processing
if not warnings:
    print("Everything is ok")