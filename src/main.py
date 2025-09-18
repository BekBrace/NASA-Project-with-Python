import webbrowser, requests

import time, json, datetime

import turtle


def get_astros_data(api_url: str = "http://api.open-notify.org/astros.json"):
    data = requests.get(api_url).json()

    if data['message'] == 'success':
        with open('iss-astros.json', 'w') as iss_file:
            json.dump(data, iss_file, indent=4)
            # Optional to open the file in browser .
            # webbrowser.open('iss-astros.json')

        print(f"There are currently {data['number']} people on the iss .")
        for person in data['people']:
            print(
                f"{person['name']} is currently on the iss, Craft: {person['craft']}"
            )

    else:
        print('Failed to obtain astronauts data .')


def get_iss_turtle(resoloution: tuple = (1280, 720)):
    # Setup the world map in turtle module
    screen = turtle.Screen()
    screen.setup(*resoloution)
    screen.setworldcoordinates(-180, -90, 180, 90)

    # load the world map image
    screen.bgpic("images/world-map.gif")
    screen.register_shape("images/iss-icon.gif")
    iss = turtle.Turtle()
    iss.shape("images/iss-icon.gif")
    iss.setheading(45)
    iss.penup()

    return iss


def update_possition(iss: turtle.Turtle,
                     api_url: str = "http://api.open-notify.org/iss-now.json",
                     sleep_duration: int = 5):

    while True:
        # load the current status of the ISS in real-time
        try:
            data = requests.get(api_url).json()
        except Exception as e:
            print(e)
            update_possition(iss, api_url, sleep_duration)

        if data['message'] == 'success':
            # Extract the ISS location
            location = data["iss_position"]
            latitude = float(location['latitude'])
            longitude = float(location['longitude'])

            print(
                f"\nCurrent coordinates Latitude: {latitude}, Longitude: {longitude}"
            )

            print(
                f"Current time: {datetime.datetime.fromtimestamp(data['timestamp'])}"
            )

            # Update the ISS turtle object location on the map
            iss.goto(longitude, latitude)
            iss.pendown()

            # Refresh each sleep duration seconds
            time.sleep(sleep_duration)

        else:
            print("Failed to obtain iss position data .")


def main():
    get_astros_data()
    iss_turtle = get_iss_turtle()
    update_possition(iss_turtle)


if __name__ == "__main__":
    main()
