import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r'C:\Users\Vytas\Desktop\DataSets\students_performance.csv', sep=';')

#                                     -Ar 'preparation course' studentams padėjo gauti geresnius ivertinimus?

#---------------------------------------------DUOMENU FILTAVIMAS-------------------------------------------------

df.rename(columns={'test preparation course': 'prep course'}, inplace=True)     #pakeiciu pavadinima stulpelio
df = df.loc[:, ~df.columns.isin(['gender', 'parental level of education',
                                 'race/ethnicity', 'lunch'])]        #ismetu stulpelius, kuriu man nereikia

df['prep course'] = df['prep course'].replace(['none'], 0) # 0 - False (nebaigta)
df['prep course'] = df['prep course'].replace(['completed'], 1) # 1 - True (pabaigta)

#                                     ---VISI ISLAIKE lygu/daugiau 90 SU ARBA BE 'prep course'---
def islaike_gerai(prep = 1):
    islaike_gerai = len(df[(df['math score'] >= 90) & (df['reading score'] >= 90) & (
                df['writing score'] >= 90) & (df['prep course'] == prep)])
    return islaike_gerai

islaike_gerai()

is_viso_90_ir_daugiau = islaike_gerai() + islaike_gerai(0)

#                                     ---NEISLAIKE (maziau nei 40) SU ARBA BE 'prep course'---

def neislaike(prep = 1):
    neislaike = len(df[(df['math score'] < 40) & (df['reading score'] < 40) & (
                df['writing score'] < 40) & (df['prep course'] == prep)])
    return neislaike

neislaike()             # 1 - su 'prep course, 0 - be
                        #Su prep course visi islaike

#                                     ---VISI ISLAIKE SU ARBA BE 'prep course'---

def islaike_su_be_prep_course(prep = 1):
    islaike_su_arba_be_prep = df[(df['math score'] >= 40) & (df['reading score'] >= 40) & (
                df['writing score'] >= 40) & (df['prep course'] == prep)]
    return islaike_su_arba_be_prep

islaike_su_be_prep_course()                 # 1 - su 'prep course, 0 - be

#######################################################################################################################
#######################################################################################################################

#                                     ---VISU IŠLAIKIUSIU be 'prep course' BENDRAS VIDURKIS---

df_avg = islaike_su_be_prep_course(0)
def average_of_subjects_be_prep():
    average_of_subjects = ((sum(df_avg['math score'])+sum(df_avg['reading score'])+sum(df_avg['writing score']))/len(df_avg))/3
    return round(average_of_subjects, 2)

average_of_subjects_be_prep()

#                                     ---VISU IŠLAIKIUSIU su 'prep course' BENDRAS VIDURKIS---

df_avg2 = islaike_su_be_prep_course(1)
def average_of_subjects_su_prep():
    average_of_subjects = ((sum(df_avg2['math score'])+sum(df_avg2['reading score'])+sum(df_avg2['writing score']))/len(df_avg2))/3
    return round(average_of_subjects, 2)

average_of_subjects_su_prep()

#######################################################################################################################
#                                    ---BENDRAS STUDENTU VIDURKIS---
# print(f'Bendras studentu vidurkis su "preparation test": {average_of_subjects_su_prep()}\n'
#       f'Bendras studentu vidurkis be "preparation test": {average_of_subjects_be_prep()}')
#######################################################################################################################
#                                    ---NEISLAIKE BENT 1 EGZAMINO---

neislaike_1_arba_2 = len(df) - (len(islaike_su_be_prep_course(1)) + len(islaike_su_be_prep_course(0)) + neislaike(0))

#-----------------------------------------------Grafikai---------------------------------------------------
        # 1 GRAFIKAS
# reiksmes = np.array([len(islaike_su_be_prep_course(1)), len(islaike_su_be_prep_course(0)), neislaike(0), neislaike_1_arba_2])
# pavadinimai = (['Turėjo "Preparation course"', 'Neturėjo "Preparation course"', 'Neišlaikė nei vieno egzamino', 'Neišlaikė bent vieno egzamino'])
# fig, ax = plt.subplots(figsize=(8, 5))
# fig.patch.set_facecolor('#0C0B0B')  #backgroundas
# explode = [0, 0, 0.2, 0]
# patches, texts, pcts = ax.pie(reiksmes, labels=pavadinimai, autopct='%.1f%%', pctdistance=0.65, explode = explode,
#          startangle=-30, colors=['#224880', '#326BBF', 'red', 'grey'], textprops={'color':'#326BBF'}, shadow=True)
# plt.setp(pcts, color='#FFFAE4')
# ax.set_title('Studentų (išlaikiusių visus 3 egzaminus) skaičiai', fontsize=15, color = '#8EBCFF')
# plt.legend(reiksmes,loc=[-0.3, 0.7], fancybox=True, framealpha=0.3, prop={'size': 12})
# plt.tight_layout()
#
# plt.show()
#-----------------------------------------BAR chartas Kiek išlaikė su/be "Preparation course----------------------------
#         #2 GRAFIKAS
# labels = ['Su \n"Preparation course"', 'Be \n"Preparation course"', 'Bendras sk.']
# reiksmes = [islaike_gerai(), islaike_gerai(0), is_viso_90_ir_daugiau]
# plt.figure(facecolor = '#0C0B0B', figsize=(8, 5)) #backgroundas aplinkui
# ax = plt.axes()
# ax.set_facecolor("#0C0B0B") #vidinis backgroundas
# barplot = plt.bar(x = labels, height = reiksmes)
# plt.bar_label(barplot, labels=reiksmes, label_type = 'edge', padding = 2, color = '#8EBCFF')
# plt.ylim([0,30])
# plt.title('Studentai surinkę 90 ir daugiau balų', weight = 'bold', color = '#8EBCFF') #pavadinimas
# plt.xticks(color = '#8EBCFF')
# plt.yticks(color = '#8EBCFF')
#
# plt.show()

#-----------------------------------------------IŠVADOS---------------------------------------------------

# - Iš duomenų matome, kad didesnė dalis (59.8%, t.y. 595 studentai) išlaikė visus tris dalykus, neturėdami
#  "preparation course" ir mažesnė dalis (35.1%, t.y. 351 studentai) išlaikė baigę "preparation course". (1 Grafikas)
#
# - Neišlaikiusiūjų nei 1 egzamino - 1.8%, t.y. 18 studentų, visi jie neturėjo "preparation course", tuo tarpu tarp
# turėjusių šį kursą neišlaikiusių nebuvo. (1 Grafikas)

# - Bendras studentu vidurkis su "preparation course": 73.3
# - Bendras studentu vidurkis be "preparation course": 67.12
#
# - Labai gerai išlaikiusių studentų (t.y. 90 ir daugiau balų):
#                                                 - su "preparation test": 17 (60.71%)
#                                                 - be "preparation test": 11 (39.29%)

# - Ar 'preparation course' studentams padėjo gauti geresnius ivertinimus?

#         - Rezultatus vertinant kaip bendrą visumą, 'preparation course' padėjo studentams gauti geresnius įvertinimus,
#           su šiuo kursu išlaikiusiūjų bendras vidurkis buvo didesnis.
#
#
