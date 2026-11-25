import argparse
import json
from pathlib import Path
import sys

# TODO 1 : importez la fonction de prédiction de predict.py et le seuil de config.py
from logiai.config import ALERT_THRESHOLD
from logiai.predict import Predictor


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="logiai-predict")
    parser.add_argument("fichier", help="fichier JSON d'une livraison")
    args = parser.parse_args(argv)
    chemin = Path(args.fichier)
    if not chemin.exists():
        print(f"Fichier introuvable : {chemin}", file=sys.stderr)
        return 1
    livraison = json.loads(chemin.read_text(encoding="utf-8"))

    # TODO 2 : calculer la probabilité de retard
    predictor = Predictor()
    resultat = predictor.predict(livraison)
    proba = resultat["probabilite_retard"]

    # TODO 3 : afficher « Probabilité de retard : 87 % (ALERTE) » (seuil : ALERT_THRESHOLD)
    pourcentage = round(proba * 100)
    if proba >= ALERT_THRESHOLD:
        print(f"Probabilité de retard : {pourcentage} % (ALERTE)")
    else:
        print(f"Probabilité de retard : {pourcentage} %")
    return 0


if __name__ == "__main__":
    sys.exit(main())
