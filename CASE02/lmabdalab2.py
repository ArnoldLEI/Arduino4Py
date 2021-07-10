id = "A123456789"
sex  = id[1]
area = id[2]
print(sex)
print(area)

sex_info = {
    1: lambda : print("Male"),
    2: lambda : print("Famle")

}
area_info = {
    0: lambda : print("Taiwan"),
    1: lambda : print("Taiwan"),
    2: lambda : print("Taiwan"),
    3: lambda : print("Taiwan"),
    4: lambda : print("Taiwan"),
    5: lambda : print("Taiwan"),
    6: lambda : print("外國"),
    7: lambda : print("NoHome"),
    8: lambda : print("HK"),
    9: lambda : print("China")
}

sex_error = lambda : print("Error")
print(area_info.get(int(area))(), sex_info.get(int(sex))())


