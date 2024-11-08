import tkinter
import tkinter as tk
import cv2
from tkinter import filedialog

def read_qr_code_dialog():
    global entry
    dialog = tk.Toplevel()
    dialog.title("Input path of the QR code")

    label = tk.Label(dialog, text="Enter your path of the QR code")
    label.pack()

    entry_path = tk.Entry(dialog)
    entry_path.pack()

    def get_path():
        global entry
        entry = entry_path.get()
        dialog.destroy()

    button = tk.Button(dialog, text="after input the path,please click", command=get_path)
    button.pack()

    dialog.wait_window()
    d = cv2.QRCodeDetector()
    if not entry:
        print("Error: Entry is empty.")
        return
    datapath1 = entry
    datapath2 = datapath1
    name = datapath2.split('\\')[-1]

    text_area.config(state=tk.NORMAL)
    # Clear the contents of the text area from the first character of the first line to
    # the end of the text
    text_area.delete("1.0", tk.END)
    # Insert a message prompting the user to enter a valid number, at
    # the end of the current content

    text_area.insert(tk.END, f"the directory of the QR code：{datapath1}\n")
    caps_val = d.detectAndDecode(cv2.imread(datapath1))  # 绝对路径也可
    text1 = caps_val[0]

    text_area.insert(tk.END, f"the information of the QR code：{text1}\n")
    text_area.config(state=tk.DISABLED)


def read_qr_code_window():
    file_path = filedialog.askopenfilename(title="Select QR Code File",
                                           filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
    print("Selected file path:", file_path)  # Add this line to print the file path
    img = cv2.imread(file_path)
    detector = cv2.QRCodeDetector()
    decoded_info, points, straight_qrcode = detector.detectAndDecode(img)
    text_area.config(state=tk.NORMAL)
    if decoded_info:
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END,
                         f'the information of the QR code：{decoded_info}\n，the directory of the QR code：\n{file_path}')
    else:
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, "No QR code detected")


def read_qr_code_camera():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    data_written = False

    while True:
        _, img = cap.read()
        data, bbox, _ = detector.detectAndDecode(img)

        if bbox is not None:
            n_lines = len(bbox[0])
            for i in range(n_lines):
                point1 = tuple(map(int, bbox[0][i]))
                point2 = tuple(map(int, bbox[0][(i + 1) % n_lines]))
                cv2.line(img, point1, point2, (255, 0, 255), thickness=10)

        if data and not data_written:
            text_area.config(state=tk.NORMAL)
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, f'the information of the QR code：\n{data}\n')
            text_area.config(state=tk.DISABLED)
            data_written = True

        cv2.imshow("vediocamera", img)

        if data_written:
            break

        if cv2.waitKey(200) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


root = tk.Tk()

root.title("read_qr_code")
root.geometry("600x500")

text_area = tk.Text(root, height=10, width=40)
text_area.pack(padx=10, pady=10)

text_area.config(state=tk.NORMAL)
text_area.delete("1.0", tk.END)
text_area.insert(tk.END, f"please choose a method to read the QR code：\n"
                         f"read_qr_path\t read_qr_window \t read_qr_camera\n")
text_area.config(state=tk.DISABLED)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# button1 = tk.Button(cap_convert_low_frame, text="read_qr_code", command=read_qr_code)
# button1.pack()

read_var_path = tkinter.Button(frame, text="read_qr_path", command=read_qr_code_dialog)
read_var_path.pack(side='left')

read_var_window = tkinter.Button(frame, text="read_qr_window", command=read_qr_code_window)
read_var_window.pack(side='left')

read_qr_code_camera = tk.Button(frame, text="read_qr_code_camera", command=read_qr_code_camera)
read_qr_code_camera.pack()

root.mainloop()
