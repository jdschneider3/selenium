# beater.py

# Summary:
#   Simulates typing on the 10fastfingers.com typing speed test.
#   Updated to work with 10fastfingers.com v3.0 (April 14 2026)  

# Arguments:
#   1) [Optional] -e: Number of simulated typing mistakes to make

# Notes:
#   Cmd to launch chrome in remote debugging mode:
#     taskkill /F /IM chrome.exe /T 
#     C:\"Program Files (x86)"\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\sel_profile"

import argparse
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def type_words():
  
  # Handle Argument(s)
  parser = argparse.ArgumentParser(
    description="Simulates typing on the 10fastfingers.com typing speed test.")
  parser.add_argument("-e", "--err", type=int, default=0, help="The percentage of words on which to simulate typing errors.")
  args = parser.parse_args()

  chrome_options = Options()
  chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

  # Sleep for 5 seconds to allow the user to manuver the cursor
  for i in range(5, 0, -1):
    print(f"Please focus the cursor on the text input. Starting in: {i} seconds...", end="\r", flush=True)
    time.sleep(1);
  
  # Note: Moves output to the next line 
  print()

  try:
    
    driver = webdriver.Chrome(options=chrome_options)
    error_words = args.err

    # Focus on the typing input box
    input_area = driver.switch_to.active_element
    
    running = True

    while running:

      # Fetch pieces of the next word
      js_script = """
        let firstCharSpan = document.querySelector('.word-box-active-char.word-box-active-word');
        let restOfWordSpan = document.querySelector('span[class="word-box-active-word"]');
        
        return {
            "first_char": firstCharSpan ? firstCharSpan.innerText : null,
            "rest_of_word": restOfWordSpan ? restOfWordSpan.innerText : null
        };
      """

      data = driver.execute_script(js_script)

      if not data:
        print("ERROR: The next word was unable to be fetched.")
        return

      # Build the target word
      first_char = data.get("first_char")
      rest_of_word = data.get("rest_of_word")

      target_word = ""

      if first_char is not None:
        target_word += first_char
          
      if rest_of_word is not None:
        target_word += rest_of_word

      if not target_word:
        print("ERROR: Word was found, but it appears to be empty.")

      print(f"Next Word: '{target_word}'")

      # Simulate typing of the target word into the input box
      for char in target_word.strip():
        input_area.send_keys(char)
        time.sleep(random.uniform(.00001, .00002)) # This controls the typing speed

      # Send a space before the next word
      input_area.send_keys(Keys.SPACE)

  except Exception as e:
    print(f"Error: {e}")


if __name__ == "__main__":
  try:
    type_words()
  except KeyboardInterrupt:
    raise SystemExit(130)
