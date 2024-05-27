#final_calc_emags
import math
import customtkinter as ctk

class ElectricForceCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Electric Force Calculator")
        self.geometry("710x765")
        self.resizable(False, False)

        # Configure style
        self.configure_style()

        self.initUI()

    def configure_style(self):
        # Configure default font and background color
        ctk.CTk.configure(self, font=("Arial", 10), background="#f0f0f0")

    def initUI(self):
        # Dielectric Constant
        dielectric_frame = ctk.CTkFrame(self)
        dielectric_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.dielectric_label = ctk.CTkLabel(dielectric_frame, text="ϵr (Relative Permittivity):   ")
        self.dielectric_input = ctk.CTkEntry(dielectric_frame, width=120)
        self.dielectric_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.dielectric_input.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Charge Exerting Force
        q1_frame = ctk.CTkFrame(self)
        q1_frame.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.q1_label = ctk.CTkLabel(q1_frame, text="Charge Exert Force Of:      ")
        self.q1_input = ctk.CTkEntry(q1_frame, width=120)
        self.q1_label.grid(row=0, column=0, padx=8, pady=10, sticky="w")
        self.q1_input.grid(row=0, column=1, padx=11, pady=10, sticky="w")

        # Q1 Position
        q1_position_frame = ctk.CTkFrame(self)
        q1_position_frame.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.x_pos_q1_label = ctk.CTkLabel(q1_position_frame, text="•Q1 X-Position:      ")
        self.x_pos_q1_input = ctk.CTkEntry(q1_position_frame, width=120)
        self.y_pos_q1_label = ctk.CTkLabel(q1_position_frame, text="•Q1 Y-Position:      ")
        self.y_pos_q1_input = ctk.CTkEntry(q1_position_frame, width=120)
        self.z_pos_q1_label = ctk.CTkLabel(q1_position_frame, text="•Q1 Z-Position:      ")
        self.z_pos_q1_input = ctk.CTkEntry(q1_position_frame, width=120)
        self.x_pos_q1_label.grid(row=0, column=0, padx=22, pady=5, sticky="w")
        self.x_pos_q1_input.grid(row=0, column=1, padx=22, pady=5)
        self.y_pos_q1_label.grid(row=1, column=0, padx=22, pady=5, sticky="w")
        self.y_pos_q1_input.grid(row=1, column=1, padx=22, pady=5)
        self.z_pos_q1_label.grid(row=2, column=0, padx=22, pady=5, sticky="w")
        self.z_pos_q1_input.grid(row=2, column=1, padx=22, pady=5)

        # Charge Receiving Force
        q2_frame = ctk.CTkFrame(self)
        q2_frame.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.q2_label = ctk.CTkLabel(q2_frame, text="Charge Receives Force Of:")
        self.q2_input = ctk.CTkEntry(q2_frame, width=120)
        self.q2_label.grid(row=0, column=0, padx=8, pady=10, sticky="w")
        self.q2_input.grid(row=0, column=1, padx=11, pady=10, sticky="w")

        # Q2 Position
        q2_position_frame = ctk.CTkFrame(self)
        q2_position_frame.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.x_pos_q2_label = ctk.CTkLabel(q2_position_frame, text="•Q2 X-Position:      ")
        self.x_pos_q2_input = ctk.CTkEntry(q2_position_frame, width=120)
        self.y_pos_q2_label = ctk.CTkLabel(q2_position_frame, text="•Q2 Y-Position:      ")
        self.y_pos_q2_input = ctk.CTkEntry(q2_position_frame, width=120)
        self.z_pos_q2_label = ctk.CTkLabel(q2_position_frame, text="•Q2 Z-Position:      ")
        self.z_pos_q2_input = ctk.CTkEntry(q2_position_frame, width=120)
        self.x_pos_q2_label.grid(row=0, column=0, padx=25, pady=5, sticky="w")
        self.x_pos_q2_input.grid(row=0, column=1, padx=25, pady=5)
        self.y_pos_q2_label.grid(row=1, column=0, padx=25, pady=5, sticky="w")
        self.y_pos_q2_input.grid(row=1, column=1, padx=25, pady=5)
        self.z_pos_q2_label.grid(row=2, column=0, padx=25, pady=5, sticky="w")
        self.z_pos_q2_input.grid(row=2, column=1, padx=25, pady=5)
        permitivity_frame = ctk.CTkFrame(self)
        permitivity_frame.grid(row=0, column=1, rowspan=7, padx=20, pady=10, sticky="nsew")

        materials = [
            ("Material", "Relative Permittivity"),
            ("Vacuum", "1 "),
            ("Air", "~1"),
            ("Teflon (PTFE)", "~2.1"),
            ("Paper", "~3.5"),
            ("FR4 (PCB Substrate)", "~4.5"),
            ("Water", "~80"),
            ("Glass", "~4-10"),
            ("Ceramic", "~5-200"),
            ("Silicon", "~11.7"),
            ("Polyethylene", "~2.25-2.4"),
            ("Paraffin wax", "~2.1-2.4"),
            ("Concrete", "~4-8.5"),
            ("Aluminum oxide", "~8.4-11"),
            ("Bakelite", "~3.3-5"),
            ("Polystyrene", "~2.4-2.7"),
            ("Quartz", "~3.8-4.5"),
            ("Wood", "~1.5-3.9"),
            ("Mica", "~3-6"),
            ("Diamond", "~5.5"),

            ("Sapphire", "~8.5")
        ]
        for i, (material, permitivity) in enumerate(materials):
            material_label = ctk.CTkLabel(permitivity_frame, text=material)
            permitivity_label = ctk.CTkLabel(permitivity_frame, text=permitivity)

            if material == "Material" or permitivity == "Relative Permittivity":
                material_label.configure(font=("Courier", 13, "bold"))
                permitivity_label.configure(font=("Courier", 13, "bold"))

            material_label.grid(row=i, column=0, padx=5, pady=2, sticky="w")
            permitivity_label.grid(row=i, column=1, padx=5, pady=2, sticky="we")

        # Result Display
        self.result_display = ctk.CTkTextbox(self, height=100, width=320)
        self.result_display.grid(row=5, column=0, padx=20, pady=10, sticky="w")

        # Calculate Button
        self.calculate_button = ctk.CTkButton(self, text="Calculate", command=self.calculate, width=320)
        self.calculate_button.grid(row=6, column=0, padx=20, pady=10, sticky="w")

        self.clear_button = ctk.CTkButton(self, text="Clear", command=self.clear_fields, width=320)
        self.clear_button.grid(row=7, column=0, padx=20, pady=10, sticky="w")

    def clear_fields(self):
        # Clear all input fields and result display
        self.dielectric_input.delete(0, 'end')
        self.q1_input.delete(0, 'end')
        self.x_pos_q1_input.delete(0, 'end')
        self.y_pos_q1_input.delete(0, 'end')
        self.z_pos_q1_input.delete(0, 'end')
        self.q2_input.delete(0, 'end')
        self.x_pos_q2_input.delete(0, 'end')
        self.y_pos_q2_input.delete(0, 'end')
        self.z_pos_q2_input.delete(0, 'end')
        self.result_display.delete("1.0", "end")


    def calculate(self):
        DIELECTRIC_CONSTANT = float(self.dielectric_input.get())

        Q1 = float(self.q1_input.get())
        X_POS_Q1 = float(self.x_pos_q1_input.get())
        Y_POS_Q1 = float(self.y_pos_q1_input.get())
        Z_POS_Q1 = float(self.z_pos_q1_input.get())

        Q2 = float(self.q2_input.get())
        X_POS_Q2 = float(self.x_pos_q2_input.get())
        Y_POS_Q2 = float(self.y_pos_q2_input.get())
        Z_POS_Q2 = float(self.z_pos_q2_input.get())

        DISPLACEMENT_X_OPP = X_POS_Q1 - X_POS_Q2
        DISPLACEMENT_Y_OPP = Y_POS_Q1 - Y_POS_Q2
        DISPLACEMENT_Z_OPP = Z_POS_Q1 - Z_POS_Q2

        DISPLACEMENT_X_SAME = X_POS_Q2 - X_POS_Q1
        DISPLACEMENT_Y_SAME = Y_POS_Q2 - Y_POS_Q1
        DISPLACEMENT_Z_SAME = Z_POS_Q2 - Z_POS_Q1

        VECTOR_MAGNITUDE = float(pythag(DISPLACEMENT_X_SAME, DISPLACEMENT_Y_SAME, DISPLACEMENT_Z_SAME))
        DIRECTION_FORCE_OPP = DISPLACEMENT_X_OPP / VECTOR_MAGNITUDE, DISPLACEMENT_Y_OPP / VECTOR_MAGNITUDE, DISPLACEMENT_Z_OPP / VECTOR_MAGNITUDE
        DIRECTION_FORCE_SAME = DISPLACEMENT_X_SAME / VECTOR_MAGNITUDE, DISPLACEMENT_Y_SAME / VECTOR_MAGNITUDE, DISPLACEMENT_Z_SAME / VECTOR_MAGNITUDE
        EO = 8.854E-12
        KCONSTANT = 9E9
        DIELECTRIC = (1) / (4 * 3.1416 * EO * DIELECTRIC_CONSTANT)
        QTOTAL = Q1 * Q2

        if DIELECTRIC_CONSTANT == 1 and QTOTAL >= 0:
            ELECTRIC_FORCE = ((KCONSTANT * abs(QTOTAL)) / (VECTOR_MAGNITUDE ** 2))
            ELECTRIC_FORCE_VECTOR = (DISPLACEMENT_X_SAME / VECTOR_MAGNITUDE) * ELECTRIC_FORCE, (
                    DISPLACEMENT_Y_SAME / VECTOR_MAGNITUDE) * ELECTRIC_FORCE, (
                                            DISPLACEMENT_Z_SAME / VECTOR_MAGNITUDE) * ELECTRIC_FORCE
            result = f'ELECTRIC_FORCE: {round(ELECTRIC_FORCE, 4)} N\n' \
                     f'DIRECTION OF FORCE: {tuple(round(coord, 4) for coord in DIRECTION_FORCE_SAME)} m\n' \
                     f'ELECTRIC FORCE VECTOR: {tuple(round(coord, 4) for coord in ELECTRIC_FORCE_VECTOR)} Nm'

        elif DIELECTRIC_CONSTANT != 1 and QTOTAL >= 0:
            ELECTRIC_FORCE = ((DIELECTRIC * abs(QTOTAL)) / (VECTOR_MAGNITUDE ** 2))
            ELECTRIC_FORCE_VECTOR = (DISPLACEMENT_X_SAME / VECTOR_MAGNITUDE) * ELECTRIC_FORCE, (
                    DISPLACEMENT_Y_SAME / VECTOR_MAGNITUDE) * ELECTRIC_FORCE, (
                                            DISPLACEMENT_Z_SAME / VECTOR_MAGNITUDE) * ELECTRIC_FORCE
            result = f'ELECTRIC_FORCE: {round(ELECTRIC_FORCE, 4)} N\n' \
                     f'DIRECTION OF FORCE: {tuple(round(coord, 4) for coord in DIRECTION_FORCE_SAME)} m\n' \
                     f'ELECTRIC FORCE VECTOR: {tuple(round(coord, 4) for coord in ELECTRIC_FORCE_VECTOR)} Nm'

        elif DIELECTRIC_CONSTANT == 1 and QTOTAL < 0:
            ELECTRIC_FORCE = ((KCONSTANT * abs(QTOTAL)) / (VECTOR_MAGNITUDE ** 2))
            ELECTRIC_FORCE_VECTOR = (DISPLACEMENT_X_OPP / VECTOR_MAGNITUDE) * ELECTRIC_FORCE, (
                    DISPLACEMENT_Y_OPP / VECTOR_MAGNITUDE) * ELECTRIC_FORCE, (
                                            DISPLACEMENT_Z_OPP / VECTOR_MAGNITUDE) * ELECTRIC_FORCE
            result = f'ELECTRIC_FORCE: {round(ELECTRIC_FORCE, 4)} N\n' \
                     f'DIRECTION OF FORCE: {tuple(round(coord, 4) for coord in DIRECTION_FORCE_SAME)} m\n' \
                     f'ELECTRIC FORCE VECTOR: {tuple(round(coord, 4) for coord in ELECTRIC_FORCE_VECTOR)} Nm'

        else:
            ELECTRIC_FORCE = ((DIELECTRIC * abs(QTOTAL)) / (VECTOR_MAGNITUDE ** 2))
            ELECTRIC_FORCE_VECTOR = (DISPLACEMENT_X_OPP / VECTOR_MAGNITUDE) * ELECTRIC_FORCE, (
                    DISPLACEMENT_Y_OPP / VECTOR_MAGNITUDE) * ELECTRIC_FORCE, (
                                            DISPLACEMENT_Z_OPP / VECTOR_MAGNITUDE) * ELECTRIC_FORCE
            result = f'ELECTRIC_FORCE: {round(ELECTRIC_FORCE, 4)} N\n' \
                     f'DIRECTION OF FORCE: {tuple(round(coord, 4) for coord in DIRECTION_FORCE_SAME)} m\n' \
                     f'ELECTRIC FORCE VECTOR: {tuple(round(coord, 4) for coord in ELECTRIC_FORCE_VECTOR)} Nm'

        # Clear previous result
        self.result_display.delete("1.0", "end")
        # Display new result
        self.result_display.insert("end", result)
    pass


def pythag(a, b, c):
    summation = a * a + b * b + c * c
    qwert = math.sqrt(summation)
    return qwert

if __name__ == "__main__":
    app = ElectricForceCalculator()
    app.mainloop()
