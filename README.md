# Dachain Waitlist Scripts 🚀

This collection of Python scripts empowers you to interact seamlessly with the Dachain Waitlist, a blockchain test network for decentralized applications. The core script, `main.py`, offers automation and multi-account support for core testnet activities.

🔗 Register: [Dachain Waitlist](https://waitlist.dachain.io/ref/DAC12841)

## ✨ Features Overview

### General Features

- **Multi-Account Support**: Reads token from `tokenX.txt` to perform actions across multiple accounts.
- **Colorful CLI**: Uses `colorama` for visually appealing output with colored text and borders.
- **Asynchronous Execution**: Built with `asyncio` for efficient blockchain interactions.
- **Error Handling**: Comprehensive error catching for blockchain transactions and RPC issues.
- **Bilingual Support**: Supports both English and Vietnamese output based on user selection.

### Included Scripts

✨ Register with Twitter OAuth

- ✅ Automatic login via Twitter OAuth2
- ✅ Automatic tasks social
- ✅ Automatic tasks submit Email | Share X
- ✅ Displays profile information, wallet, and rewards
- ✅ Supports multistream (multi-threading)
- ✅ Supports proxy (HTTP, HTTPS, SOCKS5)
- ✅ Beautiful UI with colorama

## 🛠️ Prerequisites

Before running the scripts, ensure you have the following installed:

- Python 3.8+
- `pip` (Python package manager)
- **Dependencies**: Install via `pip install -r requirements.txt` (ensure `web3.py`, `colorama`, `asyncio`, `eth-account`, `aiohttp_socks` and `inquirer` are included).
- **tokenX.txt**: Add tokens (one per line) for wallet automation.
- **proxies.txt** (optional): Add proxy addresses for network requests, if needed.

## 📦 Installation

1. **Clone this repository:**
   ```sh
   git clone https://github.com/thog9/Smashers-nft.git
   cd Smashers-nft
   ```
2. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Prepare Input Files:**
   - Open the `tokenX.txt`: Add your tokens (one per line) in the root directory.
   ```sh
   nano tokenX.txt 
   ```
   - Open the `address.txt`: Add your address (one per line) in the root directory.
   ```sh
   nano address.txt 
   ```
   - Open the `email.txt`: Add your email (one per line) in the root directory.
   ```sh
   nano email.txt 
   ```
   - Create `proxies.txt` for specific operations:
   ```sh
   nano proxies.txt
   ```
4. **Run:**
   ```sh
   python main.py
   ```
   - Choose a language (Vietnamese/English).
  
## 🚀 How to Use

### Method 1: Social with Twitter OAuth

#### 1. Prepare the `tokenX.txt` file

Format: `auth_token|ct0` or `auth_token:ct0` (one account per line)

For example:
```
abc123def456|xyz789uvw012
abc123def456:xyz789uvw012
```

**How ​​to get auth_token and ct0:**

1. Log in to Twitter/X
2. Open DevTools (F12)
3. Go to the Application/Storage tab → Cookies → https://x.com
4. Find the cookies `auth_token` and `ct0`
5. Copy the values

## 📨 Contact

Connect with us for support or updates:

- **Telegram**: [thog099](https://t.me/thog099)
- **Channel**: [CHANNEL](https://t.me/thogairdrops)
- **Group**: [GROUP CHAT](https://t.me/thogchats)
- **X**: [Thog](https://x.com/thog099) 

----

## ☕ Support Us

Love these scripts? Fuel our work with a coffee!

🔗 BUYMECAFE: [BUY ME CAFE](https://buymecafe.vercel.app/)

🔗 WEBSITE: [BUY SCRIPS](https://thogtoolhub.com/)
