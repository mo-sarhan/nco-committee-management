import re
def convert_to_arabic(value):
    arabic_numbers = '٠١٢٣٤٥٦٧٨٩'
    english_numbers = '0123456789'
    value = str(value).translate(str.maketrans(english_numbers,arabic_numbers))
    return value


def reverse_date(match):
    date_str = match.group(0)
    spliter = '-' if '-' in date_str else '/'
    date_split = date_str.split(spliter)
    return spliter.join(date_split[::-1])

def convert_date(text):
    regular_exp = r'\d{1,2}[-/]\d{1,2}[-/]\d{1,4}'
    date_after = re.sub(regular_exp,reverse_date,text)
    return convert_to_arabic(date_after)



