

class Medical_condition:
    medical_class = 'Tough_stuff'
    def __init__(self, name, researcher, main_symptom, treatment):
        self.__name = name
        self.researcher = researcher
        self.main_symptom = main_symptom
        self.treatment = treatment

    # def get_torture(self):
    #     return f'You will suffer from {self.main_symptom}'

    def death(self):
        return 'Last_memories'


    def get_name(self):
        return f'You will suffer from {self.__name}'

    def set_name(self, new_name):
        return new_name

Medical_condition1 = Medical_condition('Plague', 'Samoylovich', 'bubos', 'antibiotics')
print(Medical_condition1._Medical_condition__name, Medical_condition1.researcher, Medical_condition1.main_symptom, Medical_condition1.treatment)

Medical_condition2 = Medical_condition('Novichok_Poisoning', 'Jelyeznyakov', 'convulsions', 'atropine')
print(Medical_condition2._Medical_condition__name, Medical_condition2.researcher, Medical_condition2.main_symptom, Medical_condition2.treatment)

Medical_condition3 = Medical_condition('Delirium Manihaeismum', 'Dide', 'Antagonistic_Ideas', 'Antipsychotocs')
print(Medical_condition3._Medical_condition__name, Medical_condition3.researcher, Medical_condition3.main_symptom, Medical_condition3.treatment)


print(Medical_condition3.__dict__)
print(Medical_condition3.set_name('Psychosis'))
print(Medical_condition3.get_name())
print(Medical_condition3._Medical_condition__name)





def decor(func):
    def shitty_f(x):
        if x == 666 or x == 13:
            return('Hail, Baphomet')
        return func(x)
    return shitty_f

@decor
def cause(x):
    return('You are blessed')

x = int(input('Enter the number'))
print(cause(x))
