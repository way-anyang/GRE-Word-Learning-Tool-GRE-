# GRE词汇整理表及背诵小程序

## GRE词汇整理表
特别鸣谢：词汇表整理自《再要你命3000》（单词、释义），《学而思GRE填空核心3000词Excel版》（例句），三列内容分别为：单词-释义-例句
部分单词缺少例句（但不缺少释义），正在持续更新中……
每个单词的不同释义在不同行展示

## 背诵小程序
仅支持python
### 使用方法
·下载py文件，选择打开方式为“python”，双击运行即可（推荐）

·Windows系统：win+R，输入cmd，运行指令：py word_gui.py【注意文件位置】

·linux：py word_gui.py【注意文件位置】

【注意：本地运行，需要同时下载词汇表xlsx文件和word_gui.py 文件，下载原始xlsx文件之后，建议下载到桌面，否则需要手动修改小程序中的“EXCEL_PATH 常量”为文件地址】

### 内容
#### 背诵模式
<img width="849" height="555" alt="image" src="https://github.com/user-attachments/assets/7316eefa-81b6-4853-8c57-bbdb3bcddb87" />

如上图，展示单词、释义、例句。

#### 选择题（单选）
<img width="850" height="811" alt="image" src="https://github.com/user-attachments/assets/e40b2b5e-b0b3-43e6-996b-8ce20086ad67" />

如上图，在四个选项中挑选一个，若正确：

<img width="850" height="814" alt="image" src="https://github.com/user-attachments/assets/ded28f40-75b1-42ba-b0f8-ed09fffad2d4" />

若错误：

<img width="849" height="803" alt="image" src="https://github.com/user-attachments/assets/05135fa3-2888-42b0-8561-2ac2b461c3ae" />

#### 填空题

<img width="850" height="631" alt="image" src="https://github.com/user-attachments/assets/2189aaa1-ecca-4f9c-867a-63bc9ba34027" />

如上图，输入正确答案即可。

### 按键
中间四个按键依次为：学习、选择题、填空题、下一题，用于选择模式：

<img width="332" height="65" alt="image" src="https://github.com/user-attachments/assets/33baee8a-f979-43a1-80e9-cdbf063db37f" />

最下方有一个“掌握”按键，用于确认此单词已经学会，日后将不会出现在学习、选择题、填空题中：
<img width="107" height="57" alt="image" src="https://github.com/user-attachments/assets/7fa69fda-ca28-4dcf-80f8-7b0b639acf45" />


填空题下方有“提交”按钮

<img width="1170" height="77" alt="image" src="https://github.com/user-attachments/assets/e5c6ab65-5d82-4086-bc48-c897d62a2720" />

所有按键的功能皆如字面意思。

## 网页运行
网页源代码在word_app.py

由Streamlit Cloud支持
#### 网址为：https://gzdawbflaz3z6ucvphbx9x.streamlit.app/
进入页面：

<img width="1113" height="422" alt="image" src="https://github.com/user-attachments/assets/4d507222-6658-42ab-bd74-ee517c85de2b" />

学习模式：

<img width="871" height="541" alt="image" src="https://github.com/user-attachments/assets/7e9b11ac-65ed-40c2-889b-6804da53b85d" />

选择题模式：

<img width="786" height="790" alt="image" src="https://github.com/user-attachments/assets/1d80d275-ea70-4458-88e7-ddfc440aa9a1" />

填空题模式：

<img width="1043" height="846" alt="image" src="https://github.com/user-attachments/assets/0000ced4-c5b3-4e64-a669-70ce34ad2a14" />

网页按键与上述基本一致，不再赘述。


