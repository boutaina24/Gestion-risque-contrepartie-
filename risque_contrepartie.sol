// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GestionnaireRisqueContrepartie {
    struct Contrepartie {
        address portefeuille;
        uint256 scoreCredit;
        uint256 limiteExposition;
        uint256 expositionCourante;
        uint256 collaterale; // Champ ajouté pour le collatéral
        bool estActif;
    }

    // Variables d'état
    mapping(address => Contrepartie) public contreparties;
    mapping(address => mapping(address => uint256)) public expositions;

    // Événements
    event ContrepartieAjoutee(address indexed contrepartie, uint256 limiteExposition);
    event ExpositionMiseAJour(address indexed contrepartie, uint256 nouvelleExposition);
    event LimiteDepassee(address indexed contrepartie, uint256 exposition);
    event CollateralMisAJour(address indexed contrepartie, uint256 nouveauCollaterale);

    // Ajouter une nouvelle contrepartie
    function ajouterContrepartie(
        address _portefeuille,
        uint256 _scoreCredit,
        uint256 _limiteExposition,
        uint256 _collaterale
    ) public {
        require(_portefeuille != address(0), "Adresse invalide");
        require(contreparties[_portefeuille].portefeuille == address(0), "Contrepartie existe deja");

        contreparties[_portefeuille] = Contrepartie({
            portefeuille: _portefeuille,
            scoreCredit: _scoreCredit,
            limiteExposition: _limiteExposition,
            expositionCourante: 0,
            collaterale: _collaterale,
            estActif: true
        });

        emit ContrepartieAjoutee(_portefeuille, _limiteExposition);
    }

    // Mettre à jour l'exposition d'une contrepartie
    function mettreAJourExposition(address _portefeuille, uint256 _nouvelleExposition) public {
        Contrepartie storage contrepartie = contreparties[_portefeuille];
        require(contrepartie.portefeuille != address(0), "Contrepartie inexistante");
        require(contrepartie.estActif, "Contrepartie inactive");

        contrepartie.expositionCourante += _nouvelleExposition;

        // Vérification si la limite d'exposition est dépassée
        if (contrepartie.expositionCourante > contrepartie.limiteExposition) {
            emit LimiteDepassee(_portefeuille, contrepartie.expositionCourante);
        }

        emit ExpositionMiseAJour(_portefeuille, contrepartie.expositionCourante);
    }

    // Mettre à jour le collatéral d'une contrepartie
    function mettreAJourCollateral(address _portefeuille, uint256 _nouveauCollaterale) public {
        Contrepartie storage contrepartie = contreparties[_portefeuille];
        require(contrepartie.portefeuille != address(0), "Contrepartie inexistante");
        require(contrepartie.estActif, "Contrepartie inactive");

        contrepartie.collaterale = _nouveauCollaterale;
        emit CollateralMisAJour(_portefeuille, _nouveauCollaterale);
    }

    // Calculer le risque d'une contrepartie 
    function calculerRisque(address _portefeuille) public view returns (uint256) {
        Contrepartie memory c = contreparties[_portefeuille];
        require(c.portefeuille != address(0), "Contrepartie inexistante");
        require(c.limiteExposition > 0 && c.scoreCredit > 0, "Parametres invalides pour le risque");

        // Nouvelle formule : (expositionCourante * 10000) / (limiteExposition * scoreCredit)
        return (c.expositionCourante * 10000) / (c.limiteExposition * c.scoreCredit);
    
    }

    // Calculer le ratio de couverture (collateral / exposition totale)
    function calculerRatioCouverture(address _portefeuille) public view returns (uint256) {
        Contrepartie storage contrepartie = contreparties[_portefeuille];
        require(contrepartie.portefeuille != address(0), "Contrepartie inexistante");

        if (contrepartie.expositionCourante == 0) {
            return 0;
        }

        // Ratio : (collateral * 100) / expositionCourante
        uint256 ratio = (contrepartie.collaterale * 100) / contrepartie.expositionCourante;
        return ratio;
    }
}
