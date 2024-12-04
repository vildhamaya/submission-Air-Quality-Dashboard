import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df  = pd.read_csv('all_data.csv')
st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    st.title("Analisis Dataset Air Quality Kota Wanliu dan Wanshouxigong")

    menu  = ["EDA","Question"]
    
    with st.sidebar:
        st.title("Menu")
        pilihan = st.sidebar.selectbox("Menu",menu)


    if pilihan == "EDA":
        st.subheader("Exploratory Data Analysis")
        st.pyplot(corr())
        st.pyplot(avg_yearly_summary())
        
        
        st.write("Ringkasan analisis tahunan di Wanliu dan Wanshouxigong,kadar polutan yang ditampilkan yaitu PM2.5, PM10, SO2, NO2 , dan CO untuk CO saya pisahkan sendiri karena nilainya yang terlalu besar dibanding field yang lain bertujuan agar dapat terlihat jelas untuk visualisasi datanya")
        yearly_summary(['PM2.5', 'PM10', 'SO2', 'NO2'],'Wanliu')
        yearly_summary(['CO'],'Wanliu')
        yearly_summary(['PM2.5', 'PM10', 'SO2', 'NO2'],'Wanshouxigong')
        yearly_summary(['CO'],'Wanshouxigong')
    else :
        st.subheader("Question")
        st.write("Pertanyaan 1: Bagaimana kondisi harian udara di Wanliu dan Wanshouxigong,pada jam berapa kadar polutan cenderung tinggi?")
        stations = df['station'].unique()
        question1(['PM2.5', 'PM10', 'SO2', 'NO2'], stations[:2], '2016-01-01')
        st.write("Pertanyaan 2: Bagaimana Ringkasan kadar polutan Tahunan di Wanliu dan Wanshouxigong pada bulan Mei 2015?")
        st.write("Conclusion :")
        st.write("Pada grafik dibawah merupakan data polutan pada tanggal 1 Mei 2015 di Wanliu dan Wanshouxigong.X merupakan Jam dalam sehari sedangkan Y merupakan tingkat konsntrasi polutan.dari grafik kita dapat menyimpulkan kadar polutan cendeerung tinggi pada jam pagi-siang hari.polutan mulai mengalami kenaikan pada sekitar dini hari hingga mencapai titik tertinggi pada jam 6 di kota wanliu dan jam 5 di kota wanshouxigong.hal tersebut menunjukkan bahwa aktivitas masyarakat, industri, ataupun pabrik yang menyebabkan kadar polutan cenderung dilakukan pada pagi hingga siang hari dan kadar polutan mulai turun pada jam 14.")
          
        
        st.write("Kadar Polutan PM2.5")
        question2('2015-05-01', '2015-05-29',['PM2.5'])
        st.write("Kadar Polutan PM10")
        question2('2015-05-01', '2015-05-29',['PM10'])
        st.write("Kadar Polutan SO2")
        question2('2015-05-01', '2015-05-29',['SO2'])
        st.write("Kadar Polutan NO2")
        question2('2015-05-01', '2015-05-29',['NO2'])
        st.write("Kadar Polutan CO")
        question2('2015-05-01', '2015-05-29',['CO'])
        st.write("Kadar Polutan O3")
        question2('2015-05-01', '2015-05-29',['O3'])
        st.write("Conclusion :")
        st.write("Visualisasi data kadar polutan yang ada di Wanliu dan Wanshouxigong mulai 1 Mei 2015 sampai 29 Mei 2015 Grafik diatas berisi informasi tentang kadar polutan yang ada,garis tengah menunjukkan rata2 kadar polutan dalam sehari sedangkan offside dari garis tersebut menunjukkan data tertinggi dan data terendah kadar polutan dalam seharinya.kadar polutan pada bulan mei 2015 cenderung tinggi pada tanggal 17 Mei 2015.secara keseluruhan bulan mei 2015 kadar polutannya cukup tinggi meskipun disaat weekday dan ketika weekend kadar polutan berada dalam peak tertingginya yaiut tanggal 17 Mei 2015. Hal tersebut menunjukkan betapa aktifnya kegiatan masyarakat Wanliu dan wanshouxigong yang menghasilkan polutan pada bulan ini.")

def corr():
    st.write("Visualisasi korelasi antar field,Merah melambagkan korelasi positif antar field contoh PM2.5 memiliki tingkat korelasi 0.88 dengan PM10 artinya nilai antara PM2.5 linear dengan PM10 jika PM2.5 memiliki nilai yang tinggi maka otomatis pm 10 juga akan meiliki nilai yang tinggi dan sebaliknya jika memiliki korelasi negatif suatu nilai akan berkebalikan dengan nilai lainnya conohnya antara PRES dan TEMP , PRES merupakan tekanan udara sedangkan TEMP adalah temperatur, jika TEMP tinggi maka PRES akan rendah nilainya dan sebaliknya.")
    kolom_korelasi = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']


    korelasi = df[kolom_korelasi].corr()

    plt.figure(figsize=(12, 8))
    sns.heatmap(korelasi, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Heatmap Korelasi')
    plt.show()

def yearly_summary(fields,station):
    yearly_monthly_mean = df.groupby(['year', 'month','station']).mean(numeric_only=True).reset_index()

    # Mendapatkan daftar tahun unik dari dataset
    years = df['year'].unique()

    # Mendapatkan daftar bulan unik dan diurutkan dari dataset
    monthly = df['month'].unique()
    monthly.sort()


    # Membuat plot untuk setiap tahun
    for i,year in enumerate(years):
        yearly_data = yearly_monthly_mean[(yearly_monthly_mean['year'] == year )& (yearly_monthly_mean['station'] == station)]

        # Membuat plot untuk setiap polutan dalam satu gambar
        fig, axes = plt.subplots(1, 1, figsize=(15, 6))

        for polutan in fields:
            plt.plot(yearly_data['month'], yearly_data[polutan], label=polutan,marker='o')

        plt.xlabel('Bulan')
        plt.ylabel('Rata-rata Kualitas Udara')
        # plt.title(f'Rata-rata Kadar Polutan per Bulan di {station} - Tahun {year}')
        st.write(f'Rata-rata Kadar Polutan per Bulan di {station} - Tahun {year}')
        plt.legend()
        plt.grid(True)
        plt.xticks(monthly)
        plt.tight_layout()
        st.pyplot(fig)
        
        
def avg_yearly_summary():
    st.write("Rata rata kadar polutan tiap tahun")
    # df['year'] = df['date'].dt.year

    # Agregasi data berdasarkan tahun
    annual_mean = df.groupby('year').mean(numeric_only=True)

    # Visualisasi tren kualitas udara dari tahun ke tahun
    plt.figure(figsize=(10, 6))
    plt.plot(annual_mean.index, annual_mean['PM2.5'], marker='o', label='PM2.5')
    plt.plot(annual_mean.index, annual_mean['PM10'], marker='o', label='PM10')
    plt.plot(annual_mean.index, annual_mean['SO2'], marker='o', label='SO2')
    plt.plot(annual_mean.index, annual_mean['NO2'], marker='o', label='NO2')
    # plt.plot(annual_mean.index, annual_mean['CO'], marker='o', label='CO')
    plt.title('Tren Kualitas Udara dari Tahun ke Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata Kualitas Udara')
    plt.legend()
    plt.grid(True)

def get_data(station, date):
    data = df.loc[(df['date'] == date) & (df['station'] == station)]
    return data


def question1(polutan, stations,date):
    # data = df.loc[(df['date'] == date) & (df['station'] == stations)]
    
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))
    fig.suptitle(f'Pembandingan Kualitas Udara Polutan per Jam pada {date}', y=0.98)

    for i, station in enumerate(stations):
        data_station = get_data(station, date)
        for pol in polutan:
            axes[i].plot(data_station['hour'], data_station[pol], marker='o', linestyle='-', label=f'{pol} - {station}')
            axes[i].set_title(f'Kualitas Udara di {station}')
            axes[i].set_xlabel('Jam dalam Sehari')
            axes[i].set_ylabel('Konsentrasi Polutan')
            axes[i].grid(True)
            axes[i].legend()

    plt.tight_layout()
    st.pyplot(fig)


def question2(start_date, end_date,content_value):
    # Filter data berdasarkan tanggal mulai dan akhir
    filtered_data = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    stations = filtered_data['station'].unique()

    num_rows = 1
    num_cols = 2

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 8))
    axes = axes.flatten()  # Mengubah matriks 2D menjadi array 1D

    contents = content_value

    for i, station in enumerate(stations):
        station_data = filtered_data[filtered_data['station'] == station]

        for content in contents:
            sns.lineplot(data=station_data, x='date', y=content, ax=axes[i], label=content,)


        axes[i].set_title(station)

        if i >= num_cols * (num_rows - 1):
            axes[i].set_xlabel('Date')

        axes[i].tick_params(axis='x', rotation=45)
        axes[i].set_ylabel('PPM')

        if i == len(stations) - 1:
            axes[i].legend()

    plt.tight_layout()
    st.pyplot(fig)
    
if __name__ == '__main__':
    main()
        
        
