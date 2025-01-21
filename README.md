# 🛠️ WinFixer Ultimate - أداة إصلاح نظام التشغيل ويندوز | Windows System Repair Tool

![Windows Repair Tool](https://img.shields.io/badge/Windows-Repair%20Tool-blue?style=for-the-badge&logo=windows)
![Python](https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge&logo=python)
![Open Source](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🌍 **الوصف | Description**

### **🔧 WinFixer Ultimate**
أداة قوية ومجانية لإصلاح جميع المشاكل الشائعة وغير الشائعة في أنظمة تشغيل Windows.  
تم تصميم هذه الأداة لمساعدة المستخدمين على تحسين أداء أنظمتهم، إصلاح الأخطاء التقنية، وتنظيف الملفات غير الضرورية باستخدام قائمة شاملة من الأوامر الفعالة.

WinFixer Ultimate is a powerful and free tool designed to fix common and uncommon issues in Windows operating systems.  
This tool helps users optimize system performance, repair technical errors, and clean unnecessary files using a comprehensive list of effective commands.

---

## ✨ **مميزات الأداة | Features**

- **إصلاح شامل لنظام التشغيل Windows.**
- **تنظيف الملفات المؤقتة وغير الضرورية لتحسين الأداء.**
- **إصلاح الشبكة وإعادة تعيين إعدادات DNS.**
- **فحص وإصلاح ملفات النظام التالفة باستخدام أوامر SFC وDISM.**
- **إدارة الطاقة لتحسين الأداء وتقليل استهلاك الموارد.**
- **عرض تقرير شامل ومحدث لحظيًا عن جميع العمليات المنفذة.**
- **جمع معلومات شاملة عن نظام التشغيل والجهاز.**
- **سهولة الاستخدام بدون الحاجة إلى معرفة تقنية متقدمة.**

---

## 🛠️ **الفرق بين النسختين | Differences Between Versions**

| **الميزة**                       | **repair_with_chkdsk.py**                              | **repair_without_chkdsk.py**                       |
|-----------------------------------|-------------------------------------------------------|---------------------------------------------------|
| **`chkdsk /f /r`**                | ✔️ مدعوم (يتطلب إعادة تشغيل لفحص القرص)                | ❌ غير مدعوم (لأداء أسرع)                           |
| **إعادة تشغيل النظام تلقائيًا**   | يتم إعادة تشغيل النظام تلقائيًا بعد الانتهاء.          | يطلب تأكيد المستخدم قبل إعادة التشغيل.            |
| **حذف ملف الحالة JSON**           | ❌ لا يتم الحذف.                                      | ✔️ يتم حذف ملف الحالة بعد انتهاء جميع العمليات.    |
| **أداء الأداة**                   | قد يكون أبطأ بسبب تشغيل `chkdsk`.                     | أسرع بدون `chkdsk`.                               |

---

## 📝 **كيفية الاستخدام | How to Use**

1. قم بتنزيل أحد البرنامجين:  
   - **`repair_with_chkdsk.py`** (لإصلاح شامل يتضمن فحص القرص).  
   - **`repair_without_chkdsk.py`** (لإصلاح سريع بدون فحص القرص).

2. تأكد من تشغيل البرنامج بصلاحيات المسؤول (Admin).  
3. افتح البرنامج من خلال نافذة Command Prompt أو بالنقر المزدوج على الملف.  
4. انتظر حتى يتم تنفيذ جميع العمليات.  
5. تحقق من ملف التقرير **`repair_log.html`** للحصول على التفاصيل.

---

## 📋 **الأوامر المستخدمة | Commands Used**

### **إصلاح النظام | System Repair**
- `DISM /Online /Cleanup-Image /CheckHealth`
- `DISM /Online /Cleanup-Image /ScanHealth`
- `DISM /Online /Cleanup-Image /RestoreHealth`
- `DISM /Online /Cleanup-Image /StartComponentCleanup`
- `SFC /scannow`
- `bootrec /fixmbr`
- `bootrec /fixboot`
- `bootrec /rebuildbcd`

### **تنظيف الملفات | File Cleanup**
- `cleanmgr /sagerun:1`
- `del /s /q %temp%\*`
- `del /s /q C:\Windows\Temp\*`
- `del /s /q C:\Windows\Prefetch\*`

### **إصلاح الشبكة | Network Repair**
- `ipconfig /release`
- `ipconfig /renew`
- `ipconfig /flushdns`
- `netsh int ip reset`
- `netsh winsock reset`

### **تحسين الأداء | Performance Optimization**
- `defrag C: /O`
- `powercfg /hibernate off`
- `winget upgrade --all`

### **إعدادات DNS الافتراضية | Default DNS Settings**
- IPv4:  
  - `8.8.8.8`  
  - `8.8.4.4`  
- IPv6:  
  - `2001:4860:4860::8888`  
  - `2001:4860:4860::8844`

---

## 📂 **التقارير | Reports**

- يتم إنشاء ملف HTML يحتوي على:
  - تفاصيل النظام (اسم الجهاز، نظام التشغيل، تاريخ التثبيت).
  - جميع العمليات التي تم تنفيذها مع حالتها (نجاح/فشل).  
- ملف التقرير يتم تحديثه لحظيًا أثناء تشغيل الأداة.  

---

## 🖼️ **لقطات شاشة | Screenshots**

### **واجهة التقرير HTML**
![HTML Report Screenshot](https://via.placeholder.com/800x400.png?text=HTML+Report+Screenshot)

---

## 📥 **روابط التنزيل | Download Links**

- **[Download repair_with_chkdsk.py](https://github.com/FahadMAlsamiti/WinFixer-Ultimate)**
- **[Download repair_without_chkdsk.py](https://github.com/FahadMAlsamiti/WinFixer-Ultimate)**

---

## ⚖️ **الرخصة | License**

هذا المشروع مفتوح المصدر تحت رخصة MIT.  
This project is open source under the MIT License.

---

## 🤝 **المساهمة | Contributing**

مرحب بجميع المساهمات لتحسين المشروع!  
Contributions to enhance the project are welcome!

---

## 📧 **للتواصل | Contact**

- **En.FahadAlsamiti**  
- [📧 Fahad's X Profile](https://x.com/fahadalsamiti)  
- [📧 Fahad's GitHub](https://github.com/FahadMAlsamiti)
