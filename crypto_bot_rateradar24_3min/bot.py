
import requests
import time
from telegram import Bot

TOKEN = "8102585508:AAHNUBMDqv6HU8Ki6ZiRAr2RtUQqsgYcl78"
CHANNEL_ID = "@RateRadar24"
bot = Bot(token=TOKEN)

def get_usdt_price_irr():
    try:
        response = requests.get("https://api.nobitex.ir/market/stats")
        data = response.json()
        price = float(data["stats"]["usdt-rls"]["latest"])
        return price
    except Exception as e:
        print(f"خطا در دریافت نرخ تتر از نوبیتکس: {e}")
        return 58000

def get_crypto_prices(usdt_to_irr):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum,tether,xrp,dogecoin,shiba-inu,toncoin",
            "vs_currencies": "usd"
        }
        response = requests.get(url, params=params)
        data = response.json()

        btc = data["bitcoin"]["usd"] * usdt_to_irr
        eth = data["ethereum"]["usd"] * usdt_to_irr
        usdt = data["tether"]["usd"] * usdt_to_irr
        xrp = data["xrp"]["usd"] * usdt_to_irr
        doge = data["dogecoin"]["usd"] * usdt_to_irr
        shiba = data["shiba-inu"]["usd"] * usdt_to_irr
        ton = data["toncoin"]["usd"] * usdt_to_irr

        message = f"""
📊 قیمت لحظه‌ای ارزهای دیجیتال (به تومان):

🟡 بیت‌کوین (BTC): {btc:,.0f} تومان
🟣 اتریوم (ETH): {eth:,.0f} تومان
🟢 تتر (USDT): {usdt:,.0f} تومان
🔵 ریپل (XRP): {xrp:,.0f} تومان
🐶 دوج‌کوین (DOGE): {doge:,.0f} تومان
🐾 شیبا (SHIBA): {shiba:,.4f} تومان
💎 تون‌کوین (TON): {ton:,.0f} تومان

⏰ بروز‌رسانی خودکار هر ۳ دقیقه ✅
        """
        return message
    except Exception as e:
        print(f"خطا در دریافت قیمت ارزها: {e}")
        return None

def main():
    while True:
        try:
            usdt_irr = get_usdt_price_irr()
            text = get_crypto_prices(usdt_irr)
            if text:
                bot.send_message(chat_id=CHANNEL_ID, text=text)
            time.sleep(180)  # هر ۳ دقیقه
        except Exception as e:
            print(f"خطای اصلی: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
