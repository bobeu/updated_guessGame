from algosdk.v2client import algod
from algosdk import account
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn
import time, sys, random
import logging, json

# Setup HTTP client w/guest key provided by PureStake
class Connect():
    def __init__(self):
        # declaring the third party API
        self.algod_address = "https://testnet-algorand.api.purestake.io/ps2"
        self.algod_token = os.environ.get('PERSONAL_API_TOKEN_PURESTAKE') #shortened
        self.headers = {"X-API-Key": self.algod_token}

    def connectToNetwork(self):
        # establish connection
        return algod.AlgodClient(self.algod_token, self.algod_address, self.headers)


#Logs output to guessgame.log file
logging.basicConfig(filename='{}.log'.format("guessgame"), level=logging.INFO)
c = Connect()
algo_client = c.connectToNetwork()
#Determining winning algorithm
randomSeal = random.randint(int(49799), int(50001))
winRounds = int(0)
playRound = int(0)
ACTIVE = True
max_reward = (int(200))

# Get network params for transactions before every transaction.
params = algo_client.suggested_params()

# Generating 3 addresses for the host, game(where player sends fee) and player (for testing)
# 3 accounts generated - initialize each account with ALGO from
# https://bank.testnet.algorand.network/ we will need minimum transaction fee for each of account
host_sk, host_pk = account.generate_account()
game_sk, game_pk = account.generate_account()
player_sk, player_pk = account.generate_account()

print("Host sk: {}".format(host_sk)
print("Host pk: {}".format(host_sk)
print("Game sk: {}".format(game_sk)
print("Game pk: {}".format(game_pk)
print("Player sk: {}".format(player_sk)
print("Player pk: {}".format(player_pk)
      
# Hey python, go take some rest, wake up after 2 mins. I need to get some pizzas fund the accounts before proceeding
# while the execution pauses, look up the addresses from terminal and fund them.
time.sleep(120)

# create a list of addresses and keys to easily loop through them excluding host's
accounts = {
    game_sk: game_pk,
    player_sk: player_pk
}

 # generate seedphrase from sk
def convertToMnemonic():
    host_mnemonic = mnemonic.from_private_key(host_sk)
    game_mnemonic = mnemonic.from_private_key(game_sk)
    player_mnemonic = mnemonic.from_private_key(player_sk)
    return {
        "host_mnemonic": "\{}\".format(host_mnemonic),
        "game_mnemonic": "\{}\".format(game_mnemonic),
        "player_mnemonic": "\{}\".format(player_mnemonic)
    }
 
# Utility for restoring account from mnemonics
def restoreAccount(_seedPhrase):
    p_addr = ""
    s_addr = ""
    success = True
    s_key = mnemonic.to_private_key(_seedPhrase)
    p_key = mnemonic.to_public_key(_seedPhrase)
    for key in accounts:
        if key == s_key:
            p_addr = p_key
            s_addr = s_addr
            print(p_key, s_key)
        return (success, "\n", s_key, "\n", p_key)

      
m = convertToMnemonic()
seed = m["player_mnemonic"]
restore = restoreAccount(seed)
print(restore)
      
# In practice, you don not want to reveal secret key, but we only reference it here so we can
# access and retrieve it.
# Log accounts to file
logging.info("...@dev/created Asset WIN... \nHost Address: {}\nHost sk: {}\nGame Address : {}\nGame sk: {}\nPlayer Address: {}\nPlayer sk: {}\n".format(
    host_pk,
    host_sk,
    game_pk,
    game_sk,
    player_pk,
    player_sk
    ))

#  Utiltity for Waiting transaction to be confirmed
# Usually, transaction are confirmed in 2secs to 5 secs window
def wait_for_confirmation(txid):
    """Utility function to wait until the transaction is
    confirmed before proceeding."""
    last_round = algo_client.status().get('last-round')
    txinfo = algo_client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        wait = "Waiting for confirmation..."
        last_round += 1
        status = algo_client.status_after_block(last_round)
        txinfo = algo_client.pending_transaction_info(txid)
        logging.info("..@dev wait for confirmation.. \nStatus: {}\nTransaction {} confirmed in round {}\nTxn Info: {}\nResponse: {}".format(
        status,
        txid,
        txinfo.get('confirmed-round'),
        txinfo,
        wait
        ))
    return txinfo

#   Utility function used to print created asset for account and assetid
def print_created_asset(accountaddr, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algo_client.account_info(accountaddr)
    idx = 0
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['index'] == assetid):
            asset_id = scrutinized_asset['index']
            data_json = json.dumps(my_account_info['params'], indent=4)
            logging.info("...##Asset holding... \nAddress: {}.\n Asset ID: {}\nData in Json: {}\nOperation: {}\n".format(
                account,
                asset_id,
                data_json,
                print_created_asset.__name__
                ))
            return data_json
        else:
            ACTIVE = False
            return("Asset does not exist")

# Utility function used to print asset holding for account and assetid
def print_asset_holding(accountaddr, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algo_client.account_info(accountaddr)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == assetid):
            asset_id = scrutinized_asset['asset-id']
            data_json = json.dumps(scrutinized_asset, indent=4)
            logging.info("...##Asset holding... \nAddress: {}.\n Asset ID: {}\nData in Json: {}\nOperation: {}\n".format(
                account,
                asset_id,
                data_json,
                print_asset_holding.__name__
                ))
            return data_json
        else:
            ACTIVE = False
            return("You do not own WIN asset balance")

# Utility for grabbing the assetID without the using Indexer (Note that this works
# only for v1). If you're using v2client, this obviously won't work.
def getAssetIdv1(creatorAddr):
    keyList = []
    list1 = []
    # Get account info of asset creator
    account_info = algo_client.account_info(creatorAddr)
    # Loop through and target the value
    for key, value in account_info.items():
        list1.append(value)
    print(list1)
    # Target the key, strip into a list
    # First element in the list should be what we need
    for key, value in list1[7].items():
        keyList.append(key)
    print(keyList)
    assetID = keyList[0]
    return assetID

# Utility for grabbing the assetID in v2client without the using Indexer
# upgrade to v2client to use this function. See documentation
# https://developer.algorand.org/docs/reference/sdks/migration/

# Function getAssetIdv2() pulls asset's ID if called after asset is created. Calling at this point throws error. 
# So it is only declared at this point. Intepreter reads and remebers it but not executing it.
# It is needed as a global function function to inialized a global variable so as to be able to use it elsewhere in the program
# 
# Note that behavious may be different if you use goal. This code is written using VSCode
# To execute, initialize and call it. For instance:
            # asset_id = getAssetIdv2(<supply creator's addr as arguement>)
            # print(asset_id)
        
def getAssetIdv2(creatorAddr):
    # Get account info of asset creator
    account_info = algo_client.account_info(creatorAddr)
    _Id = account_info["assets"][0]["asset-id"]
    return _Id
      
# creating asset
def createAsset(
    creator,
    sk,
    asset_total,
    toFreeze,
    unitName,
    assetName,
    mngr_addr,
    rsv_addr,
    frz_addr,
    clwbck_addr,
    asst_link,
    asset_decimal
):
    # Account "host" creates an asset called "WIN" and
    # sets Host as the manager, reserve, freeze, and clawback address.
    # Asset Creation transaction
    params = algo_client.suggested_params()
    # comment these two lines if you want to use suggested params
    params.fee = 1000
    params.flat_fee = True

    # Host Account creates an asset called WIN and
    # Game Account as the manager, reserve, freeze, and clawback address.
    # Asset Creation transaction

    txn = AssetConfigTxn(
        sender=creator,
        sp=params,
        total=asset_total,
        default_frozen=toFreeze,
        unit_name=unitName,
        asset_name=assetName,
        manager=mngr_addr,
        reserve=rsv_addr,
        freeze=frz_addr,
        clawback=clwbck_addr,
        url=asst_link,
        decimals=asset_decimal)
    # Sign with secret key of creator
    stxn = txn.sign(sk)

    # Send the transaction to the network and retrieve the txid.
    txid = algo_client.send_transaction(stxn, headers={'content-type': 'application/x-binary'})

    # Retrieve the asset ID of the newly created asset by first
    # ensuring that the creation transaction was confirmed,
    # then grabbing the asset id from the transaction.

    # Wait for the transaction to be confirmed
    wait_for_confirmation(txid)
    time.sleep(3)
    try:
        # Pull account info of the creator
        # get asset_id from tx
        # Get the new asset's information from the creator account

        # Using this method makes asset_id available only inside this try block
        # Meanwhile I needd to use it elsewhere so an external function would be ideal
        ptx = algo_client.pending_transaction_info(txid) #I tried this but didn't work for me hence I created alternative
        asset_id = ptx["asset-index"]                     # function getAssetIdv2() to get asset_id

        # asset_id = getAssetIdv2(host_pk) # Ignore this line if method above does work for you to get asset_id

        createdAsset = print_created_asset(host_pk, asset_id)
        assetHolding = print_asset_holding(host_pk, asset_id)
        logging.info("...@dev/created Asset WIN... \nHost Address: {}\nPlayer Address: {}\nOperation 1 : {}\nOperation 2: {}\nOperation 3: {}\nAsset ID: {}\nCreated Asset: {} \nAsset Holding: {}\n".format(
            host_pk,
            player_pk,
            createAsset.__name__,
            print_created_asset.__name__,
            print_asset_holding.__name__,
            asset_id,
            createdAsset,
            assetHolding
            ))
    except Exception as e:
        print(e)

# comment line below to halt execute createAsset()
createAsset(host_pk, host_sk, 50000, False, "WIN", "Smarthead", game_pk, game_pk, game_pk, game_pk, "asset_info_link.com", 0)
      
      
# Opt in to accept assets
def optIn(pk, sk):
    # RECEIVER TO OPT-IN FOR ASSET
    # Check if asset_id is in player's asset holdings prior to opt-in
    assetId = getAssetIdv2(host_pk)
    account_info_pk = algo_client.account_info(pk)
    holding = None
    idx = 0
    for my_account_info in account_info_pk['assets']:
        scrutinized_asset = account_info_pk['assets'][idx]
        idx = idx + 1
        if (scrutinized_asset['asset-id'] == assetId):
            holding = True
            break
    if not holding:
        # Use the AssetTransferTxn class to transfer assets and opt-in
        txn = AssetTransferTxn(
        sender=pk,
        sp=params,
        receiver=pk,
        amt=0,
        index=assetId)
        stxn = txn.sign(sk)
        txid = algo_client.send_transaction(stxn, headers={'content-type': 'application/x-binary'})
        msg = "Transaction was signed with: {}.".format(txid)
        wait = wait_for_confirmation(txid)
        time.sleep(5)
        hasOptedIn = bool(wait != None)
        # Now check the asset holding for that account.
        # This should now show a holding with balance of win.
        assetHolding = print_asset_holding(player_pk, assetId)
        logging.info("...##Asset Transfer... \nOpt in address: {}.\nMessage: {}\nHas Opted in: {}\nOperation: {}\n".format(
            pk,
            msg,
            hasOptedIn,
            optIn.__name__
            ))
        return hasOptedIn

# Broadcast signed transaction to the network
# Log outputs to guessgame.log file
def forwardTransaction(signedTrxn, sk, assetBal, sender, receiver, amt, algobalance):
    # logging.basicConfig(filename='{}.log'.format("guessgame"), level=logging.INFO)
    try:
        assetId = getAssetIdv2(player_sk)
        txid = "Transaction was signed with {}.".format(algo_client.send_transaction(signedTrxn, headers={'content-type': 'application/x-binary'}))
        wait_for_confirmation(txid)
        # The balance should now be updated.
        holding = print_asset_holding(player_pk, assetId)
        logging.info("...##Forward Transaction... \nPlayer's Alc info: {}.\nSender: {}\nReceiver : {}\nAmount: {} WIN\n Operation: {}\nAlgo Balance: {}\nTxn ID: {}\nHolding: {}\nAsset balance: {}\n".format(
            algo_client.account_info(player_sk),
            sender,
            receiver,
            amt,
            forwardTransaction.__name__,
            algobalance,
            txid,
            holding,
            assetBal
            ))
    except Exception as e:
        print(e)

# transfer asset between accounts
def pay(senderAddr, receiverAddr, sk, amount):
    global ACTIVE
    min_pay_1 = int(50)
    sub_play = int(30)
    assetBalnce = algo_client.account_info(senderAddr)["assets"][0]["amount"]
    algoBalance = algo_client.account_info(senderAddr)['amount-without-pending-rewards']
    assetId = getAssetIdv2(host_pk)
    txn = AssetTransferTxn(
        sender=senderAddr,
        sp=params,
        receiver=receiverAddr,
        amt=amount,
        index=assetId)
    #If sender not host and has not played in this game for once
    if((senderAddr == host_pk) and (sendRound == 0) and (playRound == 0)):
        txn.amount = 50
        signedTrxn = txn.sign(sk)
        forwardTransaction(signedTrxn, host_sk, assetBalnce, senderAddr, receiverAddr, txn.amount, algoBalance)
        sendRound = sendRound+1

    if((senderAddr == host_pk) and (sendRound > 0) and (playRound > 0)):
        txn.amount = 200
        signedTrxn = txn.sign(sk)
        forwardTransaction(signedTrxn, host_sk, assetBalnce, senderAddr, receiverAddr, txn.amount, algoBalance)
        sendRound = sendRound+1

    elif ((senderAddr != host_pk) and ((playRound == int(0)) and winRounds == int(0))):
        # check that player's balances in WIN/ALGO are enough account
        #check if address is valid and player is new
        if ((len(senderAddr) == 58) and ((algoBalance > 1000) and (assetBalnce >= min_pay_1))):
            if(txn.amount >= min_pay_1):
                ACTIVE = ACTIVE
                signedTrxn = txn.sign(sk)
                # validate token transfer
                txn.amount = min_pay_1
                signedTrxn = txn.sign(sk)
                forwardTransaction(signedTrxn, sk, assetBalnce, senderAddr, receiverAddr, txn.amounty, algoBalance)
    # Check that player has made more than one round
    # Give fee discount if true
    elif(playRound > int(0) and winRounds > 0):
        assert((algoBalance > 1000) and (assetBalnce > min_pay_1))
        ACTIVE = True
        txn.amount = sub_play
        signedTrxn = txn.sign(sk)
        forwardTransaction(signedTrxn, sk, assetBalnce, senderAddr, receiverAddr, txn.amount, algoBalance)
    else:
        ACTIVE = False
        return


# Modelling Guessgame Class
class GuessGame():
    """Prototyping"""
    def __init__(self):
        self.alcInfo = algo_client.account_info(host_pk)
        self.round = self.alcInfo["round"]
        self.__asset_id = getAssetIdv2(host_pk)
        self.threshold = int(self.__asset_id/2)
        self.roundminus = int((self.round + randomSeal)-self.threshold)
        self.suggestedNumbers = range(self.roundminus - (int(self.threshold) - int(4500000)), self.round+randomSeal, randomSeal)
        self.active = False

    # suggested a series of numbers where winning number is among
    def suggestedNNumbers(self):
        sug_nums = set()
        print("Find the winning number in one round?:\n")
        for num in self.suggestedNumbers:
            sug_nums.add(num)
        # pop a random number from set, replaced with winning number
        win_position = random.randint(int(0), len(sug_nums))
        result = []
        for i, j in enumerate(list(sug_nums)):
            if i == win_position:
                j = self.roundminus
            result.append(j)
        new_set = set(result)
        print("There are {} suggested numbers in total".format(len(sug_nums)))
        print(new_set)

    # function for guessgame
    def guessByRound(self, player_pk, guess, sk):
        # logging.basicConfig(filename='{}.log'.format("guessgame"), level=logging.INFO)
        global winRounds
        global playRound

        # opt in player except for host, game address is the manager
        # With this, player will be able to receive asset we send to them
        optIn(player_pk, sk)
        print(algo_client.account_info(player_pk))
        print(algo_client.account_info(host_pk))

        # Display suggested nunmbers
        i = GuessGame()
        i.suggestedNNumbers()
        self.luckyNum = self.roundminus
        while ACTIVE:
            # send minimum play fee for this round to Guessgame Address
            send = pay(player_pk, game_pk, sk)
            if guess != self.luckyNum:
                winRounds = winRounds
                print("Oop! This roll does not match.")
                self.active = False
                print("Last guess was: " + str(guess))
                # break
            # Player finds winning number, rounds equaL plus 1
            # Host sends 200 WIN Asset to player
            elif guess == self.luckyNum:
                self.active = True
                playRound = playRound+1
                winRounds = winRounds+1
                msg = "Congratulations! You won!" + "\n" + "200 WINGOLDEN was sent to you."
                # Sent from Host account if player wins
                send = pay(host_pk, player_pk, host_sk)
                msg_2 = "You are in the {} round and {} playround.".format(winRounds, playRound)
                # Log output to file
                logging.info("\n...##Guessgame... \nPlayer Address: {}\nYou guessed: {}\nMessage: {}\nOperation: {}\nAlgo Balance: {}\nAsset balance: {}\nReminder: {}".format(
                    player_pk,
                    guess,
                    msg,
                    GuessGame.__name__,
                    algo_client.account_info(player_pk)['amount-without-pending-rewards'],
                    algo_client.account_info(player_pk)["assets"][0]["amount"],
                    msg_2
                    ))
            # Player wishes to replay?
            print("Do you want to make more guess? '\n'")           
            replay = input("Press 'y' to continue, 'n' to quit: ")
            replay = replay.lower()
            if(replay == "n"):
                self.active = False
                print("That was really tough right?", "\n", "Algorand Blockchain is awesome!.")
                print("Your total balance is {}".format(algo_client.account_info(player_pk)['assets'][0]["amount"]))
                sys.exit(int(1))
            elif(replay == "y"):
                self.active == True
            continue

toGuess = GuessGame()
m = toGuess.guessByRound(player_pk, <YOUR-GUESSED-NUMBER>, player_sk)
