# _Mastering Blockchain_ (Safari books)

## Examples
* steemit.com - social
* status.im - private/secure communications
* ipfs.io - storage/filesystem

---

Microsoft built decentralized identity network: [Identity Overlay Network (ION)](https://github.com/decentralized-identity/ion) 
on top of BTC

## Languages
* Bitcoin --> Script
	- _not_ Turing complete, can't be used for app development
* Etherum --> Solidity

## Consensus algorithms
* New ETH version (with PoS) is called "Serenity"
* Proof-of-Activity (PoA) is a combination of PoS and PoW, but much more energy-efficient

---

**Ethereum Swarm**: storage, do they reward participation? 
	- Filecoin does

**Firechat**: P2P mesh network between iphones (opengarden.com/firechat)

:question: How do you get storage capacity on IPFS? And how much? Can I put my backups on it?

[IPFS site](https://ipfs.io/) --> [ecosystem](https://ecosystem.ipfs.io/) --> 
data science --> [Qri](https://ecosystem.ipfs.io/project/qri)

[Ethlance job market](https://ethlance.com/): no results?

## DApp Architecture

### Traditional
```
user <-->    web app UI     <--> web server <--> backend server
		     (frontend)
```

### DApp
```
user <-->     web app UI    <-->     API    <--> blockchain running
		    (DApp frontend)       					smart contracts
```

---

**EOS**: decentralized operating system

demand-side economies of scale: the more users use a network, the more valuable it becomes

BitCoin Cash (BCH) increased the block limit from 1MB -> 8MB
	- block interval also from 10 min --> 10 sec

Bitcoin Gold: result of a hard fork to address mining centralization with Equihash algorithm
instead of PoW (ASIC-resistant and uses GPUs now)

Smart contracts cannot inherently access external data. Oracles—an off-chain source of information—
were introduced to address this.
	- blockchains are closed systems without any direct access to the real world

## Testing & Vetting Smart Contracts

[securify.ch](https://github.com/eth-sri/securify2) - formally verify smart contract code

[www.michelson.org](https://michelson.org/) - for Tezos blockchain

[Vyper](https://github.com/vyperlang/vyper) - reasonable choice of language for them, created from 
scratch, simple

Serpent - Python-like language, but _not used anymore_, go with Solidity instead

[Augur](https://www.augur.net/) - a decentralized prediction market implemented on Ethereum

[stateofthedapps.com](https://www.stateofthedapps.com/) - catalog of ETH DApps

The primary IDE is [Remix](https://remix.ethereum.org/)

## The decentralized ecosystem
```
	--------- Ethereum ------------
	|		  (compute)	          |
	|						      |
	|							  |
Whisper ----------------------- Swarm
(messaging)				        (storage)
```

---

**Ganache**: simulated personal (Ethereum) blockchain w/ CLI and GUI
	- great for development and testing

**Truffle**: development environment and framework

**Drizzle**: a web UI framework

**Brownie**: python-based framework for ETH smart contract development
	- full support of Solidity and Vyper
	- [eth-brownie.readthedocs.io](https://eth-brownie.readthedocs.io/en/stable/)

---

## Serenity: Ethereum 2.0
* original vision was a "World Computer": network of nodes running P2P contracts without shutting
down, being censored, or hacked
* ewasm: an improved version of the EVM

A user can stake a minimum of 32 ETH to get the ability to verify and attest the validity of blocks

> if someone stakes 32 ETH @ $240/ETH with uptime of 80%, the annual interest will be around 8%

but in the calculation, max effective balance is always 32 no matter how much you stake

---

## Hyperledger
* a project by the Linux Foundation in 2015 to advance blockchain technology

---

**DEX**: decentralized exchanges, peer-to-peer token exchanging, not required to transfer funds to
an intermediary

Examples: Uniswap, Bancor, WavesDEX, IDEX

**BitDNS** (2010): decentralized domain naming, gave rise to Namecoin. 

IoT: sensing | reacting | collecting | communicating


# What is Web3? 
https://www.freecodecamp.org/news/what-is-web3/

Web infrastructure protocols that have issued utility tokens that govern how the protocol
functions:
* Filecoin - a decentralized storage network
* Livepeer - build and scale next gen streaming platforms and services
* Arweave - store documents and applications; sustainable information permanence (permaweb)
* The Graph - organizing blockchain data and making it easily accessible; an indexing protocol
for querying networks like Ethereum and IPFS.

Radicle - decentralized GitHub alternative which allows stakeholders to participate in the
governance of their project.

Gitcoin - allows developers to get paid in crypto for jumping in and working on open source issues

[How to Get Into Ethereum, Crypto, and Web3 as a Developer](https://www.freecodecamp.org/news/breaking-into-ethereum-crypto-web3-as-a-developer/) – This is an introduction to the space in general, coming from a developer, for developers looking to break into the industry.

[The Complete Guide to Full Stack Ethereum Development](https://www.freecodecamp.org/news/full-stack-ethereum-development) – This is a tutorial that teaches you how to build out your first dapp.

[The Complete Guide to Full Stack Solana Development with React, Anchor, Rust, and Phantom](https://dev.to/dabit3/the-complete-guide-to-full-stack-solana-development-with-react-anchor-rust-and-phantom-3291) - This guide dives into Solana to show you how to build a full stack dapp.


# Building DApps

from _Building Blockchain Apps_ (Safari): http://buidl.secondstate.io is an IDE.

[CryptoZombies](https://cryptozombies.io/) is a good starting resource for Ethereum dapp 
development.

Tools for formal verification: 
- https://isabelle.in.tum.de/ 
- https://coq.inria.fr/

A [great overview of development](https://thecontrol.co/a-brief-overview-of-dapp-development-b8ac1648322c)

Blockchain prediction market: Augur, WeBet.

A Twitter thread on [how to build in crypto](https://twitter.com/das_connor/status/1395732795117428737?s=27) - Connor Daly

Chapter 12 of _Building Ethereum Dapps_ walks you through creating a voting dapp.


# ENS: Ethereum Name Service

https://registrar.ens.domains

https://medium.com/the-ethereum-name-service/a-beginners-guide-to-buying-an-ens-domain-3ccac2bdc770

