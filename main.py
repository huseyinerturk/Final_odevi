import sqlite3
from flask import Flask, redirect,render_template,request, url_for




data =[]

def veriEkle(baslik,yazar,tarih):
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("insert into tblBook (booktitle,bookauthor,bookyear,isReaded) values (?,?,?,0)",(baslik,yazar,tarih))
        con.commit()
    
def readed(id):
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("update tblBook set isReaded = ? where id=?",(1,id))


def veriSil(id):
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("delete from tblBook where id = ?", [id])

def veriAl():
    global data
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("select * from tblBook order by id asc")
        data = cur.fetchall()
        for i in data:  
            print(i)


def veriGuncelle(id,title,author,date):
    with sqlite3.connect("book.db") as con:
        cur = con.cursor()
        cur.execute("update tblBook set bookTitle = ?, bookAuthor = ?, bookYear = ? where id = ?",
                    (title, author, date, id,))
        con.commit()


veriAl()
app = Flask(__name__)
@app.route("/")
def index():
    veriAl()
    return render_template("index.html",data=data)


@app.route("/kitap")
def kitap():
    veriAl()
    return render_template("kitap.html",veri=data)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/kitap_ekle", methods=['POST','GET'])
def kitapEkle():
    print("kitap_ekle")
    if request.method == 'POST':
        bookTitle = request.form["bookTitle"]
        bookAuthor = request.form["bookAuthor"]
        bookYear = request.form["bookYear"]

        veriEkle(bookTitle, bookAuthor, bookYear)  
    return render_template("kitap_ekle.html")

@app.route("/kitapDetay/<string:id>")
def bookDetail(id):
    detailData = []
    for d in data:
        if str(d[0]) == id:
            detailData = list(d)
    return render_template("kitapDetay.html",data = detailData)


@app.route("/kitapEdit/<string:id>", methods = ["GET", "POST"])
def bookEdit(id):
    if request.method == "POST":
        id = request.form["id"]
        bookTitle = request.form["bookTitle"]
        bookAuthor = request.form["bookAuthor"]
        bookYear = request.form["bookYear"]
        veriGuncelle(id,bookTitle,bookAuthor,bookYear)
        return redirect(url_for("kitap"))
    else:
        updateData = []
        for d in data:
            if str(d[0]) == id:
                updateData = list(d)
    return render_template("kitapEdit.html", data = updateData)

@app.route("/kitapSil/<string:id>")
def bookDelete(id):
    veriSil(id)
    return redirect(url_for("kitap"))

@app.route("/kitapOku/<string:id>")
def kitapOkundu(id):
    readed(id)
    return redirect(url_for("kitap"))

@app.route("/okunanlar")
def kitapOku():
    veriAl()
    return render_template("okunanlar.html",datas = data)

if __name__ == "__main__":

    app.run(debug=True)
