import streamlit as st
from web3 import Web3

# Configuration de la connexion Web3
st.title("Gestionnaire de Risque Contrepartie")

web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))  # Connexion à Ganache local
if web3.is_connected():
    st.success("Connecté au réseau Ethereum via Ganache")
else:
    st.error("Impossible de se connecter au réseau Ethereum")
    st.stop()

# Adresse et ABI du contrat
contract_address = "0x42Ef0dC51A873277bb72512dddC6975db8B5DC9c"  # Adresse de votre contrat
contract_abi = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_scoreCredit",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_limiteExposition",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_collaterale",
				"type": "uint256"
			}
		],
		"name": "ajouterContrepartie",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "contrepartie",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "nouveauCollaterale",
				"type": "uint256"
			}
		],
		"name": "CollateralMisAJour",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "contrepartie",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "limiteExposition",
				"type": "uint256"
			}
		],
		"name": "ContrepartieAjoutee",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "contrepartie",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "nouvelleExposition",
				"type": "uint256"
			}
		],
		"name": "ExpositionMiseAJour",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "contrepartie",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "exposition",
				"type": "uint256"
			}
		],
		"name": "LimiteDepassee",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_nouveauCollaterale",
				"type": "uint256"
			}
		],
		"name": "mettreAJourCollateral",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_nouvelleExposition",
				"type": "uint256"
			}
		],
		"name": "mettreAJourExposition",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			}
		],
		"name": "calculerRatioCouverture",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			}
		],
		"name": "calculerRisque",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "contreparties",
		"outputs": [
			{
				"internalType": "address",
				"name": "portefeuille",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "scoreCredit",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "limiteExposition",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "expositionCourante",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "collaterale",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "estActif",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "expositions",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# Connexion au contrat
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Section : Ajouter une contrepartie
st.header("Ajouter une Contrepartie")
portefeuille = st.text_input("Adresse du portefeuille (Ethereum)")
score_credit = st.number_input("Score de crédit", min_value=0, step=1)
limite_exposition = st.number_input("Limite d'exposition", min_value=0, step=1)
collateral = st.number_input("Collatéral", min_value=0, step=1)

if st.button("Ajouter une Contrepartie de Test"):
    try:
        tx_hash = contract.functions.ajouterContrepartie(
            "0x42Ef0dC51A873277bb72512dddC6975db8B5DC9c",  # Adresse
            80,  # Score de crédit
            1000,  # Limite d'exposition
            500   # Collatéral
        ).transact({"from": web3.eth.accounts[0]})
        st.success(f"Transaction envoyée : {tx_hash.hex()}")
    except Exception as e:
        st.error(f"Erreur : {e}")


# Section : Mettre à jour l'exposition
st.header("Mettre à jour l'exposition")
portefeuille_expo = st.text_input("Adresse du portefeuille pour mise à jour")
nouvelle_expo = st.number_input("Nouvelle exposition", min_value=0, step=1)
est_longue = st.checkbox("Exposition longue ?")

if st.button("Mettre à jour l'exposition"):
    try:
        if not Web3.is_address(portefeuille_expo):
            st.error("Adresse Ethereum invalide.")
        else:
            address_checksum = Web3.to_checksum_address(portefeuille_expo)
            tx_hash = contract.functions.mettreAJourExposition(
                address_checksum, nouvelle_expo  # Retirez le troisième argument
            ).transact({"from": web3.eth.accounts[0]})
            st.success(f"Transaction envoyée : {tx_hash.hex()}")
    except Exception as e:
        st.error(f"Erreur : {e}")

# Section : Calculer le risque
st.header("Calculer le Risque")
portefeuille_risque = st.text_input("Adresse du portefeuille (Risque)")

if st.button("Calculer le risque"):
    try:
        if not Web3.is_address(portefeuille_risque):
            st.error("Adresse Ethereum invalide.")
        else:
            address_checksum = Web3.to_checksum_address(portefeuille_risque)
            risque = contract.functions.calculerRisque(address_checksum).call()
            st.info(f"Score de Risque : {risque}")
    except Exception as e:
        st.error(f"Erreur : {e}")

# Section : Calculer le ratio de couverture
st.header("Calculer le Ratio de Couverture")
portefeuille_couverture = st.text_input("Adresse du portefeuille (Couverture)")

if st.button("Calculer le ratio de couverture"):
    try:
        if not Web3.is_address(portefeuille_couverture):
            st.error("Adresse Ethereum invalide.")
        else:
            address_checksum = Web3.to_checksum_address(portefeuille_couverture)
            ratio = contract.functions.calculerRatioCouverture(address_checksum).call()
            st.info(f"Ratio de Couverture : {ratio}%")
    except Exception as e:
        st.error(f"Erreur : {e}")


# Section : Mettre à jour le collateral
st.header("Mettre à jour le Collatéral")
portefeuille_collateral = st.text_input("Adresse du portefeuille (Collatéral)")
nouveau_collateral = st.number_input("Nouveau collatéral", min_value=0, step=1)

if st.button("Mettre à jour le collatéral"):
    try:
        if not Web3.is_address(portefeuille_collateral):
            st.error("Adresse Ethereum invalide.")
        else:
            address_checksum = Web3.to_checksum_address(portefeuille_collateral)
            tx_hash = contract.functions.mettreAJourCollateral(
                address_checksum, nouveau_collateral
            ).transact({"from": web3.eth.accounts[0]})
            st.success(f"Transaction envoyée : {tx_hash.hex()}")
    except Exception as e:
        st.error(f"Erreur : {e}")