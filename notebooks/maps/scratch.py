items = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4
}


message = '{a} {b} {c} {d}'.format(**items)


print(message)
