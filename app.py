import threading
import time
import tkinter as tk
import serial

SERIAL_PORT = "COM3"  # À adapter ("COMx" sous Windows ou "/dev/ttyUSB0" sous Linux)
BAUD_RATE = 9600

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2)
except Exception as e:
    print(f"Arduino non détecté ({e}), passage en mode simulation.")
    arduino = None


# --- GESTION DE L'ÉTAT DE L'INTERFACE ---
def verrouiller_interface():
    """Désactive le bouton et les sélecteurs pendant la distribution."""
    btn_commander.config(state="disabled", text="Distribution en cours...", bg="#A5D6A7")
    spin_r1.config(state="disabled")
    spin_r2.config(state="disabled")
    spin_r3.config(state="disabled")


def deverrouiller_interface():
    """Réactive l'interface une fois la commande terminée."""
    btn_commander.config(state="normal", text="Valider la commande", bg="#4CAF50")
    spin_r1.config(state="normal")
    spin_r2.config(state="normal")
    spin_r3.config(state="normal")


# --- LOGIQUE D'ENVOI ---
def envoyer_commande():
    qte1 = spin_r1.get()
    qte2 = spin_r2.get()
    qte3 = spin_r3.get()

    total = int(qte1) + int(qte2) + int(qte3)
    if total == 0:
        log_message("Sélectionne au moins 1 bonbon.")
        return

    # Verrouillage immédiat dès le clic
    verrouiller_interface()

    commande = f"CMD:{qte1},{qte2},{qte3}\n"

    if arduino and arduino.is_open:
        arduino.write(commande.encode("utf-8"))
        log_message(f"Envoyé à l'Arduino : R1={qte1}, R2={qte2}, R3={qte3}")
    else:
        # Simulation : déverrouillage automatique après 3 secondes si pas d'Arduino branché
        log_message(f"[SIMU] Envoi : {commande.strip()}")
        root.after(3000, simuler_fin_commande)


def simuler_fin_commande():
    log_message("[SIMU] Distribution terminée.")
    deverrouiller_interface()


def log_message(txt: str):
    text_log.insert(tk.END, f"{txt}\n")
    text_log.see(tk.END)


def traiter_ligne_arduino(ligne: str):
    log_message(f"Arduino > {ligne}")
    
    # Détection de la fin du travail côté Arduino
    if ligne == "COMMANDE_TERMINEE":
        deverrouiller_interface()


def lecture_serie():
    """Écoute continue du port série en arrière-plan."""
    while True:
        if arduino and arduino.is_open:
            try:
                line = arduino.readline().decode("utf-8", errors="ignore").strip()
                if line:
                    # Exécute la mise à jour UI sur le thread principal de Tkinter
                    root.after(0, traiter_ligne_arduino, line)
            except Exception:
                break
        time.sleep(0.05)


# --- INTERFACE TKINTER ---
root = tk.Tk()
root.title("Candy Dispenser - Commande")
root.geometry("390x380")
root.resizable(False, False)

tk.Label(root, text="Choisis tes bonbons", font=("Helvetica", 13, "bold")).pack(pady=10)

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=5)

# Réservoir 1
tk.Label(frame_inputs, text="Réservoir 1 (Menthe) :", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", pady=4, padx=5)
spin_r1 = tk.Spinbox(frame_inputs, from_=0, to=10, width=5, font=("Helvetica", 10))
spin_r1.grid(row=0, column=1, pady=4)

# Réservoir 2
tk.Label(frame_inputs, text="Réservoir 2 (Fraise) :", font=("Helvetica", 10)).grid(row=1, column=0, sticky="w", pady=4, padx=5)
spin_r2 = tk.Spinbox(frame_inputs, from_=0, to=10, width=5, font=("Helvetica", 10))
spin_r2.grid(row=1, column=1, pady=4)

# Réservoir 3
tk.Label(frame_inputs, text="Réservoir 3 (Citron) :", font=("Helvetica", 10)).grid(row=2, column=0, sticky="w", pady=4, padx=5)
spin_r3 = tk.Spinbox(frame_inputs, from_=0, to=10, width=5, font=("Helvetica", 10))
spin_r3.grid(row=2, column=1, pady=4)

# Bouton de commande (référence accessible globalement)
btn_commander = tk.Button(
    root,
    text="Valider la commande",
    bg="#4CAF50",
    fg="white",
    font=("Helvetica", 11, "bold"),
    padx=10,
    pady=5,
    command=envoyer_commande,
)
btn_commander.pack(pady=12)

# Console de suivi
text_log = tk.Text(root, height=8, width=44, font=("Consolas", 9), bg="#F2F2F2")
text_log.pack(padx=10, pady=5)

# Thread pour surveiller la réponse Arduino
threading.Thread(target=lecture_serie, daemon=True).start()

root.mainloop()