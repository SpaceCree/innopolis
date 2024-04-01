import sqlite3
import os

month = {"01": "Январь", "02": "Февраль", "03": "Март", "04": "Апрель", "05": "Май", "06": "Июль", "07": "Июнь",
             "08": "Август", "09": "Сентябрь", "10": "Октябрь", "11": "Ноябрь", "12": "Декабрь"}
class Database:
    def __init__(self, db_file):
        db_path = os.path.abspath(db_file)
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def close(self): #Закрываем соединение(проверка закрылось ли)
        self.connection.close()
        try:
            check_connect = self.connection.execute("SELECT * FROM weather_data LIMIT 1;")
            print("Соединено")
        except sqlite3.ProgrammingError as e:
            print("Соединение разорвано")

    def get_average_temperature_by_country(self,region):
        try:
            self.cursor.execute(f'SELECT AVG({region}_temperature) FROM weather_data')
            average_temperature = round(self.cursor.fetchone()[0], 2)
            ans = (f"Средняя температура в регионе {region}: {average_temperature}")
        except Exception as e:
            ans = (f"Для региона {region} нет данных о температуре или его не существует")
        return ans


    def get_lowAvg_annual_temperature(self,region):
        try:
            self.cursor.execute(f'SELECT AVG({region}_temperature), strftime("%Y", "utc_timestamp") FROM weather_data GROUP BY strftime("%Y", "utc_timestamp") ORDER BY AVG({region}_temperature) ASC LIMIT 1')
            year = self.cursor.fetchone()[1]
            ans = (f"Год с самой низкой среднегодовой температурой в {region}: {year}")
        except Exception as e:
            ans = (f"Для региона {region} нет данных о температуре или его не существует")
        return ans

    def get_coldMon(self,region):
        try:
            self.cursor.execute(
                f'SELECT AVG({region}_temperature), strftime("%m", "utc_timestamp") FROM weather_data GROUP BY strftime("%m", "utc_timestamp") ORDER BY AVG({region}_temperature) ASC LIMIT 1')
            mm = self.cursor.fetchall()[0][1]
            ans = (f"Самый холодный месяц в {region}: {month[mm]} {mm}")
        except Exception as e:
            ans = (f"Для региона {region} нет данных о температуре или его не существует")
        return ans



    def maximum_spread(self,region): #Два запроса чтобы найти максимум и минимум
        try:
            temp_max = []
            for i in region:
                self.cursor.execute(
                    f'SELECT AVG({i}_temperature), strftime("%Y", "utc_timestamp") FROM weather_data GROUP BY strftime("%Y", "utc_timestamp") ORDER BY AVG({i}_temperature) ASC LIMIT 1')
                first = self.cursor.fetchone()
                self.cursor.execute(
                    f'SELECT AVG({i}_temperature), strftime("%Y", "utc_timestamp") FROM weather_data GROUP BY strftime("%Y", "utc_timestamp") ORDER BY AVG({i}_temperature) DESC LIMIT 1')
                second = self.cursor.fetchone()
                print(i,first,second)
                for j in range(0, 1):
                    a = second[j] - first[j]
                    temp_max.append(a)
            b = temp_max.index(max(temp_max))
            ans = f'Регион: {region[b]}: {(max(temp_max))}'
            return ans
        except Exception as e:
            print(e)


    def get_max(self, region):
        try:
            self.cursor.execute(f'SELECT  MAX({region}_temperature) FROM weather_data')
            max = self.cursor.fetchone()[0]
            return max
        except Exception as e:
            print(e)

    def get_min(self, region):
        try:
            self.cursor.execute(f'SELECT  MIN({region}_temperature) FROM weather_data')
            min = self.cursor.fetchone()[0]
            return min
        except Exception as e:
            print(e)

    def couldMon(self,regions):
        try:
            temp_list = []
            for region in regions:
                self.cursor.execute(
                    f'SELECT AVG({region}_temperature), strftime("%m", "utc_timestamp") FROM weather_data GROUP BY strftime("%m", "utc_timestamp") ORDER BY AVG({region}_temperature) ASC LIMIT 1')
                mm = self.cursor.fetchall()
                temp_list.append(mm)
                a = temp_list.index(min(temp_list))
            ans = f"Регион с самым холодным месяцем: {regions[a]}  {month[min(temp_list)[0][1]]} {str(min(temp_list)[0][0])}"
            return ans
        except Exception as e:
            print(e)


def main():
    db = Database('weather_data.sqlite')
    regions = ['AT', 'BE', 'BG', 'CH', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GB', 'GR', 'HR', 'HU','IE', 'IT',
               'LT', 'LU', 'LV', 'NL', 'NO', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK']

    while True: #Основное меню
        try:
            question_number = int(input("Введите номер вопроса 1 - 6 (0 для выхода): "))
            if question_number == 0:
                db.close()
                break
            elif question_number == 1:
                print("1) Все регионы\n2) Выбрать регион\n3) Назад\n")
                choice = input()
                if choice == '1':
                    for i in regions:
                        ans1 = db.get_average_temperature_by_country(i)
                        print(ans1)
                elif choice == '2':
                    ans1 = db.get_average_temperature_by_country(input(f"{regions}\nНазвание региона:\t"))
                    print(ans1)
                elif choice == '3':
                    continue
                else:
                    print("Некорректный ввод")
            elif question_number == 2:
                print("1) Все регионы\n2) Выбрать регион\n3) Назад\n")
                choice2 = input()
                if choice2 == '1':
                    for i in regions:
                        ans2 = db.get_lowAvg_annual_temperature(i)
                        print(ans2)
                elif choice2 == '2':
                    ans2 = db.get_lowAvg_annual_temperature(input(f"{regions}\nНазвание региона:\t"))
                    print(ans2)
                elif choice == '3':
                    continue
                else:
                    print("Некорректный ввод")
            elif question_number == 3:
                print("1) Все регионы\n2) Выбрать регион\n3) Назад\n")
                choice3 = input()
                if choice3 == '1':
                    for i in regions:
                        ans3 = db.get_coldMon(i)
                        print(ans3)
                elif choice3 == '2':
                    ans3 = db.get_coldMon(input(f"{regions}\nНазвание региона:\t"))
                    print(ans3)
                elif choice3 == '3':
                    continue
                else:
                    print("Некорректный ввод")
            elif question_number == 4:
                ans4 = db.couldMon(regions)
                print(ans4)
            elif question_number == 5:
                ans5 = db.maximum_spread(regions)
                print(ans5)
            elif question_number == 6:
                print("1) Все регионы\n2) Выбрать регион\n3) Назад\n")
                choice6 = input()
                if choice6 == '1':
                    for i in regions:
                        max = db.get_max(i)
                        min = db.get_min(i)
                        print(f"Минимальная: {min}, Максимальная: {max}")
                elif choice6 == '2':
                    reg = input(f"{regions}\nНазвание региона:\t")
                    max = db.get_max(reg)
                    min = db.get_min(reg)
                    print(f"Минимальная: {round(min,2)}, Максимальная: {round(max,2)}")
                elif choice == '3':
                    continue
                else:
                    print("Некорректный ввод")
            else:
                print("Некорректное число")
        except ValueError:
            print("Некорректный ввод. Введите целое число.")

if __name__ == "__main__":
    main()