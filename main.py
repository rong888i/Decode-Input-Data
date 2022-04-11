from web3 import Web3
import re
import requests
from prettytable import PrettyTable

Type = {
    0: "Address",
    1: "Uint",
    2: "Sign"
}

if __name__ == '__main__':
    # 接口网站https://www.4byte.directory/signatures/?bytes4_signature=
    while True:
        try:
            data = input("输入要解析的data:")
            if data.startswith("0x"):
                fun = data[0:10]
                res = requests.get(url="https://www.4byte.directory/signatures/?bytes4_signature=" + fun).text
                fun_abi = re.findall(
                    r'<td class="id">([\s\S]*?)</td>[\s\S]*?<td class="text_signature">([\s\S]*?)</td>[\s\S]*?<td class="bytes_signature"><code>([\s\S]*?)</code></td>',
                    res)
                tab = PrettyTable(["Text Signature", "Bytes Signature"])
                tab.title = fun
                if len(fun_abi) > 0:
                    for f in fun_abi:
                        tab.add_row([f[1], f[2]])
                    print(tab)
                data = data.replace(fun, "")

            tab = PrettyTable(["default data", "type", "data"])
            tab.title = "function {}".format(fun)
            for x in re.findall(r"[0-9A-Za-z]{64}", data):
                x_m = Web3.toInt(hexstr=x)
                x_s = ["Address", f"0x{x[-40:]}"] if x[-42:-40] == "00" else ["Sign", f"0x{x}"]
                x_s = ["Uint", x_m] if len(str(x_m)) < 40 else x_s
                tab.add_row([x, x_s[0], x_s[1]])
            print(tab)
        except Exception as e:
            print(e)
        finally:
            print("\n")
