
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import streamlit as st
from skimage import io

#cargar strike_reports
df = pd.read_csv('STRIKE_REPORTS.csv')

#Titulo
st.title("Dashboard, Impactos de Aves en Aeronaves")

#Encabezado
st.header("Utilizando la base de datos 'STRIKE_REPORTS.csv'")

#imagen
img = io.imread("https://revistajaraysedal.es/wp-content/uploads/2021/10/buitre-choca-avion-madrid.jpg")
fig = px.imshow(img)
fig.show()

#Texto y lista
st.write("Head de datos")
st.write(df.head())


#correlacion entre numeros
df['INCIDENT_DATE'] = pd.to_datetime(df['INCIDENT_DATE'])
dfcorrelacion=df[["INCIDENT_DATE","LATITUDE","LONGITUDE","EMA","EMO","AC_MASS","NUM_ENGS","ENG_1_POS","ENG_2_POS","ENG_3_POS","ENG_4_POS","HEIGHT","SPEED",
                "DISTANCE","AOS","BIRD_BAND_NUMBER","NR_INJURIES","NR_FATALITIES"]]
z=dfcorrelacion.corr()
st.write("Revisamos si hay alguna correlación entre las columnas con variables de tipo numéricas")
heat=sns.heatmap(z,annot=True,annot_kws={'size': 7},fmt='.1f')
st.write(heat)


#barra lateral con boton para incidentes por tiempo
opt=st.sidebar.radio("Seleccione un grafico de incidentes a lo largo del tiempo",
                     options=("Años","Meses"))


#grafico de incidentes por año
st.write("Grafico en el cual observamos la cantidad de incidentes por año")
df2=df['INCIDENT_YEAR']
df2.dropna(inplace=True)
fig=px.line(df2['INCIDENT_YEAR'].value_counts().sort_index(), title='Cantidad de reportes por año',labels={'value':'Reportes',"INCIDENT_YEAR":"Años"}, markers=True)
fig.add_bar(x=df2['INCIDENT_YEAR'].value_counts().sort_index().index, y=df2['INCIDENT_YEAR'].value_counts().sort_index().values)
st.write(fig)


#grafico incidentes por mes por cada año
st.write("Grafico en el cual observamos la cantidad de incidentes por mes correspondiente a cada año")
df3=df[["INCIDENT_MONTH","INCIDENT_YEAR"]]
df3['REPORTES']=1
df4=df3.groupby(['INCIDENT_YEAR','INCIDENT_MONTH']).count()
df4.reset_index(inplace=True)
df4['INCIDENT_MONTH']=df4['INCIDENT_MONTH'].replace(1,'Enero')
df4['INCIDENT_MONTH']=df4['INCIDENT_MONTH'].replace(2,'Febrero')
df4['INCIDENT_MONTH']=df4['INCIDENT_MONTH'].replace(3,'Marzo')
df4['INCIDENT_MONTH']=df4['INCIDENT_MONTH'].replace(4,'Abril')
df4['INCIDENT_MONTH']=df4['INCIDENT_MONTH'].replace(5,'Mayo')
df4['INCIDENT_MONTH']=df4['INCIDENT_MONTH'].replace(6,'Junio')
df4['INCIDENT_MONTH']=df4['INCIDENT_MONTH'].replace(7,'Julio')
df4['INCIDENT_MONTH']=df4['INCIDENT_MONTH'].replace(8,'Agosto')
df4['INCIDENT_MONTH']=df4['INCIDENT_MONTH'].replace(9,'Septiembre')
df4['INCIDENT_MONTH']=df4['INCIDENT_MONTH'].replace(10,'Octubre')
df4['INCIDENT_MONTH']=df4['INCIDENT_MONTH'].replace(11,'Noviembre')
df4['INCIDENT_MONTH']=df4['INCIDENT_MONTH'].replace(12,'Diciembre')
fig = px.bar(df4, x="INCIDENT_YEAR", y="REPORTES", color="INCIDENT_MONTH", title="Años y meses")
st.write(fig)


#grafico de modelos de aviones
dfaircraft=df[["AIRCRAFT"]]
dfaircraft.dropna(inplace=True)
dfaircraft['Reportes']=1
df_aircraft=dfaircraft.groupby('AIRCRAFT').count().sort_values(by='Reportes',ascending=False)
df_aircraft_2=df_aircraft.head(11)
df_aircraft_2.reset_index(inplace=True)
df_aircraft_2.loc[11]=['Otros',113314]
fig=px.pie(df_aircraft_2,values='Reportes',names=df_aircraft_2['AIRCRAFT'],title='Modelos de aeronaves con más reportes', labels={"UNKNOWN":"Desconocido"})
st.write(fig)


#grafico especie de aves
dfspecies=df[["SPECIES"]]
dfspecies.dropna(inplace=True)
dfspecies['Reportes']=1
df_species=dfspecies.groupby('SPECIES').count().sort_values(by='Reportes',ascending=False).head(13)
df_species.reset_index(inplace=True)
df_species.loc[13]=['Otros',99790]
fig=px.pie(df_species,values='Reportes',names=df_species['SPECIES'],title='Especies con más reportes')
st.write(fig)


#barra lateral con boton para hora en la que ocurren los incidentes
opt2=st.sidebar.radio("Seleccione un algo",options=("Barras","Densidad"))


#grafico de horas
df5=df[["TIME"]]
df5.dropna(inplace=True)
df5["Frecuencia"]=1
df_tiempor=df5.groupby('TIME').count()
df_tiempor.reset_index(inplace=True)
fig=px.bar(df_tiempor,x="TIME",y="Frecuencia",
           title='Horas con más reportes')
st.write(fig)


#horas densidad
fig=px.density_heatmap(df5.sort_values(by='TIME',ascending=True),x="TIME",y="Frecuencia",
           title='Horas con más reportes')
st.write(fig)
























#lugares donde ocurren los incidentes
df8=df[["INCIDENT_YEAR","LATITUDE","LONGITUDE"]]
df8.dropna(inplace=True)
df8['FRECUENCIA']=1
df_coor=df8.groupby(['INCIDENT_YEAR','LATITUDE','LONGITUDE']).count()
df_coor.reset_index(inplace=True)
px.scatter_mapbox(df_coor,lat="LATITUDE",lon="LONGITUDE",
                  mapbox_style="open-street-map",
                  width=1200,height=800,
                  zoom=3,
                  animation_frame="INCIDENT_YEAR",
                  size="FRECUENCIA")
















