#%%
import pandas as pd
from datetime import datetime
from datetime import date
from datetime import timedelta
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from repo_tools_pkg.file_tools import find_latest_file

today=datetime.now().date()
yesterday=today-timedelta(days=1)
#%% Find latest files Covid
file_path=os.path.dirname(__file__)
parent_directory=os.path.normpath(os.path.join(file_path, '..',''))
covid_path_latest=find_latest_file(os.path.join(parent_directory))
print(covid_path_latest)

#%% Read Covid

covid_df=pd.read_csv(covid_path_latest[0])
covid_df["Meldedatum"]=pd.to_datetime(covid_df["Meldedatum"]).dt.date

#%% Sum Data

covid_df_sum=covid_df.groupby("Meldedatum").agg({"AnzahlFall":"sum","AnzahlTodesfall":"sum"}).sort_values("Meldedatum",ascending=True)
covid_df_sum.index=pd.to_datetime(covid_df_sum.index)
#Ein Datensatz pro Tag mit 0 aufüllen
covid_df_sum=covid_df_sum.resample("1D").asfreq().fillna(0)
covid_df_sum["AnzahlFall_7d_mean"]=covid_df_sum["AnzahlFall"].rolling(7).mean()
covid_df_sum["AnzahlTodesfallfall_7d_mean"]=covid_df_sum["AnzahlTodesfall"].rolling(7).mean()
covid_df_sum.index=pd.to_datetime(covid_df_sum.index)
covid_df_sum=covid_df_sum.sort_index(ascending=True)
covid_df_sum["Cum_sum"]=covid_df_sum["AnzahlFall"].cumsum()

#%% Read Testzahl
testzahl_path=find_latest_file(os.path.join(parent_directory,"Testzahlen","raw_data"))[0]
testzahl_df=pd.read_excel(testzahl_path,sheet_name='1_Testzahlerfassung', skipfooter=1)
testzahl_df=testzahl_df.drop(0)
datum=[]

for key, value in testzahl_df.iterrows():
    kalender=value['Kalenderwoche'].split('/')
    datum.append(date.fromisocalendar(int(kalender[1]), int(kalender[0]),7))
testzahl_df.index=pd.to_datetime(datum)
testzahl_df=testzahl_df.resample("1D").backfill()
testzahl_df.sort_index(ascending=True)
testzahl_df["Testungen_7d_mean"]=testzahl_df["Anzahl Testungen"]/7

#%% Read Intensivregister

ir_path=find_latest_file(os.path.join(parent_directory,"Intensivregister","raw_data"),'bundesland')[0]
ir_df=pd.read_csv(ir_path)

#%% Eval Intensivregister

ir_df["Datum"]=pd.to_datetime(ir_df["Datum"], utc=True).dt.date
ir_df=ir_df[ir_df["Bundesland"]=="DEUTSCHLAND"].groupby("Datum").last()
ir_df.index=pd.to_datetime(ir_df.index)
ir_df=ir_df.resample("1D").backfill()

#%% Plot

fig, ax = plt.subplots(4, figsize=(10,20))
ax[0].plot(covid_df_sum.index,covid_df_sum["AnzahlFall_7d_mean"])
ax[0].set_title("Covid Fälle pro Tag im 7 Tage Mittel")
ax[1].plot(covid_df_sum.index,covid_df_sum["AnzahlTodesfallfall_7d_mean"])
ax[1].set_title("Covid Todesfälle pro Tag im 7 Tage Mittel")
ax[2].plot(testzahl_df.index,testzahl_df["Testungen_7d_mean"])
ax[2].set_title("Testungen pro Tag im 7 Tage Mittel")
ax[3].plot(ir_df.index,ir_df["Aktuelle_COVID_Faelle_Erwachsene_ITS"])
ax[3].set_title("Anzahl belgter Intensivbetten mit Covd-Patienten")
fig.tight_layout()
plt.savefig("Covid_summary.png")
plt.show()

#%% Read impfmonitoring
im_path=os.path.normpath(os.path.join(os.path.abspath(''),'..','Impfquotenmonitoring','raw_data', 'RKI_COVID19_Impfquotenmonitoring_latest.xlsx'))
im_df=pd.read_excel(im_path,sheet_name="Impfungen_proTag",skipfooter=7)
im_df=im_df.dropna()
im_df["Datum"]=pd.to_datetime(im_df["Datum"]).dt.date
im_df['Cum_sum_1']=im_df["Erstimpfung"].cumsum()
im_df['Cum_sum_2']=im_df["Zweitimpfung"].cumsum()
im_df['Cum_sum_gesamt']=im_df["Gesamtzahl verabreichter Impfstoffdosen"].cumsum()

#%% Plot impfmonitoring + Covic

min_date=pd.to_datetime(im_df["Datum"].min())
covid_df_sum_im=covid_df_sum[covid_df_sum.index>=min_date]
scale_y = 1e6
ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_y))

fig2, ax2 = plt.subplots()
ax2.plot(im_df["Datum"], im_df["Cum_sum_1"], label="Erstimpfung kumuliert")
ax2.plot(covid_df_sum_im.index,covid_df_sum_im["Cum_sum"], label="Erkrankte")
ax2.axhline(y=83020000*0.7, color='r', linestyle='-', label="Herdenimmunität (70%)")
ax2.legend()
ax2.yaxis.set_major_formatter(ticks_y)
ax2.set_ylabel('Anzahl Personen in Millionen')
plt.xticks(rotation=45)
fig2.tight_layout()
fig2.savefig('Herdenimmunitaet.png')
fig2.show()