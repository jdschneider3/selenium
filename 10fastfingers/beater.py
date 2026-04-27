# beater.py

# Summary:
#   Simulates typing on the 10fastfingers.com typing speed test.  

# Arguments:
#   1) [Optional] -e: Number of simulated typing mistakes to make

# Notes:
#   Cmd to launch chrome in remote debugging mode:
#     C:\"Program Files (x86)"\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\sel_profile"

import argparse
import time
import random
from numpy import number
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def type_words():
  
  # Handle Argument(s)
  parser = argparse.ArgumentParser(
    description="Simulates typing on the 10fastfingers.com typing speed test.")
  parser.add_argument("-e", "--errors", type=int, help="The number of words on which to simulate typing errors.")
  args = parser.parse_args()

  chrome_options = Options()
  chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

  try:
    driver = webdriver.Chrome(options=chrome_options)

    error_words = args.errors

    running = True
    while running:

      # Get the next word
      target_word = driver.execute_script(
        "return document.querySelector('span.highlight').innerText;")

      if not target_word:
        print("Word was found, but it appears to be empty.")
        return

      print(f"JavaScript found word: '{target_word}'")

      if error_words != 0:
        simulate_a_mistake = True

      # Focus on the typing input box
      input_area = driver.find_element(By.ID, "inputfield")
      input_area.click()

      # Simulate typing of the word into the input box
      for char in target_word.strip():
        if simulate_a_mistake:
          input_area.send_keys('x')
          error_words = error_words - 1
          simulate_a_mistake = False # Do not make a mistake again on this word
        else:
          input_area.send_keys(char)

        time.sleep(random.uniform(0.0000001, .0000002)) # This controls the typing speed

      input_area.send_keys(Keys.SPACE)
      print("Done.")

  except Exception as e:
    print(f"Error: {e}")


if __name__ == "__main__":
  try:
    type_words()
  except KeyboardInterrupt:
    raise SystemExit(130)
