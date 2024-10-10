# Pubkey_Finder
Find the corresponding public key via hash160.

# BTC_puzzle
https://privatekeys.pw/puzzles/bitcoin-puzzle-tx

# Description
For low bit bitcoin puzzles, such as 66 or 67, the public key can be used to quickly solve the private key via the Kangaroo algorithm without brute-force cracking. However, the public key is only leaked every 5 bits, so how do we get the public key for the lower puzzles? The answer is to find it through hash160.

When we know a bitcoin address, its corresponding hash160 is naturally known.By point addition of elliptic curves, we can quickly solve for the public key, which is much faster than scalar multiplication.

# Example
For puzzle 67, suppose a private key ```40000000000000000```, the corresponding pubkey is ```041238c0766eaebea9ce4068a1f594d03b8ed4930d072d9c8b9164643e1516e6338a9db02dbb271359d6c979e2d1c3dc170946252dcc74022805cdb728c77b7805```, by point add 1, publickey is ```0414dad36d4491f7f00db31f074bbc77ef19ec7245a4d81f8f5b25e3707ee4dd09207528c7b30b70fea5839b3f10a5868e324b18fe7b67ad2a1397d55cc9704d0e```, then calculate the hash160, in here is ```cd1577dd1559e362c85d360414e235d0e099540f```, by performs point add operations without stopping, until hash160 is equal to puzzle 67's hash160 ```739437bb3dd6d1983e66629c5f08c70e52769371```, we can get corresponding pubkey and put it in kangaroo to find private key. 

# About Code
You can directly use it or change num_processes to your want. It is made for puzzle 67.
