import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import os
import time


class WordleConnection:

    def __init__(self, headless=False):
        self.headless = headless
        self.driver = self.connect()
        self.board, self.tiles = self.load_board_and_tiles()

        self.current_index = 0
        self.keyboard = self.load_keyboard()
        self.close_pop_ups()


    def connect(self):
        options = Options()
        options.headless = self.headless
        url = "https://www.nytimes.com/games/wordle/index.html"
        #url = "https://wordlegame.org/"
        if os.name =="nt":
            chrome_service = Service("C:\Program Files\Chromedriver\chromedriver.exe")
        else:
            chrome_service = Service("/Users/a1/Downloads/Code/chromedriver")
        driver = webdriver.Chrome(service=chrome_service, options=options)
        driver.get(url)

        return driver

    def disconnect(self):
        self.driver.quit()

    def load_board_and_tiles(self):
        board = self.driver.find_element(By.CLASS_NAME, "Board-module_board__lbzlf")
        tiles = self.driver.find_elements(By.CLASS_NAME, "Tile-module_tile__3ayIZ")[:30:]
        return board, tiles

    def read_last_row(self):
        if self.current_index == 0:
            return [tile.text for tile in self.tiles[self.current_index:self.current_index+5:]]
        return [tile.text for tile in self.tiles[self.current_index-5:self.current_index:]]

    def load_keyboard(self):
        buttons = self.driver.find_elements(By.CLASS_NAME,"Key-module_key__Rv-Vp")
        keyboard = {b.get_attribute("data-key"): b for b in buttons}


        keyboard["del"] = keyboard['←']
        keyboard["enter"] = keyboard['↵']
        keyboard.pop('←')
        keyboard.pop('↵')
        return keyboard

    def get_coloring(self):
        time.sleep(1)
        result = ""
        if self.current_index >= 0:
            greens = []
            for i, tile in enumerate(self.tiles[self.current_index:self.current_index+5:]):
                state = tile.get_attribute("data-state")
                print(dir(tile))
                print(state)
                if state == 'absent':
                    result+=tile.text.lower()
                elif state == "correct":
                    result+=tile.text.upper()
                    greens.append(i)
                elif state == "present":
                    result+=tile.text.upper()
                else:
                    print("HEREEE")
                    for i in range(5):
                        self.keyboard["del"].click()
                    return False, False
            self.current_index += 5
        print(result)
        print(greens)
        return result, greens

    def close_pop_ups(self):
        close_button_1 = self.driver.find_element(By.ID, "pz-gdpr-btn-closex")
        close_button_1.click()

        close_button_2 = self.driver.find_element(By.CLASS_NAME, "Modal-module_closeIcon__b4z74")
        close_button_2.click()

        #action = webdriver.common.action_chains.ActionChains(self.driver)
        #action.move_to_element_with_offset(close_button_2, -400, -400)
        #action.click()
        #action.perform()

    def write(self, guess):
        print("Try to write: ",guess)
        for b in guess:
            self.keyboard[b].click()
        self.keyboard["enter"].click()
        return self.get_coloring()



if __name__ == "__main__":
    wordle_connection = WordleConnection()

    while True:
        try:
            c = input("r to read, w to write, q to quit: ")
            if c == "q":
                break
            if c == "r":
                print(wordle_connection.read_last_row())
            if c == "w":
                guess = input("enter guess: ")
                wordle_connection.write(guess=guess)
        except:
            print(traceback())
    wordle_connection.disconnect()

