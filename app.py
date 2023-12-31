import streamlit as st
import cv2
import numpy as np
import os   
from PIL import Image 
from stqdm import stqdm


# img 格式一律用RGB
states = ["stage","select_picture","img","go","result","download_btn","UpperbH","LowerbH","UpperbS","LowerbS","UpperbV","LowerbV"]
for state in states:
    if state not in st.session_state:
        st.session_state[state] = ""
        if state == "stage":
            st.session_state[state] = 0

def renderimg():
    if str(st.session_state.img) != "":
        with st.container():
            st.image(st.session_state.img,use_column_width="always")

def chang_stage(i):
    st.session_state["stage"] = i

def slic(image,num_superpixels,num_levels,num_iter,output_directory = 'output_images'):
    # print(image,num_superpixels,num_levels,num_iter)
    pic = Image.open(image)
    cv_image = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2Lab)

    slic = cv2.ximgproc.createSuperpixelSLIC(cv_image, cv2.ximgproc.SLIC, num_superpixels, num_levels)
    slic.iterate(num_iter)  # 迭代次數
    # 獲取超像素分割結果
    labels = slic.getLabels()

    # 創建一個目錄來保存輸出圖像
    
    os.makedirs(output_directory, exist_ok=True)    
    
    # 獲取已存在的輸出圖像數量
    # existing_output_images = [f for f in os.listdir(output_directory) if f.startswith('output_image')]
    existing_output_images = [f for f in os.listdir(output_directory)]
    next_image_index = len(existing_output_images)

    # 顏色分類
    unique_labels = np.unique(labels)
    for  label in stqdm(unique_labels,st_container=st.sidebar):
        # 提取每個超像素的平均顏色
        mask = (labels == label)
        mean_color = np.mean(cv_image[mask], axis=0)
        # print(mean_color)
        # 在圖像上繪製超像素的平均顏色區域
        cv_image[mask] = mean_color
    # 假如是一般調用，顯示結果
    if output_directory == 'output_images':
        st.session_state.img = cv2.cvtColor(cv_image,cv2.COLOR_LAB2RGB)
    # 暫存結果
    tmp = cv2.cvtColor(cv_image,cv2.COLOR_LAB2RGB)
    # 保存結果，使用不同的文件名
    output_filename = os.path.join(output_directory, f'output_image{next_image_index}.jpeg' if output_directory == 'output_images' else f'{image.name}')
    # CV2 統一用BGR做儲存
    cv2.imwrite(output_filename, cv2.cvtColor(tmp,cv2.COLOR_RGB2BGR))

def set_download_btn():
    st.session_state.download_btn = True

def process_HSV():
    try:
        img_hsv=cv2.cvtColor(st.session_state.img,cv2.COLOR_RGB2HSV)
    except:
        return
    # 定義 HSV 上下限
    lower_bound = np.array([st.session_state.LowerbH, st.session_state.LowerbS, st.session_state.LowerbV])
    upper_bound = np.array([st.session_state.UpperbH, st.session_state.UpperbS, st.session_state.UpperbV])
    # 建立二值掩模，根據顏色範圍篩選影像
    mask = cv2.inRange(img_hsv, lower_bound, upper_bound)
    img = cv2.cvtColor(st.session_state.img,cv2.COLOR_RGB2BGR)
    result = cv2.bitwise_and(img, img, mask=mask)
    st.session_state.result = cv2.cvtColor(result,cv2.COLOR_BGR2RGB)
    st.image(st.session_state.result,use_column_width="always")


st.sidebar.title("域值標註工具")
st.sidebar.write("## 請先上傳圖片")
uploaded_files = st.sidebar.file_uploader("Select a Image", type=['png', 'jpeg', 'jpg'], accept_multiple_files=True)
num_of_image = len(uploaded_files)

if num_of_image != 0 :
    render = st.sidebar.toggle("顯示圖片",on_change=chang_stage,args=[st.session_state["stage"]])
    for uploaded_file in uploaded_files:
        st.sidebar.write(uploaded_file.name)
        if render:
            st.sidebar.image(uploaded_file,use_column_width="always")
    st.session_state.select_picture = st.sidebar.selectbox('選擇圖片',[uploaded_file.name for uploaded_file in uploaded_files],on_change=chang_stage,args=[0])
    num_superpixels = st.sidebar.slider("超像素數量",10,200,50,step=10,on_change=chang_stage,args=[0])  # 超像素的數量 1~200
    num_levels      = st.sidebar.slider("金字塔層級數",1,10,4,step=1,on_change=chang_stage,args=[0])  # 金字塔的層級數 固定
    num_iter        = st.sidebar.slider("迭代次數",1,100,10,step=1,on_change=chang_stage,args=[0]) # 迭代次數
    
    st.session_state.go = st.sidebar.button(":star: SLIC",on_click=chang_stage,args=[1])
if st.session_state.go:
    slic([ uploaded_file for uploaded_file in uploaded_files if uploaded_file.name == st.session_state.select_picture][0]
                            ,num_superpixels,num_levels,num_iter)
    st.balloons()

import downloader      
if st.session_state["stage"] >= 1:
    renderimg()
    if str(st.session_state.img) != "":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.UpperbH = st.slider("UpperbH",0.0,255.0,255.0,step=0.1,on_change=chang_stage,args=[2])
            st.session_state.LowerbH = st.slider("LowerbH",0.0,255.0,0.0,step=0.1,on_change=chang_stage,args=[2])
        with col2:
            st.session_state.UpperbS = st.slider("UpperbS",0.0,255.0,255.0,step=0.1,on_change=chang_stage,args=[2])
            st.session_state.LowerbS = st.slider("LowerbS",0.0,255.0,0.0,step=0.1,on_change=chang_stage,args=[2])
        with col3:
            st.session_state.UpperbV = st.slider("UpperbV",0.0,255.0,255.0,step=0.1,on_change=chang_stage,args=[2])
            st.session_state.LowerbV = st.slider("LowerbV",0.0,255.0,0.0,step=0.1,on_change=chang_stage,args=[2])
        
        # FIXME: 批量處理
        one_click_slic = st.sidebar.button(":star2: 一鍵處理",on_click=chang_stage,args=[2])
        if one_click_slic:
            for uploaded_file in uploaded_files:
                # print(uploaded_file.name)
                slic(uploaded_file,num_superpixels,num_levels,num_iter,output_directory = 'all_output_images')    
            st.balloons()
            # 壓縮all_output_images資料夾
            downloader.zip_folder("all_output_images","all_output_images.zip")
            # 下載all_output_images.zip
            with open("all_output_images.zip", "rb") as fp:
                download_btn = st.sidebar.download_button(
                    label=":rocket: Download ZIP",
                    data=fp,
                    file_name="all_output_images.zip",
                    mime="application/zip",
                    on_click= set_download_btn
                )
        if  st.session_state.download_btn:
            # 刪除all_output_images資料夾
            import shutil
            shutil.rmtree("all_output_images")
            # 刪除all_output_images.zip
            os.remove("all_output_images.zip")
            # print("刪除all_output_images資料夾")
            st.session_state.download_btn = False


if st.session_state["stage"] >= 2:
    process_HSV()

