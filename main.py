from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui
import keyboard
import time
import os

paused = True

game_coords = [1641, 381, 2241, 801]

min_orange = np.array([100, 20, 100])
max_orange = np.array([250, 255, 255])

pyautogui.PAUSE = 0


def shoot(coords):
    pyautogui.moveTo(coords)
    pyautogui.click()


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

if paused:
    print("Clicker is currently paused! Press 'p' to unpause or pause again, and press 'q' to leave!")

while True:
    clear_console()
    if keyboard.is_pressed("q"):
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
        try:
            start = time.time()
            actual_screen = np.array(ImageGrab.grab(bbox=game_coords))
            print(f"Taking actual screenshot took {time.time() - start}")
            filtered_screen = cv2.cvtColor(actual_screen, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(filtered_screen, min_orange, max_orange)

            filtered_screen = mask
            start = time.time()
            circles = cv2.HoughCircles(filtered_screen, cv2.HOUGH_GRADIENT, 1.2, 100, param1=44, param2=22, minRadius=0, maxRadius=0)
            print(f"Hough circles took {time.time() - start}")
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                print("Circles found:", len(circles))
                if len(circles) > 10:
                    break

                for (x, y, r) in circles:
                    # cv2.circle(actual_screen, (x, y), r, (0, 255, 0), 4)
                    # cv2.rectangle(actual_screen, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                    start = time.time()
                    shoot((x + game_coords[0], y + game_coords[1]))
                    print(f"Clicking took {time.time() - start}")
                    # cv2.imshow("actual_screen", actual_screen)
                    # cv2.imshow("filtered_screen", filtered_screen)
                    # cv2.waitKey(1)
            else:
                pass

        except Exception as e:
            print(e)
