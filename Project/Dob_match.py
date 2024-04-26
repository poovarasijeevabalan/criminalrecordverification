def dob_match(dob1, dob2):

    if "(" in dob2:
        dob2 = dob2.split("(")[0].strip()
    if '/' in dob1 and '/' in dob2:
        separator = '/'
    elif '-' in dob1 and '-' in dob2:
        separator = '-'
    else:
        return "Invalid date format"

    m1, d1, y1 = dob1.split(separator)
    m2, d2, y2 = dob2.split(separator)

    if dob1 == dob2:
        return "match"
  
    if d1 == d2 and m1 == m2 and abs(int(y1) - int(y2)) == 1:
        return 'partial'
  
    if m1 == m2 and y1 == y2 and d1 != d2:
        return 'partial'
 
    if d1 == d2 and y1 == y2 and abs(int(m1) - int(m2)) == 1:
        return 'partial'
  
    else:
        return "notmatch"

if __name__ == "__main__":
    dob1 = "11/27/1970"
    dob2 = "11/27/1970"
    print(dob_match(dob1, dob2))

    dob1 = "10/27/1969"
    dob2 = "10/26/1969"
    print(dob_match(dob1, dob2))

    dob1 = "11/27/1969"
    dob2 = "11/27/1970"
    print(dob_match(dob1, dob2))

    dob1 = "10/27/1969"
    dob2 = "10/26/1969"
    print(dob_match(dob1, dob2))

    dob1 = "10/27/1969"
    dob2 = "8/15/1968"
    print(dob_match(dob1, dob2))

    dob1 = "10-27-1969 00:00:00"
    dob2 = "8-15-1968 00:00:00"
    print(dob_match(dob1, dob2))
