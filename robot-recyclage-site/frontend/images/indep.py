"""
=============================================================
SIMULATION MONTE CARLO — FIABILITÉ DU PARC AVEC DÉPENDANCE
=============================================================
Projet : Analyse de fiabilité — EMINES / UM6P
Contexte : 1000 serveurs, chaque serveur a n=2 composants
           en parallèle (k=1). On lève l'hypothèse
           d'indépendance via une copule de Clayton.
=============================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ─────────────────────────────────────────────
# 1. PARAMÈTRES DU MODÈLE
# ─────────────────────────────────────────────
N_SIM = 100_000   # nombre de simulations Monte Carlo
N = 1_000     # nombre de serveurs dans le parc
n = 2         # composants par serveur (fixé par le projet)
k = 1         # seuil interne : k=1 = parallèle (1 suffit)
m = 950       # seuil du parc : il faut m serveurs sur N

# Paramètres Weibull de chaque composant
beta = 2.5       # paramètre de forme
eta = 3_000.0   # paramètre d'échelle (heures)
t_star = 1_500.0   # horizon d'évaluation (heures)

# Coûts
Cc = 100       # coût d'un composant (€)
Cf = 500_000   # coût d'une défaillance du parc (€)

# Valeurs de θ à tester
thetas = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]


# ─────────────────────────────────────────────
# 2. FONCTIONS UTILITAIRES
# ─────────────────────────────────────────────

def weibull_survival(t, beta, eta):
    """
    Fiabilité d'un composant Weibull à l'instant t.
    R(t) = exp(-(t/eta)^beta)
    """
    return np.exp(-(t / eta) ** beta)


def clayton_sample(theta, size):
    """
    Génère un tableau (size, 2) de valeurs uniformes corrélées
    selon la copule de Clayton de paramètre θ.

    Méthode de Marshall-Olkin (méthode des frailties) :
    ─────────────────────────────────────────────────────
    Étape 1 : Tirer V ~ Gamma(1/θ, 1)    ← variable latente commune
    Étape 2 : Tirer E1, E2 ~ Exp(1)      ← chocs individuels
    Étape 3 : U_j = (1 + E_j / V)^(-1/θ) ← uniformes corrélées

    Interprétation physique :
    V représente la "fragilité" commune du serveur
    (qualité de fabrication, environnement de fonctionnement).
    Plus V est petit → serveur fragile → les deux composants
    tombent en panne tôt et ensemble.

    Cas limite θ → 0 : indépendance (V → ∞, les E_j dominent)
    Cas limite θ → ∞ : co-monotonie (U1 = U2 toujours)
    """
    if theta == 0:
        # Cas limite : indépendance totale
        return np.random.uniform(size=(size, 2))

    # Étape 1 : fragilité commune
    V = np.random.gamma(shape=1.0 / theta, scale=1.0, size=size)

    # Étape 2 : chocs individuels indépendants
    E1 = np.random.exponential(scale=1.0, size=size)
    E2 = np.random.exponential(scale=1.0, size=size)

    # Étape 3 : transformation inverse de Clayton
    U1 = (1.0 + E1 / V) ** (-1.0 / theta)
    U2 = (1.0 + E2 / V) ** (-1.0 / theta)

    return np.column_stack([U1, U2])


def uniform_to_weibull(U, beta, eta):
    """
    Transforme une uniforme U ∈ (0,1) en durée de vie Weibull.
    Utilise la transformée inverse : T = eta * (-ln U)^(1/beta)
    car si T ~ Weibull(β,η), alors R(T) = exp(-(T/η)^β) ~ U(0,1).
    """
    return eta * (-np.log(U + 1e-15)) ** (1.0 / beta)


def fiabilite_analytique(N, n, k, m, beta, eta, t_star):
    """
    Calcule la fiabilité analytique du parc sous hypothèse
    d'indépendance, via l'approximation normale.
    """
    # Fiabilité d'un composant
    Rc = weibull_survival(t_star, beta, eta)

    # Fiabilité d'un serveur (formule binomiale k-sur-n)
    from math import comb
    Rserv = sum(
        comb(n, j) * (Rc ** j) * ((1 - Rc) ** (n - j))
        for j in range(k, n + 1)
    )

    # Approximation normale pour le parc
    mu = N * Rserv
    sigma = np.sqrt(N * Rserv * (1 - Rserv))
    z = (m - mu) / sigma
    Rparc = 1 - norm.cdf(z)

    return Rc, Rserv, Rparc


# ─────────────────────────────────────────────
# 3. SIMULATION MONTE CARLO
# ─────────────────────────────────────────────

def simuler_parc(theta, N_sim, N, n, k, m, beta, eta, t_star, seed=42):
    """
    Simule le comportement du parc sur N_sim scénarios.

    Pour chaque scénario i :
    1. Pour chaque serveur : tirer (U1, U2) via Clayton(θ)
    2. Convertir en durées de vie Weibull : T1, T2
    3. Serveur OK si au moins k composants ont T > t* (ici k=1)
    4. Parc OK si nombre de serveurs OK ≥ m
    5. Estimer R_parc = proportion de scénarios où parc OK

    Retourne : (R_parc estimé, intervalle de confiance 95%)
    """
    np.random.seed(seed)
    succes = 0

    for _ in range(N_sim):
        # ── Pour les N serveurs en une seule vectorisation ──
        # Tirer les (U1, U2) corrélés pour tous les serveurs
        U = clayton_sample(theta, size=N)   # shape (N, 2)

        # Convertir en durées de vie
        T = uniform_to_weibull(U, beta, eta)  # shape (N, 2)

        # Tester chaque serveur : parallèle (k=1) → max(T1,T2) > t*
        serveurs_ok = np.sum(T > t_star, axis=1) >= k  # shape (N,)

        # Compter les serveurs opérationnels
        S_i = np.sum(serveurs_ok)

        # Parc opérationnel si S_i >= m
        if S_i >= m:
            succes += 1

    R_hat = succes / N_sim

    # Intervalle de confiance binomial (approximation normale)
    se = np.sqrt(R_hat * (1 - R_hat) / N_sim)
    ic_bas = R_hat - 1.96 * se
    ic_haut = R_hat + 1.96 * se

    return R_hat, ic_bas, ic_haut


def simuler_parc_vectorise(theta, N_sim, N, n, k, m, beta, eta, t_star, seed=42):
    """
    Version vectorisée (plus rapide) de la simulation.
    Tire tous les scénarios d'un coup en mémoire.
    Attention : nécessite N_sim * N * n valeurs en mémoire.
    Pour N=1000, N_sim=100000, n=2 → 200M flottants ~ 1,6 Go.
    Utiliser la version par boucle si mémoire insuffisante.
    """
    np.random.seed(seed)

    if theta == 0:
        U = np.random.uniform(size=(N_sim, N, n))
    else:
        # Fragilités communes : une par (simulation, serveur)
        V = np.random.gamma(1.0 / theta, 1.0, size=(N_sim, N))
        E = np.random.exponential(1.0, size=(N_sim, N, n))
        U = (1.0 + E / V[:, :, np.newaxis]) ** (-1.0 / theta)

    # Durées de vie Weibull
    T = eta * (-np.log(U + 1e-15)) ** (1.0 / beta)

    # Serveurs opérationnels : au moins k composants survivent
    serveurs_ok = np.sum(T > t_star, axis=2) >= k   # (N_sim, N)
    S = np.sum(serveurs_ok, axis=1)         # (N_sim,)

    # Fiabilité estimée
    succes = np.sum(S >= m)
    R_hat = succes / N_sim
    se = np.sqrt(R_hat * (1 - R_hat) / N_sim)

    return R_hat, R_hat - 1.96 * se, R_hat + 1.96 * se


# ─────────────────────────────────────────────
# 4. EXÉCUTION — RÉSULTATS ANALYTIQUE + MC
# ─────────────────────────────────────────────

print("=" * 60)
print("ANALYSE DE FIABILITÉ — MONTE CARLO AVEC COPULE DE CLAYTON")
print("=" * 60)

# Référence analytique
Rc, Rserv, Rparc_analytique = fiabilite_analytique(
    N, n, k, m, beta, eta, t_star
)
print(f"\nRéférence analytique (indépendance)")
print(f"  Rc(t*)       = {Rc:.4f}")
print(f"  R_serv       = {Rserv:.4f}")
print(f"  R_parc (m={m}) = {Rparc_analytique:.6f}")
print(f"\n{'─'*60}")
print(f"{'θ':>6} | {'R_parc MC':>10} | {'IC bas':>8} | {'IC haut':>8} | {'vs analytique':>14} | {'≥ 0.95':>6}")
print(f"{'─'*60}")

resultats = []
for theta in thetas:
    R_hat, ic_bas, ic_haut = simuler_parc_vectorise(
        theta, N_SIM, N, n, k, m, beta, eta, t_star, seed=42
    )
    delta = Rparc_analytique - R_hat
    ok = "Oui" if R_hat >= 0.95 else "Non"
    print(f"{theta:>6.1f} | {R_hat:>10.4f} | {ic_bas:>8.4f} | {ic_haut:>8.4f} | {delta:>+14.4f} | {ok:>6}")
    resultats.append((theta, R_hat, ic_bas, ic_haut))

print(f"{'─'*60}")


# ─────────────────────────────────────────────
# 5. GRAPHIQUES
# ─────────────────────────────────────────────

thetas_plot = [r[0] for r in resultats]
R_plots = [r[1] for r in resultats]
ic_bas_p = [r[2] for r in resultats]
ic_haut_p = [r[3] for r in resultats]
deltas = [Rparc_analytique - r for r in R_plots]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle(
    "Impact de la dépendance sur la fiabilité du parc\n"
    f"N={N} serveurs, n={n} composants/serveur, k={k}, m={m}, "
    f"β={beta}, η={eta}h, t*={t_star}h",
    fontsize=11
)

# ── Graphique 1 : R_parc en fonction de θ ──
ax = axes[0]
ax.axhline(Rparc_analytique, color='steelblue', lw=1.5,
           linestyle='--', label=f'Analytique (θ=0) = {Rparc_analytique:.4f}')
ax.axhline(0.95, color='green', lw=1.2,
           linestyle=':', label='R_min = 0,95')
ax.fill_between(thetas_plot, ic_bas_p, ic_haut_p,
                alpha=0.2, color='darkorange', label='IC 95%')
ax.plot(thetas_plot, R_plots, 'o-', color='darkorange',
        lw=2, ms=6, label='Monte Carlo')
ax.axhspan(0, 0.95, alpha=0.06, color='red')
ax.set_xlabel('Paramètre de dépendance θ (copule de Clayton)')
ax.set_ylabel('Fiabilité du parc $R_{parc}$')
ax.set_title('Fiabilité du parc vs dépendance')
ax.legend(fontsize=9)
ax.set_ylim(0.87, 1.005)
ax.grid(True, alpha=0.3)

# ── Graphique 2 : Dégradation ΔR ──
ax2 = axes[1]
ax2.bar(thetas_plot, [d * 100 for d in deltas],
        color=['green' if d * 100 < 5 else 'darkorange' for d in deltas],
        width=0.35, edgecolor='white')
ax2.axhline(5.0, color='red', lw=1.2, linestyle='--',
            label='Seuil critique (R_min non garanti)')
ax2.set_xlabel('Paramètre de dépendance θ')
ax2.set_ylabel('Dégradation ΔR (points de %)')
ax2.set_title('Dégradation due à la dépendance')
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/resultat_monte_carlo.png',
            dpi=150, bbox_inches='tight')
plt.show()
print("\nGraphique sauvegardé.")
