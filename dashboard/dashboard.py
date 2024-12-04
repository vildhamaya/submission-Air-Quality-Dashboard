import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('all_data.csv')
st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    st.title("Analisis Dataset Air Quality Kota Wanliu dan Wanshouxigong")

    menu = ["EDA", "Question"]
    
    with st.sidebar:
        st.title("Menu")
        pilihan = st.sidebar.selectbox("Menu", menu)

    if pilihan == "EDA":
        st.subheader("Exploratory Data Analysis")
        
        # Filter interaktif
        st.sidebar.subheader("Filter")
        selected_station = st.sidebar.selectbox("Pilih Stasiun", df['station'].unique())
        selected_year = st.sidebar.selectbox("Pilih Tahun", df['year'].unique())
        
        st.pyplot(corr())
        st.pyplot(avg_yearly_summary(selected_station, selected_year))
        
        st.write("Ringkasan analisis tahunan di Wanliu dan Wanshouxigong, kadar polutan yang ditampilkan yaitu PM2.5, PM10, SO2, NO2, dan CO.")
        yearly_summary(['PM2.5', 'PM10', 'SO2', 'NO2'], selected_station, selected_year)
        yearly_summary(['CO'], selected_station, selected_year)
    else:
        st.subheader("Question")
        st.write("Pertanyaan 1: Bagaimana kondisi harian udara di Wanliu dan Wanshouxigong, pada jam berapa kadar polutan cenderung tinggi?")
        stations = df['station'].unique()
        question1(['PM2.5', 'PM10', 'SO2', 'NO2'], stations[:2], '2016-01-01')
        st.write("Pertanyaan 2: Bagaimana Ringkasan kadar polutan Tahunan di Wanliu dan Wanshouxigong pada bulan Mei 2015?")
        st.write("Conclusion :")
        st.write("Pada grafik di bawah merupakan data polutan pada tanggal 1 Mei 2015 di Wanliu dan Wanshouxigong.")
        
        st.write("Kadar Polutan PM2.5")
        question2('2015-05-01', '2015-05-29', ['PM2.5'])
        st.write("Kadar Polutan PM10")
        question2('2015-05-01', '2015-05-29', ['PM10'])
        st.write("Kadar Polutan SO2")
        question2('2015-05-01', '2015-05-29', ['SO2'])
        st.write("Kadar Polutan NO2")
        question2('2015-05-01', '2015-05-29', ['NO2'])
        st.write("Kadar Polutan CO")
        question2('2015-05-01', '2015-05-29', ['CO'])
        st.write("Kadar Polutan O3")
        question2('2015-05-01', '2015-05-29', ['O3'])
        st.write("Conclusion :")
        st.write("Visualisasi data kadar polutan yang ada di Wanliu dan Wanshouxigong mulai 1 Mei 2015 sampai 29 Mei 2015.")

def corr():
    st.write("Visualisasi korelasi antar field.")
    kolom_korelasi = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
    korelasi = df[kolom_korelasi].corr()

    plt.figure(figsize=(12, 8))
    sns.heatmap(korelasi, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Heatmap Korelasi')
    plt.show()

def yearly_summary(fields, station, year):
    yearly_monthly_mean = df.groupby(['year', 'month', 'station']).mean(numeric_only=True).reset_index()
    yearly_data = yearly_monthly_mean[(yearly_monthly_mean['year'] == year) & (yearly_monthly_mean['station'] == station)]

    # Mendapatkan daftar bulan unik dan diurutkan dari dataset
    monthly = df['month'].unique()
    monthly.sort()

    # Membuat plot untuk setiap polutan dalam satu gambar
    fig, axes = plt.subplots(1, 1, figsize=(15, 6))

    for polutan in fields:
        plt.plot(yearly_data['month'], yearly_data[polutan], label=polutan, marker='o')

    plt.xlabel('Bulan')
    plt.ylabel('Rata-rata Kualitas Udara')
    st.write(f'Rata-rata Kadar Polutan per Bulan di {station} - Tahun {year}')
    plt.legend()
    plt.grid(True)
    plt.xticks(monthly)
    plt.tight_layout()
    st.pyplot(fig)

def avg_yearly_summary(station, year):
    st.write("Rata-rata kadar polutan tiap tahun")
    annual_mean = df[df['station'] == station].groupby('year').mean(numeric_only=True)

    # Visualisasi tren kualitas udara dari tahun ke tahun
    plt.figure(figsize=(10, 6))
    plt.plot(annual_mean.index, annual_mean['PM2.5'], marker='o', label='PM2.5')
    plt.plot(annual_mean.index, annual_mean['PM10'], marker='o', label='PM10')
    plt.plot(annual_mean.index, annual_mean['SO2'], marker='o', label='SO2')
    plt.plot(annual_mean.index, annual_mean['NO2'], marker='o', label='NO2')
    plt.title('Tren Kualitas Udara dari Tahun ke Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata Kualitas Udara')
    plt.legend()
    plt.grid(True)
    # st.pyplot()

def get_data(station, date):
    data = df.loc[(df['date'] == date) & (df['station'] == station)]
    return data

def question1(polutan, stations, date):
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

def question2(start_date, end_date, content_value):
    filtered_data = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    stations = filtered_data['station'].unique()

    num_rows = 1
    num_cols = 2

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 8))
    axes = axes.flatten()

    contents = content_value

    for i, station in enumerate(stations):
        station_data = filtered_data[filtered_data['station'] == station]

        for content in contents:
            sns.lineplot(data=station_data, x='date', y=content, ax=axes[i], label=content)

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
