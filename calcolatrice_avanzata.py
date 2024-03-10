import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import math
from tkinter.filedialog import asksaveasfilename
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# Setup della GUI principale
root = tk.Tk()
root.title("Calcolatrice Avanzata")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

tab1 = ttk.Frame(notebook)  # Matematica di Base
tab2 = ttk.Frame(notebook)  # Finanza
tab3 = ttk.Frame(notebook)  # Fisica
tab4 = ttk.Frame(notebook)  # Salva come PDF
notebook.add(tab1, text='Matematica di Base')
notebook.add(tab2, text='Finanza')
notebook.add(tab3, text='Fisica')
notebook.add(tab4, text='Salva come PDF')
# Inizializzazione dell'area di testo per ciascun tab
text_areas = {tab1: None, tab2: None, tab3: None, tab4: None}
for tab in [tab1, tab2, tab3, tab4 ]:
    text_area = tk.Text(tab, height=15, state='disabled')
    text_area.pack(expand=True, fill='both')
    text_areas[tab] = text_area

def update_text_area(tab, text):
    text_area = text_areas[tab]
    text_area.configure(state='normal')
    text_area.insert(tk.END, text + "\n")
    text_area.configure(state='disabled')
    text_area.see(tk.END)

def salva_pdf(text, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter  # Larghezza e altezza della pagina per letter
    
    # Inizializza le coordinate iniziali per il testo
    x = 100  # Margine sinistro
    y = height - 100  # Margine superiore (parte dall'alto)
    line_height = 14  # Altezza di ogni linea di testo
    
    for line in text.split('\n'):
        if y < 100:  # Controlla se è necessario creare una nuova pagina
            c.showPage()
            y = height - 100  # Resetta la posizione y alla parte superiore della nuova pagina
        
        c.drawString(x, y, line)
        y -= line_height  # Sposta 'y' verso il basso per la prossima linea
        
    c.save()
    messagebox.showinfo("PDF Salvato", "Il PDF è stato salvato con successo in: " + filename)

def calculate(operation, tab):
    try:
        a = simpledialog.askfloat("Input", "Inserisci il primo numero")
        if a is None:
            return  # Uscita se l'utente cancella o inserisce un valore non valido

        b = None
        if operation != 'sqrt':
            b = simpledialog.askfloat("Input", "Inserisci il secondo numero")
            if b is None:
                return  # Uscita se l'utente cancella o inserisce un valore non valido

        operations = {
            'add': lambda a, b: a + b,
            'sub': lambda a, b: a - b,
            'mul': lambda a, b: a * b,
            'div': lambda a, b: a / b if b != 0 else 'Errore: Divisione per zero',
            'exp': lambda a, b: pow(a, b),
            'sqrt': lambda a: math.sqrt(a)
        }

        result = operations[operation](a, b) if operation != 'sqrt' else operations[operation](a)
        
        op_symbol = {'add': '+', 'sub': '-', 'mul': '*', 'div': '/', 'exp': '^', 'sqrt': '√'}.get(operation, '?')
        operation_text = f"{a} {op_symbol} {b}" if operation != 'sqrt' else f"{op_symbol}{a}"
        update_text_area(tab, f"il risultato dell'operazione  è: {operation_text} = {result:.2f}")

    except ValueError:
        messagebox.showerror("Errore", "Inserisci solo valori numerici.")
    except Exception as e:
        messagebox.showerror("Errore", str(e))


def calcola_interessi_composti():
    P = simpledialog.askfloat("Input", "Capitale iniziale (P)")
    r = simpledialog.askfloat("Input", "Tasso di interesse annuo (r) in %") / 100
    t = simpledialog.askfloat("Input", "Durata in anni (t)")
    if None in (P, r, t): return
    
    R = simpledialog.askfloat("Input", "Rata annuale della rendita (R)")
    i = simpledialog.askfloat("Input", "Tasso di interesse annuo (i) in %") / 100
    n = simpledialog.askfloat("Input", "Numero di anni (n)")
    if None in (R, i, n): return
    
    PV = R * ((1 - math.pow((1 + i), -n)) / i)
    update_text_area(tab2, f"Valore attuale della rendita: {PV:.2f} EUR")

def esegui_calcolo_montante():
    # Questi valori dovrebbero essere ottenuti, ad esempio, da input dell'utente
    capitale = simpledialog.askfloat("Input", "Inserisci il capitale iniziale")
    tasso_interesse = simpledialog.askfloat("Input", "Inserisci il tasso di interesse annuo") / 100
    anni = simpledialog.askfloat("Input", "Inserisci il numero totale di anni")
    periodo = simpledialog.askfloat("Input", "Inserisci la frazione dell'ultimo anno")

    # Assicurati che tutti gli input siano stati forniti
    if None in (capitale, tasso_interesse, anni, periodo):
        messagebox.showerror("Errore", "Tutti i campi devono essere compilati.")
        return

    f = esegui_calcolo_montante(capitale, tasso_interesse, anni, periodo)
    
    # Ora puoi usare 'f' per aggiornare l'area di testo correttamente
    update_text_area(tab2, f"Montante finale: {f:.2f} EUR")



# Valore attuale di una rendita posticipata
def valore_attuale_rendita_posticipata(rendita, tasso_interesse, periodi):
    if tasso_interesse == 0:
        return rendita * periodi
    return rendita * ((1 - (1 + tasso_interesse) ** -periodi) / tasso_interesse)

def mostra_valore_attuale_rendita_posticipata():
    rendita = simpledialog.askfloat("Input", "Inserisci l'importo della rendita annuale")
    tasso_interesse = simpledialog.askfloat("Input", "Inserisci il tasso di interesse annuo") / 100
    periodi = simpledialog.askfloat("Input", "Inserisci il numero di periodi")
    
    if None in (rendita, tasso_interesse, periodi):
        messagebox.showerror("Errore", "Devi inserire tutti i valori richiesti.")
        return
    
    risultato = valore_attuale_rendita_posticipata(rendita, tasso_interesse, periodi)
    update_text_area(tab2, f"Valore attuale della rendita posticipata: {risultato:.2f} EUR")

    

 
# Calcolo del tasso equivalente annuo
def tasso_equivalente_annuo(tasso_periodale, periodi_annuali):
    return (1 + tasso_periodale)**periodi_annuali - 1
 
def esegui_fattore_montante():
    capitale = simpledialog.askfloat("Input", "Inserisci il capitale")
    tasso_interesse = simpledialog.askfloat("Input", "Inserisci il tasso di interesse annuo") / 100
    anni = simpledialog.askfloat("Input", "Inserisci la durata totale in anni")
    periodo = simpledialog.askfloat("Input", "Inserisci il periodo dell'ultimo anno")
    risultato = esegui_fattore_montante(capitale, tasso_interesse, anni, periodo)
    update_text_area(tab2, f"Fattore di montante: {risultato:.2f}")

def calculate_future_value():

    P = simpledialog.askfloat("Input", "Inserisci il capitale iniziale (P)")
    r = simpledialog.askfloat("Input", "Inserisci il tasso di interesse annuo (r) in %") / 100
    n = simpledialog.askfloat("Input", "Inserisci il numero di anni (n)")
    if None in (P, r, n): return  # Controllo input validi
    
    FV = P * pow((1 + r), n)
    update_text_area(tab2, f"Valore futuro: {FV:.2f}")

def calculate_free_fall():
    h = simpledialog.askfloat("Input", "Inserisci l'altezza (in metri)")
    if h is None: return  # Controllo input validi
    
    g = 9.81  # Accelerazione gravitazionale in m/s^2
    t = math.sqrt((2 * h) / g)
    update_text_area(tab3, f"Tempo di caduta: {t:.2f} secondi")

def calcolo_iva():
    # Chiedi all'utente di inserire l'aliquota IVA desiderata
    iva_action = simpledialog.askstring("Input", "Seleziona l'aliquota IVA desiderata (22, 10, 4): ")
    aliquota_iva = {"22": 1.22, "10": 1.10, "4": 1.40}
    
    if iva_action in aliquota_iva:
        # Chiedi all'utente di inserire la cifra su cui calcolare l'IVA
        a = simpledialog.askfloat("Input", "Inserisci una cifra:")
        if a is not None:  # Se l'utente non preme Cancel
            risultato_iva = a * aliquota_iva[iva_action]
        update_text_area(tab2, f"Il risultato dell'IVA al {iva_action}% su {a} è: {risultato_iva:.2f}")
    else:
        messagebox.showerror("Errore", "Selezione non valida. Riprova.")

def scorporo_iva():
    # Chiedi all'utente di inserire l'aliquota IVA desiderata
    iva_action = simpledialog.askstring("Input", "Seleziona l'aliquota IVA desiderata (22, 10, 4): ")
    aliquota_iva = {"22": 22, "10": 10, "4": 4}  # Usa l'aliquota percentuale diretta
    importo_totale = simpledialog.askfloat("Input", "Scrivi l'importo da scorporare")  # Usa askfloat per numeri

    if iva_action in aliquota_iva and importo_totale is not None:
        # Calcola l'importo netto e l'IVA scorporata
        aliquota_percentuale = aliquota_iva[iva_action] / 100
        risultato_iva = importo_totale / (1 + aliquota_percentuale)
        iva_scorporata = importo_totale - risultato_iva
        
        # Visualizza il risultato
        update_text_area(tab2, f"L'importo netto senza IVA al {iva_action}% su {importo_totale}€ è: {risultato_iva:.2f}€, IVA scorporata: {iva_scorporata:.2f}€")
    else:
        messagebox.showerror("Errore", "Selezione non valida o importo non inserito correttamente. Riprova.")


def salva_testo_come_pdf():
    testo_completo = ""
    for tab, txt_area in text_areas.items():
        testo_completo += txt_area.get("1.0", tk.END) + "\n\n"

    filename = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if filename:
        salva_pdf(testo_completo, filename)



tk.Button(tab4, text="Salva come PDF", command=salva_testo_come_pdf).pack()
# Aggiunta di bottoni per le operazioni
tk.Button(tab3, text="Calcola caduta libera", command=calculate_free_fall).pack()
tk.Button(tab2, text="Calcola interessi composti", command=calcola_interessi_composti).pack()
tk.Button(tab2, text="Calcola valore  montante composto", command=esegui_calcolo_montante).pack()
tk.Button(tab2, text="Calcola fattore montante", command=esegui_fattore_montante).pack()
tk.Button(tab2, text="Calcolaco valore attuale rendita posticipata", command= mostra_valore_attuale_rendita_posticipata).pack()
tk.Button(tab2, text="Calcolo IVA", command=calcolo_iva).pack()
tk.Button(tab2, text="Scorporo  IVA", command=scorporo_iva).pack()
tk.Button(tab1, text="Addizione", command=lambda: calculate('add', tab1)).pack()
tk.Button(tab1, text="sottrazione", command=lambda: calculate('sub', tab1)).pack()
tk.Button(tab1, text="Moltiplicazione", command=lambda: calculate('mul', tab1)).pack()
tk.Button(tab1, text="divisione", command=lambda: calculate('div', tab1)).pack()
tk.Button(tab1, text="calcolo esponenziale", command=lambda: calculate('exp', tab1)).pack()
tk.Button(tab1, text="radice quadrata", command=lambda: calculate('sqrt', tab1)).pack()





# Altri pulsanti e funzionalità possono essere aggiunti seguendo lo stesso schema

root.mainloop()
