from pprint import pprint
import re
import csv

with open("phonebook_raw.csv") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

# TODO 1: выполните пункты 1-3 ДЗ
# форматирование телефонов:
for id_person, person in enumerate(contacts_list):
  if id_person > 0:
    for id_string, string in enumerate(person):
      if id_string == 5:
        pattern_find_phone = r"([\+7|8]+)\D?\D?([\d]{3})\D?\D?([\d]{3})\D?([\d]{2})\D?([\d]{2})"
        pattern_new_format_phone = r"+7(\2)\3-\4-\5"
        contacts_list[id_person][5] = re.sub(pattern_find_phone, pattern_new_format_phone, string)
        if re.search("доб", string):
          pattern_ad_find = r"\D*(доб)\D*(\d+)\D?"
          pattern_new_format_addition = r" доб.\2"
          contacts_list[id_person][5] = re.sub(pattern_ad_find, pattern_new_format_addition, contacts_list[id_person][5])

# приведение к формату Ф, И, О
for id_person, person in enumerate(contacts_list):
  if id_person > 0:
    for id_string, string in enumerate(person):
      pattern = "(\S+)\s?(\S+)\s?(\S+)?"
      if id_string == 0 and re.search(" ", string):
        reasult = re.search(pattern, string)
        contacts_list[id_person][id_string] = reasult.group(1)
        contacts_list[id_person][id_string + 1] = reasult.group(2)
        contacts_list[id_person][id_string + 2] = reasult.group(3)
      if id_string == 1 and re.search(" ", string):
        reasult = re.search(pattern, string)
        contacts_list[id_person][id_string] = reasult.group(1)
        contacts_list[id_person][id_string + 1] = reasult.group(2)

# объединение данных у повторяющихся персон
my_list = []
result = contacts_list[0]
cursor = 0
for id_person, person in enumerate(contacts_list):
  if id_person > 0:
    ident_1 = [person[0], person[1]]
    result = person
    cursor = id_person + 1
    for id_person2, person2 in enumerate(contacts_list[cursor:]):
      ident_2 = [person2[0], person2[1]]
      if ident_1 == ident_2:
        result = []
        for id, position in enumerate(person):
          if position != '':
            result.append(position)
          else:
            result.append(person2[id])
        contacts_list[id_person+id_person2+1] = result
  my_list.append(result)

# удаление повторяющихся записей
final_list=[]
for id_person, person in enumerate(my_list):
  duplicat = 0
  ident_1 = [person[0], person[1]]
  cursor = id_person + 1
  for personx in my_list[cursor:]:
    ident_2 = [personx[0], personx[1]]
    if ident_1 == ident_2:
      duplicat = 1
  if duplicat == 0:
    final_list.append(person)
final_list.sort()


# TODO 2: сохраните получившиеся данные в другой файл

with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(final_list)
