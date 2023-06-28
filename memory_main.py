from memocard_Layout import*
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer #new
from random import shuffle 
from memo_data import* #відредаговано
from memo_edit_layout import* #new
from memo_main_layout import * #new

card_width, card_height = 600, 500#додаємо розміри вікна картки
main_width, main_height = 1000, 450 # додаємо розміри головного вікна
time_unit = 1000    # стільки триває одна одиниця часу з тих, що потрібно заснути
                    # (в робочій версії програми збільшить у 60 разів!)

text_wrong = 'Невірно'#створюємо змінну з текстом для відображення у впиадку невірної відповіді
text_correct = 'Вірно'#створюємо змінну з текстом для відображення у випадку вірної відповіді

questions_listmodel = QuestionListModel() # створюємо список запитань
win_card = QWidget()#створюємо вікно картки
win_main = QWidget()#створюємо вікно редагування запитань
frm_card = 0 # тут буде зв'язуватися запитання з формою тесту

frm_edit = QuestionEdit(0, txt_Question, txt_Answer, txt_Wrong1, txt_Wrong2, txt_Wrong3)#модель редагування запитань
timer = QTimer()#створюємо таймер

radio_list = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]#створюємо список radio_list для відповідей

def click_OK():#функція для перевірки натискання тої чи іншої кнопки у тесті
    ''' перевіряє запитання або завантажує нове запитання '''
    if btn_OK.text() != 'Наступне питання':#якщо не натиснули кнопку "Наступне питання", то значить натиснули кнопку "Відповісти", що значить нам потрібно перевірити відповідь
        frm_card.check()#перевіряємо відповідь
        show_result()#показуємо результат
    else:
        # напис на кнопці 'Наступне питання', тому створюємо наступне випадкове запитання:
        show_random()

#створюємо функцію для тестових данних
def testList():
    frm = Question('Яблуко', 'apple', 'application', 'pinapple', 'apply')#створюємо запитання та чотири відповіді
    questions_listmodel.form_list.append(frm)#додаємо до списку запитань frm
    frm = Question('Дім', 'house', 'horse', 'hurry', 'hour')
    questions_listmodel.form_list.append(frm)
    frm = Question('Миша', 'mouse', 'mouth', 'muse', 'museum')
    questions_listmodel.form_list.append(frm)
    frm = Question('Число', 'number', 'digit', 'amount', 'summary')
    questions_listmodel.form_list.append(frm)

#функція для вигляду картки
def set_card():
    win_card.resize(card_width, card_height)#встановлюємо ширину та висоту длянашого вікна
    win_card.move(300, 300)#переміщаємо вікно вкординати 300х300
    win_card.setWindowTitle('Memory Card')#встановлюємо назву для додатка, яке буде відображатися зверху вікна
    win_card.setLayout(layout_card)#встановлюємо межу картки

#функція, що задає вигляд головного вікна
def set_main():
    win_main.resize(main_width, main_height)#надаємо нашому вікну розмірів
    win_main.move(100, 100)#переміщаємо вікнов в кординати 100 по х та у на екрані
    win_main.setWindowTitle("Список запитань")#встановлює назвудля вікна
    win_main.setLayout(layout_main)#встановлюємо розмежування для вікна взяте з файлу memo_main_layout
    
#функція для відображення випадкового питання
def show_random():
    global frm_card #global вдастивості вікна, а frm_card поточна форма з данними картки
#отримуємо випадкові данні і віправляємо їх варіанти відповідей по радіокнопкам
    frm_card = random_AnswerCheck(questions_listmodel, lb_Question, radio_list, lb_Correct, lb_Result)
#функція 
# буде запущена через функцію click_OK, тобто коли функція click_OK запискатиметься, то ця вже буде створена
    frm_card.show()#завантажуємо потрібні данні та відповідні віджети для функції
    show_question()#відображаємо на панелі питань

#повернення звікна тесту на головне/редагування вікно
def back_to_menu():
    win_card.hide()
    win_main.showNormal()

#на почтаку тесту функція прив'язується до випадкового питання і відображається
def strat_test():
    show_random()
    win_card.show()
    win_main.showMinimized()


def show_card():
    win_card.show()
    timer.stop()


def add_form(): #створюємо функцію для додавання питання до тесту
    questions_listmodel.insertRows()
    last = questions_listmodel.rowCount(0) - 1#останній елемент списку
    index = questions_listmodel.index(last)
    list_Question.setCurrentIndex(index)
    edit_question(index)
    txt_Question.setFocus(Qt.TabFocusReason)

def edit_question(index): #створюємо функцію для редагування доданих питань
    if index.isValid():
        i = index.row()
        frm = questions_listmodel.form_list[i]
        frm_edit.change(frm)
        frm_edit.show()

def del_form(): #видаляє запитання за індексом
    questions_listmodel.removeRows(list_Question.currentIndex().row())
    edit_question(list_Question.currentIndex())

def sleep_card():#фуе
    win_card.hide()#
    timer.setInterval(time_unit * box_Minuets.value())#
    timer.start()#

#втсановлення потрібних зв'язків

def connects():
    list_Question.setModel(questions_listmodel)#зв'зуємо список на екрані зі списком запитань
    btn_start.clicked.connect(strat_test)#нажимаємо кнопку почати тест
    btn_OK.clicked.connect(click_OK)#нажимаємо кнопку "ОК" у формі теста
    btn_Menu.clicked.connect(back_to_menu)#нажимаємо кнопку "Меню"для повернення із тесту у вікно питань
    list_Question.clicked.connect(edit_question)
    btn_add.clicked.connect(add_form)
    btn_delete.clicked.connect(del_form)
    btn_Sleep.clicked.connect(sleep_card)
    timer.timeout.connect(show_card)

#запускаємо всі потрібні функції
testList()
set_card()
set_main()
connects()

#було win_card.show()
win_main.show()#стало, тому що нам потрібно відкривати тепер не тест відразу, а вікно редагування перше
app.exec_()#утримує вікно відкритим доки не натиснуто хрестик