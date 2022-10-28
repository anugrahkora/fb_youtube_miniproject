import re

#function to search CVE
def searchCVE(regular_expression, content_text):
    result = []
    result = re.findall(regular_expression, content_text, re.IGNORECASE)
    return result


#function to search CVE
def searchDomain(regular_expression, content_text):
    result = []
    result = re.findall(regular_expression, content_text, re.IGNORECASE)
    return result
