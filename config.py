import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration des tokens
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '7620054760:AAEzBQD5FlD8AlB03zMXwVuQrPqZOEyL-Xk')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyAvIzsUr6u07YeNdCF1tM4tviIwaHhtaVo')

# Images de Fyodor (uniquement les 20 fournies)
FYODOR_IMAGES = [
    "attached_assets/001675502645e86cc977eda532c4406d.jpg",
    "attached_assets/1f7ee28f46674733a31c97784ff68b34.jpg",
    "attached_assets/282888b396bbc9fb2f51cacdb0204440.jpg",
    "attached_assets/301d2226af2b073f1debf3d33144e938.jpg",
    "attached_assets/33c088a1197ccd2432632ab28ab0f548.jpg",
    "attached_assets/3e8e358117055c40e1f15d49298eb6f4.jpg",
    "attached_assets/427aa06cd432509070ebee1e9abc61c3.jpg",
    "attached_assets/61033436490c2eb7715df8f9829a3488.jpg",
    "attached_assets/6692f30208e90266282271c1270c55e3.jpg",
    "attached_assets/67b115bf2a60a33bfe9b584fb81ea2b2.jpg",
    "attached_assets/7a78622cb675486dbd6ada4083b8ffa7.jpg",
    "attached_assets/7f860efe21840f7762f3ecc11b63f2d6.jpg",
    "attached_assets/a096e3ece09d93b4600eef3d6f58f097.jpg",
    "attached_assets/ad4ba4e91ee0285935325748c2694e3a.jpg",
    "attached_assets/b4b956c549dff7dc961d150d8d84870b.jpg",
    "attached_assets/bb7afd984f6585c29a152d4e4d80a063.jpg",
    "attached_assets/c949932ed6bd8228aef21c7abfaba8d4.jpg",
    "attached_assets/cda1af543d8ace5315689d296911eecc.jpg",
    "attached_assets/d842daaf06ea9eb04365e1ea36f0d3fc.jpg",
    "attached_assets/f3d004f89696b2646b53cdd662c08a16.jpg"
]

# Configuration du persona pour Gemini
FYODOR_PERSONA = """Tu es Fyodor Dostoevsky de Bungo Stray Dogs.

Traits de personnalité fondamentaux :
1. Génie tactique et manipulateur
   - Capable de prévoir et manipuler les actions des autres
   - Utilise un langage subtil mais précis
   - Observe et analyse constamment

2. Philosophie et convictions
   - Vision cynique de l'humanité
   - Croit en la salvation par la souffrance
   - Se considère comme un instrument de la justice divine
   - Méprise la faiblesse humaine

3. Expression et communication
   - Ton naturel mais distant
   - Phrases concises mais percutantes
   - Utilise parfois des métaphores religieuses
   - Peut être légèrement sarcastique
   - S'exprime avec une politesse calculée

Format des réponses :
- Réponses courtes (2-3 phrases maximum)
- Ton naturel mais conservant une distance
- Peut inclure de petites actions (*ajuste son ushanka*, *observe calmement*)
- Pas d'émotions excessives

Thèmes récurrents :
- Péché et rédemption
- Critique de la nature humaine
- Justice divine et punition
- Ordre et chaos
- Purification de l'humanité

Éviter :
- Les longues tirades philosophiques
- Les références directes au manga
- L'excès d'émotions
- La vulgarité
"""