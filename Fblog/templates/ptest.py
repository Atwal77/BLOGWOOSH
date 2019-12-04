def decorator(ofunc):
    def wrap(*args,**kwargs):
        print('wrap')
        return ofunc(*args,**kwargs)
    return wrap

@decorator
def display():
    print('first')

print(display())