from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
import sqlite3, random, datetime, os

app = Flask(__name__)
app.secret_key = os.urandom(24)
DATABASE = "sawit.db"

FLAG_B64 = os.environ.get("FLAG_B64", "VENDe2xvY2FsX2R1bW15X2ZsYWdfc2VjY2Vzc30=")

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL, password TEXT NOT NULL,
        full_name TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'user',
        perusahaan TEXT, lokasi TEXT, no_telp TEXT,
        total_order INTEGER DEFAULT 0, bergabung TEXT DEFAULT '2026'
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS pesanan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER, kode_pesanan TEXT, jenis_sawit TEXT,
        berat_kg REAL, harga_per_kg REAL,
        status TEXT DEFAULT 'Menunggu', tanggal TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        admin_pass = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$", k=24))
        users = [
            ("budi_santoso",   "budi123",    "Budi Santoso",      "user",  "PT Sawit Makmur",      "Riau",       "0812-1111-0001", 14, "Maret 2026"),
            ("dewi_rahayu",    "dewi456",    "Dewi Rahayu",       "user",  "CV Hijau Nusantara",   "Kalimantan", "0813-2222-0002", 7,  "April 2026"),
            ("agus_priyanto",  "agus789",    "Agus Priyanto",     "user",  "PT Borneo Palm",       "Kalimantan", "0821-3333-0003", 22, "Januari 2026"),
            ("siti_aminah",    "siti321",    "Siti Aminah",       "user",  "UD Subur Jaya",        "Sumatera",   "0822-4444-0004", 5,  "Juni 2026"),
            ("hendra_wijaya",  "hendra654",  "Hendra Wijaya",     "user",  "PT Sawit Unggul",      "Jambi",      "0815-5555-0005", 18, "Februari 2026"),
            ("rina_kusuma",    "rina987",    "Rina Kusuma Dewi",  "user",  "CV Mitra Tani",        "Bengkulu",   "0816-6666-0006", 3,  "Juli 2026"),
            ("bambang_eko",    "bambang111", "Bambang Eko Putra", "user",  "PT Eko Sawit",         "Riau",       "0817-7777-0007", 31, "Desember 2026"),
            ("nurul_hidayah",  "nurul222",   "Nurul Hidayah",     "user",  "UD Berkah Tani",       "Aceh",       "0818-8888-0008", 9,  "Agustus 2026"),
            ("wahyu_setiawan", "wahyu333",   "Wahyu Setiawan",    "user",  "PT Setiawan Agro",     "Kalimantan", "0819-9999-0009", 27, "November 2026"),
            ("fitri_lestari",  "fitri444",   "Fitri Lestari",     "user",  "CV Lestari Abadi",     "Sumatera",   "0851-1010-0010", 11, "September 2026"),
            ("joko_susilo",    "joko555",    "Joko Susilo",       "user",  "PT Susilo Palm Oil",   "Jambi",      "0852-1111-0011", 6,  "Oktober 2026"),
            ("maya_indrawati", "maya666",    "Maya Indrawati",    "user",  "UD Indra Sawit",       "Bengkulu",   "0853-1212-0012", 19, "Mei 2026"),
            ("XrunZ",          admin_pass,   "XrunZ",            "admin", "WSE DIVISION",         "Pusat",      "0800-0000-0000", 0,  "Januari 2026"),
            ("ahmad_fauzi",    "ahmad777",   "Ahmad Fauzi",       "user",  "PT Fauzi Agri",        "Riau",       "0854-1313-0014", 42, "Agustus 2026"),
            ("lilis_suryani",  "lilis888",   "Lilis Suryani",     "user",  "CV Surya Tani",        "Sumatera",   "0855-1414-0015", 8,  "Oktober 2026"),
            ("doni_prakoso",   "doni999",    "Doni Prakoso",      "user",  "PT Prakoso Sawit",     "Kalimantan", "0856-1515-0016", 15, "Juli 2026"),
            ("yanti_marlina",  "yanti000",   "Yanti Marlina",     "user",  "UD Marlina Sejahtera", "Aceh",       "0857-1616-0017", 4,  "November 2026"),
            ("rudi_hartono",   "rudi101",    "Rudi Hartono",      "user",  "PT Hartono Agro",      "Jambi",      "0858-1717-0018", 33, "April 2026"),
            ("sri_wahyuni",    "sri202",     "Sri Wahyuni",       "user",  "CV Wahyuni Palm",      "Sumatera",   "0859-1818-0019", 12, "Maret 2026"),
            ("teguh_prasetyo", "teguh303",   "Teguh Prasetyo",    "user",  "PT Prasetyo Sawit",    "Kalimantan", "0878-1919-0020", 20, "Februari 2026"),
        ]
        for u in users:
            cur.execute("INSERT INTO users (username,password,full_name,role,perusahaan,lokasi,no_telp,total_order,bergabung) VALUES (?,?,?,?,?,?,?,?,?)", u)

        jenis = ["TBS (Tandan Buah Segar)", "CPO (Crude Palm Oil)", "PKO (Palm Kernel Oil)", "Kernel Sawit"]
        status_list = ["Selesai","Selesai","Selesai","Diproses","Menunggu"]
        for uid in [1,2,3,4,5,6,7,8,9,10,11,12,14,15,16,17,18,19,20]:
            for _ in range(random.randint(2,5)):
                kode = f"PSN-{uid:03d}-{random.randint(1000,9999)}"
                berat = round(random.uniform(500,5000),1)
                harga = round(random.uniform(1800,2500),0)
                tgl = f"{random.randint(1,28):02d}/{random.randint(1,12):02d}/2026"
                cur.execute("INSERT INTO pesanan (user_id,kode_pesanan,jenis_sawit,berat_kg,harga_per_kg,status,tanggal) VALUES (?,?,?,?,?,?,?)",
                    (uid,kode,random.choice(jenis),berat,harga,random.choice(status_list),tgl))
    conn.commit()
    conn.close()

# ── helpers ──────────────────────────────────────────────
def get_user(uid):
    conn = get_db()
    u = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    conn.close()
    return u

def get_orders(uid):
    conn = get_db()
    rows = conn.execute("SELECT * FROM pesanan WHERE user_id=? ORDER BY id DESC",(uid,)).fetchall()
    conn.close()
    return rows

# ── routes ────────────────────────────────────────────────

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        uname = request.form.get("username","").strip()
        pwd   = request.form.get("password","").strip()
        conn  = get_db()
        user  = conn.execute("SELECT * FROM users WHERE username=? AND password=?",(uname,pwd)).fetchone()
        conn.close()
        if user:
            session["user_id"]  = user["id"]
            session["username"] = user["username"]
            session["role"]     = user["role"]
            return redirect(url_for("dashboard", user_id=user["id"]))
        error = "invalid"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ── DASHBOARD (IDOR vulnerable) ───────────────────────────
@app.route("/dashboard/<int:user_id>")
@login_required
def dashboard(user_id):
    user   = get_user(user_id)
    if not user:
        return render_template("404.html"), 404
    orders = get_orders(user_id)
    is_admin = (user["role"] == "admin")
    flag_b64 = FLAG_B64 if is_admin else ""
    return render_template("dashboard.html", user=user, orders=orders,
        is_admin=is_admin, flag_b64=flag_b64, logged_in=session, page="dashboard")

# ── PESANAN ───────────────────────────────────────────────
@app.route("/pesanan/<int:user_id>")
@login_required
def pesanan(user_id):
    user   = get_user(user_id)
    if not user: return render_template("404.html"), 404
    orders = get_orders(user_id)
    return render_template("pesanan.html", user=user, orders=orders,
        logged_in=session, page="pesanan")

# ── BUAT PESANAN ──────────────────────────────────────────
@app.route("/buat-pesanan/<int:user_id>", methods=["GET","POST"])
@login_required
def buat_pesanan(user_id):
    user = get_user(user_id)
    if not user: return render_template("404.html"), 404
    success = False
    if request.method == "POST":
        jenis = request.form.get("jenis","")
        berat = request.form.get("berat","0")
        harga = {"TBS (Tandan Buah Segar)":"2145","CPO (Crude Palm Oil)":"9800",
                 "PKO (Palm Kernel Oil)":"7200","Kernel Sawit":"3100"}.get(jenis,"2000")
        tgl = datetime.date.today().strftime("%d/%m/%Y")
        kode = f"PSN-{user_id:03d}-{random.randint(1000,9999)}"
        conn = get_db()
        conn.execute("INSERT INTO pesanan (user_id,kode_pesanan,jenis_sawit,berat_kg,harga_per_kg,status,tanggal) VALUES (?,?,?,?,?,?,?)",
            (user_id, kode, jenis, float(berat), float(harga), "Menunggu", tgl))
        conn.commit()
        conn.close()
        success = True
    return render_template("buat_pesanan.html", user=user,
        logged_in=session, page="buat_pesanan", success=success)

# ── TRANSAKSI ─────────────────────────────────────────────
@app.route("/transaksi/<int:user_id>")
@login_required
def transaksi(user_id):
    user   = get_user(user_id)
    if not user: return render_template("404.html"), 404
    orders = get_orders(user_id)
    selesai = [o for o in orders if o["status"] == "Selesai"]
    return render_template("transaksi.html", user=user, orders=selesai,
        logged_in=session, page="transaksi")

# ── PROFIL ────────────────────────────────────────────────
@app.route("/profil/<int:user_id>")
@login_required
def profil(user_id):
    user = get_user(user_id)
    if not user: return render_template("404.html"), 404
    return render_template("profil.html", user=user,
        logged_in=session, page="profil")

# ── PENGATURAN ────────────────────────────────────────────
@app.route("/pengaturan/<int:user_id>")
@login_required
def pengaturan(user_id):
    user = get_user(user_id)
    if not user: return render_template("404.html"), 404
    return render_template("pengaturan.html", user=user,
        logged_in=session, page="pengaturan")

# ── API ───────────────────────────────────────────────────
@app.route("/api/profile/<int:user_id>")
@login_required
def api_profile(user_id):
    conn = get_db()
    user = conn.execute("SELECT id,username,full_name,role,perusahaan,lokasi FROM users WHERE id=?",(user_id,)).fetchone()
    conn.close()
    if not user: return jsonify({"error":"Not found"}), 404
    return jsonify(dict(user))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
