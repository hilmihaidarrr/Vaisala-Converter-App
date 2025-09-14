## 📌 About – Vaisala Converter App

**Vaisala Converter App** is a **Python-based desktop application (Tkinter/CustomTkinter)** designed to simplify the process of converting raw data from the **Vaisala WXT520 weather sensor**. Typically, the sensor outputs data in **ASCII (.txt)** format, which can be difficult to interpret directly. This application provides a clean and user-friendly interface to convert raw logs into more accessible formats:

* **CSV (Comma-Separated Values)** → Easily analyzed using tools like **Excel**, **Pandas**, or other statistical software.
* **MH2 (Meteorological Data Format for PC-COSYMA)** → A standard format that can be directly used as input for **PC-COSYMA** in nuclear dispersion simulations.

### ✨ Key Features

* 🔄 **Automatic Conversion** from `.txt` to both **.csv** and **.mh2**.
* 📂 **Batch Processing** to convert multiple files at once.
* 🖥️ **Modern GUI** built with **CustomTkinter** for an intuitive user experience.
* 📜 **Accurate Data Parsing** powered by a custom `txt_to_csv.py` parser.
* 🧹 **Data Cleaning** to ensure the converted output is structured and ready for further analysis.

### 🎯 Purpose

The application was developed to support research on **radioactive substance dispersion modeling** at **BRIN (National Research and Innovation Agency, Indonesia)** by:

* Providing **readable meteorological datasets** from Vaisala WXT520 sensors.
* Streamlining the workflow for researchers to prepare input data for **PC-COSYMA** and other analysis tools.
