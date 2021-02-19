#
# Model
#

record = list()

def model():
    return "model"

# C R U D

def create(name):
    global record
    record = record + [name]
    return 0

def read():
    return record

def update(a, b):
    global record

    # replace all a to b
    #
    # record.replace(a, b) ???
    #
    record = [b if x==a else x for x in record]
    return 0

def delete(name):
    global record

    # delete all a from list
    while name in record: record.remove(name)

    return 0