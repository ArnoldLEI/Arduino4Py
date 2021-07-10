id = "A223456789"
sex = id[1]
print(sex)

sex_info = {
    1: lambda : print("Male"),
    2: lambda : print("Famle")
}

sex_error = lambda : print("Error")
sex_info.get(int(sex),sex_error)()

salary_weight = {
    1: lambda salary: print("男", salary),
    2: lambda salary: print("女", salary * 1.2)
}
sex_error = lambda : print("性別錯誤")
salary_weight.get(int(sex), sex_error)(30000)