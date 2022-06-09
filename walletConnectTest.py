from logging import basicConfig, DEBUG
from time import sleep

from pywalletconnect.client import WCClient

# Enable for debug output
# basicConfig(level=DEBUG)

# Dapp demo, using the Ethereum Kovan network
# WC v1 at https://example.walletconnect.org/
# WC v2 at https://react-app.walletconnect.com/


def WCCLIdemo():
    print(" ")
    print(" pyWalletConnect minimal demo - Kovan chain")
    uri = input("Paste a Dapp WC URI (v1 or v2) >")

    wallet_address = "0x7b3CaB0aBE2D9333D5400DE56F0B05E9af94c025"
    wallet_chain_id = 4  # Rinkeby

    # Required for v2
    WCClient.set_project_id("5af34a5c60298f270f4281f8bae67f33")

    wclient = WCClient.from_wc_uri(uri)

    print("Connecting with the Dapp ...")
    session_data = wclient.open_session()

    # Waiting for user accept the Dapp request
    user_ok = input(
        f"WalletConnect pairing request from {session_data[2]['name']}. Approve? [y/N]>"
    )
    if user_ok.lower() != "y":
        print("User denied the pairing.")
        wclient.reject_session_request(session_data[0])
        return

    print("Accepted, continue connecting with the Dapp ...")
    wclient.reply_session_request(session_data[0], wallet_chain_id, wallet_address)

    print("Connected.")
    print(" To quit : Hit CTRL+C, or disconnect from Dapp.")
    print("Now waiting for dapp messages ...")
    while True:
        try:
            sleep(0.3)
            # get_message return : (id, method, params) or (None, "", [])
            read_data = wclient.get_message()
            if read_data[0] is not None:
                print("\n <---- Received WalletConnect wallet query :")
                print(read_data)
                # Detect quit
                #  v1 disconnect
                if (
                    read_data[1] == "wc_sessionUpdate"
                    and read_data[2][0]["approved"] == False
                ):
                    print("User disconnects from Dapp (WC v1).")
                    break
                #  v2 disconnect
                if read_data[1] == "wc_sessionDelete" and read_data[2].get("reason"):
                    print("User disconnects from Dapp (WC v2).")
                    print("Reason :", read_data[2]["reason"]["message"])
                    break
        except KeyboardInterrupt:
            print("Demo interrupted.")
            break
    wclient.close()
    print("WC disconnected.")


if __name__ == "__main__":
    WCCLIdemo()