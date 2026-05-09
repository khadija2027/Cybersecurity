# 🌱 EcoShred - Site Web Marketing

Site web professionnel pour présenter le robot intelligent de recyclage de bouteilles PET.

## 📋 Table des Matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Structure du Projet](#structure-du-projet)
- [Installation](#installation)
- [Personnalisation](#personnalisation)
- [Hébergement](#hébergement)
- [Technologies Utilisées](#technologies-utilisées)
- [Maintenance](#maintenance)

## 🎯 Aperçu

EcoShred est un site web marketing moderne et responsive conçu pour présenter un robot de recyclage intelligent de bouteilles en PET. Le site cible les investisseurs, partenaires, écoles et centres de tri.

### Sections du Site

1. **Accueil** - Hero section avec CTA
2. **Le Projet** - Description du défi PET et de la solution
3. **Fonctionnalités** - Cahier des charges technique
4. **Architecture** - Les 4 blocs du robot
5. **Système** - Électronique et informatique
6. **Roadmap** - Timeline du développement
7. **Résultats** - Tests et améliorations
8. **L'Équipe** - Présentation des membres
9. **Contact** - Formulaire et informations

## ✨ Fonctionnalités

- ✅ Design responsive (mobile, tablette, desktop)
- ✅ Animations fluides au scroll
- ✅ Menu de navigation sticky
- ✅ Compteurs animés pour les statistiques
- ✅ Timeline interactive pour la roadmap
- ✅ Formulaire de contact
- ✅ Bouton scroll-to-top
- ✅ Optimisé SEO
- ✅ Performance optimisée

## 📁 Structure du Projet

```
robot-recyclage-site/
│
├── index.html          # Page principale
├── styles.css          # Styles CSS
├── script.js           # JavaScript interactions
└── README.md           # Ce fichier
```

## 🚀 Installation

### Option 1 : Ouverture Locale

1. Téléchargez tous les fichiers dans un même dossier
2. Double-cliquez sur `index.html`
3. Le site s'ouvre dans votre navigateur

### Option 2 : Serveur Local

Pour un développement avec rechargement automatique :

**Avec Python :**
```bash
cd robot-recyclage-site
python -m http.server 8000
```
Ouvrez `http://localhost:8000`

**Avec Node.js (live-server) :**
```bash
npm install -g live-server
cd robot-recyclage-site
live-server
```

## 🎨 Personnalisation

### 1. Modifier les Couleurs

Dans `styles.css`, modifiez les variables CSS (lignes 7-16) :

```css
:root {
    --primary-color: #2c8c99;      /* Couleur principale */
    --secondary-color: #4CAF50;     /* Couleur secondaire */
    --accent-color: #00BCD4;        /* Couleur d'accent */
}
```

### 2. Modifier le Contenu

#### Textes et Titres
Ouvrez `index.html` et recherchez la section concernée :
- Hero : ligne ~30
- Projet : ligne ~100
- Fonctionnalités : ligne ~200
- etc.

#### Statistiques (Hero)
Modifiez les attributs `data-target` (ligne ~75) :
```html
<h3 class="stat-number" data-target="1000">0</h3>
```

#### Membres de l'Équipe
Section équipe (ligne ~650). Format :
```html
<div class="team-card">
    <div class="team-photo">
        <i class="fas fa-user"></i>
    </div>
    <h3>Nom Prénom</h3>
    <span class="team-role">Rôle</span>
    <p>Description</p>
</div>
```

### 3. Ajouter des Images

#### Remplacer les Placeholders

**Logo du Robot (Hero) :**
```html
<!-- Remplacer ligne ~50 -->
<div class="hero-image">
    <img src="images/robot.png" alt="Robot EcoShred">
</div>
```

**Images d'Architecture :**
```html
<!-- Remplacer dans chaque bloc architecture -->
<div class="arch-image-placeholder">
    <img src="images/bloc1.jpg" alt="Bloc 1">
</div>
```

**Photos de l'Équipe :**
```html
<div class="team-photo">
    <img src="images/team/nom.jpg" alt="Nom Prénom">
</div>
```

Créez un dossier `images/` et ajoutez vos images.

### 4. Modifier les Informations de Contact

Dans `index.html`, section Contact (ligne ~750) :

```html
<div class="contact-item">
    <i class="fas fa-envelope"></i>
    <div>
        <h4>Email</h4>
        <p>votre-email@exemple.com</p>
    </div>
</div>
```

### 5. Configurer le Formulaire de Contact

Le formulaire actuel est en mode démo. Pour le rendre fonctionnel :

#### Option A : FormSubmit (gratuit, sans serveur)
```html
<form action="https://formsubmit.co/votre-email@exemple.com" method="POST">
    <input type="hidden" name="_subject" value="Nouveau message EcoShred">
    <input type="hidden" name="_captcha" value="false">
    <!-- vos champs -->
</form>
```

#### Option B : Formspree
1. Créez un compte sur [formspree.io](https://formspree.io)
2. Modifiez l'attribut `action` :
```html
<form action="https://formspree.io/f/VOTRE_ID" method="POST">
```

#### Option C : Backend personnalisé
Modifiez `script.js` (ligne ~150) pour envoyer à votre API.

### 6. Liens Sociaux

Modifiez les liens (ligne ~780) :
```html
<div class="social-links">
    <a href="https://linkedin.com/company/ecoshred" class="social-link">
        <i class="fab fa-linkedin"></i>
    </a>
    <a href="https://wa.me/212XXXXXXXXX" class="social-link">
        <i class="fab fa-whatsapp"></i>
    </a>
</div>
```

## 🌐 Hébergement

### Option 1 : GitHub Pages (Gratuit)

1. Créez un repository GitHub
2. Uploadez les fichiers
3. Allez dans Settings > Pages
4. Source : `main` branch
5. Votre site sera disponible à : `https://votre-username.github.io/nom-repo`

### Option 2 : Netlify (Gratuit)

1. Inscrivez-vous sur [netlify.com](https://netlify.com)
2. Glissez-déposez votre dossier
3. Site en ligne immédiatement
4. Domaine personnalisé possible

### Option 3 : Vercel (Gratuit)

1. Inscrivez-vous sur [vercel.com](https://vercel.com)
2. Importez depuis GitHub ou uploadez
3. Déploiement automatique

### Option 4 : Hébergement Classique

Uploadez via FTP sur votre hébergeur :
- OVH
- o2switch
- Hostinger
- etc.

## 🛠 Technologies Utilisées

- **HTML5** - Structure sémantique
- **CSS3** - Styles modernes avec variables CSS, Grid, Flexbox
- **JavaScript Vanilla** - Interactions sans framework
- **Font Awesome 6.4.0** - Icônes
- **Google Fonts** - Typographie (Segoe UI fallback)

### Compatibilité

- ✅ Chrome (dernières versions)
- ✅ Firefox (dernières versions)
- ✅ Safari (dernières versions)
- ✅ Edge (dernières versions)
- ✅ Mobile (iOS, Android)

## 📝 Maintenance

### Mise à Jour Régulière

#### 1. Roadmap (Phase du Projet)
Mettez à jour les badges dans la section Roadmap :
```html
<span class="timeline-badge completed">Terminé</span>
<span class="timeline-badge in-progress">En cours</span>
<span class="timeline-badge upcoming">À venir</span>
```

#### 2. Statistiques
Actualisez les chiffres dans les compteurs :
```html
<h3 class="stat-number" data-target="2000">0</h3>
```

#### 3. Résultats de Tests
Ajoutez de nouveaux tests dans la section Résultats.

#### 4. Barres de Progression
Modifiez les pourcentages (ligne ~630) :
```html
<div class="bar-fill" style="width: 95%"></div>
```

### Optimisation SEO

#### 1. Meta Tags
Ajoutez dans `<head>` :
```html
<meta name="author" content="EMINES - Équipe EcoShred">
<meta property="og:title" content="EcoShred - Robot Recyclage Intelligent">
<meta property="og:description" content="Solution innovante...">
<meta property="og:image" content="URL_IMAGE">
<meta name="twitter:card" content="summary_large_image">
```

#### 2. Fichier robots.txt
Créez `robots.txt` :
```
User-agent: *
Allow: /
Sitemap: https://votre-site.com/sitemap.xml
```

#### 3. Fichier sitemap.xml
Générez sur [xml-sitemaps.com](https://www.xml-sitemaps.com)

### Performance

Le site est déjà optimisé, mais vous pouvez :
- Compresser les images (TinyPNG, ImageOptim)
- Minifier CSS/JS (online tools)
- Activer la compression Gzip sur le serveur
- Utiliser un CDN pour les assets

### Analytics

Ajoutez Google Analytics avant `</head>` :
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 🐛 Dépannage

### Le menu mobile ne s'ouvre pas
- Vérifiez que `script.js` est bien chargé
- Ouvrez la console (F12) pour voir les erreurs

### Les animations ne fonctionnent pas
- Vérifiez la compatibilité du navigateur
- Désactivez les extensions qui bloquent JavaScript

### Les icônes ne s'affichent pas
- Vérifiez la connexion Internet (Font Awesome via CDN)
- Alternative : téléchargez Font Awesome localement

### Le formulaire ne fonctionne pas
- Configurez un service de formulaire (voir section Personnalisation)
- Vérifiez la console pour les erreurs JavaScript

## 📞 Support

Pour toute question technique :
- Email : contact@ecoshred-robot.com
- GitHub Issues : [créez une issue](https://github.com/votre-repo/issues)

## 📄 Licence

© 2025 EcoShred - EMINES. Tous droits réservés.

---

**Développé avec 💚 pour la planète**

♻️ Recyclons intelligemment pour un avenir durable
