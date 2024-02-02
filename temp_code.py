def name_dict(i, method=None):
    if type(i) is not int:
        if method is not None:
            method = method + '_'
        if i < 0:
            return(method + f'm({abs(i)})')
        else:
            return(method + f'p({abs(i)})')
    else:
        raise TypeError
