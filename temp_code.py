def name_dict(i):
    if type(i) is int:
        if i < 0:
            return(f'm({abs(i)})')
        else:
            return(f'p({abs(i)})')
    else:
        raise TypeError
