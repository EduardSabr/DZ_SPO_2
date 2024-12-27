import telebot
import random
import logging
import math

from telebot import types

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("tgbot.log")

bot = telebot.TeleBot("8149032596:AAF-RPvPHAVXqHkaEMSP_T5c0QdX1iz9K9U")


# Функция для генерации математического примера
def generate_math_problem(difficulty):
    if difficulty == 'easy':
        a, b = random.randint(1, 10), random.randint(1, 10)
        return f"{a} + {b}", a + b
    elif difficulty == 'normal':
        a = random.randint(10, 50)
        b = random.randint(1, 20)
        operator = random.choice(['-', '*', '/'])
        if operator == '-':
            return f"{a} - {b}", a - b
        elif operator == '*':
            return f"{a} * {b}", a * b
        elif operator == '/':
            # Делаем деление с десятичными числами
            while b == 0:
                b = random.randint(1, 20)
            return f"{a} / {b}", round(a / b, 2)
    elif difficulty == 'hard':
        # Линейное уравнение: ax + b = c
        a = random.randint(1, 10)
        b = random.randint(5, 20)
        c = random.randint(20, 100)
        # Решаем уравнение для x: ax = c - b
        x = (c - b) / a
        return f"{a}x + {b} = {c}", round(x, 2)

    elif difficulty == 'very_hard':
        problem_type = random.choice(['logarithmic', 'discriminant', 'theorem'])

        # Задачи с логарифмами
        if problem_type == 'logarithmic':
            a = random.randint(2, 10)
            b = random.randint(1, 50)
            c = random.randint(1, 10)
            # Логарифмическое уравнение вида: log_a(x) = b
            # То есть a^b = x
            x = a ** b
            return f"log_{a}(x) = {b}", x

        # Задачи с дискриминантом
        elif problem_type == 'discriminant':
            a = random.randint(1, 10)
            b = random.randint(-20, 20)
            c = random.randint(1, 20)
            # Квадратное уравнение ax^2 + bx + c = 0
            discriminant = b ** 2 - 4 * a * c
            if discriminant >= 0:
                # Корни квадратного уравнения
                x1 = (-b + math.sqrt(discriminant)) / (2 * a)
                x2 = (-b - math.sqrt(discriminant)) / (2 * a)
                return f"{a}x^2 + {b}x + {c} = 0", (round(x1, 2), round(x2, 2))
            else:
                return f"{a}x^2 + {b}x + {c} = 0", "Нет решений"

        # Задачи по теореме Пифагора
        elif problem_type == 'theorem':
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            # Задача на нахождение гипотенузы: a^2 + b^2 = c^2
            c = math.sqrt(a ** 2 + b ** 2)
            return f"Найдите гипотенузу треугольника с катетами {a} и {b}", round(c, 2)


# Хранение текущих вопросов и ответов
current_problems = {}


@bot.message_handler(commands=['start'])
def welcome(message):
    logger.info(f"Пользователь {message.from_user.first_name} начал взаимодействие с ботом.")

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("📘 Легкий пример")
    item2 = types.KeyboardButton("📗 Средний пример")
    item3 = types.KeyboardButton("📙 Сложный пример")
    item4 = types.KeyboardButton("📚 Очень сложный пример")

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}! Выберите уровень сложности для математического примера.".format(
                         message.from_user),
                     parse_mode='html', reply_markup=markup)
    logger.info("Выведено приветственное сообщение.")


@bot.message_handler(content_types=['text'])
def chat(message):
    if message.chat.type == 'private':
        logger.info(f"Получено сообщение от пользователя {message.from_user.first_name}: {message.text}")

        if message.text == '📘 Легкий пример':
            problem, answer = generate_math_problem('easy')
            current_problems[message.chat.id] = answer
            bot.send_message(message.chat.id, f"Решите: {problem}")
        elif message.text == '📗 Средний пример':
            problem, answer = generate_math_problem('normal')
            current_problems[message.chat.id] = answer
            bot.send_message(message.chat.id, f"Решите: {problem}")
        elif message.text == '📙 Сложный пример':
            problem, answer = generate_math_problem('hard')
            current_problems[message.chat.id] = answer
            bot.send_message(message.chat.id, f"Решите: {problem}")
        elif message.text == '📚 Очень сложный пример':
            problem, answer = generate_math_problem('very_hard')
            current_problems[message.chat.id] = answer
            bot.send_message(message.chat.id, f"Решите: {problem}")
        elif message.text.replace('.', '', 1).isdigit():  # Проверка на десятичные числа
            user_answer = float(message.text)
            correct_answer = current_problems.get(message.chat.id)
            if correct_answer is not None:
                if round(float(user_answer), 2) == round(float(correct_answer), 2):
                    bot.send_message(message.chat.id, "✅ Правильно! Молодец!")
                else:
                    bot.send_message(message.chat.id, f"❌ Неправильно. Правильный ответ: {correct_answer}")
                del current_problems[message.chat.id]
            else:
                bot.send_message(message.chat.id,
                                 "ℹ️ У вас нет активного задания. Выберите уровень сложности, чтобы начать.")
        else:
            bot.send_message(message.chat.id, "Я не понял ваш запрос. Попробуйте снова.")


if __name__ == "__main__":
    logger.info("Бот запущен.")
    bot.polling(none_stop=True)