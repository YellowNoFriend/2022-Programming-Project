def integer_input_validation(input_message, default_value, lower, upper):
    '''
    Prompt an integer input with input_message shown to user, 
    and require the input to be bounded between lower and upper.
    If the requirements are satisfied, return the integer user inputs. 
    Otherwise, return default_value.
    '''
    test_input = input(f'Please enter {input_message}. \
                       This is an integer between {lower} and {upper} inclusive.')
    try:
        test_int = int(test_input)
        if test_int <= upper and test_int >= lower:
            print(f'{input_message} set as the value {test_int}')
            return test_int
        else:
            print(f'Out of bounds: using the default value of {default_value}.')
            return default_value
    except:
        print(f'Type Error: using the default value of {default_value}.')
        return default_value
def float_input_validation(input_message, default_value, lower, upper):
    '''
    Prompt an float input with input_message shown to user, 
    and require the input to be bounded between lower and upper.
    If the requirements are satisfied, return the integer user inputs. 
    Otherwise, return default_value.
    '''
    test_input = input(f'Please enter {input_message}. \
                       This is a real number (float) between {lower} and {upper} inclusive.')
    try:
        # Try to Convert the message to a float
        test_int = float(test_input)
        if test_int <= upper and test_int >= lower:
            print(f'{input_message} set as the value {test_int}')
            return test_int
        else:
            print(f'Out of bounds: using the default value of {default_value}.')
            return default_value
    except:
        print(f'Type Error: using the default value of {default_value}.')
        return default_value