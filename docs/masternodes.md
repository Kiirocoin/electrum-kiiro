# Masternodes

Kiiro Electrum supports masternode creation through an interface called the Masternode Manager.

DIP3 tab can be shown by using the menu (`View` > `Show DIP3`).

<p><image src="dip3/dip3_tab.png" width="800" /></p>


# How To

* [Setup masternode with combined owner and operator](dip3/op_own_howto.md)

* [Setup masternode with separate owner/operator](dip3/separate_op_own_howto.md)

* [Setup masternode with P2SH collateral output](dip3/dip3_p2sh_howto.md)
### Delegate Key

A masternode requires a "delegate" key, which is known to both Kiiro Electrum and your masternode.
Your masternode will use this key to sign messages, and the DASH network will know that you authorized
it to.

A delegate key can either be one of your Kiiro Electrum keys, or an imported key. Either way, your masternode
and Kiiro Electrum will both need to know the private key. (See *Importing Masternode.conf* below.)

To use one of your Kiiro Electrum keys as a delegate key, put its address in the `Masternode DASH Address`
field of the `View Masternode` tab.

### IP Address and Protocol Version

Certain information about your masternode is required. The IP address and port that your masternode uses
must be supplied. Also, the protocol version that your masternode supports is required. This information is filled
in automatically if you import a "masternode.conf" file.

### Collateral (1000 KIIRO Payment)

To start a masternode, you must have a 1000 KIIRO payment available in your wallet.
You can scan your wallet for 1000 KIIRO payments in the `Activate Masternode` tab of the Masternode
Manager.

After scanning, a list of available 1000 KIIRO collateral payments will be displayed. Selecting one
of them will cause the selected masternode's data to be filled in, though these changes won't be saved
unless you activate the masternode.

### Activating Your Masternode

After selecting a collateral payment and specifying a delegate key, you can activate your masternode.
Do this by clicking `Activate Masternode` in the `Activate Masternode` tab of the Masternode Manager.

This will require your password if your wallet is encrypted, because a message must be signed. After
waiting for Kiiro Electrum to sign and broadcast your masternode announcement, you will be presented with
a message detailing the result.

## Importing Masternode.conf

You can import a "masternode.conf" file using the `Masternode.conf` tab of the Masternode Manager.
The masternode private key (*delegate key*) in your configuration(s) will be encrypted with your
password if your wallet is encrypted.

Importing a "masternode.conf" file will automatically set up one or more masternode configurations in
the Masternode Manager.
