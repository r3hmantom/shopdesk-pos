import customtkinter as ctk
from tkinter import messagebox

def build_register_frame(root, auth_controller, on_back_click):
    frame = ctk.CTkFrame(root, corner_radius=0)
    
    # Center Box
    reg_box = ctk.CTkFrame(frame, width=500, corner_radius=15)
    reg_box.place(relx=0.5, rely=0.5, anchor="center")

    title = ctk.CTkLabel(reg_box, text="Create Account", font=("Roboto Medium", 26))
    title.pack(pady=(30, 20))

    # Grid for inputs
    input_frame = ctk.CTkFrame(reg_box, fg_color="transparent")
    input_frame.pack(pady=10, padx=40)

    first_name = ctk.CTkEntry(input_frame, placeholder_text="First Name", width=200)
    first_name.grid(row=0, column=0, padx=10, pady=10)
    
    last_name = ctk.CTkEntry(input_frame, placeholder_text="Last Name", width=200)
    last_name.grid(row=0, column=1, padx=10, pady=10)

    phone = ctk.CTkEntry(input_frame, placeholder_text="Phone Number", width=200)
    phone.grid(row=1, column=0, padx=10, pady=10)

    cnic = ctk.CTkEntry(input_frame, placeholder_text="CNIC", width=200)
    cnic.grid(row=1, column=1, padx=10, pady=10)

    username = ctk.CTkEntry(input_frame, placeholder_text="Username", width=420)
    username.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    password = ctk.CTkEntry(input_frame, placeholder_text="Password", show="*", width=420)
    password.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    role_var = ctk.StringVar(value="Cashier")
    role_combo = ctk.CTkComboBox(input_frame, values=["Cashier", "Manager", "Admin"], variable=role_var, width=420)
    role_combo.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def createAcc():
        u = username.get()
        p = password.get()
        fn = first_name.get()
        ln = last_name.get()
        ph = phone.get()
        c = cnic.get()
        role = role_var.get()

        if not u or not p:
            messagebox.showerror("Error", "Username and Password are required")
            return

        success, message = auth_controller.register(u, p, role, fn, ln, ph, c)
        if success:
            messagebox.showinfo("Success", message)
            on_back_click()
        else:
            messagebox.showerror("Error", message)

    btn_reg = ctk.CTkButton(reg_box, text="Sign Up", width=420, height=40, font=("Roboto Medium", 15), command=createAcc)
    btn_reg.pack(pady=20)

    btn_back = ctk.CTkButton(reg_box, text="Back to Login", fg_color="transparent", text_color="gray", hover_color="#eee", command=on_back_click)
    btn_back.pack(pady=(0, 20))

    return frame
