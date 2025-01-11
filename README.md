# Tokopedia Product Scraper

## Fitur

1. Pencarian berdasarkan input keyword.
2. Multiple url sekali klik.
3. Import otomatis ke csv.
4. Fitur retry jika terjadi error connection.
5. Ambil data nama toko, produk, harga, rating, penjualan, url product, dan gambar produk.

## Screenshot 

![Kodingan Tokopedia Scraper dengan Python](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/s1mrioyhl6onweq4y3f9.png)

<center>Gambar 1: Kodingan Tokopedia Scraper dengan Python</center>


![Hasil Running Script](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vc8nifq79u7gmj4poaly.png)
<center>Gambar 2: Hasil Running Script</center>
&nbsp;

![Data Hasil Scraping](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2rdlctov8q1eiy1zeb3z.png)
<center>Gambar 3: Data Hasil Scraping</center>
&nbsp;

## Cara Penggunaan

1. Download dan install python3 di OS kamu jika belum menginstall. Cek: [Download pyhton](https://www.python.org/downloads/)

2. Clone atau download repository tokped scraper via. 
`git clone https://github.com/rahmatalhakam/tokopedia-scraper.git`

3. Install library python yang dibutuhkan.
`pip install requests beautifulsoup4 pandas`

4. Setting keyword pencarian di file config.json
    ```json
    {
        "keyword": "mouse b100"
    }
    ```
5. Tambahkan url toko yang ingin di file tokopedia_shops.csv. Contoh:
    ```
    url
    https://www.tokopedia.com/elscomputer
    https://www.tokopedia.com/starcomporigin
    https://www.tokopedia.com/youngscom/
    https://www.tokopedia.com/anandamcomputer
    https://www.tokopedia.com/computajogja
    https://www.tokopedia.com/harrismajogja
    https://www.tokopedia.com/jabenjogja
    ```
6. run script pyhon di dengan cara
`python tokpedscraper.py`

## Note
Jika script ini bermanfaat dan memang digunakan, request fitur baru dapat saya pertimbangkan. Jangan lupa like, follow, dan komen di bawah. Kira-kira fitur apa yang perlu didevelop. Terimakasih. 😃

