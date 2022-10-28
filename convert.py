def listToString(s):
       
    # initialize an empty string
    str1 = "\n"
   
    # return string 
    return (str1.join(s))


def convertTime(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d:%02d" % (hour, minutes, seconds)
     



