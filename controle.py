from PyQt5 import uic, QtWidgets
import mysql.connector


conexao = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root',
    password ='',
    database = 'cadastro_produtos'
)

numero_id = 0

def excluir():
    remover = lista.tableWidget.currentRow()
    lista.tableWidget.removeRow(remover)

    cursor = conexao.cursor()
    cursor.execute('SELECT id FROM produtos')
    leitura_banco = cursor.fetchall()
    valor_id = leitura_banco[remover][0]
    cursor.execute(f'DELETE FROM produtos WHERE id={str(valor_id)}')

    conexao.commit()

def edit():
    global numero_id
    dados = lista.tableWidget.currentRow()
    cursor = conexao.cursor()
    cursor.execute('SELECT id FROM produtos')
    leitura_banco = cursor.fetchall()
    valor_id = leitura_banco[dados][0]
    cursor.execute(f'SELECT * FROM produtos WHERE id={str(valor_id)}')
    leitura_banco = cursor.fetchall()

    edit.show()
    numero_id = valor_id

    edit.txtAlterarID.setText(str(leitura_banco[0][0]))
    edit.txtAlteraProduto.setText(str(leitura_banco[0][1]))
    edit.txtAlterarPreco.setText(str(leitura_banco[0][2]))
    edit.txtAlterarQuantidade.setText(str(leitura_banco[0][3]))


def salvar_dados():
    global numero_id

    id = edit.txtAlterarID.text()
    produto = edit.txtAlteraProduto.text()
    preco = edit.txtAlterarPreco.text()
    estoque = edit.txtAlterarQuantidade.text()

    cursor = conexao.cursor()
    cursor.execute(f'UPDATE produtos SET id="{id}", produto="{produto}", preco="{preco}", estoque="{estoque}" WHERE id={numero_id}')

    edit.close()
    lista.close()
    form.show()
    conexao.commit()


def lista():
    lista.show()

    cursor = conexao.cursor()
    comando_SQL = 'SELECT * FROM produtos'
    cursor.execute(comando_SQL)
    leitura_banco = cursor.fetchall()

    lista.tableWidget.setRowCount(len(leitura_banco))
    lista.tableWidget.setColumnCount(4)

    for i in range(0, len(leitura_banco)):
        for j in range(0, 4):
            lista.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(leitura_banco[i][j])))


def inserir():
    produto = form.txtProduto.text()
    preco = form.txtPreco.text()
    estoque = form.txtEstoque.text()

    cursor = conexao.cursor()
    comando_SQL = 'INSERT INTO produtos (produto, preco, estoque) VALUES (%s, %s, %s)'
    dados = (str(produto), str(preco), str(estoque))
    cursor.execute(comando_SQL, dados)
    conexao.commit()

    form.txtProduto.setText('')
    form.txtPreco.setText('')
    form.txtEstoque.setText('')


app = QtWidgets.QApplication([])
form = uic.loadUi('form.ui')
form.btnCadastrar.clicked.connect(inserir)
form.btnRelatorio.clicked.connect(lista)

lista=uic.loadUi('lista.ui')
lista.btnAlterar.clicked.connect(edit)
lista.btnApagar.clicked.connect(excluir)

edit=uic.loadUi('edit.ui')
edit.btnConfirmarAlteracao.clicked.connect(salvar_dados)

form.show()
app.exec()