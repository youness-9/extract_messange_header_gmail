import os

# تحديد المسار إلى الدليل الأصلي
original = 'original'  # استبدل هذا بالمسار الفعلي الخاص بك

# الحصول على قائمة بجميع الملفات في الدليل
cc = os.listdir(original)

# فتح ملف النتيجة لكتابة النتائج
with open("result.txt", "a", encoding="utf-8") as result_file:
    # تمرير كل ملف في الدليل
    for filename in cc:
        # تأكد من أن الملف نصي فقط
        if filename.endswith('.eml'):
            file_path = os.path.join(original, filename)  # إنشاء المسار الكامل للملف
            
            # فتح وقراءة محتوى الملف النصي
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

                # البحث عن آخر سطر يحتوي على "Received"
                received_index = -1
                for i in range(len(lines) - 1, -1, -1):
                    if "Received" in lines[i]:
                        received_index = i
                        break
                
                # البحث عن أول سطر فارغ بعد السطر الذي يحتوي على "Received"
                empty_line_index = -1
                if received_index != -1:
                    for i in range(received_index + 1, len(lines)):
                        if lines[i].strip() == "":  # سطر فارغ أو يحتوي على مسافات فقط
                            empty_line_index = i
                            break

                # استخراج النص بين السطر الذي يأتي بعد "Received" وأول سطر فارغ بعده
                if received_index != -1 and empty_line_index != -1:
                    extracted_text = "".join(lines[received_index + 1:empty_line_index])
                    # كتابة النص المستخرج إلى ملف النتائج
                    result_file.write(f"Extracted from {filename}:\n")
                    result_file.write(extracted_text)
                    result_file.write("\n" + "-" * 40 + "\n")  # فصل بين الملفات
