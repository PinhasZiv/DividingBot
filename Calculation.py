from UpdateDB import get_expenses_list, get_members_balance
import itertools


def get_calculation(context):
    users_sum = get_expenses_list(context)
    users_balance = get_members_balance(users_sum)
    return calculate(users_balance)


def calculate(users_balance, MIN_DEBT=0.49, MAX_USERS_FOR_OPTIMAL=10):
    results = []
    # remove members with absolute balance close to zero
    remove_users = [user for user in users_balance if abs(users_balance[user]) < MIN_DEBT]
    for user in remove_users:
        users_balance.pop(user)
    print('users_balance:', users_balance)
    # check if left only one user
    if len(users_balance) == 1:
        return results

    # find combinations to remove from basic calculation to increase the speed of calculation
    if len(users_balance) <= MAX_USERS_FOR_OPTIMAL:
        n = 2
        while n < len(users_balance) - 1:
            for size in range(len(users_balance) + 1):
                balances_list = list(map(dict, itertools.combinations(
                    users_balance.items(), size)))
                for subset in balances_list:
                    found = False
                    sum_balances = 0
                    for user in subset:
                        sum_balances += subset[user]
                    if abs(sum_balances) <= MIN_DEBT:
                        values = basic_calculation(subset, MIN_DEBT=0.49)
                        results += values
                        for user in subset:
                            users_balance.pop(user)
                        found = True
                    if found:
                        break
                    n += 1
            values = basic_calculation(users_balance, MIN_DEBT=0.49)
            # need to check what exactly returns from 'basic_calculation'
            results += values
            # maybe needs to sort the debts according to who should pay
            return results


def basic_calculation(users_dict, MIN_DEBT=0.49):
    debts = []
    resolved_members_num = 0
    while resolved_members_num != len(users_dict):
        sender_key = min(users_dict, key=users_dict.get)
        receiver_key = max(users_dict, key=users_dict.get)
        sender_should_send = abs(users_dict[sender_key])
        receiver_should_receive = abs(users_dict[receiver_key])
        amount = None
        if sender_should_send > receiver_should_receive:
            amount = receiver_should_receive
        else:
            amount = sender_should_send
        users_dict[sender_key] += amount
        users_dict[receiver_key] -= amount

        values = dict()
        values['from'] = sender_key
        values['to'] = receiver_key
        values['amount'] = amount
        debts.append(values)
        print('values:', values)

        if abs(sender_should_send) <= MIN_DEBT:
            resolved_members_num += 1
        if abs(receiver_should_receive) <= MIN_DEBT:
            resolved_members_num += 1

    print('debts:', debts)
    # remove_debts = [debt for debt in debts if debt['amount'] <= MIN_DEBT]
    # for debt in remove_debts:
    #     debts.pop(debt)
    debts = list(filter(lambda debt: debt['amount'] > MIN_DEBT, debts))

    print('debts:', debts)
    return debts


