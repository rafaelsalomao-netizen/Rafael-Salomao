#!/usr/bin/env python3
"""Calculadora de preço mínimo para peças impressas em 3D (varejo e lote para empresas).

Uso:
    python3 calculadora_preco.py GRAMAS HORAS_IMPRESSAO MINUTOS_TRABALHO [--qtd N]

Exemplos:
    python3 calculadora_preco.py 8 0.42 6            # 1 chaveiro, varejo
    python3 calculadora_preco.py 7 0.33 4 --qtd 50   # 50 chaveiros com logo para empresa

Edite a seção PARAMETROS com os seus números reais.
"""
import sys

# ---------------- PARAMETROS (edite) ----------------
PRECO_FILAMENTO_KG  = 110.0   # R$ por kg de PLA
CUSTO_ENERGIA_KWH   = 0.95    # R$ por kWh na conta de luz
CONSUMO_IMPRESSORA  = 0.10    # kW médios imprimindo PLA
VALOR_IMPRESSORA    = 2800.0  # R$ pagos na máquina
VIDA_UTIL_HORAS     = 3000.0  # horas até trocar/revisar
MANUTENCAO_POR_H    = 0.40    # R$ por hora (bicos, placa, lubrificante)
TAXA_FALHA          = 0.10    # 10% das impressões dão errado
VALOR_HORA_TRABALHO = 35.0    # R$ pela hora dela (preparar, trocar cor, acabamento, embalar, atender)
EMBALAGEM_UNIT      = 2.50    # saquinho + fita + adesivo, por peça
EMBALAGEM_PEDIDO    = 4.00    # caixa/envelope de envio, por pedido
MARGEM_LUCRO        = 0.40    # 40% sobre o custo
# taxas por canal: (percentual, custo fixo por unidade, frete que você paga)
CANAIS = {
    "site":    (0.0399, 0.0, 0.0),   # Pix/link Mercado Pago ~4%; cliente paga o frete
    "ml79":    (0.13,   6.5, 0.0),   # ML Clássico ~13% + custo fixo p/ item < R$79. Confira no simulador!
    "ml":      (0.17,   0.0, 22.0),  # ML Premium ~17% + frete grátis obrigatório (>= R$79)
    "empresa": (0.0,    0.0, 0.0),   # Pix/boleto com nota; frete cobrado à parte
}
# desconto progressivo do trabalho por peça em lote (setup é diluído)
def fator_trabalho(qtd):
    return 1.0 if qtd < 20 else 0.6 if qtd < 50 else 0.45 if qtd < 100 else 0.35
# ----------------------------------------------------

def custo_unit(g, h, m, qtd):
    material = g/1000 * PRECO_FILAMENTO_KG
    energia  = h * CONSUMO_IMPRESSORA * CUSTO_ENERGIA_KWH
    maquina  = h * (VALOR_IMPRESSORA/VIDA_UTIL_HORAS + MANUTENCAO_POR_H)
    producao = (material + energia + maquina) * (1 + TAXA_FALHA)
    trabalho = m/60 * VALOR_HORA_TRABALHO * fator_trabalho(qtd)
    emb      = EMBALAGEM_UNIT + EMBALAGEM_PEDIDO/qtd
    return {"material":material,"energia":energia,"maquina":maquina,
            "falhas":producao-(material+energia+maquina),"trabalho":trabalho,
            "embalagem":emb,"total":producao+trabalho+emb}

def preco(c, canal):
    pct, fixo, frete = CANAIS[canal]
    return (c*(1+MARGEM_LUCRO) + fixo + frete) / (1-pct)

def main():
    args=[a for a in sys.argv[1:] if not a.startswith("--")]
    qtd = int(sys.argv[sys.argv.index("--qtd")+1]) if "--qtd" in sys.argv else 1
    if len(args)<3: print(__doc__); sys.exit(1)
    g,h,m = map(float,args[:3]); c = custo_unit(g,h,m,qtd)
    print(f"Peça: {g:.0f} g, {h*60:.0f} min de impressão, {m:.0f} min de trabalho, lote de {qtd}")
    for k in ("material","energia","maquina","falhas","trabalho","embalagem"):
        print(f"  {k:10s} R$ {c[k]:7.2f}")
    print(f"  {'CUSTO/un':10s} R$ {c['total']:7.2f}")
    print()
    canais = ("empresa",) if qtd>=20 else ("site","ml79","ml")
    for n in canais:
        p = preco(c["total"], n); pct,fixo,frete = CANAIS[n]
        lucro = p*(1-pct)-fixo-frete-c["total"]
        print(f"  canal {n:8s} preço mínimo R$ {p:7.2f}/un  (lucro R$ {lucro:6.2f}/un, R$ {lucro/max(h,0.05):6.2f} por hora de impressora)")
    if qtd>=20:
        print(f"\n  Lote: R$ {preco(c['total'],'empresa')*qtd:,.2f} + frete · {h*qtd:.0f} h de impressora ({h*qtd/20:.1f} dias a 20 h/dia)")
    print("\nArredonde para cima (R$ 19,90; R$ 12,90). Preço de mercado acima do mínimo é lucro; abaixo, não venda.")

if __name__=="__main__": main()
