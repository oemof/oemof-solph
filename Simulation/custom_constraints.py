import pyomo.environ as pyo
import pandas as pd
import numpy as np

def add_multi_market_constraints(model, storage_component, market_bus, 
                                 fcr_prices, 
                                 afrp_pos_cap_prices, afrp_neg_cap_prices,
                                 afrp_pos_energy_prices, afrp_neg_energy_prices,
                                 p_max, e_max,
                                 fcr_duration=0.25, 
                                 afrr_duration=1.0, 
                                 market_block_size=16,
                                 activation_factor_pos=0.0, 
                                 activation_factor_neg=0.0,
                                 enable_fcr=True,
                                 enable_afrr_pos=True,
                                 enable_afrr_neg=True
                                 ):
    """
    V4: MIT PHYSIKALISCHER LIEFERVERPFLICHTUNG (SOC bewegt sich!)
    """
    
    time_steps = list(model.TIMESTEPS)
    
    # Block-Mapping
    t_to_block = {}
    blocks = set()
    for idx, t in enumerate(time_steps):
        block_id = idx // market_block_size
        t_to_block[t] = block_id
        blocks.add(block_id)
    sorted_blocks = sorted(list(blocks))
    
    # --- 1. VARIABLEN ---
    model.fcr_capacity_block = pyo.Var(sorted_blocks, domain=pyo.NonNegativeReals)
    model.afrp_pos_capacity_block = pyo.Var(sorted_blocks, domain=pyo.NonNegativeReals)
    model.afrp_neg_capacity_block = pyo.Var(sorted_blocks, domain=pyo.NonNegativeReals)
    
    if not enable_fcr:
        for b in sorted_blocks: model.fcr_capacity_block[b].fix(0)
    if not enable_afrr_pos:
        for b in sorted_blocks: model.afrp_pos_capacity_block[b].fix(0)
    if not enable_afrr_neg:
        for b in sorted_blocks: model.afrp_neg_capacity_block[b].fix(0)

    # Flows Identifizieren
    # NEU (SICHER & ROBUST):
    # Wir konstruieren den Schlüssel direkt, da wir wissen: (Quelle, Ziel)
    in_flow_uid = (market_bus, storage_component)  # Fluss: Netz -> Speicher
    out_flow_uid = (storage_component, market_bus) # Fluss: Speicher -> Netz
    
    # Listen Vorbereiten
    val_fcr = list(fcr_prices)
    val_afrp_pos_cap = list(afrp_pos_cap_prices)
    val_afrp_neg_cap = list(afrp_neg_cap_prices)
    val_afrp_pos_en = list(afrp_pos_energy_prices)
    val_afrp_neg_en = list(afrp_neg_energy_prices)
    
    is_act_pos_list = hasattr(activation_factor_pos, '__iter__')
    is_act_neg_list = hasattr(activation_factor_neg, '__iter__')
    if is_act_pos_list: val_act_pos = list(activation_factor_pos)
    if is_act_neg_list: val_act_neg = list(activation_factor_neg)

    # --- 2. LEISTUNGS-RESTRIKTIONEN (POWER HEADROOM) ---
    # Wir müssen Platz lassen für die Reserven
    
    def charge_power_rule(m, t):
        b = t_to_block[t]
        # Realer Fluss + Reservierte Leistung <= P_max
        real_flow_in = m.flow[in_flow_uid[0], in_flow_uid[1], t]
        res_fcr = m.fcr_capacity_block[b]
        res_afrr_neg = m.afrp_neg_capacity_block[b]
        return (real_flow_in + res_fcr + res_afrr_neg <= p_max)
    model.charge_power_limit = pyo.Constraint(time_steps, rule=charge_power_rule)

    def discharge_power_rule(m, t):
        b = t_to_block[t]
        real_flow_out = m.flow[out_flow_uid[0], out_flow_uid[1], t]
        res_fcr = m.fcr_capacity_block[b]
        res_afrr_pos = m.afrp_pos_capacity_block[b]
        return (real_flow_out + res_fcr + res_afrr_pos <= p_max)
    model.discharge_power_limit = pyo.Constraint(time_steps, rule=discharge_power_rule)

    # --- 3. ENERGIE-RESTRIKTIONEN (SOC HEADROOM) ---
    
    def soc_headroom_rule(m, t):
        b = t_to_block[t]
        soc = m.GenericStorageBlock.storage_content[storage_component, t]
        res_fcr = m.fcr_capacity_block[b]
        res_afrr_neg = m.afrp_neg_capacity_block[b]
        return (soc + (res_fcr * fcr_duration) + (res_afrr_neg * afrr_duration) <= e_max)
    model.soc_max_reserve = pyo.Constraint(time_steps, rule=soc_headroom_rule)

    def soc_footroom_rule(m, t):
        b = t_to_block[t]
        soc = m.GenericStorageBlock.storage_content[storage_component, t]
        res_fcr = m.fcr_capacity_block[b]
        res_afrr_pos = m.afrp_pos_capacity_block[b]
        return (soc >= (res_fcr * fcr_duration) + (res_afrr_pos * afrr_duration))
    model.soc_min_reserve = pyo.Constraint(time_steps, rule=soc_footroom_rule)

    # --- 5. PHYSIKALISCHE LIEFERPFLICHT (NEU & WICHTIG!) ---
    # Hier zwingen wir Oemof, den Strom auch wirklich fließen zu lassen.
    
    def force_physical_discharge(m, t):
        # Der Fluss AUS der Batterie muss mindestens so groß sein wie der Abruf
        # Flow_Out >= Reserve_Pos * Activation_Factor
        b = t_to_block[t]
        idx = time_steps.index(t)
        act_p = val_act_pos[idx] if is_act_pos_list else activation_factor_pos
        
        # Oemof Flow Variable (Physikalischer Fluss)
        phy_flow = m.flow[out_flow_uid[0], out_flow_uid[1], t]
        
        return phy_flow >= m.afrp_pos_capacity_block[b] * act_p

    model.force_phys_discharge = pyo.Constraint(time_steps, rule=force_physical_discharge)

    def force_physical_charge(m, t):
        # Der Fluss IN die Batterie muss mindestens so groß sein wie der Abruf
        # Flow_In >= Reserve_Neg * Activation_Factor
        b = t_to_block[t]
        idx = time_steps.index(t)
        act_n = val_act_neg[idx] if is_act_neg_list else activation_factor_neg
        
        phy_flow = m.flow[in_flow_uid[0], in_flow_uid[1], t]
        
        return phy_flow >= m.afrp_neg_capacity_block[b] * act_n

    model.force_phys_charge = pyo.Constraint(time_steps, rule=force_physical_charge)


    # --- 4. ZIELFUNKTION (CASHFLOW) ---
    obj_expr = model.objective.expr
    revenue_term = 0
    dt = 0.25
    
    for idx, t in enumerate(time_steps):
        b = t_to_block[t]
        
        # Leistungserlöse
        revenue_term += model.fcr_capacity_block[b] * val_fcr[idx] * dt
        revenue_term += model.afrp_pos_capacity_block[b] * val_afrp_pos_cap[idx] * dt
        revenue_term += model.afrp_neg_capacity_block[b] * val_afrp_neg_cap[idx] * dt
        
        # Arbeitserlöse
        act_p = val_act_pos[idx] if is_act_pos_list else activation_factor_pos
        act_n = val_act_neg[idx] if is_act_neg_list else activation_factor_neg
        
        revenue_term += model.afrp_pos_capacity_block[b] * act_p * val_afrp_pos_en[idx] * dt
        revenue_term -= model.afrp_neg_capacity_block[b] * act_n * val_afrp_neg_en[idx] * dt

    model.objective.expr = obj_expr - revenue_term

    if not hasattr(model, 't_to_block_map'): model.t_to_block_map = {}
    for t in time_steps:
        model.t_to_block_map[t] = t_to_block[t]

    return model

##################################################################
# Funktion für Abrufwahrscheinlickeiten
################################################################

def calculate_activation_profile_with_volume(market_prices, total_activation_mw, my_bid_price, my_p_max):
    """
    Berechnet den binären Abruf basierend auf Preis UND verfügbarem Marktvolumen.
    """
    activation_factors = []
    np.random.seed(42) 
    
    # Sicherstellen, dass wir mit sauberen Listen/Arrays arbeiten
    # Falls Pandas Series reinkommen, wandeln wir sie um
    prices = np.array(market_prices)
    volumes = np.array(total_activation_mw)
    
    for price, total_vol in zip(prices, volumes):
        
        # 1. PREIS CHECK
        if price > my_bid_price:
            planned_percent = 1.0 
        elif price < my_bid_price:
            planned_percent = 0.0
        else:
            planned_percent = np.random.choice([0.0, 1.0]) # Münzwurf
            
        # 2. VOLUMEN CHECK
        if planned_percent > 0:
            available_vol = abs(total_vol) # Volumen ist immer positiv betrachten
            
            if available_vol < my_p_max:
                real_percent = available_vol / my_p_max # Drosselung
            else:
                real_percent = 1.0 # Alles okay
                
            activation_factors.append(real_percent)
        else:
            activation_factors.append(0.0)
            
    return np.array(activation_factors)
##################################################################
#Funktion für flexible Lasten (Transformatoren)
##################################################################

def add_transformer_load_constraints(model, transformer_component, input_bus,
                                     afrp_pos_cap_prices, afrp_neg_cap_prices,
                                     afrp_pos_energy_prices, afrp_neg_energy_prices,
                                     p_max,
                                     market_block_size=16,
                                     activation_factor_pos=0.0, # Zeitreihe oder Wert
                                     activation_factor_neg=0.0, # Zeitreihe oder Wert
                                     enable_afrr_pos=True,
                                     enable_afrr_neg=True
                                     ):
    """
    Fügt Constraints für einen flexiblen Verbraucher (PtH/Boiler) hinzu.
    Version: V4 (Mit physikalischer Lieferpflicht & Strategie-Support)
    """
    
    time_steps = list(model.TIMESTEPS)
    
    # 1. Block-Mapping erstellen (z.B. 4h Blöcke)
    t_to_block = {}
    blocks = set()
    for idx, t in enumerate(time_steps):
        block_id = idx // market_block_size
        t_to_block[t] = block_id
        blocks.add(block_id)
    sorted_blocks = sorted(list(blocks))
    
    # 2. Variablen für Reservelistung (Kapazität)
    model.trans_afrr_pos_block = pyo.Var(sorted_blocks, domain=pyo.NonNegativeReals)
    model.trans_afrr_neg_block = pyo.Var(sorted_blocks, domain=pyo.NonNegativeReals)
    
    # Fixieren, falls deaktiviert
    if not enable_afrr_pos:
        for b in sorted_blocks: model.trans_afrr_pos_block[b].fix(0)
    if not enable_afrr_neg:
        for b in sorted_blocks: model.trans_afrr_neg_block[b].fix(0)

    # 3. Flow-Variable identifizieren (Input Flow = Stromverbrauch)
    # Wir suchen den Flow (Input_Bus -> PtH_Component)
    in_flow_uid = (input_bus, transformer_component)  # Fluss: Netz -> PtH

    # Listen vorbereiten für schnellen Zugriff
    val_cap_pos = list(afrp_pos_cap_prices)
    val_cap_neg = list(afrp_neg_cap_prices)
    val_en_pos = list(afrp_pos_energy_prices)
    val_en_neg = list(afrp_neg_energy_prices)
    
    is_act_pos_list = hasattr(activation_factor_pos, '__iter__')
    is_act_neg_list = hasattr(activation_factor_neg, '__iter__')
    if is_act_pos_list: val_act_pos = list(activation_factor_pos)
    if is_act_neg_list: val_act_neg = list(activation_factor_neg)

    # --- CONSTRAINTS ---

    # A) HEADROOM (Platz nach oben für Lasterhöhung / Neg. aFRR)
    # Aktueller Fahrplan + Reserve <= Maximale Leistung
    def headroom_rule(m, t):
        b = t_to_block[t]
        flow = m.flow[in_flow_uid[0], in_flow_uid[1], t]
        reserve_neg = m.trans_afrr_neg_block[b]
        return (flow + reserve_neg <= p_max)
    
    model.trans_headroom = pyo.Constraint(time_steps, rule=headroom_rule)

    # B) FOOTROOM (Platz nach unten für Lastabwurf / Pos. aFRR)
    # Aktueller Fahrplan >= Reserve
    # (Ich muss mind. 5 MW verbrauchen, um 5 MW abschalten zu können)
    def footroom_rule(m, t):
        b = t_to_block[t]
        flow = m.flow[in_flow_uid[0], in_flow_uid[1], t]
        reserve_pos = m.trans_afrr_pos_block[b]
        return (flow >= reserve_pos)
    
    model.trans_footroom = pyo.Constraint(time_steps, rule=footroom_rule)

    # C) PHYSIKALISCHE LIEFERPFLICHT (V4 Update)
    # Wenn wir abgerufen werden, muss der Strom auch fließen!
    
    # Fall 1: Negative aFRR (Wir MÜSSEN Strom verbrauchen)
    def force_consumption_rule(m, t):
        b = t_to_block[t]
        idx = time_steps.index(t)
        act_n = val_act_neg[idx] if is_act_neg_list else activation_factor_neg
        
        flow = m.flow[in_flow_uid[0], in_flow_uid[1], t]
        reserved_cap = m.trans_afrr_neg_block[b]
        
        # Der Verbrauch muss mindestens so hoch sein wie der Abruf
        return flow >= reserved_cap * act_n

    model.trans_force_cons = pyo.Constraint(time_steps, rule=force_consumption_rule)

    # Fall 2: Positive aFRR (Wir MÜSSEN abschalten / weniger verbrauchen)
    # Wenn wir voll abgerufen werden (Faktor 1.0), darf der Verbrauch max (P_max - Reserve) sein?
    # Nein, eigentlich: Wenn Abruf da ist, muss Baseline - Abruf = RealFlow sein.
    # Da Oemof keine Baseline kennt, arbeiten wir hier mit Capping.
    # "Wenn pos. Abruf aktiv ist, darf ich nicht vollast fahren".
    def force_reduction_rule(m, t):
        b = t_to_block[t]
        idx = time_steps.index(t)
        act_p = val_act_pos[idx] if is_act_pos_list else activation_factor_pos
        
        flow = m.flow[in_flow_uid[0], in_flow_uid[1], t]
        reserved_cap = m.trans_afrr_pos_block[b]
        
        # Der Fluss darf maximal P_max minus den Abruf betragen
        return flow <= p_max - (reserved_cap * act_p)

    model.trans_force_red = pyo.Constraint(time_steps, rule=force_reduction_rule)


    # --- ZIELFUNKTION (CASHFLOW) ---
    obj_expr = model.objective.expr
    revenue_term = 0
    dt = 0.25 # 15 min
    
    for idx, t in enumerate(time_steps):
        b = t_to_block[t]
        
        # 1. Leistungspreis (Prämie für Bereithaltung) - Einnahme
        revenue_term += model.trans_afrr_pos_block[b] * val_cap_pos[idx] * dt
        revenue_term += model.trans_afrr_neg_block[b] * val_cap_neg[idx] * dt
        
        # 2. Arbeitspreis (Wenn abgerufen)
        act_p = val_act_pos[idx] if is_act_pos_list else activation_factor_pos
        act_n = val_act_neg[idx] if is_act_neg_list else activation_factor_neg
        
        # aFRR Pos (Wir senken Last -> Verkaufen virtuelle Energie): Einnahme
        revenue_term += model.trans_afrr_pos_block[b] * act_p * val_en_pos[idx] * dt
        
        # aFRR Neg (Wir erhöhen Last -> Kaufen Energie): Ausgabe (meistens)
        # Achtung Vorzeichen: Wenn Preis positiv ist, zahlen wir. Wenn negativ, bekommen wir Geld.
        # Wir ziehen Kosten ab (also += wenn Preis negativ).
        # Standard Oemof Objective ist Minimierung (Kosten). 
        # Hier bauen wir einen Revenue Term (Einnahmen).
        # Wir müssen diesen Term von den Gesamtkosten abziehen (model.objective.expr - revenue).
        
        # Kosten für negative Arbeit = Menge * Preis.
        cost_neg = model.trans_afrr_neg_block[b] * act_n * val_en_neg[idx] * dt
        revenue_term -= cost_neg

    # Aktualisiere die Zielfunktion (Minimiere: Kosten - Einnahmen)
    model.objective.expr = obj_expr - revenue_term
    
    # Mapping für Auswertung speichern
    if not hasattr(model, 'trans_map'): model.trans_map = {}
    model.trans_map[transformer_component] = t_to_block

    return model