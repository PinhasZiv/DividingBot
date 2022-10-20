import itertools
#
# mySql_select_query = """SELECT UserID, Amount FROM distributions WHERE UserID = 190866836"""
# mySql_select_sum_query = """SELECT SUM(Amount) AS sum FROM distributions WHERE UserID = {user: .2f}"""
# data_to_insert = 12345
# s = mySql_select_sum_query.format(user = data_to_insert)
# print(s)
# mySql_insert_query = """INSERT INTO distributions (UserID, ChatID, Amount, Reason, MessageID, Timestamp)
#                           VALUES
#                           (%s, %s, %s, %s, %s, %s)"""
# data_to_insert = ('111', '222', '333', '444', '555', '666')
#
# print(mySql_insert_query.format(data_to_insert))
#
# txt = "For only {price:.2f} dollars!"
# print(txt.format(price = 49))

stuff = {'a': 80, 'b': -2000, 'c': -400}
# for size in range(len(stuff) + 1):
#     balances_list = list(map(dict, itertools.combinations(
#         stuff.items(), size)))
#     for subset in balances_list:
#         found = False
#         sum = 0
#         for user in subset:
#             sum += subset[user]
#         print('subset:', subset, 'sum:', sum)

a = dict(sorted(stuff.items(), key=lambda item: item[1]))
for key, value in stuff.items():
    print('key:', key, ', value:', value)
print('stuff', stuff)
# print(max(list(stuff.values())))
fin_max = max(stuff, key=stuff.get)
print(fin_max)
fin_min = min(stuff, key=stuff.get)
print(fin_min)
# print(max(stuff))
# print(min(stuff))
# print(stuff.get(max()))

# my_new_dict = {"q": 18, "z": 10, "o": 13}
#
# fin_max = max(my_new_dict, key=my_new_dict.get)
# print("Maximum value:",fin_max)
a = dict
print(a)
