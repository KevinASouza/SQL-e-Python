import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class LojaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Estoque")
        self.root.geometry("600x500")

        self.conn = self.conectar_bd()
        if not self.conn:
            self.root.destroy()
            return

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.frame_categoria = ttk.Frame(self.notebook)
        self.frame_fornecedor = ttk.Frame(self.notebook)
        self.frame_produto = ttk.Frame(self.notebook)

        self.notebook.add(self.frame_categoria, text="Inserir Categoria")
        self.notebook.add(self.frame_fornecedor, text="Inserir Fornecedor")
        self.notebook.add(self.frame_produto, text="Inserir Produto")
        
        self.criar_widgets_categoria()
        self.criar_widgets_fornecedor()
        self.criar_widgets_produto()
        
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_app)
        
    def conectar_bd(self):
        try:
            conn = sqlite3.connect('estoque_loja_virtual.db')
            return conn
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {e}")
            return None
            
    def fechar_app(self):
        if self.conn:
            self.conn.close()
        self.root.destroy()

    # --- Seção Categoria ---
    def criar_widgets_categoria(self):
        ttk.Label(self.frame_categoria, text="Nome da Categoria:").pack(pady=5)
        self.entry_nome_categoria = ttk.Entry(self.frame_categoria)
        self.entry_nome_categoria.pack(pady=5)
        
        ttk.Button(self.frame_categoria, text="Inserir Categoria", command=self.inserir_categoria).pack(pady=10)

    def inserir_categoria(self):
        nome = self.entry_nome_categoria.get()
        if not nome:
            messagebox.showwarning("Aviso", "O nome da categoria não pode ser vazio.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Categorias (nome_categoria) VALUES (?)", (nome,))
            self.conn.commit()
            messagebox.showinfo("Sucesso", f"Categoria '{nome}' inserida com sucesso!")
            self.entry_nome_categoria.delete(0, tk.END)
            self.atualizar_dropdown_produto()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", f"A categoria '{nome}' já existe.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao inserir categoria: {e}")

    # --- Seção Fornecedor ---
    def criar_widgets_fornecedor(self):
        ttk.Label(self.frame_fornecedor, text="Nome do Fornecedor:").pack(pady=5)
        self.entry_nome_fornecedor = ttk.Entry(self.frame_fornecedor)
        self.entry_nome_fornecedor.pack(pady=5)

        ttk.Label(self.frame_fornecedor, text="Contato:").pack(pady=5)
        self.entry_contato_fornecedor = ttk.Entry(self.frame_fornecedor)
        self.entry_contato_fornecedor.pack(pady=5)

        ttk.Label(self.frame_fornecedor, text="CNPJ:").pack(pady=5)
        self.entry_cnpj_fornecedor = ttk.Entry(self.frame_fornecedor)
        self.entry_cnpj_fornecedor.pack(pady=5)
        
        ttk.Button(self.frame_fornecedor, text="Inserir Fornecedor", command=self.inserir_fornecedor).pack(pady=10)

    def inserir_fornecedor(self):
        nome = self.entry_nome_fornecedor.get()
        contato = self.entry_contato_fornecedor.get()
        cnpj = self.entry_cnpj_fornecedor.get()

        if not nome or not cnpj:
            messagebox.showwarning("Aviso", "Nome e CNPJ são campos obrigatórios.")
            return
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO Fornecedores (nome_fornecedor, contato, cnpj) VALUES (?, ?, ?)", (nome, contato, cnpj))
            self.conn.commit()
            messagebox.showinfo("Sucesso", f"Fornecedor '{nome}' inserido com sucesso!")
            self.entry_nome_fornecedor.delete(0, tk.END)
            self.entry_contato_fornecedor.delete(0, tk.END)
            self.entry_cnpj_fornecedor.delete(0, tk.END)
            self.atualizar_dropdown_produto()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", f"O CNPJ '{cnpj}' já existe.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao inserir fornecedor: {e}")

    # --- Seção Produto ---
    def criar_widgets_produto(self):
        ttk.Label(self.frame_produto, text="Nome do Produto:").pack(pady=5)
        self.entry_nome_produto = ttk.Entry(self.frame_produto)
        self.entry_nome_produto.pack(pady=5)

        ttk.Label(self.frame_produto, text="Descrição:").pack(pady=5)
        self.entry_descricao_produto = ttk.Entry(self.frame_produto)
        self.entry_descricao_produto.pack(pady=5)

        ttk.Label(self.frame_produto, text="Preço de Custo:").pack(pady=5)
        self.entry_custo_produto = ttk.Entry(self.frame_produto)
        self.entry_custo_produto.pack(pady=5)

        ttk.Label(self.frame_produto, text="Preço de Venda:").pack(pady=5)
        self.entry_venda_produto = ttk.Entry(self.frame_produto)
        self.entry_venda_produto.pack(pady=5)
        
        # Dropdown para Categoria
        ttk.Label(self.frame_produto, text="Categoria:").pack(pady=5)
        self.combobox_categoria = ttk.Combobox(self.frame_produto, state="readonly")
        self.combobox_categoria.pack(pady=5)

        # Dropdown para Fornecedor
        ttk.Label(self.frame_produto, text="Fornecedor:").pack(pady=5)
        self.combobox_fornecedor = ttk.Combobox(self.frame_produto, state="readonly")
        self.combobox_fornecedor.pack(pady=5)
        
        self.atualizar_dropdown_produto()
        
        ttk.Button(self.frame_produto, text="Inserir Produto", command=self.inserir_produto).pack(pady=10)

    def atualizar_dropdown_produto(self):
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT id_categoria, nome_categoria FROM Categorias")
        categorias = cursor.fetchall()
        self.categoria_map = {nome: id for id, nome in categorias}
        self.combobox_categoria['values'] = [nome for id, nome in categorias]

        cursor.execute("SELECT id_fornecedor, nome_fornecedor FROM Fornecedores")
        fornecedores = cursor.fetchall()
        self.fornecedor_map = {nome: id for id, nome in fornecedores}
        self.combobox_fornecedor['values'] = [nome for id, nome in fornecedores]

    def inserir_produto(self):
        nome = self.entry_nome_produto.get()
        descricao = self.entry_descricao_produto.get()
        custo = self.entry_custo_produto.get()
        venda = self.entry_venda_produto.get()
        categoria_nome = self.combobox_categoria.get()
        fornecedor_nome = self.combobox_fornecedor.get()

        if not all([nome, custo, venda, categoria_nome, fornecedor_nome]):
            messagebox.showwarning("Aviso", "Todos os campos obrigatórios devem ser preenchidos.")
            return

        try:
            id_categoria = self.categoria_map.get(categoria_nome)
            id_fornecedor = self.fornecedor_map.get(fornecedor_nome)
            
            custo_float = float(custo)
            venda_float = float(venda)

            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Produtos (nome_produto, descricao, preco_custo, preco_venda, fk_id_categoria, fk_id_fornecedor)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nome, descricao, custo_float, venda_float, id_categoria, id_fornecedor))
            self.conn.commit()
            messagebox.showinfo("Sucesso", f"Produto '{nome}' inserido com sucesso!")
            self.entry_nome_produto.delete(0, tk.END)
            self.entry_descricao_produto.delete(0, tk.END)
            self.entry_custo_produto.delete(0, tk.END)
            self.entry_venda_produto.delete(0, tk.END)
            self.combobox_categoria.set('')
            self.combobox_fornecedor.set('')

        except ValueError:
            messagebox.showerror("Erro", "Preços devem ser números válidos.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao inserir produto: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LojaApp(root)
    root.mainloop()
