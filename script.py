import requests
import time
import json
import time
import telebot
from telebot import types
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import datetime
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
# загрузка пользователей
admins_chat_id_adr = []
chat_list = []
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--no-sandbox')
options.add_argument("--ignore-certificate-error")
options.add_argument("--ignore-ssl-errors")
browser = webdriver.Chrome(r'C:\Users\Administrator\Desktop\cian\chromedriver.exe', options=options)
count_aut = 0
TOKEN = '1914102772:AAHDSYNJRSPraCLS3qFWoIpb472hv37zHjY'
bot = telebot.TeleBot(TOKEN)

def parse_cian(message):
    check_zakaz = 0
    count_zakaz = 0
    if message.text == '❌ Стоп':
        bot.send_message(message.from_user.id, '❌ Стоп\nПрекращена работа!')
        bot_message(message)
        return 
    # Загрузка пользователей
    with open(r'chat_id.json', encoding='utf-8-sig') as f:
        tmp_chat_list = json.load(f)

    for i in tmp_chat_list:
        chat_list.append(i['chat_id'])
    
    check_while = False
    # Загруза админов
    with open(r'admins_chat_id_adr.json', encoding='utf-8-sig') as f:
        tmp_amdin_list = json.load(f)
    for i in tmp_amdin_list:
        admins_chat_id_adr.append(i['chat_id'])
        
    result_town_list = ['Кудрово','Мурино','Шушары','Ломоносов','Пушкин','Рыбацкое','Санкт-Петербург']
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    markup_admin = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item3 = types.KeyboardButton('✅ Старт')
    item6 = types.KeyboardButton('➕ Добавить пользователя')
    markup.add(item3)
    markup_admin.add(item3, item6)
    
    bot.send_message(message.from_user.id, 'Начался анализ ваших заявок! После покупки 5 заказов бот окончит работу!')
    lastsave = time.time()
    while True:
        if count_zakaz >= 5:
            if str(message.from_user.id) in admins_chat_id_adr:
                bot.send_message(message.from_user.id, 'Бот окончил работу. Было выбрано ' + str(count_zakaz) + ' заказов', reply_markup = markup_admin)
                return
            elif str(message.from_user.id) in chat_list: 
                bot.send_message(message.from_user.id, 'Бот окончил работу. Было выбрано ' + str(count_zakaz) + ' заказов', reply_markup = markup)
                return
        else:
            link_leads = browser.get('https://my.cian.ru/leads')
            time.sleep(3)
            list_of_tr = browser.find_elements_by_class_name('f341f0ad46--container--n4AuU')
            for i in list_of_tr:
                main_page = i
                bodyText = ''
                towm_div = i.find_element_by_class_name('f341f0ad46--container--2IJCh')
                town = towm_div.find_element_by_tag_name('span').text
                
                deystvie_div = i.find_element_by_class_name('f341f0ad46--container--1yzcw')
                deystvie = deystvie_div.find_element_by_tag_name('span').text
                for tw in result_town_list:
                    if town in tw:
                        check_while = True
                if check_while:
                    check_while = False
                    if deystvie == 'Сдать':
                        cost = ''
                        cost_tmp = i.find_element_by_class_name('f341f0ad46--two-column--3gCRv')
                        cost_tmp_tmp = cost_tmp.find_element_by_class_name('f341f0ad46--top--1xG88')
                        cost_tmp_tmp_tmp = cost_tmp_tmp.find_element_by_class_name('f341f0ad46--left--SYG1U')

                        main_page_inner = cost_tmp_tmp_tmp.get_attribute('innerHTML')
                        soup_cost = BeautifulSoup(main_page_inner, 'html.parser')
                        cost_list = soup_cost.find_all("span", class_="f341f0ad46--color_black_100--A_xYw f341f0ad46--lineHeight_20px--2dV2a f341f0ad46--fontWeight_normal--2G6_P f341f0ad46--fontSize_14px--10R7l f341f0ad46--display_inline--2gjyY f341f0ad46--text--2_SER")
                        for j in cost_list:
                            if 'мес' in j.get_text():
                                cost = j.get_text()
                                break



                        if 'мес' in cost:
                            if 'тыс' in cost:
                                cost = cost.replace('тыс.', '000')
                            cost_on_number = re.findall(r'\d*\s*\d*', cost)

                            cost_on = cost_on_number[0].replace('\xa0','')


                            if int(cost_on) >= 15000 or (len(cost_on) == 2 and int(cost_on) > 15):
                                
                                button_zakaz_tmp = i.find_element_by_class_name('f341f0ad46--three-column--3gA7K')
                                button_zakaz_tmp_tmp = button_zakaz_tmp.find_element_by_tag_name('div')
                                button_zakaz_tmp_tmp_tmp = button_zakaz_tmp_tmp.find_element_by_class_name('f341f0ad46--top--1xG88')
                                button_zakaz = button_zakaz_tmp_tmp_tmp.find_element_by_tag_name('button')
                                button_zakaz.click()
                                browser.switch_to.window(browser.window_handles[-1])
                                try:
                                    time.sleep(3)
                                    
                                    if 'Заявка недоступна' in bodyText:
                                        browser.switch_to.window(browser.window_handles[0])
                                        time.sleep(3)
                                        continue
                                    

                                    div_cont = browser.find_element_by_xpath('//*[@id="lk-container"]/div/div/div/main/div[1]/div/div[2]/div[2]/div[1]')
                                    div_con_in = div_cont.find_element_by_tag_name('div')
                                    div_con_main = div_con_in.find_elements_by_class_name('e06d409602--buy_item--1UsmV')
                                    
                                    time.sleep(2)
                                    if len(div_con_main) == 2:
                                        button_x = div_con_main[1].find_element_by_class_name('e06d409602--button_container--1RQrZ')
                                        button_x_div = button_x.find_element_by_tag_name('div')
                                        button_buy = button_x_div.find_element_by_tag_name('button')
                                        button_buy.click()

                                    elif len(div_con_main) == 1:
                                        browser.find_element_by_xpath('//*[@id="lk-container"]/div/div/div/main/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/button').click()
                                    time.sleep(3)
                                    browser.find_element_by_xpath('//*[@id="lk-container"]/div/div/div/main/div[1]/div/div[1]/div/div/div[2]/div[2]/div/div[3]/button[1]').click()

                                    time.sleep(3)
                                    bot.send_message(message.from_user.id,'❗️❗️❗️\nНовая заявка куплена\nОтзвонитесь клиенту❗️❗️❗️')
                                    text_from_flat = browser.find_element_by_class_name('e06d409602--container--1o2aJ').text
                                    bot.send_message(message.from_user.id,'Информация о квартире:\n\n' + text_from_flat)

                                    telephone_number = browser.find_element_by_class_name('e06d409602--phone--3LTga').text
                                    bot.send_message(message.from_user.id,'☎️☎️☎️ Телефон: ' + telephone_number)
                                    count_zakaz+=1
                                    time.sleep(3)
                                    browser.switch_to.window(browser.window_handles[0])
                                    time.sleep(3)
                                    
                                except Exception as e:
                                    print(e)
                                    
                                    browser.switch_to.window(browser.window_handles[0])
                                    time.sleep(3)
                                    if str(message.from_user.id) in admins_chat_id_adr:
                                        
                                        bot.send_message(message.chat.id, 'Что-то пошло не так... Возможно нехватка средств! \nЗаново нажмите кнопку ✅ Старт!'.format(message.from_user), reply_markup = markup_admin)            
                                        return
                                    elif str(message.from_user.id) in chat_list:
                                        
                                        bot.send_message(message.chat.id, 'Что-то пошло не так... Возможно нехватка средств! \nЗаново нажмите кнопку ✅ Старт!'.format(message.from_user), reply_markup = markup)
                                        return
                            else:
                                continue

                    elif deystvie == 'Продать':
                        cost = ''
                        cost_tmp = i.find_element_by_class_name('f341f0ad46--two-column--3gCRv')
                        cost_tmp_tmp = cost_tmp.find_element_by_class_name('f341f0ad46--top--1xG88')
                        cost_tmp_tmp_tmp = cost_tmp_tmp.find_element_by_class_name('f341f0ad46--left--SYG1U')

                        main_page = cost_tmp_tmp_tmp.get_attribute('innerHTML')
                        soup_cost = BeautifulSoup(main_page, 'html.parser')
                        cost_list = soup_cost.find_all("span", class_="f341f0ad46--color_black_100--A_xYw f341f0ad46--lineHeight_20px--2dV2a f341f0ad46--fontWeight_normal--2G6_P f341f0ad46--fontSize_14px--10R7l f341f0ad46--display_inline--2gjyY f341f0ad46--text--2_SER")
                        for j in cost_list:
                            if 'млн' in j.get_text():
                                cost = j.get_text()
                                break


                        if 'млн' in cost:
                            cost_on_number = re.findall(r'\d*\s*\d*', cost)

                            cost_on = cost_on_number[0].replace('\xa0','')

                            
#                                 if int(cost_on) >= 4 and int(cost_on) < 6:

                            button_zakaz_tmp = i.find_element_by_class_name('f341f0ad46--three-column--3gA7K')
                            button_zakaz_tmp_tmp = button_zakaz_tmp.find_element_by_tag_name('div')
                            button_zakaz_tmp_tmp_tmp = button_zakaz_tmp_tmp.find_element_by_class_name('f341f0ad46--top--1xG88')
                            button_zakaz = button_zakaz_tmp_tmp_tmp.find_element_by_tag_name('button')
                            button_zakaz.click()
                            browser.switch_to.window(browser.window_handles[-1])
                            

                            try:
                                time.sleep(3)
                                bodyText = browser.find_element_by_tag_name('body').text
                                if 'Заявка недоступна' in bodyText:
                                    browser.switch_to.window(browser.window_handles[0])
                                    time.sleep(3)
                                    continue
                                div_cont = browser.find_element_by_xpath('//*[@id="lk-container"]/div/div/div/main/div[1]/div/div[2]/div[2]/div[1]')
                                div_con_in = div_cont.find_element_by_tag_name('div')
                                div_con_main = div_con_in.find_elements_by_class_name('e06d409602--buy_item--1UsmV')
                                
                                if len(div_con_main) == 2:
                                    button_x = div_con_main[1].find_element_by_class_name('e06d409602--button_container--1RQrZ')
                                    button_x_div = button_x.find_element_by_tag_name('div')
                                    button_buy = button_x_div.find_element_by_tag_name('button')
                                    button_buy.click()

                                elif len(div_con_main) == 1:
                                    browser.find_element_by_xpath('//*[@id="lk-container"]/div/div/div/main/div[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div/button').click()
                                time.sleep(3)
                                browser.find_element_by_xpath('//*[@id="lk-container"]/div/div/div/main/div[1]/div/div[1]/div/div/div[2]/div[2]/div/div[3]/button[1]').click()


                                time.sleep(5)
                                bot.send_message(message.from_user.id,'❗️❗️❗️\nНовая заявка куплена\nОтзвонитесь клиенту❗️❗️❗️')
                                text_from_flat = browser.find_element_by_class_name('e06d409602--container--1o2aJ').text
                                bot.send_message(message.from_user.id,'Информация о квартире:\n\n' + text_from_flat)

                                telephone_number = browser.find_element_by_class_name('e06d409602--phone--3LTga').text
                                bot.send_message(message.from_user.id,'☎️☎️☎️ Телефон: ' + telephone_number)
                                count_zakaz+=1
                                time.sleep(3)
                                browser.switch_to.window(browser.window_handles[0])
                                time.sleep(3)
                                    
                                

                            except Exception as e:
                                print(e)
                                browser.switch_to.window(browser.window_handles[0])
                                time.sleep(3)
                                if str(message.from_user.id) in admins_chat_id_adr:
                                    bot.send_message(message.chat.id, 'Что-то пошло не так... Возможно нехватка средств!\nЗаново нажмите кнопку ✅ Старт!'.format(message.from_user), reply_markup = markup_admin)            
                                    return
                                elif str(message.from_user.id) in chat_list:
                                    bot.send_message(message.chat.id, 'Что-то пошло не так... Возможно нехватка средств!\nЗаново нажмите кнопку ✅ Старт!'.format(message.from_user), reply_markup = markup)
                                    return
#                                 elif int(cost_on) >= 6:
#                                     button_zakaz_tmp = i.find_element_by_class_name('f341f0ad46--three-column--3gA7K')
#                                     button_zakaz_tmp_tmp = button_zakaz_tmp.find_element_by_tag_name('div')
#                                     button_zakaz_tmp_tmp_tmp = button_zakaz_tmp_tmp.find_element_by_class_name('f341f0ad46--top--1xG88')
#                                     button_zakaz = button_zakaz_tmp_tmp_tmp.find_element_by_tag_name('button')
#                                     button_zakaz.click()
#                                     browser.switch_to.window(browser.window_handles[count_zakaz+1])

#                                     try:
#                                         time.sleep(3)
#                                         div_cont = browser.find_element_by_xpath('//*[@id="lk-container"]/div/div/div/main/div[1]/div/div[2]/div[2]/div[1]')
#                                         div_con_in = div_cont.find_element_by_tag_name('div')
#                                         div_con_main = div_con_in.find_elements_by_class_name('e06d409602--buy_item--1UsmV')
#                                         print(len(div_con_main))
#                                         if len(div_con_main) == 2:
#                                             browser.find_element_by_xpath('//*[@id="lk-container"]/div/div/div/main/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/button').click()
#                                         time.sleep(3)                                
#                                         browser.find_element_by_xpath('//*[@id="lk-container"]/div/div/div/main/div[1]/div/div[1]/div/div/div[2]/div[2]/div/div[3]/button[1]').click()
#                                         time.sleep(3)
#                                         bot.send_message(message.from_user.id,'❗️❗️❗️\nНовая заявка куплена\nОтзвонитесь клиенту❗️❗️❗️')
#                                         text_from_flat = browser.find_element_by_class_name('e06d409602--container--1o2aJ').text
#                                         bot.send_message(message.from_user.id,'Информация о квартире:\n\n' + text_from_flat)

#                                         telephone_number = browser.find_element_by_class_name('e06d409602--phone--3LTga').text
#                                         bot.send_message(message.from_user.id,'☎️☎️☎️ Телефон: ' + telephone_number)
#                                         count_zakaz+=1
#                                     except Exception as e:
#                                         print(e)
#                                         if str(message.from_user.id) in admins_chat_id_adr:
#                                             bot.send_message(message.chat.id, 'Что-то пошло не так... Возможно нехватка средств!\nЗаново нажмите кнопку ✅ Старт!'.format(message.from_user), reply_markup = markup_admin)            
#                                             return
#                                         elif str(message.from_user.id) in chat_list:
#                                             bot.send_message(message.chat.id, 'Что-то пошло не так... Возможно нехватка средств!\nЗаново нажмите кнопку ✅ Старт!'.format(message.from_user), reply_markup = markup)
#                                             return
                        else:
                            continue
def code_from_tel(message):
  
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('❌ Стоп')

    markup.add(item1)

    if message.text == '❌ Стоп':
        bot_message(message)
        return 
    elif message.text == ' ':
        bot.send_message(message.from_user.id, 'Вы успешно вошли в Циан.\nДля работы бота введите любое сообщение!', reply_markup = markup)
        bot.register_next_step_handler(message, parse_cian)
    code = message.text
    check_code = re.match(r'^-?[0-9]+$', code)
    if check_code and len(code) == 4:
        time.sleep(3)
        code_click = browser.find_element_by_class_name('b7635b5199--input--2vxTR')    
        code_click.send_keys(code)
        
        bot.send_message(message.from_user.id, 'Вы успешно вошли в Циан.\n❗️❗️❗️\n\nДля начала работы бота введите любое сообщение\n\n❗️❗️❗️', reply_markup = markup)
        bot.register_next_step_handler(message, parse_cian)
       
    else:
        bot.send_message(message.from_user.id, 'Введите числовое корректное значение!', reply_markup = markup)
        bot.register_next_step_handler(message, code_from_tel)
        
def add_telephone(message):
    with open(r'chat_id.json', encoding='utf-8-sig') as f:
        tmp_chat_list = json.load(f)
    if message.text == '⬅️ Назад':
        bot_message(message)
        return 
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('➕ Хочу еще добавить пользователя!')
    back = types.KeyboardButton('⬅️ Назад')
    markup.add(item1, back)
    tel = message.text
    if int(tel) >= 900000000:
        bot.send_message(message.from_user.id, 'Пользователь успешно добавлен!', reply_markup = markup)
        for i in tmp_chat_list:
            if i['tel'] == '':
                i['tel'] = tel
                break
        with open(r'chat_id.json', 'w',encoding='utf-8-sig') as f:
            json.dump(tmp_chat_list,f)
    else:
        bot.send_message(message.from_user.id, 'Введите числовое корректное значение!', reply_markup = markup)
        bot.register_next_step_handler(message, add_telephone)

# Функционал 
# запись в базу

def get_chat_id(message):
    with open(r'chat_id.json', encoding='utf-8-sig') as f:
        tmp_chat_list = json.load(f)
    if message.text == '⬅️ Назад':
        bot_message(message)
        return 
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('➕Хочу еще добавить пользователя!')
    back = types.KeyboardButton('⬅️ Назад')
    markup.add(item1, back)
    
    # Проверка на содержание только чисел
    matched = re.match(r'^-?[0-9]+$',message.text )
    if matched:        
        chat_id = int(message.text)
        
        if int(chat_id) >= 100000000 and int(chat_id) < 1000000000:
            bot.send_message(message.from_user.id, 'Пользователь с chat_id = ' + str(chat_id) + ' добавлен. Введите номер телефона пользователя в формате (9990001122).', reply_markup = markup)
            tmp_chat_list.append({
                'chat_id' : str(chat_id),
                'tel': ''
            })
            with open(r'chat_id.json', 'w',encoding='utf-8-sig') as f:
                json.dump(tmp_chat_list,f)
            bot.register_next_step_handler(message, add_telephone)
            
        else:
            bot.send_message(message.from_user.id, 'Введите числовое корректное значение!', reply_markup = markup)
            bot.register_next_step_handler(message, get_chat_id)
    else:
            bot.send_message(message.from_user.id, 'Введите числовое корректное значение!', reply_markup = markup)
            bot.register_next_step_handler(message, get_chat_id)


@bot.message_handler(commands=['start'])
def start(message):
    
   
    # Загрузка пользователей
    with open(r'chat_id.json', encoding='utf-8-sig') as f:
        tmp_chat_list = json.load(f)

    for i in tmp_chat_list:
        chat_list.append(i['chat_id'])

    
    # Загруза админов
    with open(r'admins_chat_id_adr.json', encoding='utf-8-sig') as f:
        tmp_amdin_list = json.load(f)
    for i in tmp_amdin_list:
        admins_chat_id_adr.append(i['chat_id'])
        
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    markup_admin = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('✅ Старт')
    item4 = types.KeyboardButton('➕ Добавить пользователя')
    markup.add(item1)
    markup_admin.add(item1, item4)
    if str(message.from_user.id) in admins_chat_id_adr:
        bot.send_message(message.chat.id, 'Здраствуйте, Светлана. Начнем работу!'.format(message.from_user), reply_markup = markup_admin)            
        
    elif str(message.from_user.id) in chat_list:
        bot.send_message(message.chat.id, 'Здравствуйте, {0.first_name}! Начнем работу! \nВыберите действие!'.format(message.from_user), reply_markup = markup)
    else:
        bot.send_message(message.chat.id, 'Здравствуйте, {0.first_name}! У Вас нет права доступа пользоваться данным ботом.)'.format(message.from_user))
    
    
@bot.message_handler(content_types=['text'])
def bot_message(message):
    global count_aut
    # Загрузка пользователей
    with open(r'chat_id.json', encoding='utf-8-sig') as f:
        tmp_chat_list = json.load(f)

    for i in tmp_chat_list:
        chat_list.append(i['chat_id'])

    # Загруза админов
    with open(r'admins_chat_id_adr.json', encoding='utf-8-sig') as f:
        tmp_amdin_list = json.load(f)
    for i in tmp_amdin_list:
        admins_chat_id_adr.append(i['chat_id'])
    for i in tmp_chat_list:
        if str(message.from_user.id) == i['chat_id']:
            tel = i['tel']
        
    if message.chat.type == 'private':
        
        if message.text == '✅ Старт':
            time.sleep(1)
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            bot.send_message(message.chat.id, '✅ Старт!\n\nПодождите! \n\nДождитесь следующего сообщения!!!')
            if count_aut == 0:
                browser.get('https://www.cian.ru/authenticate/')
                time.sleep(2)
                check_form_class_telephone = browser.find_element_by_xpath('//*[@id="authentication-frontend"]/div/div/div/div[1]/div/button/span')
                time.sleep(2)
                count_aut +=1
                if check_form_class_telephone.text == 'Войти по email или id':
                    time.sleep(3)
                    form_class = browser.find_element_by_class_name('b7635b5199--input--2vxTR')
                    form_class.send_keys(tel)
                    time.sleep(2)
                    click_button = browser.find_element_by_class_name('b7635b5199--content--3t70w')
                    click_button.click()
                    bot.send_message(message.chat.id, '\nВведите код, пришедший на ваш номер телефона!'.format(message.from_user))
                    bot.register_next_step_handler(message, code_from_tel)

                elif check_form_class_telephone.text == 'Войти по телефону':
                    time.sleep(3)
                    button_css = browser.find_element_by_xpath('//*[@id="authentication-frontend"]/div/div/div/div[1]/div/button')
                    button_css.click()
                    time.sleep(3)
                    form_class = browser.find_element_by_class_name('b7635b5199--input--2vxTR')
                    form_class.send_keys(tel)
                    time.sleep(1)
                    click_button = browser.find_element_by_class_name('b7635b5199--content--3t70w')
                    click_button.click()
                    bot.send_message(message.chat.id, '\nВведите код, пришедший на ваш номер телефона!'.format(message.from_user))
                    bot.register_next_step_handler(message, code_from_tel)
            else:
                bot.send_message(message.chat.id, 'Вы успешно вошли в Циан.\nДля работы бота введите любое сообщение!'.format(message.from_user))
                bot.register_next_step_handler(message, parse_cian)
        elif message.text == '➕ Добавить пользователя':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('➕ Хочу еще добавить пользователя!')
            back = types.KeyboardButton('⬅️ Назад')
            markup.add(back) 
            bot.send_message(message.chat.id, 'Введите chat_id нового пользователя. \nДля его получения перешлите сообщение от пользователя, которого хотите добавить на этот адрес @get_id_bot\nВпоследствии введеите число из строки "Chat ID = "', reply_markup = markup)
            
            bot.register_next_step_handler(message, get_chat_id)
            
        elif message.text == '➕ Хочу еще добавить пользователя!':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            back = types.KeyboardButton('⬅️ Назад')
            markup.add(back) 
            bot.send_message(message.chat.id, 'Введите chat_id нового пользователя. \nДля его получения перешлите сообщение от пользователя, которого хотите добавить на этот адрес @get_id_bot\nВпоследствии введеите число из строки "Chat ID = "', reply_markup = markup)
            bot.register_next_step_handler(message, get_chat_id)
        
        elif message.text == '❌ Стоп':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            markup_admin = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('✅ Старт')
            item4 = types.KeyboardButton('➕ Добавить пользователя')
            markup.add(item1)
            markup_admin.add(item1, item4)
            if str(message.from_user.id) in admins_chat_id_adr: 
                bot.send_message(message.chat.id, '❌ Стоп\nБот окончил работу!', reply_markup = markup_admin)
            else:
                bot.send_message(message.chat.id, '❌ Стоп\nБот окончил работу!', reply_markup = markup)
            
            
            
        elif message.text == '⬅️ Назад':
            
            
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            markup_admin = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('✅ Старт')
            item4 = types.KeyboardButton('➕ Добавить пользователя')
            markup.add(item1)
            markup_admin.add(item1, item4)
            if str(message.from_user.id) in admins_chat_id_adr: 
                bot.send_message(message.chat.id, '⬅️ Назад', reply_markup = markup_admin)
            else:
                bot.send_message(message.chat.id, '⬅️ Назад', reply_markup = markup)


while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e) 
        time.sleep(15)
