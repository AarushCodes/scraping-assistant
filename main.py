from selenium import webdriver
import speech_recognition as sr
import pyttsx3
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import csv

#Headers
headers = {
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'

}


# initailizing pyttsx3
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# defining speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Recognizing function
def recognize():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        audio = r.listen(source)

    try:
        print('Recognizing')
        query = r.recognize_google(audio, language='en-in')
        print(f'User said: {query}\n')

    except Exception as e:
        print("I didn't quite understand that, try saying it again?")
        return 'None'
    return query

if __name__ == '__main__':
    while True:
        query = recognize().lower()
        if 'most popular video of' in query:
            try:
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                driver = webdriver.Chrome(chrome_options=chrome_options)
                channel = query.replace('most popular video of', '').strip().replace(' ', '+')
                driver.get(f'https://www.youtube.com/results?search_query={channel}&sp=EgIQAg%253D%253D')
                channel_url_element1 = driver.find_element_by_xpath('//*[@id="avatar-section"]/a')
                channel_url_element = channel_url_element1.get_attribute('href')
                channel_url = f'{channel_url_element}/videos?view=0&sort=p&flow=grid'
                driver.get(channel_url)
                most_popular_video1 = driver.find_element_by_xpath('//*[@id="video-title"]')
                most_popular_video = most_popular_video1.get_attribute('title')
                views = driver.find_element_by_xpath('//*[@id="metadata-line"]/span[1]').text
                what_to_say = (f'the most popular video of the channel is {most_popular_video} with {views}')
                speak(what_to_say)
                print(what_to_say)
                driver.close()
            except Exception as e:
                speak('Sorry there was an error')
                print(e)
                driver.close()
        elif "what is the weather in" in query:
            location = query.replace("what is the weather in", '').replace(' ', '+')
            html_text = requests.get(f'https://www.google.com/search?q=weather+in+{location}', headers=headers).text
            soup = BeautifulSoup(html_text, 'lxml')
            results = soup.find('div', class_='nawv0d')
            temperature_ = results.find('div', class_='vk_bk TylWce')
            temperature = temperature_.find('span').text
            what_it_is_like = results.find('div', class_='wob_dcp').text
            google_location = results.find('div', class_='wob_loc mfMhoc').text
            result = f'The temperature in {google_location} is {temperature} degrees celsius and it is {what_it_is_like}'
            speak(result)
            print(result)
        elif 'amazon scraper' in query:
            print('which search do you want to scrape')
            command = input('>>')
            search = command.replace(' ', '+')
            f = open('results.csv', 'w', encoding='UTF8', newline="")
            writer = csv.writer(f)
            _1 = ('Title', 'Price', 'No of Ratings', 'Rating')
            writer.writerow(_1)
            html_code = requests.get(f'https://www.amazon.in/s?k={search}&ref=nb_sb_noss_1', headers=headers).text
            soup = BeautifulSoup(html_code, 'lxml')
            items = soup.find_all('div', class_='sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20')
            for item in items:
                try:
                    title = item.find('span', class_ = 'a-size-medium a-color-base a-text-normal').text
                except Exception as e:
                    title = 'Title not found'
                try:
                    price = item.find('span', class_='a-price-whole').text
                except Exception as e:
                    price = 'Price Not found'
                try:
                    ratings = item.find('span', class_='a-size-base').text
                except Exception as e:
                    ratings = 'No Ratings'
                try:
                    rating = item.find('span', class_='a-icon-alt').text
                except Exception as e:
                    rating = 'Rating Not Found'
                _2 = (title.strip(), price.strip(), ratings.strip(), rating.strip())
                writer.writerow(_2)
            f.close()
            print('All results of page 1 saved to results.csv')
        elif 'stop' in query:
            exit()
        elif 'thank you' in query:
            speak('Welcome')