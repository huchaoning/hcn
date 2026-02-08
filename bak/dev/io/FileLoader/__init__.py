from .FileLoader import FileLoader

def read(input_):
    try:
        data = FileLoader(input_)._any()
    except (NotImplementedError, TypeError, FileNotFoundError): 
        return input_

    return data




