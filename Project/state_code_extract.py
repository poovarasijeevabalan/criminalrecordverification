import re

def state_code_extr(address):
    state_code_pattern = r',\s*([A-Z]{2})\b'  
    state_code_matches = re.findall(state_code_pattern, address)
    if state_code_matches:
        return state_code_matches[0] 
    else:
        return None

if __name__ == "__main__":
    address = """1320 SCOTT ST UNIT 2303
    HOUSTON, TX 77003
    HARRIS
    RESIDENCE"""
    print(state_code_extr(address))

    address = """
    INS CUSTODY
    INCARCERATED, FL 00000
    UNKNOWN
    RESIDENTIAL
    """

    print(state_code_extr(address))

    address = """
     2116 GREEN ST
    SAGINAW, Michigan 48638
    """
    print(state_code_extr(address))

    address = """
      5399 BRASS HILLS CT
      LAS VEGAS, NV 89122
      CLARK
      RESIDENCE

      181 N WATER ST
      HENDERSON, NV 89015
      CLARK
      EMPLOYMENT
    """
    print(state_code_extr(address)) 

# import re

# def state_code_extr(addresses):
#     state_code_pattern = r'\b[A-Z]{2}\b|\b[A-Z]{2}\s\d{5}\b'  # Matches two uppercase letters OR two uppercase letters followed by a space and 5 digits
#     state_codes = []
#     addresses_list = addresses.split('\n\n')  # Split addresses by double newline
#     for address in addresses_list:
#         state_code_match = re.search(state_code_pattern, address)
#         if state_code_match:
#             state_codes.append(state_code_match.group())
#     return state_codes

# if __name__ == "__main__":
#     address1 = """
#     5399 BRASS HILLS CT
#     LAS VEGAS, NV 89122
#     CLARK
#     RESIDENCE

#     181 N WATER ST
#     HENDERSON, NV 89015
#     CLARK
#     EMPLOYMENT
#     """
#     print(state_code_extr(address1))  # Output: ['NV']

#     address2 = """1320 SCOTT ST UNIT 2303
#     HOUSTON, TX 77003
#     HARRIS 
#     RESIDENCE"""
#     print(state_code_extr(address2))  # Output: ['TX']
