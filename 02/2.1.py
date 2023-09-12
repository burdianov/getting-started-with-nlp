def print_warning(temperature):
    if temperature >= 45:
        print("Caution: Hot Water!")
    else:
        print("You may use water as usual")


print_warning(46)
