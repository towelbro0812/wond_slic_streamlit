# 超像素分割Streamlit 網頁端

因專案所需，需要把傷口的照片進型超像素分割，因此開發了一個 web APP，用來解決多張照片的EDA SLIC工作
1. 在左方sidebar上傳圖片(支援多張照片)
2. 選擇所需要的圖片
3. 進行SLIC參數調整
4. 下方Button可以開始進行SLIC算法
5. 算完之後可以在右方查看SLIC分割結果
6. 圖片下方可以進行HSV域值調整mask參數
7. 下方可以使用一鍵處理所有上傳圖片，處理完之後會出現下載按鈕，可以把處理的圖片一鍵打包下載下來

## 依賴庫
- python=3.8.12
- streamlit
- PIL
- stqdm
- opencv-contrib-python
- numpy

## 安裝
**要把requirements.txt 中的 opencv-contrib-python-headless 改成opencv-contrib-python**
> pip install -r requirements.txt

## 使用方法
> streamlit run app.py

## 已部屬雲端
[https://wondslic.streamlit.app/](https://wondslic.streamlit.app/)