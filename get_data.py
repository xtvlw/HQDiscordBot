from requests import get
from bs4 import BeautifulSoup as bs
from random import randrange
from os import mkdir, listdir, system


def get_reference(name):
    link = f'https://hqdragon.com/pesquisa?nome_hq={name}'
    info_list = []
    page = get(link).text
    soup_elements = bs(page, 'html.parser')
    main_elements = soup_elements.find('div', class_='blog-post')
    opition_element = main_elements.find_all('a')
    mark = True
    for i in range(0, len(opition_element)):
        if mark == True:
            info = {'link': opition_element[i].get('href')}
            info["image_link"] = opition_element[i].find('img').get('src')
            info["name"] = opition_element[i].find('img').get('alt')
            info_list += [info]
            mark = False
        else:
            mark = True
    return info_list


def get_reference_info(reference_link):
    info_list = {}
    args = ['name', 'publisher', 'year', 'scan', 'status', 'sinopse']
    page = get(reference_link).text
    soup_elements = bs(page, 'html.parser')
    main_elements = soup_elements.find('div', 'col-md-8')
    opition_element = main_elements.find_all('p')
    info_list["name"] = opition_element[0].text
    for i in range(0, len(opition_element)):
        info_list[args[i]] = opition_element[i].text
    main_elements = soup_elements.find('table', 'table table-bordered')
    list_capthers = main_elements.find_all('a')
    anual_capters = 0
    for i in list_capthers:
        if 'A' in i.text:
            anual_capters += 1
    info_list['anual_capters'] = anual_capters
    info_list['normal_capters'] = int(list_capthers[0].text.replace('Ler #', ''))
    return info_list


def get_reference_images(reference_link):
    name = reference_link.replace('https://hqdragon.com/leitor/', '')
    name = name.replace('/', '').replace('(', '').replace(')', '')
    page = get(reference_link).text
    soup_elements = bs(page, 'html.parser')
    main_elements = soup_elements.find('div', class_='col-sm-12 text-center')
    image_list = []
    for i in main_elements.find_all('img'):
        image_list += [i.get('src')]
    return {"links":image_list, "name": name}


def make_pdf(image_list, name):
    path = f'/home/nf/Documents/python/HQDiscordBot/{name}_{randrange(0, 10)}'
    mkdir(path)
    for i in range(len(image_list)):
        if i < 10:
            i = f'0{i}'
        with open(f'{path}/page{i}.png', 'wb') as image:
            image.write(get(image_list[int(i)]).content)
    system(f'convert {path}/*.png /home/nf/Documents/python/HQDiscordBot/pdf/{name}.pdf && rm -rf {path}')
    return f'/home/nf/Documents/python/HQDiscordBot/pdf/{name}.pdf'


def make_html(image_list, name):
    arc_images = open(f'/home/nf/Documents/python/HQDiscordBot/html/{name}_{randrange(0, 10)}.html', 'w')
    for i in image_list:
        arc_images.write(f"<center><div><img src='{str(i)}'></div></center>")
    return arc_images

'''
list = get_reference_images('https://hqdragon.com/leitor/Tony_Stark_Homem_de_Ferro_(2018)/01')

make_html(list['links'], list['name'])'''
