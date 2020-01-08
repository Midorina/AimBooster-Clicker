from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui
import keyboard
import time
import os

paused = True
debug_mode = False

# [x coord of left upper corner,
# y coord of left upper corner,
# x coord of right bottom corner,
# y coord of right bottom corner]
game_coords = [1641, 381, 2241, 801]

min_orange = np.array([100, 20, 100])
max_orange = np.array([250, 255, 255])

pyautogui.PAUSE = 0


def shoot(coords):
    pyautogui.moveTo(coords)
    pyautogui.click()


def clear_console():  # doesnt work for some reason
    os.system('cls' if os.name == 'nt' else 'clear')


def spread_coord(coord):
    arr_to_return = []
    for _x in range(-3, 4):
        for _y in range(-3, 4):
            arr_to_return.append((coord[0] + _x, coord[1] + _y))

    return arr_to_return

last_clicked_coords = []

if paused:
    print("Clicker is currently paused! Press 'p' to unpause or pause again, and press 'q' to leave!")

while True:
    if keyboard.is_pressed("q"):
        print("Exiting...")
        break

    elif keyboard.is_pressed("p"):
        if paused:
            print("Continuing...")
            time.sleep(1)
            paused = False

        else:
            paused = True
            print("Paused!")
            time.sleep(1)

    if not paused:
        start = time.time()
        actual_screen = np.array(ImageGrab.grab(bbox=game_coords))
        print(f"Taking actual screenshot took {time.time() - start}")
        filtered_screen = cv2.cvtColor(actual_screen, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(filtered_screen, min_orange, max_orange)

        filtered_screen = mask
        start = time.time()
        circles = cv2.HoughCircles(filtered_screen, cv2.HOUGH_GRADIENT, 1.2, 100, param1=44, param2=22, minRadius=0, maxRadius=0)
        print(f"Hough circles took {time.time() - start}")
        print("Circles found:", len(circles))

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            if len(circles) > 10:
                print("Too many circles. Breaking...")
                break

            current_clicked_coords = []
            for (x, y, r) in circles:
                if (x, y) not in last_clicked_coords:
                    start = time.time()
                    shoot((x + game_coords[0], y + game_coords[1]))
                    print(f"Clicking took {time.time() - start}")
                    current_clicked_coords += spread_coord((x, y))

                    if debug_mode:
                        cv2.circle(actual_screen, (x, y), r, (0, 255, 0), 4)
                        cv2.rectangle(actual_screen, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                        cv2.imshow("actual_screen", actual_screen)
                        cv2.imshow("filtered_screen", filtered_screen)
                        cv2.waitKey(1)

            last_clicked_coords = current_clicked_coords

