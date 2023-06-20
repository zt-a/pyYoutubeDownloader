from pytube import YouTube
from tqdm import tqdm
from pytube.exceptions import PytubeError, AgeRestrictedError
import requests
from bs4 import BeautifulSoup
from termcolor import colored
from pyfiglet import Figlet


def getVideoName(url=''):
    print(colored('[!] Start scraping video', 'green'))
    # Отправляем GET-запрос к указанному URL и получаем содержимое страницы
    print(colored('[@] Get url', 'yellow'))
    response = requests.get(url=url)
    print(colored('[@] Get content', 'yellow'))
    content = response.content

    # Создаем объект BeautifulSoup для парсинга HTML-контента
    print(colored('[@] Parser', 'yellow'))
    soup = BeautifulSoup(content, 'html.parser')

    # Ищем элемент с заголовком видео
    title_element = soup.find('meta', property='og:title')

    # Получаем текст заголовка видео
    video_title = title_element['content'] if title_element else None
    # videoName = ''
    # for el in video_title.split(' '):
    #     videoName+=f'{el}_'
    #     print(videoName)
    # print(videoName, video_title)
    print(colored('[+] Finish scraping video', 'green'))
    return str(video_title)


def downloader(url='', videoName='video.mp4'):
    print(colored('[!] Start download video', 'green'))
    try:
        video = YouTube(url)
        # stream = video.streams.get_highest_resolution()  # Выбираем наивысшее разрешение
        # stream = video.streams.get_by_resolution('720p')  # Выбираем разрешение 720p
        stream = video.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
        total_size = stream.filesize
        print(colored('[!] Download video', 'green'))
        # with tqdm(total=total_size, unit='bytes', unit_scale=True) as progress_bar:
        #     stream.download(filename=f'{videoName}.mp4', skip_existing=False,
        #                     on_progress_callback=lambda chunk, file_handle, bytes_remaining: progress_bar.update(
        #                         file_handle.tell()))
        response = requests.get(stream.url, stream=True)
        with open(f'{videoName}.mp4', 'wb') as f:
            with tqdm(total=total_size, unit='bytes', unit_scale=True) as progress_bar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))

        stream.download(filename=f'{videoName}.mp4')  # Скачиваем видео
        print(colored(f'[@] videoName: {videoName}.mp4', 'yellow'))
        print(colored(f"[+] Видео успешно скачано под именем '{videoName}.mp4'!", 'green'))
    except AgeRestrictedError:
        print(colored("[-] Ошибка: Видео имеет возрастное ограничение. Пожалуйста, выполните вход в аккаунт YouTube.",
                      'red'))
    except PytubeError as pytubeEx:
        print(colored(f"[-] Произошла ошибка при скачивании видео: {pytubeEx}", 'red'))
    except Exception as ex:
        print(colored(f"[-] Произошла ошибка при скачивании видео: {ex}", 'red'))


def downloader(urls=[]):
    for url in urls:
        videoName = getVideoName(url=url)
        print(colored('[!] Start download video', 'green'))
        try:
            video = YouTube(url)
            # stream = video.streams.get_highest_resolution()  # Выбираем наивысшее разрешение
            # stream = video.streams.get_by_resolution('720p')  # Выбираем разрешение 720p
            stream = video.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
            total_size = stream.filesize
            print(colored('[!] Download video', 'green'))
            # with tqdm(total=total_size, unit='bytes', unit_scale=True) as progress_bar:
            #     stream.download(filename=f'{videoName}.mp4', skip_existing=False,
            #                     on_progress_callback=lambda chunk, file_handle, bytes_remaining: progress_bar.update(
            #                         file_handle.tell()))
            response = requests.get(stream.url, stream=True)
            with open(f'{videoName}.mp4', 'wb') as f:
                with tqdm(total=total_size, unit='bytes', unit_scale=True) as progress_bar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            progress_bar.update(len(chunk))

            stream.download(filename=f'{videoName}.mp4')  # Скачиваем видео
            print(colored(f'[@] videoName: {videoName}.mp4', 'yellow'))
            print(colored(f"[+] Видео успешно скачано под именем '{videoName}.mp4'!", 'green'))
        except AgeRestrictedError:
            print(
                colored("[-] Ошибка: Видео имеет возрастное ограничение. Пожалуйста, выполните вход в аккаунт YouTube.",
                        'red'))
        except PytubeError as pytubeEx:
            print(colored(f"[-] Произошла ошибка при скачивании видео: {pytubeEx}", 'red'))
        except Exception as ex:
            print(colored(f"[-] Произошла ошибка при скачивании видео: {ex}", 'red'))


def start():
    print('-' * 20, colored('[@] [S.T.A.R.T]', 'yellow'), '-' * 20)
    url = str(input(colored('URL: ', 'yellow')))
    print()
    print(colored('URL:', 'green'), colored(f'{url}', 'yellow'))
    print(colored('Имя:', 'green'), colored(f'{getVideoName(url=url)}', 'yellow'))
    print()
    downloader(url=url, videoName=getVideoName(url=url))
    print('-' * 20, colored('[@] [F.I.N.I.S.H]', 'yellow'), '-' * 20)


def bigstart():
    print('-' * 20, colored('[@] [S.T.A.R.T]', 'yellow'), '-' * 20)
    urls = list(map(str, input(colored('URLs: ', 'yellow')).split(' ')))
    print()
    print(colored('URLs:', 'green'), colored(f'{urls}', 'yellow'))
    print(colored('Имя каждего URLs:', 'green'), colored('Будут заданы автоматически', 'yellow'))
    print()
    downloader(urls=urls)
    print('-' * 20, colored('[@] [F.I.N.I.S.H]', 'yellow'), '-' * 20)


def main():

    print(colored('\t\tВыбирайте варианты:)', 'blue'))
    print(colored('\t\t1: Один раз', 'green'))
    print(colored('\t\t2: Много раза(список url)<url url url>', 'yellow'))
    print()
    print(colored('\t\t0: Выход (exit)', 'red'))

    command = int(input(colored('command: ', 'red')))
    if command == 1:
        print(colored('Задайте url @:', 'green'))
        start()
    elif command == 2:
        print(colored('Задайте список URLs через пробелы', 'yellow'))
        bigstart()
    elif command == 0:
        print(colored('Пока :(', 'red'), colored('Буду рад ещё раз встретится с тобой', 'yellow'))
        exit()


if __name__ == '__main__':
    preview_text = Figlet(font='slant')
    print(colored(preview_text.renderText('Youtube'), 'green'))
    print(colored(preview_text.renderText('Downloader'), 'yellow'))
    main()
