BMI = lambda w,h: print(str(w/(h/100)**2)+"(過輕)") \
    if w/(h/100)**2 <= 18 else print(str((w/(h/100)**2))+"(過重)") \
    if w/(h/100)**2 >  23 else print(str((w/(h/100)**2))+"(正常)")
BMI(60,170)
