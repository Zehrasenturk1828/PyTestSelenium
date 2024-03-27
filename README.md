Dekoratörler:
Dekoratörler, kapsamasını istediğimiz fonksiyonların üzerine, önünde @ karakteri konularak yazılır. Buna pie syntax denir. Aslında bu yazım stili sadece bir kısayoldan ibarettir.
ÖRNEK:
Yöntem 1:
@decorator
def func():
    pass

Yöntem 2:
def func():
    pass
    
func = decorator(func)

Yukarıdaki örnekte; üstteki pie syntax ile yazılmış dekoratörün yaptığı iş aslında hemen altındaki bölümün yaptığı iş ile aynıdır. Kullanım kolaylığı sağlamak ve okunabilirliği artırmak açısından böyle bir söz dizimi tercih edilmiş.

Aşağıda en basit kullanımıyla bir dekoratör görüyorsunuz. Fonksiyon çalışmadan önce bir mesaj yazdırıyor. Asıl fonksiyonda ise fonksiyonun çalıştığını yazdırıyoruz.
ÖRNEK:
def decorator(func):
    def wrapper(*args, **kwargs):
        print('Fonksiyon çalışacak...')
        func()
    return wrapper


@decorator
def func():
    print('Fonksiyon çalıştı.')


func()

Bir dekoratör kullanıldığında, kullanılan fonksiyon dekoratöre parametre olarak düşer. Dekoratör içinde bir kapsayıcı (wrapper) iç fonksiyon oluşturur ve asıl fonksiyona gelen parametreleri bununla yakalarız. Dilediğimiz işlemleri yaptıktan sonra iç fonksiyondan, parametre olarak gelen asıl fonksiyondan dönen değeri, dekoratörden ise iç fonksiyonun kendisini geriye döndürürüz.

Parametreli Dekoratörler:
Bildiğiniz üzere dekoratörlere parametre de verebiliyoruz. Örneğin aşağıda Flask frameworkten bir view görüyorsunuz.
ÖRNEK:
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

Anasayfayı görüntülemek için home isimli bir view yazılmış ve route dekoratörü kullanılmış. Bu dekoratörün birinci parametresi bu view’ın hangi URL’e (bu örnekte kök adres) karşılık vereceği, ikinci opsiyonel parametre ise hangi HTTP methodlarının kullanılabilir olacağı.

Parametreli dekoratörlerde, iç fonksiyon (wrapper) parametreyi alacak ek bir iç fonksiyon (decorator) içine alınır.

Zincirleme Dekoratörler:
Dekotörler uç uca eklenebilirler. Diğer bir deyişle, bir fonksiyon üzerinde birden fazla dekoratör kullanabilirsiniz. Örneğin, aşağıdaki gibi yazdığımız @benchmark ve @has_permission dekoratörlerinin ikisi birden kullanabiliriz.
ÖRNEK:
@benchmark
@has_permission('can_view_dashboard')
def view_dashboard(**kwargs):
    user = kwargs.pop('user')

    print('\n- DASHBOARD')
    print('- Merhaba {username}, giriş başarılı.'.format(
        username=user.name
    ))


view_dashboard(user=user)

Ancak bir problem var. Fonksiyonu çalıştırdığınızda göreceksiniz ki, @benchmark dekoratörü asıl fonksiyon yerine alttan gelen wrapper fonksiyonunun ölçümünü yapıyor. Bu problemi aşmak için functools modülündeki wraps dekoratörünü kullanacağız. Bu dekoratör, bizim dekoratörümüzün parametre olarak aldığı fonksiyonu ismi, parametre listesi, docstring vs. gibi tüm üst bilgisi ile beraber döndürmesini sağlayacak.

Şimdi, @has_permission dekoratörünü aşağıdaki gibi düzenleyelim.

def has_permission(permission):
    def decorator(func):
        from functools import wraps

        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get('user')
            assert permission in user.permissions

            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator

Sınıfları Dekoratör Olarak Kullanmak:
Önceki örneklerde sadece fonksiyonları dekoratör oluşturmak için kullandık. Ancak sınıfları ve onların __call__ sihirli fonksiyonlarını kullanarak da dekoratör oluşturabiliriz. Bu fonksiyon, bir sınıfa callable gibi davranıldığında yani fonksiyon gibi çalıştırıldığında çalışır. Dekoratör parametresini almak için __init__ sihirli fonksiyonunu kullanacağız. Bu fonksiyon bildiğiniz üzere sınıf ilk defa oluşturulduğunda çalışır.
ÖRNEK:
class sleep:
    def __init__(self, secs):
        self.secs = secs

    def __call__(self, func):
        from functools import wraps

        @wraps(func)
        def wrapper(*args, **kwargs):
            from time import sleep

            sleep(self.secs)
            return func(*args, **kwargs)

        return wrapper

Yukarıdaki örnekte dekoratör kullanılan fonksiyonu, parametre olarak verilen saniye değeri kadar bekletip sonra çalıştıran bir dekoratör görüyorsunuz. İlk olarak __init__ içinde, verilen saniyeyi sınıf içine kaydediyoruz, __call__ methodu tetiklendiğinde asıl fonksiyonu sınıf içindeki secs kadar bekletip çalıştırıyoruz. Kullanımı ise aşağıdaki gibi:

@sleep(5)
def hello(name):
    print('Hello {}'.format(name))


hello('World')
hello('Umut')

Dekoratörleri Sınıflar Üzerinde Kullanmak:
Önceki örneklerde dekoratörleri hep fonksiyonlar üzerinde kullandık. Ancak sınıflar da birer çağrılabilir (callable) olduğu için elbette onlar üzerinde de kullanabiliriz.

Örneğin, oluşturduğumuz @benchmark ve @sleep dekoratörlerini yine oluşturduğumuz User sınıfı üzerinde kullanalım.
ÖRNEK:
@benchmark
@sleep(3)
class User(object):
    is_active = True

    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions

user = User('umutcoskun', ['can_view_dashboard'])

Böylece her User nesnesi oluşturulduğunda, oluşturulmadan önce 3 saniye beklenecek ve toplamda oluşturulma işleminin kaç saniye sürdüğü ekrana yazılacak.
