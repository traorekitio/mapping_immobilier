import pyautogui
import time
import keyboard

def get_mouse_position():
    """
    Affiche les coordonnées de la souris en temps réel
    Appuyez sur 'Espace' pour capturer une position
    Appuyez sur 'Échap' pour quitter
    """
    print("🎯 DÉTECTEUR DE COORDONNÉES")
    print("=" * 50)
    print("📍 Bougez votre souris vers l'élément à cibler")
    print("⏰ Attente 3 secondes avant de commencer...")
    time.sleep(3)
    
    print("\n🔴 ACTIF - Mouvez la souris vers votre cible")
    print("   [ESPACE] = Capturer cette position")
    print("   [ÉCHAP] = Quitter")
    print("-" * 50)
    
    captured_positions = []
    
    try:
        while True:
            # Obtenir la position actuelle de la souris
            x, y = pyautogui.position()
            
            # Afficher les coordonnées en temps réel (effacer la ligne précédente)
            print(f"\r📍 Position: x={x}, y={y}   ", end="", flush=True)
            
            # Vérifier si l'utilisateur appuie sur Espace
            if keyboard.is_pressed('space'):
                captured_positions.append((x, y))
                print(f"\n✅ Position capturée: x={x}, y={y}")
                print(f"   Code à utiliser: pyautogui.click(x={x}, y={y})")
                time.sleep(0.5)  # Éviter les captures multiples
            
            # Vérifier si l'utilisateur appuie sur Échap
            if keyboard.is_pressed('esc'):
                break
            
            time.sleep(0.1)  # Rafraîchissement 10 fois par seconde
    
    except KeyboardInterrupt:
        pass
    
    print("\n\n📋 RÉSUMÉ DES POSITIONS CAPTURÉES:")
    print("=" * 50)
    
    if captured_positions:
        for i, (x, y) in enumerate(captured_positions, 1):
            print(f"{i}. x={x}, y={y}")
            print(f"   pyautogui.click(x={x}, y={y})")
        
        # Sauvegarder dans un fichier
        with open("output/coordonnees_capture.txt", "w", encoding="utf-8") as f:
            f.write("Coordonnées capturées:\n")
            f.write("=" * 30 + "\n")
            for i, (x, y) in enumerate(captured_positions, 1):
                f.write(f"{i}. x={x}, y={y}\n")
                f.write(f"   pyautogui.click(x={x}, y={y})\n")
        
        print(f"\n💾 Coordonnées sauvegardées dans output/coordonnees_capture.txt")
    else:
        print("Aucune position capturée.")
    
    print("\n✅ Terminé!")


def get_click_position():
    """
    Version alternative : capture automatiquement quand on clique
    """
    print("🎯 DÉTECTEUR DE COORDONNÉES (Version Clic)")
    print("=" * 50)
    print("🖱️  Cliquez n'importe où pour capturer les coordonnées")
    print("⏰ Attente 5 secondes avant de commencer...")
    time.sleep(5)
    
    print("🔴 ACTIF - Cliquez sur votre cible!")
    
    try:
        # Attendre un clic
        x, y = pyautogui.displayMousePosition()
    except KeyboardInterrupt:
        print("\n❌ Arrêté par l'utilisateur")
        return
    
    print(f"\n✅ Position cliquée: x={x}, y={y}")
    print(f"Code à utiliser: pyautogui.click(x={x}, y={y})")


def menu_principal():
    """Menu principal pour choisir le mode"""
    print("🎯 OUTIL DE CAPTURE DE COORDONNÉES")
    print("=" * 40)
    print("1. Mode en temps réel (bougez la souris + Espace)")
    print("2. Mode clic (cliquez pour capturer)")
    print("3. Quitter")
    
    choix = input("\nVotre choix (1-3): ").strip()
    
    if choix == "1":
        get_mouse_position()
    elif choix == "2":
        get_click_position()
    elif choix == "3":
        print("👋 Au revoir!")
    else:
        print("❌ Choix invalide!")
        menu_principal()


if __name__ == "__main__":
    import os
    os.makedirs("output", exist_ok=True)
    
    try:
        menu_principal()
    except Exception as e:
        print(f"❌ Erreur: {e}")