from UpdateDB import get_expenses_list, get_members_balance
import itertools


def get_calculation(context):
    users_sum = get_expenses_list(context)
    users_balance = get_members_balance(users_sum)


def calculate(users_balance, MIN_DEBT=0.49, MAX_USERS_FOR_OPTIMAL=10):
    results = []

    # remove members with absolute balance close to zero
    for user in users_balance:
        if abs(users_balance[user] < MIN_DEBT):
            results[user] = 0
            users_balance.pop(user)

    # check if left only one user
    if len(users_balance == 1):
        # need to add code here
        pass

    # find combinations to remove from basic calculation to increase the speed of calculation
    if len(users_balance <= MAX_USERS_FOR_OPTIMAL):
        n = 2
        while n < len(users_balance) - 1:

            for size in range(len(users_balance) + 1):
                balances_list = list(map(dict, itertools.combinations(
                    users_balance.items(), size)))
                for subset in balances_list:
                    found = False
                    sum = 0
                    for user in subset:
                        sum += subset[user]
                    if abs(sum) <= MIN_DEBT:
                        values = basic_calculation(subset, MIN_DEBT=0.49)
                        #need to check what exactly returns from 'basic_calculation'
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
        sender_key = min(users_dict)
        receiver_key = max(users_dict)
        sender_should_send = abs(users_dict[sender_key])
        receiver_should_receive = abs(users_dict[receiver_key])


