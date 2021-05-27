import os
import pickle
import sys
import time
from datetime import datetime
import typing as t

from colorama import Fore, init
from flasher import Login, ShopeeBot, AvailablePaymentChannels
from flasher.types import Item, User, CartItem, Payment
import colorlog


init()
INFO = colorlog.ColorLog(Fore.LIGHTBLUE_EX + "[*]" + Fore.BLUE)
INPUT = colorlog.ColorLog(Fore.LIGHTGREEN_EX + "[?] " + Fore.GREEN)
ERROR = colorlog.ColorLog(Fore.LIGHTRED_EX + "[!]" + Fore.RED)
WARNING = colorlog.ColorLog(Fore.LIGHTYELLOW_EX + "[!]" + Fore.YELLOW)
SUCCESS = colorlog.ColorLog(Fore.LIGHTGREEN_EX + "[+]" + Fore.GREEN)


def int_input(prompt_: str, max_: int = -1, min_: int = 1) -> int:
    input_: str

    while True:
        input_ = input(f"{INPUT} {prompt_}")

        if input_.isdigit():
            input_int = int(input_)

            if min_ <= input_int <= max_ or (min_ <= input_int and max_ == -1):
                return input_int
            elif input_int > max_ != -1:
                ERROR << "Angka terlalu banyak!\n"
            elif input_int < min_:
                ERROR << "Angka terlalu sedikit!\n"
        else:
            ERROR << "Masukkan angka!\n"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def line():
    print("-" * 32)


def do_login():
    INFO << "Masukkan Username/Email/Telepon\n"
    user = input(INPUT + "User: ")
    INFO << "Masukkan Password\n"
    password = input(INPUT + "Password: ")
    INFO << "Sedang Login...\n"

    login, success = Login.init(user, password)

    if login is None:
        ERROR << "Login error\n"
        exit(1)

    if success:
        with open("cookie", 'wb') as f:
            pickle.dump(login.session.cookies, f)
            SUCCESS << "Login sukses\n"
        exit(0)

    INFO << "Pilih Metode Verifikasi\n"
    print(Fore.GREEN + "[1]", Fore.BLUE + "WhatsApp")
    print(Fore.GREEN + "[2]", Fore.BLUE + "SMS")
    print(Fore.GREEN + "[3]", Fore.BLUE + "Telepon")
    print()
    verification_channel = int_input("Input: ", 3, 1)
    cookie = login.send_otp({
        1: Login.OTPChannel.WHATSAPP,
        2: Login.OTPChannel.SMS,
        3: Login.OTPChannel.CALL
    }[verification_channel]).verify(input(INPUT + "Masukkan Kode Verifikasi: "))

    with open("cookie", 'wb') as f:
        pickle.dump(cookie, f)
        SUCCESS << "Login sukses\n"


def main():
    INFO << "Mengambil Informasi User...\n"

    with open("cookie", 'rb') as f:
        bot = ShopeeBot(pickle.load(f))

    INFO << "Welcome " << bot.user.username << "\n"
    print()

    INFO << "Masukkan Url Barang\n"
    url = input(INPUT + "Url: ")
    item = bot.fetch_item_from_url(url)
    line()
    print(Fore.LIGHTBLUE_EX, "Nama:", Fore.GREEN, item.name)
    print(Fore.LIGHTBLUE_EX, "Harga:", Fore.GREEN, item.price // 99999)
    print(Fore.LIGHTBLUE_EX, "Brand:", Fore.GREEN, item.brand)
    print(Fore.LIGHTBLUE_EX, "Stok:", Fore.GREEN, item.stock)
    print(Fore.LIGHTBLUE_EX, "Lokasi Toko:", Fore.GREEN, item.shop_location)
    line()
    print()

    selected_model = 0

    if len(item.models) > 1:
        INFO << "Pilih Model/Variasi\n"
        line()

        for index, model in enumerate(item.models):
            print(Fore.GREEN + '[' + str(index + 1) + ']' + Fore.BLUE, model.name)
            print('\t', Fore.LIGHTBLUE_EX, "Harga:", Fore.GREEN, model.price // 99999)
            print('\t', Fore.LIGHTBLUE_EX, "Stok:", Fore.GREEN, model.stock)
            print('\t', Fore.LIGHTBLUE_EX, "ID Model:", Fore.GREEN, model.model_id)
            line()

        print()
        selected_model = int_input("Pilihan: ", len(item.models))-1
        print()

    INFO << "Pilih Metode Pembayaran\n"

    for index, channel in enumerate(AvailablePaymentChannels.lists):
        print(f"{Fore.GREEN}[{index+1}] {Fore.BLUE}{channel.name}")

    print()
    selected_payment_channel = AvailablePaymentChannels.lists[int_input("Pilihan: ",
                                                                        len(AvailablePaymentChannels.lists))-1]
    print()
    selected_option_info = None

    if selected_payment_channel.has_option():
        for index, option in enumerate(selected_payment_channel.option_keys()):
            print(f"{Fore.GREEN}[{index+1}] {Fore.BLUE}{option}")

        print()
        selected_option_info = int_input("Pilihan: ")-1

    if not item.flash_sale:
        if item.upcoming_flash_sale is not None:
            flash_sale_start = datetime.fromtimestamp(item.upcoming_flash_sale.start_time)
            INFO << "Waktu Flash Sale: " << flash_sale_start.strftime("%H:%M:%S") << "\n"
            INFO << "Menunggu Flash Sale...\r"
            time.sleep((datetime.fromtimestamp(item.upcoming_flash_sale.start_time) - datetime.now())
                       .total_seconds() - 2)
            INFO << "Bersiap siap...        \n"

            while not item.flash_sale:
                item = bot.fetch_item(item.item_id, item.shop_id)
        else:
            ERROR << "Flash Sale telah lewat\n"
            exit(0)

    INFO << "Flash Sale telah tiba\n"
    start = datetime.now()
    INFO << "Menambah item ke Cart...\n"
    cart_item = bot.add_to_cart(item, selected_model)
    INFO << "Checkout...\n"
    bot.checkout(cart_item, Payment.from_channel(selected_payment_channel, selected_option_info))
    end = datetime.now() - start
    INFO << "Item berhasil dibeli dalam waktu " << end.seconds << " detik " << end.microseconds // 1000 <<\
        " milidetik\n"
    SUCCESS << "Proses selesai\n"


if __name__ == "__main__":
    clear()

    if len(sys.argv) > 1 and sys.argv[1] == "login":
        do_login()
        exit(0)

    main()
