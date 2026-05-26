def synthese_annuelle():
    dictionnaire={
            "dernier prix moyen annuel disponible en USD par GALLON AMERICAIN": """SELECT DIM_DATE.ANNEE,AVG(f.PRIX_USD / d.FACTEUR_USG) AS prix_usd_gallon_moyen
                                                from FAIT_PRIX f ,DIM_UNITE d,DIM_DATE
                                                where f.ID_UNIT=d.ID_UNIT and f.ID_DATE_DEB=DIM_DATE.ID_DATE
                                                and DIM_DATE.ANNEE <> EXTRACT(YEAR FROM SYSDATE)
                                                GROUP BY DIM_DATE.ANNEE
                                                ORDER BY DIM_DATE.ANNEE DESC
                                                FETCH FIRST 1 ROW ONLY""",
            "dernière taxe moyenne annuelle disponible en USD par GALLON AMERICAIN ": """SELECT DIM_DATE.ANNEE,AVG(f.VALEUR_USD / d.FACTEUR_USG) AS taxes_usd_gallon_moyen
                                                from FAIT_TAXE f ,DIM_UNITE d,DIM_DATE
                                                where f.ID_UNIT=d.ID_UNIT and f.ID_DATE_DEB=DIM_DATE.ID_DATE
                                                and DIM_DATE.ANNEE <> EXTRACT(YEAR FROM SYSDATE)
                                                GROUP BY DIM_DATE.ANNEE
                                                ORDER BY DIM_DATE.ANNEE DESC
                                                FETCH FIRST 1 ROW ONLY""",
            "dernière quantité consommée annuelle disponible en GALLON AMERICAIN": """select d.ANNEE,sum(f.QUANTITE_USG) AS consommation_gallon_américain
                                                        from FAIT_CONSOMMATION f, DIM_DATE d
                                                        where f.ID_DATE=d.ID_DATE
                                                        and d.ANNEE <> EXTRACT(YEAR FROM SYSDATE)
                                                        group by d.ANNEE
                                                        order by d.ANNEE DESC
                                                        FETCH FIRST 1 ROWS ONLY""",
            "dernière valeur de dépenses annuelles disponible en USD": """select d.ANNEE,sum(f.MONTANT_USD) AS somme_depense
                                            from FAIT_DEPENSE f, DIM_DATE d
                                            where f.ID_DATE=d.ID_DATE
                                            and d.ANNEE <> EXTRACT(YEAR FROM SYSDATE)
                                            group by d.ANNEE
                                            order by d.ANNEE DESC
                                            FETCH FIRST 1 ROWS ONLY"""
        }
    return dictionnaire

def tendance_mensuelle():
    dictionnaire={
            "consommation mensuelle de dernière année en GALLON AMERICAIN": """select d.ANNEE,d.MOIS,sum(f.QUANTITE_USG) AS consommation_gallon_américain
                                                        from FAIT_CONSOMMATION f, DIM_DATE d
                                                        where f.ID_DATE=d.ID_DATE
                                                        and d.ANNEE in (
                                                            SELECT d.ANNEE 
                                                            from DIM_DATE d,FAIT_CONSOMMATION fc
                                                            where fc.ID_DATE=d.ID_DATE
                                                            and d.ANNEE <> EXTRACT(YEAR FROM SYSDATE)
                                                            group by d.ANNEE
                                                            order by d.ANNEE DESC
                                                            FETCH FIRST 1 ROWS ONLY
                                                        )
                                                        group by d.ANNEE,d.MOIS
                                                        order by d.ANNEE DESC,d.MOIS DESC
                                                        FETCH FIRST 12 ROWS ONLY""",
            "dépenses mensuelles de dernière année en USD": """select d.ANNEE,d.MOIS,sum(f.MONTANT_USD) AS somme_depense
                                            from FAIT_DEPENSE f, DIM_DATE d
                                            where f.ID_DATE=d.ID_DATE
                                            and d.ANNEE in (
                                            SELECT d.ANNEE 
                                            from DIM_DATE d,FAIT_DEPENSE f
                                            where f.ID_DATE=d.ID_DATE
                                            and d.ANNEE <> EXTRACT(YEAR FROM SYSDATE)
                                            group by d.ANNEE
                                            order by d.ANNEE DESC
                                            FETCH FIRST 1 ROWS ONLY
                                            )
                                            group by d.ANNEE,d.MOIS
                                            order by d.ANNEE DESC,d.MOIS DESC
                                            FETCH FIRST 12 ROWS ONLY"""
        }
    return dictionnaire
def tendance_annuelle():
    dictionnaire={
            "consommation annuelle en GALLON AMERICAIN": """select d.ANNEE,sum(f.QUANTITE_USG) AS consommation_gallon_américain
                                                        from FAIT_CONSOMMATION f, DIM_DATE d
                                                        where f.ID_DATE=d.ID_DATE
                                                        and d.ANNEE <> EXTRACT(YEAR FROM SYSDATE)
                                                        group by d.ANNEE
                                                        order by d.ANNEE DESC""",
            "dépenses annuelles en USD": """select d.ANNEE,sum(f.MONTANT_USD) AS somme_depense
                                                        from FAIT_DEPENSE f, DIM_DATE d
                                                        where f.ID_DATE=d.ID_DATE
                                                        and d.ANNEE <> EXTRACT(YEAR FROM SYSDATE)
                                                        group by d.ANNEE
                                                        order by d.ANNEE DESC"""
        }
    return dictionnaire
def consommation_moyenne_annuelle():
    return {"consommation moyenne de chaque année en GALLON AMERICAIN": """select d.ANNEE,AVG(f.QUANTITE_USG) AS consommation_gallon_américain_moyenne
                                                        from FAIT_CONSOMMATION f, DIM_DATE d
                                                        where f.ID_DATE=d.ID_DATE
                                                        and d.ANNEE <> EXTRACT(YEAR FROM SYSDATE)
                                                        group by d.ANNEE
                                                        order by d.ANNEE DESC"""}
def depense_moyenne_annuelle():
    return {"dépense moyenne de chaque année en USD": """select d.ANNEE,AVG(f.MONTANT_USD) AS depense_moyenne
                                                        from FAIT_DEPENSE f, DIM_DATE d
                                                        where f.ID_DATE=d.ID_DATE
                                                        and d.ANNEE <> EXTRACT(YEAR FROM SYSDATE)
                                                        group by d.ANNEE
                                                        order by d.ANNEE DESC"""}
def evolution_des_prix():
    return{"prix moyenne annuelle en USD par GALLON AMERICAIN": """SELECT DIM_DATE.ANNEE,AVG(f.PRIX_USD / d.FACTEUR_USG) AS prix_usd_gallon_moyen
                                                from FAIT_PRIX f ,DIM_UNITE d,DIM_DATE
                                                where f.ID_UNIT=d.ID_UNIT and f.ID_DATE_DEB=DIM_DATE.ID_DATE
                                                and DIM_DATE.ANNEE <> EXTRACT(YEAR FROM SYSDATE)
                                                GROUP BY DIM_DATE.ANNEE
                                                ORDER BY DIM_DATE.ANNEE DESC"""}
def depenses_par_fournisseur():
    return {"dépenses par fournisseur": """
SELECT d.ANNEE,df.NOM_FOURNISSEUR, SUM(fd.MONTANT_USD) AS depenses_par_fournisseur
FROM DIM_FOURNISSEUR df, FAIT_DEPENSE fd, DIM_DATE d
WHERE df.ID_FOURNISSEUR = fd.ID_FOURNISSEUR
AND fd.ID_DATE = d.ID_DATE
AND d.ANNEE <> EXTRACT(YEAR FROM SYSDATE)
GROUP BY df.NOM_FOURNISSEUR,d.ANNEE
ORDER BY d.ANNEE,depenses_par_fournisseur DESC
    """}
def evolution_des_taxes():
    return{"taxes moyennes annuelles en USD par GALLON AMERICAIN": """SELECT DIM_DATE.ANNEE,AVG(f.VALEUR_USD / d.FACTEUR_USG) AS taxes_usd_gallon_moyen
                                                from FAIT_TAXE f ,DIM_UNITE d,DIM_DATE
                                                where f.ID_UNIT=d.ID_UNIT and f.ID_DATE_DEB=DIM_DATE.ID_DATE
                                                and DIM_DATE.ANNEE <> EXTRACT(YEAR FROM SYSDATE)
                                                GROUP BY DIM_DATE.ANNEE
                                                ORDER BY DIM_DATE.ANNEE DESC"""}
def analyse_des_couts():
    return {"analyse des coûts ": """
SELECT 
    d.ANNEE,    
    (AVG(fp.PRIX_USD / u.FACTEUR_USG) * SUM(fc.QUANTITE_USG))
    / NULLIF(SUM(fd.MONTANT_USD), 0) AS RATIO

    FROM 
    FAIT_CONSOMMATION fc,FAIT_PRIX fp,FAIT_DEPENSE fd,DIM_DATE d,DIM_UNITE u
    WHERE fp.ID_DATE_DEB = d.ID_DATE
    AND fc.ID_GEO = fp.ID_GEO
    AND fc.ID_FOURNISSEUR = fp.ID_FOURNISSEUR
    AND fc.ID_DATE BETWEEN fp.ID_DATE_DEB AND fp.ID_DATE_FIN
    AND fp.ID_UNIT = u.ID_UNIT
    AND fc.ID_DATE = fd.ID_DATE
    and d.ANNEE <> EXTRACT(YEAR FROM SYSDATE)
GROUP BY d.ANNEE
ORDER BY d.ANNEE
    """}
def vols_les_plus_consommateurs():
    return {"rank de top 3 vols les plus consommateurs chaque année en GALLON AMERICAIN": """
            SELECT *
FROM (
    SELECT 
        EXTRACT(YEAR FROM d.DATE_CALENDRIER) AS ANNEE,
        v.DEPART,
        v.ARRIVEE,
        SUM(NVL(c.QUANTITE_LITRE, 0)) AS total_consommation,

        ROW_NUMBER() OVER (
            PARTITION BY EXTRACT(YEAR FROM d.DATE_CALENDRIER)
            ORDER BY SUM(NVL(c.QUANTITE_LITRE, 0)) DESC
        ) AS rn

    FROM FAIT_CONSOMMATION c
    JOIN DIM_DATE d ON c.ID_DATE = d.ID_DATE
    JOIN DIM_VOL v ON c.ID_VOL = v.ID_VOL

    GROUP BY 
        EXTRACT(YEAR FROM d.DATE_CALENDRIER),
        v.DEPART,
        v.ARRIVEE
)
WHERE rn <= 3
ORDER BY ANNEE DESC, rn
            """
    }