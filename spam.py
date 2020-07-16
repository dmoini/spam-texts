import pyautogui
import inquirer
import time
import os
import sys

COUNTDOWN_SECONDS = 10
MAX_REPEATED_MESSAGE_COUNT = 50
WORD_PROGRESS_COUNT_PROMPT_COUNT = 100
TEXT_FILES_DIR = './texts/'


def promptConfirmationAndCountdown():
    confirmation = ''
    while True:
        confirmation = input(
            'Spamming will begin shortly. To exit script early, move your mouse to any corner of your screen. Please confirm you understand this and would like to proceed [y/n]: ').lower()
        if confirmation == 'y':
            break
        if confirmation == 'n':
            sys.exit()
    print(f'\nThe spamming will begin in {COUNTDOWN_SECONDS} second(s)')
    for i in range(COUNTDOWN_SECONDS, 0, -1):
        print(f'{i}', end=' ', flush=True)
        time.sleep(1)
    print()


def checkAndPrintWordProgressCount(wordCount):
    if wordCount % WORD_PROGRESS_COUNT_PROMPT_COUNT == 0:
        print(f'{wordCount} words sent')


def printStats(startTime, wordCount):
    totalSeconds = time.time() - startTime
    wordsPerMinute = wordCount / (totalSeconds / 60)
    print(f'\nExecution time: {totalSeconds:.2f} second(s)')
    print(f'Word count: {wordCount}')
    print(f'Words per minute: {wordsPerMinute:.2f}')


def spamMessage():
    message = input('What message would you like to send?: ')
    messageCount = 0
    while not(0 < messageCount <= MAX_REPEATED_MESSAGE_COUNT):
        messageCount = int(
            input(f'How many times would you like to send this message? (Max is {MAX_REPEATED_MESSAGE_COUNT}): '))
    print()
    promptConfirmationAndCountdown()
    startTime = time.time()
    wordCount = 0
    for i in range(messageCount):
        print('cool')
        print(message)
        pyautogui.typewrite(message)
        pyautogui.typewrite('enter')
        wordCount += 1
        checkAndPrintWordProgressCount(wordCount)
    printStats(startTime, wordCount)


def chooseFile():
    availableTexts = []
    for file in os.listdir(TEXT_FILES_DIR):
        s = ' '.join(f.capitalize() for f in file.split('-'))
        s = os.path.splitext(s)[0]
        availableTexts.append(s)
    questions = [
        inquirer.List('textFile',
                      message='What text file would you like to use?',
                      choices=availableTexts,
                      ),
    ]
    answers = inquirer.prompt(questions)
    return TEXT_FILES_DIR + answers['textFile'].replace(' ', '-').lower() + '.txt'


def spamTextFile():
    filePath = chooseFile()
    file = open(filePath, 'r')
    promptConfirmationAndCountdown()
    startTime = time.time()
    wordCount = 0
    for line in file:
        for word in line.split():
            pyautogui.typewrite(word)
            pyautogui.typewrite('enter')
            wordCount += 1
            checkAndPrintWordProgressCount(wordCount)
    file.close()
    printStats(startTime, wordCount)


def main():
    questions = [
        inquirer.List('spamChoice',
                      message='What would you like to spam?',
                      choices=['Repeated message', 'Text file word by word'],
                      ),
    ]
    answers = inquirer.prompt(questions)
    if answers['spamChoice'] == 'Repeated message':
        spamMessage()
    else:
        spamTextFile()


if __name__ == "__main__":
    main()
