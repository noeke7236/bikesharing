import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="darkgrid")

# Memuat data
rent_data = pd.read_csv('/mount/src/bikesharing/dashboard/main_data.csv')

# Proses clean data
#Menyalin DataFrame untuk menghindari modifikasi data asli
rent_data_modified = rent_data.copy()

#Merubah nama kolom
rent_data_modified.rename(columns={'instant':'no','dteday':'date','season': 'season_code', 'windspeed':'wind_speed','cnt':'count'},inplace=True)

rent_data_modified['date'] = pd.to_datetime(rent_data_modified['date'])

#Konversi suhu -> temp : Normalized temperature in Celsius. The values are divided to 41 (max)
rent_data_modified['temperature'] = rent_data_modified['temp'] * 41

#Konversi kelembaban -> hum: Normalized humidity. The values are divided to 100 (max)
rent_data_modified['humidity'] = rent_data_modified['hum'] * 100

#Konversi kecepatan angin-> windspeed: Normalized wind speed. The values are divided to 67 (max)
rent_data_modified['windspeed'] = rent_data_modified['wind_speed'] * 67

#Konversi musim -> season : season (1:springer, 2:summer, 3:fall, 4:winter)
map_season = pd.DataFrame({
    "season_code": np.arange(1, 5),
    "season": ["spring", "summer", "fall", "winter"]})

rent_data_modified = pd.merge(rent_data_modified, map_season, on='season_code')

#Konversi bulan
map_month = pd.DataFrame({
    "mnth": np.arange(1, 13),
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "June", "July", "Aug", "Sep", "Oct", "Nov", "Dec"]
})

rent_data_modified = pd.merge(rent_data_modified, map_month, on='mnth')

#Konversi  cuaca
map_weather = pd.DataFrame({
    "weathersit": np.arange(1, 5),
    "weather": ["good", "moderate", "bad", "worse"]})

rent_data_modified = pd.merge(rent_data_modified, map_weather, on='weathersit')

## Web Streamlit
st.title('Penyewaan sepeda (Bike Sharing)')

st.header('Berdasarkan parameter cuaca', divider='rainbow')

## Tabel Perhitungan
# Menghitung data suhu, kelembaban, kecepatan angin dan sepeda yang disewa
season_table = rent_data_modified.groupby(['season']).agg({
    "temperature": ["max", "min", "mean", "median", "std"],
    "humidity": ["max", "min", "mean", "median", "std"],
    "windspeed": ["max", "min", "mean", "median", "std"],
    "count": ["max", "min", "mean", "median", "std"]
}).reset_index()

# Menampilkan tabel perhitungan berdasarkan musim
st.subheader('Tabel perhitungan berdasarkan musim')
st.write("""
    Berapa nilai maksimum, minimum, mean, median dan standar deviasi 
    untuk suhu (temperature), kelembaban (humidity), kecepatan angin (windspeed) 
    dan jumlah sepeda yang disewa (count) berdasarkan musim?
    """)
st.table(season_table)
##

## Tabel Perhitungan
# Menghitung data suhu, kelembaban, kecepatan angin dan sepeda yang disewa
month_table = rent_data_modified.groupby(['mnth','month']).agg({
    "temperature": ["max", "min", "mean", "median", "std"],
    "humidity": ["max", "min", "mean", "median", "std"],
    "windspeed": ["max", "min", "mean", "median", "std"],
    "count": ["max", "min", "mean", "median", "std"]
}).reset_index()

# Menampilkan tabel perhitungan berdasarkan bulan
st.subheader('Tabel perhitungan berdasarkan bulan')
st.write("""
    Berapa nilai maksimum, minimum, mean, median dan standar deviasi 
    untuk suhu (temperature), kelembaban (humidity), kecepatan angin (windspeed) 
    dan jumlah sepeda yang disewa (count) berdasarkan bulan?
    """)
st.table(month_table)
##

## Histogram
st.subheader('1. Parameter cuaca dengan musim')
st.write(
    """
    Bagaimana perubahan suhu (temperature), kelembaban (humidity) 
    dan kecepatan angin (windspeed) di sepanjang musim?
    """
)
# Fungsi untuk menampilkan histogram
def show_histogram(data, feature, title, color):
    fig, ax = plt.subplots(figsize=(8, 5))
    data[feature].hist(by=data['season'], edgecolor='black', color=color, ax=ax)
    fig.suptitle(title, y=1.02)
    st.pyplot(fig)
    plt.close()

# Menampilkan histogram temperature
show_histogram(rent_data_modified, 'temperature', 'Histogram Suhu (Temperature)', 'yellow')

# Menampilkan histogram humidity
show_histogram(rent_data_modified, 'humidity', 'Histogram Kelembaban (Humidity)', 'purple')

# Menampilkan histogram windspeed
show_histogram(rent_data_modified, 'windspeed', 'Histogram Kecepatan Angin (Windspeed)','lightskyblue')

st.subheader('2. Parameter cuaca berdasarkan bulan')
st.write(
    """
   Berapa nilai rata-rata suhu (temperature), kelembaban (humidity), kecepatan angin (windspeed) 
   dan jumlah sepeda yang disewa (count) berdasarkan bulan?
    """
)

## Barplot
# Menghitung rata-rata temperature, humidity, windspeed dan total sepeda yang disewa per bulan
mean_month = rent_data_modified.groupby(by=["mnth","month"]).agg({
    "temperature": "mean",
    "humidity": "mean",
    "windspeed": "mean",
    "count": "mean"
}).reset_index()

fig, ax = plt.subplots(2, 2, figsize=(18, 12))

# Barplot Humidity
sns.barplot(y="humidity", x="month", data=mean_month.sort_values(by="mnth", ascending=True), color="blue", ax=ax[0, 0])
ax[0, 0].set_ylabel(None)
ax[0, 0].set_xlabel(None)
ax[0, 0].set_title("Rata-rata Humidity", loc="center", fontsize=15)
ax[0, 0].tick_params(axis='x', labelsize=12)

# Barplot Temperature
sns.barplot(y="temperature", x="month", data=mean_month.sort_values(by="mnth", ascending=True), color="yellow", ax=ax[0, 1])
ax[0, 1].set_ylabel(None)
ax[0, 1].set_xlabel(None)
ax[0, 1].set_title('Rata-rata Temperature', loc="center", fontsize=15)
ax[0, 1].tick_params(axis='x', labelsize=12)

# Barplot Rent
sns.barplot(y="count", x="month", data=mean_month.sort_values(by="mnth", ascending=True), color="green", ax=ax[1, 0])
ax[1, 0].set_ylabel(None)
ax[1, 0].set_xlabel(None)
ax[1, 0].set_title('Rata-rata Sewa/Count', loc="center", fontsize=15)
ax[1, 0].tick_params(axis='x', labelsize=12)

# Barplot Windspeed
sns.barplot(y="windspeed", x="month", data=mean_month.sort_values(by="mnth", ascending=True), color="red", ax=ax[1, 1])
ax[1, 1].set_ylabel(None)
ax[1, 1].set_xlabel(None)
ax[1, 1].set_title('Rata-rata Windspeed', loc="center", fontsize=15)
ax[1, 1].tick_params(axis='x', labelsize=12)

st.pyplot(fig)
plt.close()
##

## Scatter plot
st.subheader('3. Korelasi parameter cuaca dengan pengguna (users)')
st.write(
    """
    Apakah suhu (temperature), kelembaban (humidity) dan kecepatan angin (windspeed) 
    berkaitan erat dengan pengguna (user casual dan user registered)?
    """
)

# Scatter plot user_type(casual vs registered) berdasarkan temperature

fig_temp_user, ax_temp_user = plt.subplots()
temp_user = rent_data_modified.groupby(by="temperature").agg({
    "casual": ["min", "max"], 
    "registered": ["min", "max"]
}).reset_index()

temp_user_melted = temp_user.melt(id_vars="temperature", var_name="user_type", value_name="value")

scatter_temp_user = sns.scatterplot(x="temperature", y="value", hue="user_type", data=temp_user_melted, marker="o", ax=ax_temp_user)
scatter_temp_user.legend(title="Users Legend")
ax_temp_user.set_xlabel("Suhu (Temperature)")
ax_temp_user.set_ylabel("Pengguna (Users)")
ax_temp_user.set_title("Temperature vs Users")

# Scatter plot user_type(casual vs registered) berdasarkan humidity

fig_hum_user, ax_hum_user = plt.subplots()
hum_user = rent_data_modified.groupby(by="humidity").agg({
    "casual": ["min", "max"], 
    "registered": ["min", "max"]
}).reset_index()

hum_user_melted = hum_user.melt(id_vars="humidity", var_name="user_type", value_name="value")
colors_hum = {'casual': 'blue', 'registered': 'orange'}

scatter_hum_user = sns.scatterplot(x="humidity", y="value", hue="user_type", palette=colors_hum, data=hum_user_melted, marker="o", ax=ax_hum_user)
scatter_hum_user.legend(title="Users Legend")
ax_hum_user.set_xlabel("Kelembaban (Humidity)")
ax_hum_user.set_ylabel("Pengguna (Users)")
ax_hum_user.set_title("Humidity vs Users")

# Scatter plot user_type(casual vs registered) berdasarkan windspeed

fig_wind_user, ax_wind_user = plt.subplots()
wind_user = rent_data_modified.groupby(by="windspeed").agg({
    "casual": ["min", "max"], 
    "registered": ["min", "max"]
}).reset_index()

wind_user_melted = wind_user.melt(id_vars="windspeed", var_name="user_type", value_name="value")
colors_wind = {'casual': 'green', 'registered': 'gold'}

scatter_wind_user = sns.scatterplot(x="windspeed", y="value", hue="user_type", palette=colors_wind, data=wind_user_melted, marker="o", ax=ax_wind_user)
scatter_wind_user.legend(title="Users Legend")
ax_wind_user.set_xlabel("Kecepatan Angin (Windspeed)")
ax_wind_user.set_ylabel("Pengguna (Users)")
ax_wind_user.set_title("Windspeed vs Users")

st.pyplot(fig_temp_user)
st.pyplot(fig_hum_user)
st.pyplot(fig_wind_user)
##

## Boxplot
# Boxplot Korelasi cuaca dengan jumlah sepeda yang disewa
st.subheader('4. Korelasi jumlah sepeda yang disewa dengan kategori cuaca (good, moderate, bad, worse)')
st.markdown(
    """
    Apakah kondisi cuaca berpengaruh dengan jumlah sepeda yang disewa?
    """
)
st.markdown("***")
st.markdown("""
    Kategori cuaca:
    - Good -> 1: Clear, Few clouds, Partly cloudy, Partly cloudy
    - Moderate -> 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
    - Bad -> 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
    - Worse -> 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
""")

fig_box, ax_box = plt.subplots(figsize=(10, 6))
box_plot = sns.boxplot(data=rent_data_modified, x="weather", y="count", hue="weather")

ax_box.set_xlabel('Kategori Cuaca')
ax_box.set_ylabel('Jumlah Sepeda')
ax_box.set_title('Korelasi cuaca dengan jumlah sepeda yang disewa')

st.pyplot(fig_box)
plt.close(fig_box)
##

st.header('Berdasarkan parameter waktu', divider='rainbow')

st.subheader('1. Parameter jumlah sepeda yang disewa berdasarkan tahun dan bulan')
st.markdown(
    """
    Bagaimana statistik jumlah sepeda yang disewa berdasarkan tahun (2011 dan 2012) dan bulan?
    """
)
##Barplot
# Konversi Tahun
# - yr : year (0: 2011, 1:2012)

year_mapping = {0: "2011", 1: "2012"}
rent_data_modified['year_mapped'] = rent_data_modified['yr'].replace(year_mapping)

# Menghitung jumlah sepeda yang disewa berdasarkan bulan dan tahun
monthly_count_modified = rent_data_modified.groupby(by=["year_mapped", "mnth", "month"]).agg({
    "count": "sum"
}).reset_index()

fig_bar, ax_bar = plt.subplots(figsize=(8, 5))
bar_plot = sns.barplot(data=monthly_count_modified, x="month", y="count", hue="year_mapped", dodge=True)

ax_bar.legend(title="Tahun")
ax_bar.set_xlabel("Bulan")
ax_bar.set_ylabel("Jumlah sepeda")
ax_bar.set_title("Jumlah sepeda yang disewa berdasarkan bulan dan tahun")

st.pyplot(fig_bar)
plt.close(fig_bar)
##

st.subheader('2. Parameter jumlah sepeda yang disewa berdasarkan hari')
st.markdown(
    """
    Bagaimana trend penyewaan sepeda berdasarkan hari dalam 1 pekan?
    """
)
##Boxplot
#Konversi Hari
day_mapping = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
rent_data_modified['weekday_mapped'] = rent_data_modified['weekday'].replace(day_mapping)

fig_weekday, ax_weekday = plt.subplots(figsize=(10, 6))
box_plot_weekday = sns.boxplot(data=rent_data_modified, x="weekday", y="count", hue="weekday_mapped", legend = False)

ax_weekday.set_xlabel("Hari")
ax_weekday.set_ylabel("Jumlah sepeda")
ax_weekday.set_title("Boxplot dari jumlah sepeda yang disewa berdasarkan hari")

weekday_labels = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
box_plot_weekday.set_xticklabels(weekday_labels)

st.pyplot(fig_weekday)
plt.close(fig_weekday)
##

##Pie Chart
st.subheader('3. Parameter jumlah sepeda yang disewa berdasarkan hari kerja dan hari libur')
st.markdown(
    """
    Bagaimana trend penyewaan sepeda berdasarkan hari kerja dan hari libur di tahun 2011?
    """
)
#Jumlah sepeda yang disewa pada saat bukan hari libur dan bukan hari kerja
#Sum holiday=0, workingday=0, yr_mapped=2011
filtered_y0h0w0 = rent_data_modified.loc[(rent_data_modified['year_mapped']=="2011") & (rent_data_modified['holiday']==0) & (rent_data_modified['workingday']==0)]
total_cnt_y0h0w0 = filtered_y0h0w0['count'].sum()

#Jumlah sepeda yang disewa pada saat hari libur dan bukan hari kerja
#Sum holiday=1, workingday=0, yr_mapped=2011
filtered_y0h1w0 = rent_data_modified.loc[(rent_data_modified['year_mapped']=="2011") & (rent_data_modified['holiday']==1) & (rent_data_modified['workingday']==0)]
total_cnt_y0h1w0 = filtered_y0h1w0['count'].sum()

#Jumlah sepeda yang disewa pada saat bukan hari libur dan hari kerja
#Sum holiday=0, workingday=1, yr_mapped=2011
filtered_y0h0w1 = rent_data_modified.loc[(rent_data_modified['year_mapped']=="2011") & (rent_data_modified['holiday']==0) & (rent_data_modified['workingday']==1)]
total_cnt_y0h0w1 = filtered_y0h0w1['count'].sum()

labels = ['Hari Kerja', 'Hari Libur', 'Bukan Hari Kerja dan Bukan Hari Libur']
sizes = [total_cnt_y0h0w1, total_cnt_y0h1w0, total_cnt_y0h0w0]
colors = ['#ff9999', '#66b3ff', '#99ff99']

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax1.axis('equal')

ax1.set_title("Pie chart sepeda yang disewa berdasarkan hari kerja atau hari libur di tahun 2011")

st.pyplot(fig1)
plt.close(fig1)

##

st.markdown(
    """
    Bagaimana trend penyewaan sepeda berdasarkan hari kerja dan hari libur di tahun 2012?
    """
)
#Jumlah sepeda yang disewa pada saat bukan hari libur dan bukan hari kerja
#Sum holiday=0, workingday=0, yr_mapped=2012
filtered_y1h0w0 = rent_data_modified.loc[(rent_data_modified['year_mapped']=="2012") & (rent_data_modified['holiday']==0) & (rent_data_modified['workingday']==0)]
total_cnt_y1h0w0 = filtered_y1h0w0['count'].sum()

#Jumlah sepeda yang disewa pada saat hari libur dan bukan hari kerja
#Sum holiday=1, workingday=0, yr_mapped=2012
filtered_y1h1w0 = rent_data_modified.loc[(rent_data_modified['year_mapped']=="2012") & (rent_data_modified['holiday']==1) & (rent_data_modified['workingday']==0)]
total_cnt_y1h1w0 = filtered_y1h1w0['count'].sum()

#Jumlah sepeda yang disewa pada saat bukan hari libur dan hari kerja
#Sum holiday=0, workingday=1, yr_mapped=2012
filtered_y1h0w1 = rent_data_modified.loc[(rent_data_modified['year_mapped']=="2012") & (rent_data_modified['holiday']==0) & (rent_data_modified['workingday']==1)]
total_cnt_y1h0w1 = filtered_y1h0w1['count'].sum()

labels = ['Hari Kerja', 'Hari Libur', 'Bukan Hari Kerja dan Bukan Hari Libur']
sizes2 = [total_cnt_y1h0w1, total_cnt_y1h1w0, total_cnt_y1h0w0]
colors = ['#ff9999', '#66b3ff', '#99ff99']

fig2, ax2 = plt.subplots()
ax2.pie(sizes2, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax2.axis('equal') 

ax2.set_title("Pie chart sepeda yang disewa berdasarkan hari kerja atau hari libur di tahun 2012")

st.pyplot(fig2)
plt.close(fig2)
##

st.header('Kesimpulan', divider='rainbow')
st.write(
    """
1. Berapa nilai maksimum, minimum, mean, median dan standar deviasi untuk suhu (temperature), kelembaban (humidity), kecepatan angin (windspeed) dan jumlah sepeda yang disewa (count) berdasarkan musim?  
Kesimpulan : Berdasarkan statistik ini, bisa dilihat nilai rata-rata jumlah sepeda yang disewa per hari berdasarkan musim. Nilai rata-rata tertinggi jumlah sepeda yang disewa pada musim Fall (dengan nilai rata-rata temperature : 28,9 , humidity : 63,5 dan windspeed : 11,5). Sedangkan nilai rata-rata terendah jumlah sepeda yang disewa pada musim Spring (dengan nilai rata-rata temperature : 12,2 , humidity : 58,3 dan windspeed : 14,4)

2. Berapa nilai maksimum, minimum, mean, median dan standar deviasi untuk suhu (temperature), kelembaban (humidity), kecepatan angin (windspeed) dan jumlah sepeda yang disewa (count) berdasarkan bulan?  
Kesimpulan : Berdasarkan statistik ini, bisa dilihat nilai rata-rata jumlah sepeda yang disewa per hari berdasarkan bulan. Nilai rata-rata tertinggi jumlah sepeda yang disewa pada bulan Juni (dengan nilai rata-rata temperature : 28 humidity : 57,6 dan windspeed : 12,4). Sedangkan nilai rata-rata terendah jumlah sepeda yang disewa pada bulan Januari (dengan nilai rata-rata temperature : 9,7 , humidity : 58,6 dan windspeed : 13,8)

3. Bagaimana perubahan suhu (temperature), kelembaban (humidity) dan kecepatan angin (windspeed) di sepanjang musim?  
Kesimpulan : Pada musim summer, suhu udara yang hangat, kecepatan angin yang sedang, dan kelembaban yang rendah membuat bersepeda menjadi lebih nyaman dan menyenangkan. Hal ini karena suhu udara yang hangat akan membuat tubuh menjadi lebih rileks, kecepatan angin yang sedang tidak akan membuat sepeda menjadi terlalu sulit dikendarai, dan kelembaban yang rendah akan membuat tubuh tidak merasa lembab.
Pada musim spring dan fall, suhu udara yang tidak terlalu panas atau dingin, kecepatan angin yang sedang, dan kelembaban yang sedang juga merupakan kondisi yang baik untuk bersepeda.
Pada musim winter, suhu udara yang dingin, kecepatan angin yang kencang, dan kelembaban yang tinggi dapat membuat bersepeda menjadi tidak nyaman dan berbahaya. Hal ini karena suhu udara yang dingin dapat membuat tubuh menjadi kaku dan rentan mengalami hipotermia, kecepatan angin yang kencang dapat membuat sepeda menjadi sulit dikendarai dan meningkatkan risiko kecelakaan, dan kelembaban yang tinggi dapat membuat tubuh merasa lembab.
Berdasarkan hal tersebut, musim summer adalah musim yang paling direkomendasikan untuk bersepeda dengan parameter suhu, kecepatan angin, dan kelembaban. Musim spring dan fall juga merupakan musim yang cukup baik untuk bersepeda, tetapi dengan catatan bahwa kecepatan angin tidak terlalu kencang dan kelembaban tidak terlalu tinggi. Musim winter adalah musim yang paling tidak direkomendasikan untuk bersepeda, kecuali jika cuaca sangat cerah, kecepatan angin tidak terlalu kencang, dan kelembaban tidak terlalu tinggi.

4. Berapa nilai rata-rata suhu (temperature), kelembaban (humidity) kecepatan angin (windspeed) dan jumlah sepeda yang disewa (count) berdasarkan bulan?  
Kesimpulan : Berdasarkan grafik tersebut maka dapat disimpulkan di bulan Juni - Agustus adalah kondisi ideal untuk menyewa sepeda. Jumlah total penyewaan sepeda meningkat seiring dengan meningkatnya suhu. Untuk kelembaban (humidity) dan kecepatan angin (windspeed) tidak mempengaruhi intensitas penyewaan sepeda.

5. Apakah suhu (temperature), kelembaban (humidity) dan kecepatan angin (windspeed) berkaitan erat dengan pengguna (user casual dan user registered)?  
Kesimpulan : Seperti yang dapat kita lihat pada plot, terdapat hubungan antara pengguna (user casual dan user registered) dengan suhu (temperature). Jumlah pengguna (user casual dan user registered) sangat bergantung terhadap suhu. Ketika nilai suhu naik, maka jumlah penyewaan sepeda juga meningkat. Selain itu, kita juga dapat melihat bahwa pengguna (user registerd) menyewa lebih banyak sepeda daripada pengguna (user casual). Untuk kelembaban (humidity) dan kecepatan angin (windspeed) tidak mempengaruhi intensitas penyewaan sepeda.

6. Apakah kondisi cuaca berpengaruh dengan jumlah sepeda yang disewa?  
Kesimpulan : Jumlah sepeda yang disewa pada cuaca yang baik (good) lebih tinggi. Cuaca yang baik (good) merupakan kondisi yang baik untuk penyewaan sepeda secara umum. Pada cuaca baik (good), orang-orang cenderung merasa lebih nyaman dan aman untuk bersepeda. Situasi cuaca yang sangat buruk (worse), baik pengguna (user registered) maupun pengguna (user casual) tidak ada yang menyewa sepeda.

7. Bagaimana statistik jumlah sepeda yang disewa berdasarkan tahun (2011 dan 2012) dan bulan? 
Kesimpulan : Berdasarkan grafik tersebut, dapat ditarik beberapa kesimpulan yaitu
Jumlah sepeda yang disewa meningkat secara signifikan dari tahun 2011 ke tahun 2012. Hal ini menunjukkan bahwa semakin banyak orang yang menggunakan sepeda sebagai alat transportasi atau rekreasi.
Peningkatan jumlah sepeda yang disewa paling signifikan terjadi pada bulan-bulan musim panas (Juni-Agustus). Hal ini menunjukkan bahwa orang-orang lebih cenderung bersepeda pada cuaca yang hangat dan cerah.

8. Bagaimana trend penyewaan sepeda berdasarkan hari dalam 1 pekan?  
Kesimpulan : Jumlah sepeda yang disewa pada hari Sabtu (Saturday) dan Minggu (Sunday) lebih tinggi daripada hari-hari lainnya. Hal ini terlihat dari posisi median dan batas atas boxplot pada hari Sabtu (Saturday) dan Minggu (Sunday) yang berada di atas batas atas boxplot pada hari-hari lainnya. Karena pada hari Sabtu (Saturday) dan Minggu (Sunday), orang-orang cenderung memiliki lebih banyak waktu luang sehingga lebih banyak acara atau kegiatan yang dapat dilakukan dengan sepeda. Cuaca cenderung lebih cerah sangat mendukung kegiatan bersepeda.

9. Bagaimana trend penyewaan sepeda berdasarkan hari kerja dan hari libur di tahun 2011?
Kesimpulan : Hari kerja adalah hari dengan jumlah penyewaan sepeda terbanyak, yaitu 68,9%.
Hari libur adalah hari dengan jumlah penyewaan sepeda paling sedikit, yaitu 2,4%.
Hari sabtu dan minggu adalah hari dengan jumlah penyewaan sepeda yang cukup tinggi, yaitu 28,7%.
Hari kerja adalah hari ketika orang-orang cenderung bekerja atau sekolah. Hal ini menyebabkan mereka memiliki lebih sedikit waktu luang untuk bersepeda.

10. Bagaimana trend penyewaan sepeda berdasarkan hari kerja dan hari libur di tahun 2012?
Kesimpulan : Hari kerja adalah hari dengan jumlah penyewaan sepeda terbanyak, yaitu 70,1%.
Hari libur adalah hari dengan jumlah penyewaan sepeda paling sedikit, yaitu 2,4%.
Hari sabtu dan minggu adalah hari dengan jumlah penyewaan sepeda yang cukup tinggi, yaitu 27,6%.
Terjadi peningkatan secara signifikan di hari kerja dari tahun 2011 ke tahun 2012.
    """
)

st.subheader('Pembuat:')
st.write(
    """
    - Nama : Ponco Nugrah Wibowo
    - Email : noeke7236@gmail.com
    - Id Dicoding : noeke7236
    """
)
