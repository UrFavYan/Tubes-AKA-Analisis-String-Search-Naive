import time
import matplotlib.pyplot as plt
import gradio as gr
import sys
import tempfile # Library untuk membuat file sementara yang aman

# Menambah limit rekursi untuk input yang besar
sys.setrecursionlimit(10000)

# --- Implementasi Iteratif ---
def naive_search_iterative(text, pattern):
    n = len(text)
    m = len(pattern)
    results = []
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            results.append(i)
    return results

# --- Implementasi Rekursif ---
def naive_search_recursive(text, pattern, index=0, results=None):
    if results is None:
        results = []
    
    n = len(text)
    m = len(pattern)
    
    # Base Case: Sisa teks lebih pendek dari pola
    if index > n - m:
        return results
    
    # Cek kecocokan di indeks saat ini
    match = True
    for j in range(m):
        if text[index + j] != pattern[j]:
            match = False
            break
    if match:
        results.append(index)
    
    # Recursive Step: Pindah ke indeks berikutnya
    return naive_search_recursive(text, pattern, index + 1, results)

def run_experiment(max_size):
    sizes = []
    iterative_times = []
    recursive_times = []
    
    # Simulasi berbagai ukuran masukan
    step = max(1, max_size // 10)
    
    for size in range(1, max_size + 1, step):
        text = "A" * size + "B"
        pattern = "AB"
        
        # Hitung waktu Iteratif
        start = time.perf_counter()
        naive_search_iterative(text, pattern)
        iterative_times.append(time.perf_counter() - start)
        
        # Hitung waktu Rekursif
        start = time.perf_counter()
        try:
            naive_search_recursive(text, pattern)
            recursive_times.append(time.perf_counter() - start)
        except RecursionError:
            recursive_times.append(None)
        
        sizes.append(size)

    # Plotting Grafik
    plt.figure(figsize=(10, 5))
    plt.plot(sizes, iterative_times, label='Iteratif', marker='o')
    plt.plot(sizes, recursive_times, label='Rekursif', marker='x')
    plt.xlabel('Ukuran Input (Karakter)')
    plt.ylabel('Running Time (Detik)')
    plt.title('Perbandingan Running Time: Iteratif vs Rekursif')
    plt.legend()
    plt.grid(True)
    
    # --- PERBAIKAN DI SINI ---
    # Menggunakan tempfile agar tidak error permission/path di Windows
    plot_path = tempfile.mktemp(suffix=".png")
    plt.savefig(plot_path)
    plt.close()
    # -------------------------
    
    return plot_path, "Eksperimen Selesai. Grafik berhasil dibuat."

# Antarmuka Gradio
with gr.Blocks() as demo:
    gr.Markdown("# Analisis Perbandingan String Search Naif")
    gr.Markdown("Tugas Besar Analisis Kompleksitas Algoritma")
    
    with gr.Row():
        input_size = gr.Slider(minimum=100, maximum=5000, value=1000, label="Ukuran Maksimum Input", step=100)
        btn = gr.Button("Jalankan Analisis")
    
    output_plot = gr.Image(label="Grafik Perbandingan Running Time")
    output_text = gr.Textbox(label="Status")
    
    btn.click(fn=run_experiment, inputs=input_size, outputs=[output_plot, output_text])

if __name__ == "__main__":
    demo.launch()